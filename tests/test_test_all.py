from __future__ import annotations

import contextlib
import io
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("test_all", ROOT / "scripts/test_all.py")
assert SPEC is not None and SPEC.loader is not None
test_all = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(test_all)
VALIDATE_SPEC = importlib.util.spec_from_file_location(
    "validate",
    ROOT / "scripts/validate.py",
)
assert VALIDATE_SPEC is not None and VALIDATE_SPEC.loader is not None
validate = importlib.util.module_from_spec(VALIDATE_SPEC)
VALIDATE_SPEC.loader.exec_module(validate)


class GitStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repository = Path(self.temporary.name)
        self.environment = os.environ.copy()
        self.git("init", "-q")
        self.git("config", "user.email", "tests@example.invalid")
        self.git("config", "user.name", "Test Runner")
        (self.repository / "tracked.txt").write_text("committed\n", encoding="utf-8")
        (self.repository / ".gitignore").write_text("generated/\n", encoding="utf-8")
        self.git("add", "tracked.txt", ".gitignore")
        self.git("commit", "-qm", "fixture")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str) -> bytes:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repository,
            env=self.environment,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout

    def state(self) -> object:
        with mock.patch.object(test_all, "ROOT", self.repository):
            return test_all.git_state(self.environment)

    def test_detects_tracked_content_change_with_same_dirty_status(self) -> None:
        tracked = self.repository / "tracked.txt"
        tracked.write_text("dirty before\n", encoding="utf-8")
        before = self.state()
        self.assertEqual(self.git("status", "--porcelain=v1", "-z"), b" M tracked.txt\0")

        tracked.write_text("dirty after\n", encoding="utf-8")

        self.assertEqual(self.git("status", "--porcelain=v1", "-z"), b" M tracked.txt\0")
        self.assertNotEqual(self.state(), before)

    def test_detects_existing_untracked_content_change(self) -> None:
        untracked = self.repository / "notes.txt"
        untracked.write_text("before\n", encoding="utf-8")
        before = self.state()
        self.assertEqual(self.git("status", "--porcelain=v1", "-z"), b"?? notes.txt\0")

        untracked.write_text("after\n", encoding="utf-8")

        self.assertEqual(self.git("status", "--porcelain=v1", "-z"), b"?? notes.txt\0")
        self.assertNotEqual(self.state(), before)

    def test_detects_index_content_change_with_same_dirty_status(self) -> None:
        tracked = self.repository / "tracked.txt"
        tracked.write_text("index before\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        tracked.write_text("working tree\n", encoding="utf-8")
        before = self.state()
        self.assertEqual(self.git("status", "--porcelain=v1", "-z"), b"MM tracked.txt\0")

        blob = subprocess.run(
            ["git", "hash-object", "-w", "--stdin"],
            cwd=self.repository,
            env=self.environment,
            check=True,
            input=b"index after\n",
            stdout=subprocess.PIPE,
        ).stdout.strip()
        self.git("update-index", "--cacheinfo", f"100644,{blob.decode()},tracked.txt")

        self.assertEqual(self.git("status", "--porcelain=v1", "-z"), b"MM tracked.txt\0")
        self.assertNotEqual(self.state(), before)

    def test_main_allows_unchanged_dirty_tree(self) -> None:
        (self.repository / "tracked.txt").write_text("dirty\n", encoding="utf-8")
        (self.repository / "notes.txt").write_text("untracked\n", encoding="utf-8")

        def fake_run(
            label: str,
            command: list[str],
            *,
            environment: dict[str, str],
        ) -> None:
            del label, environment
            if "--output" in command:
                output = Path(command[command.index("--output") + 1])
                output.mkdir(parents=True)
                (output / "index.html").write_text("built\n", encoding="utf-8")

        with (
            mock.patch.object(test_all, "ROOT", self.repository),
            mock.patch.object(test_all.importlib.util, "find_spec", return_value=object()),
            mock.patch.object(test_all, "run", side_effect=fake_run),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(test_all.main(), 0)

    def test_new_ignored_output_does_not_change_state(self) -> None:
        before = self.state()
        generated = self.repository / "generated"
        generated.mkdir()
        (generated / "large-cache.bin").write_bytes(b"cache")

        self.assertEqual(self.state(), before)


class ValidationTests(unittest.TestCase):
    def test_trailing_space_and_tab_are_reported_from_collected_text(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            clean = root / "clean.txt"
            dirty = root / "dirty.txt"
            clean.write_text("clean\n", encoding="utf-8")
            dirty.write_text("first \nsecond\t\n", encoding="utf-8")

            text_files = validate.repository_text_files(root)
            with self.assertRaisesRegex(
                validate.ValidationError,
                r"dirty\.txt:1\ndirty\.txt:2",
            ):
                validate.validate_trailing_whitespace(root, text_files)

    def test_ignored_dirty_text_is_not_collected_in_git_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / ".gitignore").write_text(".venv/\n_site/\n", encoding="utf-8")
            ignored_files = []
            for directory in (".venv", "_site"):
                ignored = root / directory / "dirty.txt"
                ignored.parent.mkdir()
                ignored.write_text("ignored trailing space \n", encoding="utf-8")
                ignored_files.append(ignored)

            text_files = validate.repository_text_files(root)

            self.assertTrue(all(path not in text_files for path in ignored_files))
            validate.validate_trailing_whitespace(root, text_files)

    def test_nonignored_untracked_dirty_text_is_collected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            source = root / "source.txt"
            source.write_text("untracked trailing tab\t\n", encoding="utf-8")

            text_files = validate.repository_text_files(root)

            self.assertIn(source, text_files)
            with self.assertRaisesRegex(validate.ValidationError, r"source\.txt:1"):
                validate.validate_trailing_whitespace(root, text_files)

    def test_release_archive_collection_prunes_generated_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.txt"
            source.write_text("source\n", encoding="utf-8")
            cache = root / ".venv" / "dependency.txt"
            cache.parent.mkdir()
            cache.write_text("dependency \n", encoding="utf-8")

            text_files = validate.repository_text_files(root)

            self.assertIn(source, text_files)
            self.assertNotIn(cache, text_files)


if __name__ == "__main__":
    unittest.main()

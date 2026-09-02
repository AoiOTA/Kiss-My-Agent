#!/usr/bin/env python3
"""Run the complete deterministic contributor test suite."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path


if sys.version_info < (3, 11):
    print("test suite failed: Python 3.11 or newer is required", file=sys.stderr)
    raise SystemExit(1)


ROOT = Path(__file__).resolve().parent.parent


def run(label: str, command: list[str], *, environment: dict[str, str]) -> None:
    print(f"==> {label}", flush=True)
    subprocess.run(command, cwd=ROOT, env=environment, check=True)


def git_state(environment: dict[str, str]) -> bytes:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z"],
        cwd=ROOT,
        env=environment,
        check=True,
        stdout=subprocess.PIPE,
    )
    return result.stdout


def main() -> int:
    if importlib.util.find_spec("markdown") is None:
        print(
            "test suite failed: the contributor documentation dependency is missing; "
            "activate an isolated environment and run "
            "`python -m pip install -r requirements-site.txt`",
            file=sys.stderr,
        )
        return 1

    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    before = git_state(environment)

    try:
        run(
            "static repository validation",
            [sys.executable, "scripts/validate.py"],
            environment=environment,
        )
        run(
            "unit tests",
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-p",
                "test_*.py",
                "-v",
            ],
            environment=environment,
        )
        with tempfile.TemporaryDirectory(prefix="kiss-my-agent-site-") as temporary:
            output = Path(temporary) / "site"
            run(
                "isolated documentation build",
                [sys.executable, "scripts/build_site.py", "--output", str(output)],
                environment=environment,
            )
            generated = [path for path in output.rglob("*") if path.is_file()]
            if not generated:
                raise RuntimeError("documentation build produced no files")
        run("Git whitespace validation", ["git", "diff", "--check"], environment=environment)
    except (OSError, subprocess.CalledProcessError, RuntimeError) as error:
        print(f"test suite failed: {error}", file=sys.stderr)
        return 1

    after = git_state(environment)
    if after != before:
        print("test suite failed: tests changed the Git working tree", file=sys.stderr)
        return 1

    print("deterministic-test-suite=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

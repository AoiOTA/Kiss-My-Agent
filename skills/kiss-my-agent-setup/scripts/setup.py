#!/usr/bin/env python3
"""Set up, inspect, or remove the KISS My Agent Codex configuration."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROLE_FILES = ("kiss_explorer.toml", "kiss_coder.toml", "kiss_reviewer.toml")
ROLE_NAMES = tuple(name.removesuffix(".toml") for name in ROLE_FILES)
BEGIN_MARKER = "<!-- BEGIN KISS MY AGENT MANAGED BLOCK -->"
END_MARKER = "<!-- END KISS MY AGENT MANAGED BLOCK -->"
CONFIG_MARKER = "# KISS My Agent managed"
MANAGED_BLOCK = f"""{BEGIN_MARKER}
## KISS My Agent

People own the goal, architecture, acceptance criteria, non-goals, and stop boundary. Multi-agent work is available by default, but an explicit user instruction or effective configuration that disables it takes precedence. Select dynamically only from the current Host-exposed role catalog; `kiss_explorer`, `kiss_coder`, and `kiss_reviewer` are initial seeds that users may remove, rename, or replace, not a fixed team or workflow. Keep one operator for each shared resource, preserve unrelated changes, prefer the smallest sufficient change, propagate internal failures, and state evidence only at the level actually reached.
{END_MARKER}"""

_SECTION_RE = re.compile(r"^\s*\[\s*([A-Za-z0-9_-]+)\s*\]\s*(?:#.*)?$")
_ANY_SECTION_RE = re.compile(r"^\s*\[\[?.*\]\]?\s*(?:#.*)?$")
_ASSIGNMENT_RE = re.compile(
    r'^\s*(?:"(?P<double>[^"]+)"|\'(?P<single>[^\']+)\'|(?P<bare>[A-Za-z0-9_-]+))\s*='
)


class SetupError(RuntimeError):
    """A user-actionable preflight or transaction failure."""


@dataclass(frozen=True)
class Change:
    path: Path
    before: bytes | None
    after: bytes | None


def _read_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def _assert_regular_or_missing(path: Path) -> None:
    if path.is_symlink():
        raise SetupError(f"refusing symlinked managed path: {path}")
    if path.exists() and not path.is_file():
        raise SetupError(f"managed path is not a regular file: {path}")


def _assert_directory_or_missing(path: Path) -> None:
    if path.is_symlink():
        raise SetupError(f"refusing symlinked managed directory: {path}")
    if path.exists() and not path.is_dir():
        raise SetupError(f"managed directory path is not a directory: {path}")


def _decode(path: Path, data: bytes | None) -> str:
    if data is None:
        return ""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise SetupError(f"managed text file is not UTF-8: {path}") from error


def _parse_toml(path: Path, data: bytes | None) -> dict:
    text = _decode(path, data)
    try:
        parsed = tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise SetupError(f"invalid TOML in {path}: {error}") from error
    if not isinstance(parsed, dict):
        raise SetupError(f"unsupported TOML root in {path}")
    return parsed


def _line_key(line: str) -> str | None:
    match = _ASSIGNMENT_RE.match(line)
    if match is None:
        return None
    return match.group("double") or match.group("single") or match.group("bare")


def _section_ranges(lines: list[str]) -> dict[str, tuple[int, int]]:
    headers: list[tuple[str | None, int]] = []
    for index, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        match = _SECTION_RE.match(stripped)
        if match is not None:
            headers.append((match.group(1), index))
        elif _ANY_SECTION_RE.match(stripped):
            headers.append((None, index))
    ranges: dict[str, tuple[int, int]] = {}
    for position, (name, start) in enumerate(headers):
        if name is None:
            continue
        if name in ranges:
            raise SetupError(f"unsupported duplicate table [{name}]")
        end = headers[position + 1][1] if position + 1 < len(headers) else len(lines)
        ranges[name] = (start, end)
    return ranges


def _validate_config_shape(path: Path, data: bytes | None) -> tuple[dict, list[str], dict[str, tuple[int, int]]]:
    parsed = _parse_toml(path, data)
    text = _decode(path, data)
    lines = text.splitlines(keepends=True)
    ranges = _section_ranges(lines)
    for section, key in (("features", "multi_agent"), ("agents", "enabled")):
        value = parsed.get(section)
        if value is not None and not isinstance(value, dict):
            raise SetupError(f"unsupported config shape: {section} must be a table")
        if section in parsed and section not in ranges:
            descendant_prefixes = (f"[{section}.", f"[[{section}.")
            has_descendant_table = any(
                line.lstrip().startswith(descendant_prefixes) for line in lines
            )
            if not has_descendant_table:
                raise SetupError(f"unsupported config shape for [{section}] in {path}")
        if isinstance(value, dict) and key in value and not isinstance(value[key], bool):
            raise SetupError(f"unsupported config value: {section}.{key} must be boolean")
        if section in ranges:
            start, end = ranges[section]
            matches = [line for line in lines[start + 1 : end] if _line_key(line) == key]
            expected = isinstance(value, dict) and key in value
            if expected != bool(matches) or len(matches) > 1:
                raise SetupError(f"unsupported config syntax for {section}.{key} in {path}")
    return parsed, lines, ranges


def _config_value(parsed: dict, section: str, key: str) -> bool | None:
    table = parsed.get(section)
    return table.get(key) if isinstance(table, dict) else None


def _line_owned(line: str) -> bool:
    return CONFIG_MARKER in line


def _insert_config_key(lines: list[str], section: str, key: str) -> list[str]:
    ranges = _section_ranges(lines)
    newline = "\r\n" if any(line.endswith("\r\n") for line in lines) else "\n"
    assignment = f"{key} = true {CONFIG_MARKER}{newline}"
    if section not in ranges:
        if lines and not lines[-1].endswith(("\n", "\r")):
            lines[-1] += newline
        if lines and lines[-1].strip():
            lines.append(newline)
        lines.extend([f"[{section}]{newline}", assignment])
        return lines
    _start, end = ranges[section]
    if end > 0 and not lines[end - 1].endswith(("\n", "\r")):
        lines[end - 1] += newline
    lines.insert(end, assignment)
    return lines


def setup_config(path: Path, data: bytes | None) -> tuple[bytes, dict[str, bool | None]]:
    parsed, lines, _ranges = _validate_config_shape(path, data)
    state: dict[str, bool | None] = {}
    for section, key in (("features", "multi_agent"), ("agents", "enabled")):
        value = _config_value(parsed, section, key)
        state[f"{section}.{key}"] = value
        if value is None:
            lines = _insert_config_key(lines, section, key)
            parsed, lines, _ranges = _validate_config_shape(path, "".join(lines).encode())
    return "".join(lines).encode("utf-8"), state


def remove_owned_config(path: Path, data: bytes | None) -> bytes | None:
    _parsed, lines, ranges = _validate_config_shape(path, data)
    if data is None:
        return None
    remove_indexes: set[int] = set()
    for section, key in (("features", "multi_agent"), ("agents", "enabled")):
        if section not in ranges:
            continue
        start, end = ranges[section]
        for index in range(start + 1, end):
            if _line_key(lines[index]) == key and _line_owned(lines[index]):
                remove_indexes.add(index)
    result = "".join(line for index, line in enumerate(lines) if index not in remove_indexes)
    return result.encode("utf-8")


def _managed_block_bounds(text: str, path: Path) -> tuple[int, int] | None:
    begin_count = text.count(BEGIN_MARKER)
    end_count = text.count(END_MARKER)
    if begin_count != end_count or begin_count > 1:
        raise SetupError(f"malformed KISS My Agent managed block in {path}")
    if begin_count == 0:
        return None
    begin = text.index(BEGIN_MARKER)
    end_start = text.find(END_MARKER, begin)
    if end_start < 0:
        raise SetupError(f"malformed KISS My Agent managed block in {path}")
    end = end_start + len(END_MARKER)
    return begin, end


def setup_agents_md(path: Path, data: bytes | None) -> tuple[bytes, bool]:
    text = _decode(path, data)
    bounds = _managed_block_bounds(text, path)
    first_setup = bounds is None
    if bounds is None:
        if text and not text.endswith("\n"):
            text += "\n"
        if text and text.strip():
            text += "\n"
        text += MANAGED_BLOCK + "\n"
    else:
        start, end = bounds
        text = text[:start] + MANAGED_BLOCK + text[end:]
    return text.encode("utf-8"), first_setup


def remove_agents_md(path: Path, data: bytes | None) -> bytes | None:
    if data is None:
        return None
    text = _decode(path, data)
    bounds = _managed_block_bounds(text, path)
    if bounds is None:
        return data
    start, end = bounds
    while end < len(text) and text[end] in " \t":
        end += 1
    if end < len(text) and text[end] == "\r":
        end += 1
    if end < len(text) and text[end] == "\n":
        end += 1
    if start > 0 and text[:start].endswith("\n\n"):
        start -= 1
    return (text[:start] + text[end:]).encode("utf-8")


def _role_name(path: Path, data: bytes) -> str:
    parsed = _parse_toml(path, data)
    for field in ("name", "description", "developer_instructions"):
        value = parsed.get(field)
        if not isinstance(value, str) or not value.strip():
            raise SetupError(f"role file has no valid string {field}: {path}")
    name = parsed["name"]
    if re.fullmatch(r"[A-Za-z0-9_-]+", name) is None:
        raise SetupError(f"role file has an invalid name: {path}")
    return name


def scan_role_catalog(directory: Path) -> dict[str, dict[str, object]]:
    _assert_directory_or_missing(directory)
    result: dict[str, dict[str, object]] = {}
    names: dict[str, str] = {}
    if not directory.exists():
        return result
    for path in sorted(directory.glob("*.toml")):
        _assert_regular_or_missing(path)
        data = path.read_bytes()
        name = _role_name(path, data)
        previous = names.get(name)
        if previous is not None:
            raise SetupError(f"duplicate role name {name!r}: {previous} and {path.name}")
        names[name] = path.name
        result[path.name] = {"name": name, "bytes": data}
    return result


def _atomic_replace(path: Path, data: bytes, expected: bytes | None) -> None:
    _assert_directory_or_missing(path.parent)
    _assert_regular_or_missing(path)
    current = _read_bytes(path)
    if current != expected:
        raise SetupError(f"concurrent change detected at {path}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, 0o644)
        if _read_bytes(path) != expected:
            raise SetupError(f"concurrent change detected at {path}")
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _restore(change: Change) -> None:
    current = _read_bytes(change.path)
    if current != change.after:
        raise SetupError(f"cannot roll back concurrent change at {change.path}")
    if change.before is None:
        change.path.unlink(missing_ok=True)
    else:
        _atomic_replace(change.path, change.before, current)


def apply_changes(changes: Iterable[Change]) -> None:
    material = [change for change in changes if change.before != change.after]
    created_directories: list[Path] = []
    applied: list[Change] = []

    def verify_expected_state() -> None:
        applied_paths = {change.path for change in applied}
        for change in material:
            _assert_directory_or_missing(change.path.parent)
            _assert_regular_or_missing(change.path)
            expected = change.after if change.path in applied_paths else change.before
            if _read_bytes(change.path) != expected:
                raise SetupError(f"concurrent change detected at {change.path}")

    verify_expected_state()
    try:
        for change in material:
            verify_expected_state()
            missing: list[Path] = []
            parent = change.path.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                directory.mkdir()
                created_directories.append(directory)
            if change.after is None:
                _assert_directory_or_missing(change.path.parent)
                _assert_regular_or_missing(change.path)
                if _read_bytes(change.path) != change.before:
                    raise SetupError(f"concurrent change detected at {change.path}")
                change.path.unlink(missing_ok=True)
            else:
                _atomic_replace(change.path, change.after, change.before)
            applied.append(change)
        verify_expected_state()
    except BaseException as error:
        rollback_errors: list[str] = []
        for change in reversed(applied):
            try:
                _restore(change)
            except Exception as rollback_error:  # preserve the primary failure and report rollback damage
                rollback_errors.append(str(rollback_error))
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        if rollback_errors:
            raise SetupError(f"{error}; rollback failed: {'; '.join(rollback_errors)}") from error
        raise


class SetupManager:
    def __init__(self, scope: str, target: Path, codex_home: Path, seed_dir: Path | None = None):
        self.scope = scope
        self.target = target.absolute()
        self.codex_home = codex_home.absolute()
        self.seed_dir = seed_dir or Path(__file__).resolve().parents[3] / ".codex" / "agents"
        if scope == "project":
            self.base = self.target
            self.config_path = self.target / ".codex" / "config.toml"
            self.agents_dir = self.target / ".codex" / "agents"
            self.opposite_agents_dir = self.codex_home / "agents"
        else:
            self.base = self.codex_home
            self.config_path = self.codex_home / "config.toml"
            self.agents_dir = self.codex_home / "agents"
            self.opposite_agents_dir = self.target / ".codex" / "agents"
        self.agents_path = self.base / "AGENTS.md"
        self.override_path = self.base / "AGENTS.override.md"

    def _preflight(
        self, *, reject_opposite_conflicts: bool = True
    ) -> tuple[dict[str, bytes], dict[str, dict[str, object]], dict[str, dict[str, object]]]:
        if self.scope == "project" and (not self.target.exists() or not self.target.is_dir()):
            raise SetupError(f"project target must be an existing directory: {self.target}")
        _assert_directory_or_missing(self.base)
        _assert_directory_or_missing(self.config_path.parent)
        _assert_directory_or_missing(self.agents_dir)
        for path in (self.config_path, self.agents_path, self.override_path):
            _assert_regular_or_missing(path)
        if self.override_path.exists():
            raise SetupError(f"AGENTS.override.md prevents managed AGENTS.md setup: {self.override_path}")
        seed_catalog = scan_role_catalog(self.seed_dir)
        if set(seed_catalog) != set(ROLE_FILES):
            raise SetupError(f"bundled role catalog must contain exactly: {', '.join(ROLE_FILES)}")
        for filename, expected_name in zip(ROLE_FILES, ROLE_NAMES):
            if seed_catalog[filename]["name"] != expected_name:
                raise SetupError(f"bundled role {filename} must declare name {expected_name}")
        current_catalog = scan_role_catalog(self.agents_dir)
        opposite_catalog = scan_role_catalog(self.opposite_agents_dir)
        opposite_names = {entry["name"] for entry in opposite_catalog.values()}
        conflicts = sorted(set(ROLE_NAMES) & opposite_names)
        if conflicts and reject_opposite_conflicts:
            raise SetupError(f"project/global role conflict: {', '.join(conflicts)}")
        for filename, expected_name in zip(ROLE_FILES, ROLE_NAMES):
            existing = current_catalog.get(filename)
            if existing is not None and existing["name"] != expected_name:
                raise SetupError(f"role filename collision: {self.agents_dir / filename}")
            for other_filename, entry in current_catalog.items():
                if entry["name"] == expected_name and other_filename != filename:
                    raise SetupError(
                        f"role name collision: {entry['name']} is declared by {self.agents_dir / other_filename}"
                    )
        seeds = {filename: seed_catalog[filename]["bytes"] for filename in ROLE_FILES}
        return seeds, current_catalog, opposite_catalog

    def setup(self) -> dict[str, object]:
        seeds, current_catalog, _opposite = self._preflight()
        config_before = _read_bytes(self.config_path)
        agents_before = _read_bytes(self.agents_path)
        config_after, previous_values = setup_config(self.config_path, config_before)
        agents_after, first_setup = setup_agents_md(self.agents_path, agents_before)
        changes = [
            Change(self.config_path, config_before, config_after),
            Change(self.agents_path, agents_before, agents_after),
        ]
        installed_roles: list[str] = []
        preserved_roles: list[str] = []
        for filename in ROLE_FILES:
            path = self.agents_dir / filename
            before = _read_bytes(path)
            if before is None and first_setup:
                changes.append(Change(path, None, seeds[filename]))
                installed_roles.append(filename)
            elif before is not None:
                preserved_roles.append(filename)
        apply_changes(changes)
        disabled = [name for name, value in previous_values.items() if value is False]
        return {
            "operation": "setup",
            "scope": self.scope,
            "status": "disabled" if disabled else "configured",
            "disabled": disabled,
            "installed_roles": installed_roles,
            "preserved_roles": preserved_roles,
            "changed": any(change.before != change.after for change in changes),
        }

    def check(self) -> dict[str, object]:
        seeds, current_catalog, _opposite = self._preflight()
        config_data = _read_bytes(self.config_path)
        parsed, lines, ranges = _validate_config_shape(self.config_path, config_data)
        config: dict[str, dict[str, object]] = {}
        disabled: list[str] = []
        for section, key in (("features", "multi_agent"), ("agents", "enabled")):
            value = _config_value(parsed, section, key)
            owned = False
            if section in ranges:
                start, end = ranges[section]
                owned = any(
                    _line_key(lines[index]) == key and _line_owned(lines[index])
                    for index in range(start + 1, end)
                )
            config[f"{section}.{key}"] = {"value": value, "managed": owned}
            if value is False:
                disabled.append(f"{section}.{key}")
        agents_data = _read_bytes(self.agents_path)
        agents_text = _decode(self.agents_path, agents_data)
        bounds = _managed_block_bounds(agents_text, self.agents_path)
        block_state = "absent"
        if bounds is not None:
            start, end = bounds
            block_state = "current" if agents_text[start:end] == MANAGED_BLOCK else "outdated"
        roles: dict[str, dict[str, object]] = {}
        for filename, entry in current_catalog.items():
            roles[filename] = {
                "name": entry["name"],
                "bundled_default": filename in seeds and entry["bytes"] == seeds[filename],
            }
        config_complete = all(item["value"] is not None for item in config.values())
        has_setup_trace = (
            bounds is not None
            or any(item["managed"] for item in config.values())
            or any(entry["name"] in ROLE_NAMES for entry in current_catalog.values())
        )
        if bounds is None:
            status = "incomplete" if has_setup_trace else "absent"
        elif block_state != "current" or not config_complete:
            status = "incomplete"
        elif disabled:
            status = "disabled"
        else:
            status = "structurally-valid"
        return {
            "operation": "check",
            "scope": self.scope,
            "status": status,
            "static_only": True,
            "disabled": disabled,
            "config": config,
            "agents_managed_block": block_state,
            "roles": roles,
        }

    def remove(self) -> dict[str, object]:
        seeds, current_catalog, _opposite = self._preflight(reject_opposite_conflicts=False)
        config_before = _read_bytes(self.config_path)
        agents_before = _read_bytes(self.agents_path)
        changes = [
            Change(self.config_path, config_before, remove_owned_config(self.config_path, config_before)),
            Change(self.agents_path, agents_before, remove_agents_md(self.agents_path, agents_before)),
        ]
        removed_roles: list[str] = []
        preserved_roles: list[str] = []
        for filename in ROLE_FILES:
            entry = current_catalog.get(filename)
            if entry is None:
                continue
            path = self.agents_dir / filename
            if entry["bytes"] == seeds[filename]:
                changes.append(Change(path, entry["bytes"], None))
                removed_roles.append(filename)
            else:
                preserved_roles.append(filename)
        apply_changes(changes)
        return {
            "operation": "remove",
            "scope": self.scope,
            "status": "removed",
            "removed_roles": removed_roles,
            "preserved_modified_roles": preserved_roles,
            "changed": any(change.before != change.after for change in changes),
        }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set up, statically check, or remove KISS My Agent Codex configuration."
    )
    parser.add_argument("command", choices=("setup", "check", "remove"))
    parser.add_argument("--scope", choices=("project", "global"), default="project")
    parser.add_argument("--target", type=Path, default=Path.cwd(), help="Project root (default: cwd)")
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex home for global setup or opposite-scope collision checks",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manager = SetupManager(args.scope, args.target, args.codex_home)
    try:
        result = getattr(manager, args.command)()
    except SetupError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.command == "check" and result["status"] in {"absent", "incomplete"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

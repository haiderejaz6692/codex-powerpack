#!/usr/bin/env python3
"""Validate the portable plugin, router skill, catalog, and pinned core manifest."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROUTER = ROOT / "skills" / "skill-library-router"


def load_json(relative_path: str):
    path = ROOT / relative_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Invalid JSON in {relative_path}: {error}") from error


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_repositories(entries, label: str) -> set[str]:
    require(isinstance(entries, list) and entries, f"{label} must be a non-empty JSON array")
    repositories: set[str] = set()
    for index, entry in enumerate(entries):
        require(isinstance(entry, dict), f"{label}[{index}] must be an object")
        repo = entry.get("repo")
        category = entry.get("category")
        require(isinstance(repo, str) and re.fullmatch(r"[^/\s]+/[^/\s]+", repo) is not None, f"Invalid repo at {label}[{index}]")
        require(isinstance(category, str) and category.strip(), f"Missing category at {label}[{index}]")
        key = repo.casefold()
        require(key not in repositories, f"Duplicate repository in {label}: {repo}")
        repositories.add(key)
    return repositories


def validate_skill() -> None:
    manifest = ROUTER / "SKILL.md"
    text = manifest.read_text(encoding="utf-8")
    require(text.startswith("---\n"), "Router SKILL.md must start with YAML frontmatter")
    require("\nname: skill-library-router\n" in text, "Router skill name is incorrect")
    require("\ndescription:" in text, "Router skill description is missing")
    require((ROUTER / "agents" / "openai.yaml").is_file(), "Router agents/openai.yaml is missing")
    require((ROUTER / "scripts" / "refresh_catalog.py").is_file(), "Catalog refresh script is missing")


def validate_catalog(configured_repositories: set[str]) -> int:
    catalog_path = ROUTER / "references" / "catalog.tsv"
    with catalog_path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        expected = ["category", "repo", "ref", "commit", "path", "skill", "kind", "url"]
        require(reader.fieldnames == expected, f"Unexpected catalog columns: {reader.fieldnames}")
        rows = list(reader)
    require(rows, "Catalog must contain at least one skill manifest")
    for row in rows:
        require(row["repo"].casefold() in configured_repositories, f"Catalog repository is not configured: {row['repo']}")
        require(row["path"] == "SKILL.md" or row["path"].endswith("/SKILL.md"), f"Invalid skill path: {row['path']}")
        require(re.fullmatch(r"[0-9a-f]{40}", row["commit"]) is not None, f"Invalid commit SHA for {row['repo']}")
    return len(rows)


def validate_core_lock() -> int:
    with (ROOT / "config" / "core-skills.tsv").open(encoding="utf-8", newline="") as stream:
        core = list(csv.DictReader(stream, delimiter="\t"))
    locked = load_json("config/skills-lock.json").get("skills", [])
    lock_by_name = {entry["name"]: entry for entry in locked}
    require(len(lock_by_name) == len(locked), "Duplicate names in skills-lock.json")
    for entry in core:
        match = lock_by_name.get(entry["name"])
        require(match is not None, f"Missing lock entry for {entry['name']}")
        require(match["repository"] == entry["repo"], f"Repository mismatch for {entry['name']}")
        require(match["commit"] == entry["commit"], f"Commit mismatch for {entry['name']}")
        require(match["path"] == entry["path"], f"Path mismatch for {entry['name']}")
    return len(core)


def validate_plugin() -> None:
    plugin = load_json("plugin.json")
    require(plugin.get("name") == "codex-powerpack", "Portable plugin name is incorrect")
    require(re.fullmatch(r"\d+\.\d+\.\d+", str(plugin.get("version", ""))) is not None, "Plugin version must use semantic versioning")
    require((ROOT / "skills").is_dir(), "Portable skills directory is missing")

    compatibility = load_json(".codex-plugin/plugin.json")
    require(compatibility.get("name") == plugin["name"], "Compatibility plugin name differs")
    require(compatibility.get("version") == plugin["version"], "Compatibility plugin version differs")
    require(compatibility.get("skills") == "./skills/", "Compatibility skills path is incorrect")

    marketplace = load_json(".agents/plugins/marketplace.json")
    entries = marketplace.get("plugins", [])
    require(len(entries) == 1 and entries[0].get("name") == plugin["name"], "Marketplace must expose codex-powerpack once")


def main() -> int:
    try:
        validate_plugin()
        validate_skill()
        configured = validate_repositories(load_json("config/repositories.json"), "config/repositories.json")
        packaged = validate_repositories(load_json("skills/skill-library-router/references/repositories.json"), "packaged repositories.json")
        require(configured == packaged, "Packaged and configured repository lists differ")
        catalog_rows = validate_catalog(configured)
        core_count = validate_core_lock()
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"VALIDATION FAILED: {error}", file=sys.stderr)
        return 1

    print(f"VALIDATION PASSED: plugin, router, {len(configured)} repositories, {catalog_rows} catalog rows, {core_count} pinned core skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


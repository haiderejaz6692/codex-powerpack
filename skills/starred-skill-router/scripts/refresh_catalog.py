#!/usr/bin/env python3
"""Refresh the portable Codex skill catalog using an authenticated GitHub CLI."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote


SKILL_ROOT = Path(__file__).resolve().parent.parent
REPOSITORIES_PATH = SKILL_ROOT / "references" / "repositories.json"
OUTPUT_PATH = SKILL_ROOT / "references" / "catalog.tsv"


def gh_json(endpoint: str):
    result = subprocess.run(
        ["gh", "api", "-H", "Accept: application/vnd.github+json", endpoint],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"GitHub API request failed: {endpoint}")
    return json.loads(result.stdout)


def classify(path: str) -> str:
    lowered = f"/{path.lower()}/"
    fixture_markers = ("/test/", "/tests/", "/fixture/", "/fixtures/", "/template/", "/templates/", "/example/", "/examples/")
    host_markers = ("/.claude/", "/.cursor/", "/.gemini/", "/.grok/", "/.kiro/", "/.opencode/", "/openclaw/")

    if path.startswith("registry/blocks/") or any(marker in lowered for marker in fixture_markers):
        return "fixture"
    if any(marker in lowered for marker in host_markers):
        return "host-duplicate"
    if path.startswith(("skills/", "optional-skills/", "agent-skill/")):
        return "canonical"
    if path.startswith((".agents/skills/", ".agent/skills/")):
        return "agent"
    if "/plugin/" in lowered or "/plugins/" in lowered:
        return "plugin"
    if path == "SKILL.md":
        return "root"
    return "other"


def skill_name(repo: str, path: str) -> str:
    parts = path.split("/")
    return repo.split("/", 1)[1] if len(parts) == 1 else parts[-2]


def main() -> int:
    auth = subprocess.run(["gh", "auth", "status"], check=False, capture_output=True, text=True)
    if auth.returncode != 0:
        print("GitHub CLI is not authenticated. Run: gh auth login", file=sys.stderr)
        return 1

    repositories = json.loads(REPOSITORIES_PATH.read_text(encoding="utf-8"))
    rows: list[dict[str, str]] = []
    skipped: list[str] = []

    for entry in repositories:
        repo = entry["repo"]
        category = entry["category"]
        try:
            metadata = gh_json(f"repos/{repo}")
            ref = metadata["default_branch"]
            commit = gh_json(f"repos/{repo}/commits/{ref}")["sha"]
            tree = gh_json(f"repos/{repo}/git/trees/{commit}?recursive=1")
        except (RuntimeError, KeyError, json.JSONDecodeError) as error:
            skipped.append(f"{repo}: {error}")
            continue

        for item in tree.get("tree", []):
            path = item.get("path", "")
            if item.get("type") != "blob" or not (path == "SKILL.md" or path.endswith("/SKILL.md")):
                continue
            encoded_path = "/".join(quote(segment, safe="") for segment in path.split("/"))
            rows.append(
                {
                    "category": category,
                    "repo": repo,
                    "ref": ref,
                    "commit": commit,
                    "path": path,
                    "skill": skill_name(repo, path),
                    "kind": classify(path),
                    "url": f"https://github.com/{repo}/blob/{commit}/{encoded_path}",
                }
            )

    rows.sort(key=lambda row: (row["skill"].casefold(), row["repo"].casefold(), row["path"].casefold()))
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(
            output,
            fieldnames=("category", "repo", "ref", "commit", "path", "skill", "kind", "url"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Cataloged {len(rows)} skill manifests from {len(repositories) - len(skipped)} of {len(repositories)} repositories at {OUTPUT_PATH}")
    for message in skipped:
        print(f"WARNING {message}", file=sys.stderr)
    return 0 if not skipped else 2


if __name__ == "__main__":
    raise SystemExit(main())


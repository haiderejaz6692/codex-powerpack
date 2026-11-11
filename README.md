# Codex Powerpack

A portable, safe Codex skills setup for `haiderejaz6692`.

Instead of globally installing hundreds of overlapping skills, this repository installs a small trusted core and a router that searches a catalog of specialist skills only when a task needs one.

## What it installs

- `starred-skill-router` — searches the indexed GitHub skill library on demand.
- `humanizer` — rewrites AI-sounding prose naturally.
- `diagram-design` — creates architecture and software diagrams.
- `ui-ux-pro-max` — UI/UX design, implementation, review, and accessibility guidance.
- `karpathy-guidelines` — surgical coding and review discipline.

The catalog covers 36 selected repositories grouped into six GitHub lists, plus the optional `petrkindlmann/qa-skills` testing library. Applications and reference repositories remain catalog entries; they are not forced into Codex as skills.

## Install on Windows

```powershell
gh auth login
gh repo clone haiderejaz6692/codex-powerpack
cd codex-powerpack
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

PowerShell 7 users can replace `powershell` with `pwsh`.

## Install on macOS or Linux

```bash
gh auth login
gh repo clone haiderejaz6692/codex-powerpack
cd codex-powerpack
bash ./scripts/bootstrap.sh
```

Open a new Codex chat after installation so newly installed skills are discoverable.

## Safe behavior

- Existing skill directories are never overwritten.
- Upstream skills are downloaded at commits pinned in `config/core-skills.tsv`.
- Downloaded skills are copied but their scripts are not executed.
- Every downloaded directory must contain `SKILL.md`.
- Temporary files are removed after installation.
- Specialist repositories are indexed, not blindly installed.

## Refresh the catalog

After installation:

```powershell
python "$HOME\.codex\skills\starred-skill-router\scripts\refresh_catalog.py"
```

On macOS or Linux:

```bash
python3 "$HOME/.codex/skills/starred-skill-router/scripts/refresh_catalog.py"
```

The refresh requires an authenticated GitHub CLI. It reads repository trees and skill manifests but does not install or execute repository code.

## Update pinned core versions

Review upstream changes first, then update the commit hashes in `config/core-skills.tsv`. Running the bootstrap again skips already installed destinations, protecting local modifications. Rename or remove a destination deliberately before installing a new pinned version.

## Repository layout

```text
codex-powerpack/
├── config/
│   ├── core-skills.tsv
│   ├── repositories.json
│   └── skills-lock.json
├── scripts/
│   ├── bootstrap.ps1
│   └── bootstrap.sh
└── skills/
    └── starred-skill-router/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/catalog.tsv
        ├── references/repositories.json
        └── scripts/refresh_catalog.py
```

## Upstream licenses

This repository does not vendor the four upstream core skills. The bootstrap downloads them from their original repositories, where their own licenses and terms apply. The generated catalog contains metadata and links only.


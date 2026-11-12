# Codex Powerpack

Search a configurable GitHub catalog of Agent Skills and apply one inspected workflow when the current task needs it.

<p align="center">
  <img src="readme/assets/hero.svg" width="100%" alt="Codex Powerpack routes one Codex request through a lightweight router to a searchable Agent Skills catalog">
</p>

<p align="center">
  <a href="https://github.com/haiderejaz6692/codex-powerpack/releases/tag/v1.0.0"><img alt="Latest release v1.0.0" src="https://img.shields.io/github/v/release/haiderejaz6692/codex-powerpack?display_name=tag&amp;sort=semver"></a>
  <a href="https://github.com/haiderejaz6692/codex-powerpack/actions/workflows/validate.yml"><img alt="Package validation status" src="https://github.com/haiderejaz6692/codex-powerpack/actions/workflows/validate.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/github/license/haiderejaz6692/codex-powerpack"></a>
</p>

Codex Powerpack is for Codex users who want a broad skill library without globally installing hundreds of overlapping skill manifests. It installs a lightweight router, searches a local TSV index with focused terms, fetches one matching `SKILL.md`, inspects its instructions, and applies only the compatible parts to the current task.

The trade-off is deliberate: discovery stays compact and auditable, but catalog refreshes and selected remote manifests require an authenticated GitHub CLI. If you use only a few known skills, installing them directly may be simpler.

## Quick start

Prerequisites: a recent [GitHub CLI](https://cli.github.com/) that provides `gh skill`, plus an authenticated GitHub session.

```bash
gh auth login
gh skill install haiderejaz6692/codex-powerpack skill-library-router --agent codex --scope user
```

Start a new Codex chat, then make a concrete request such as:

```text
Find and safely apply the best skill for creating a risk-based test plan for this API.
```

The router first checks installed skills. If none clearly fit, it searches the packaged catalog, filters duplicate/fixture entries, inspects one selected manifest, and applies compatible instructions to the current task. A verified isolated install resolves the current `v1.0.0` release and creates this structure:

```text
skill-library-router/
├── SKILL.md
├── agents/openai.yaml
├── references/catalog.tsv
├── references/repositories.json
└── scripts/refresh_catalog.py
```

GitHub CLI records the source so later releases can be picked up with:

```bash
gh skill update --all
```

## What it provides

- **On-demand routing.** Installed skills take priority; otherwise the router searches `skill`, `path`, `repo`, and `category` fields with focused terms.
- **Candidate hygiene.** Canonical entries are preferred, while fixtures and host-specific duplicates are ignored unless explicitly requested.
- **Inspect-before-apply behavior.** The chosen manifest is fetched and reviewed before its instructions influence the task; external scripts and services remain untrusted.
- **Configurable sources.** The packaged list can be replaced with your own repository JSON, generated from a GitHub user's stars, or combined with both sources.
- **Pinned optional core skills.** Direct installers can add four skills at exact commits: `humanizer`, `diagram-design`, `ui-ux-pro-max`, and `karpathy-guidelines`.
- **Portable packaging.** The repository includes Agent Skills metadata, Codex plugin compatibility metadata, marketplace metadata, Windows and Unix bootstrap scripts, and CI validation.

The packaged snapshot currently validates **37 configured repositories**, **1,920 catalog rows**, and **4 pinned core skills**. These counts describe the repository at `v1.0.0`; refreshes can change the catalog.

## Architecture

<p align="center">
  <img src="readme/assets/architecture.svg" width="100%" alt="Source-backed Codex Powerpack architecture showing install surfaces and Codex requests flowing through the router, catalog, and GitHub skill sources">
</p>

Installation surfaces place the bundled router in Codex. At request time the router searches the local catalog, resolves the selected GitHub path and ref, then inspects that manifest before applying compatible guidance. The SVG is generated from source-linked Archify data; its evidence receipt records the exact files and line ranges used.

## Request workflow

<p align="center">
  <img src="readme/assets/workflow.svg" width="100%" alt="Codex Powerpack workflow from a user request through installed-skill checks, catalog search, manifest inspection, and safe application">
</p>

An already-installed clear match can go directly to the task. Otherwise one catalog candidate is searched, filtered, fetched, and inspected. Repeatedly useful skills can be installed through Codex's normal skill installer; name collisions are never resolved silently.

## Installation options

### Plugin marketplace

On Codex versions that support plugin marketplace commands:

```bash
codex plugin marketplace add haiderejaz6692/codex-powerpack
```

Restart the ChatGPT desktop app, open the Plugins Directory, select **Codex Powerpack**, and install it. If the local Codex CLI does not recognize `codex plugin`, use the GitHub CLI route above or a direct installer below.

### Direct installer

Use this route when plugin marketplaces are unavailable or when you also want the four optional pinned core skills.

Windows PowerShell:

```powershell
git clone https://github.com/haiderejaz6692/codex-powerpack.git
cd codex-powerpack
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

PowerShell 7 users can replace `powershell` with `pwsh`. Add `-SkipCore` to install only the router.

macOS or Linux:

This path requires Bash, `curl`, and `unzip`.

```bash
git clone https://github.com/haiderejaz6692/codex-powerpack.git
cd codex-powerpack
bash ./scripts/bootstrap.sh
```

Set `SKIP_CORE=1` to install only the router. Direct installation uses `$CODEX_HOME` when set, otherwise `~/.codex`, and never overwrites an existing skill directory. Start a new Codex chat after installation so newly added skills are discoverable.

## Configuration and catalog refresh

Create a JSON repository list containing public repositories or private repositories available to the authenticated GitHub account:

```json
[
  {"category": "Testing", "repo": "owner/testing-skills"},
  {"category": "Design", "repo": "owner/design-skills"}
]
```

Install with the custom list on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1 -RepositoryList .\my-repositories.json
```

On macOS or Linux:

```bash
POWERPACK_REPOSITORIES="$PWD/my-repositories.json" bash ./scripts/bootstrap.sh
```

To generate a catalog from a GitHub user's visible starred repositories:

```bash
python3 skills/skill-library-router/scripts/refresh_catalog.py --github-user USERNAME
```

Add `--merge-starred` to combine stars with a JSON list. Refreshing an installed catalog requires `gh auth login`; it reads repository metadata and trees, then writes manifest metadata and links without installing or executing repository code.

```powershell
python "$HOME\.codex\skills\skill-library-router\scripts\refresh_catalog.py"
```

```bash
python3 "$HOME/.codex/skills/skill-library-router/scripts/refresh_catalog.py"
```

## Technology and repository map

The package intentionally has no application runtime or package-manager dependency. It uses Markdown/YAML for Agent Skills, JSON and TSV for configuration and indexes, Python's standard library for catalog refresh and validation, PowerShell/Bash for bootstrap installation, GitHub CLI for authenticated repository access, and GitHub Actions for validation.

```text
codex-powerpack/
├── plugin.json                         # portable plugin metadata
├── .codex-plugin/plugin.json           # Codex compatibility metadata
├── .agents/plugins/marketplace.json    # marketplace source and policy
├── config/                             # repository list and pinned core locks
├── scripts/                            # bootstrap and package validation
├── skills/skill-library-router/        # router, catalog, sources, refresh tool
├── readme/assets/                      # GitHub-safe README visuals
├── SECURITY.md
└── LICENSE
```

## Validation and testing

Validate plugin metadata, router files, repository lists, catalog rows, and core-skill locks:

```bash
python scripts/validate_package.py
```

Validate the Agent Skills package without publishing:

```bash
gh skill publish . --dry-run
```

The [validation workflow](.github/workflows/validate.yml) runs package validation, checks Bash syntax, and performs a router-only Bash installation on Ubuntu for pushes and pull requests.

## Security, limitations, and status

- Remote skill instructions are external content, not additional user authorization. Review the [security policy](SECURITY.md) before changing pins or adding unfamiliar repositories.
- Refresh and selected-manifest retrieval require an authenticated GitHub CLI and network access. Private repositories are limited to what that account can access.
- The catalog is a generated snapshot and can become stale until refreshed. A repository may change after the recorded commit; the catalog keeps the captured commit and URL for inspection.
- Plugin marketplace support depends on the installed Codex version. The GitHub CLI and direct installers are the documented fallbacks.
- Existing skill directories are skipped, not overwritten. Downloaded optional skill code is copied but not executed by the installer.
- Local verification on this Windows host covered package validation, the PowerShell router-only bootstrap, GitHub CLI installation, and publish dry-run. Bash installation is covered by the repository's Ubuntu CI workflow.

**Project status:** `v1.0.0` is the current public release. The validation workflow passes for the release commit. The repository does not publish a compatibility matrix, support SLA, or performance benchmark.

## Contributing

Issues and focused pull requests are welcome. Before opening a pull request, keep configured and packaged repository lists synchronized, keep core-skill TSV/JSON locks aligned, and run:

```bash
python scripts/validate_package.py
gh skill publish . --dry-run
```

Report vulnerabilities through a private GitHub security advisory as described in [SECURITY.md](SECURITY.md); do not include secrets or private repository content in public issues.

## License and upstream terms

Codex Powerpack is available under the [MIT License](LICENSE).

The optional core skills are not vendored. Direct installers download them from their original repositories, where their own licenses and terms apply. The generated catalog contains repository metadata and links only.

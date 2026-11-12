# Codex Powerpack

A portable Codex plugin and direct installer for a large, searchable Agent Skills library.

Codex Powerpack keeps discovery efficient: it installs one lightweight router, indexes specialist skills, and loads only the workflow needed for the current task. It does not globally install thousands of overlapping skill manifests.

## Fastest installation: GitHub CLI

With a recent GitHub CLI that provides `gh skill`:

```bash
gh auth login
gh skill install haiderejaz6692/codex-powerpack skill-library-router --agent codex --scope user
```

Start a new Codex chat after installation. GitHub CLI records the source, so future releases can be picked up with:

```bash
gh skill update --all
```

## Plugin marketplace installation

On Codex versions that support plugin marketplace commands, add this repository as a marketplace:

Add this repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add haiderejaz6692/codex-powerpack
```

Restart the ChatGPT desktop app, open the Plugins Directory, select **Codex Powerpack**, and install it. The plugin packages `skill-library-router` and its curated catalog in the standard `skills/` layout. If the local Codex CLI does not recognize `codex plugin`, use the GitHub CLI or direct installation route instead.

## Direct installation

Use this route when plugin marketplaces are unavailable or when you also want the four optional core skills.

### Windows

```powershell
git clone https://github.com/haiderejaz6692/codex-powerpack.git
cd codex-powerpack
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

PowerShell 7 users can replace `powershell` with `pwsh`.

### macOS or Linux

```bash
git clone https://github.com/haiderejaz6692/codex-powerpack.git
cd codex-powerpack
bash ./scripts/bootstrap.sh
```

The direct installer adds:

- `skill-library-router` — searches the indexed library on demand.
- `humanizer` — improves AI-sounding prose.
- `diagram-design` — creates architecture and software diagrams.
- `ui-ux-pro-max` — supports UI/UX design, review, and implementation.
- `karpathy-guidelines` — encourages focused, verifiable code changes.

Open a new Codex chat after direct installation so the new skills are discoverable.

## Use your own repository list

The included catalog is a useful default, not a requirement. Create a JSON file containing any public or GitHub-authorized repositories:

```json
[
  {"category": "Testing", "repo": "owner/testing-skills"},
  {"category": "Design", "repo": "owner/design-skills"}
]
```

Install the router with that list on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1 -RepositoryList .\my-repositories.json
```

On macOS or Linux:

```bash
POWERPACK_REPOSITORIES="$PWD/my-repositories.json" bash ./scripts/bootstrap.sh
```

You can also build a catalog directly from any GitHub user's public stars:

```bash
python3 skills/skill-library-router/scripts/refresh_catalog.py --github-user USERNAME
```

To combine stars with a JSON list, add `--merge-starred`.

## Refresh the installed catalog

Windows:

```powershell
python "$HOME\.codex\skills\skill-library-router\scripts\refresh_catalog.py"
```

macOS or Linux:

```bash
python3 "$HOME/.codex/skills/skill-library-router/scripts/refresh_catalog.py"
```

Refresh requires an authenticated GitHub CLI (`gh auth login`). It reads repository metadata and trees; it does not install or execute repository code.

## Safe behavior

- Existing skill directories are never overwritten.
- Optional core skills are downloaded at commits pinned in `config/skills-lock.json`.
- Downloaded skill scripts are copied but never executed by the installer.
- Every installed directory must contain `SKILL.md`.
- Specialist repositories are indexed, not blindly installed.
- Private repositories work only when the local GitHub CLI account can access them.

See [SECURITY.md](SECURITY.md) before changing pinned versions or adding an unfamiliar repository.

Maintainers can validate the complete package locally with:

```bash
python scripts/validate_package.py
```

## Repository layout

```text
codex-powerpack/
├── plugin.json
├── .codex-plugin/plugin.json
├── .agents/plugins/marketplace.json
├── config/
│   ├── core-skills.tsv
│   ├── repositories.json
│   ├── repositories.example.json
│   └── skills-lock.json
├── scripts/
│   ├── bootstrap.ps1
│   └── bootstrap.sh
└── skills/
    └── skill-library-router/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/catalog.tsv
        ├── references/repositories.json
        └── scripts/refresh_catalog.py
```

## Upstream licenses

The optional core skills are not vendored. The direct installer downloads them from their original repositories, where their own licenses and terms apply. The generated catalog contains repository metadata and links only.


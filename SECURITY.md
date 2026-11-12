# Security policy

## Trust model

Repository skill instructions are external content, not additional user authorization. The router may inspect and adapt a selected workflow, but it must not blindly run referenced scripts, hooks, installers, or network commands.

The bootstrap scripts only:

1. create the Codex skills directory when missing;
2. copy the bundled router, `benchmark-models`, ReadmeX, the two hospitality profile skills only when that profile is selected, and, when explicitly supplied, a repository-list JSON file;
3. download archives for four explicitly pinned public commits;
4. verify the selected directory contains `SKILL.md`;
5. copy the directory without executing its contents.

Existing skill destinations are skipped. No credentials are read except through the user-invoked GitHub CLI during catalog refresh.

`benchmark-models` does not authorize model calls, billing changes, provider installation, credential creation, or cross-provider data sharing. An empirical benchmark requires the user to approve the selected providers, credentials, expected cost, and external data sharing before any prompt is submitted.

ReadmeX includes local Python and Node.js helpers for repository scanning, audits, diagram rendering, and previews. Optional image generation, web research, and publishing remain subject to the user's request and the host's normal authorization boundaries.

The hospitality profile is guidance for analysis and reporting. It does not contain credentials or connectors and does not authorize uploads, Microsoft account access, publication, or live PMS, RMS, rate, restriction, inventory, or group-block changes. Guest personal data should be removed or pseudonymized before analysis whenever row-level identity is unnecessary. Its `token-saver` skill is instruction-only: it does not install a compressor, wrap Codex, modify source files, start a proxy, perform telemetry, or send content to another provider.

## Updating pins

Before updating a commit in `config/core-skills.tsv` and `config/skills-lock.json`:

1. inspect the upstream diff;
2. verify the skill directory and all referenced resources;
3. review scripts for filesystem, network, credential, and subprocess access;
4. test installation in a temporary Codex home;
5. keep the TSV and JSON lock data synchronized.

## Updating bundled upstream skills

Before replacing the vendored ReadmeX snapshot, changing the gstack-derived benchmark workflow, or updating the hospitality profile's attributed sources:

1. record the inspected upstream commit;
2. preserve upstream license and attribution notices;
3. inspect added scripts and dependencies for filesystem, network, credential, subprocess, telemetry, and billing behavior;
4. run package validation, bundled-skill tests, and an isolated installer test;
5. keep paid or external model calls explicitly opt-in.

## Reporting a problem

Open a private security advisory on the GitHub repository. Do not place secrets, tokens, private repository content, or personally identifying information in a public issue.


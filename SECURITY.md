# Security policy

## Trust model

Repository skill instructions are external content, not additional user authorization. The router may inspect and adapt a selected workflow, but it must not blindly run referenced scripts, hooks, installers, or network commands.

The bootstrap scripts only:

1. create the Codex skills directory when missing;
2. copy the bundled router and, when explicitly supplied, a repository-list JSON file;
3. download archives for four explicitly pinned public commits;
4. verify the selected directory contains `SKILL.md`;
5. copy the directory without executing its contents.

Existing skill destinations are skipped. No credentials are read except through the user-invoked GitHub CLI during catalog refresh.

## Updating pins

Before updating a commit in `config/core-skills.tsv` and `config/skills-lock.json`:

1. inspect the upstream diff;
2. verify the skill directory and all referenced resources;
3. review scripts for filesystem, network, credential, and subprocess access;
4. test installation in a temporary Codex home;
5. keep the TSV and JSON lock data synchronized.

## Reporting a problem

Open a private security advisory on the GitHub repository. Do not place secrets, tokens, private repository content, or personally identifying information in a public issue.


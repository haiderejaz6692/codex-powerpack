#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
codex_home="${CODEX_HOME:-$HOME/.codex}"
skills_root="$codex_home/skills"
skip_core="${SKIP_CORE:-0}"
repository_list="${POWERPACK_REPOSITORIES:-}"
profile="${POWERPACK_PROFILE:-default}"

if [[ "$profile" != "default" && "$profile" != "hospitality-revenue" ]]; then
  printf 'Unknown POWERPACK_PROFILE: %s\n' "$profile" >&2
  exit 1
fi

mkdir -p "$skills_root"

install_directory_safely() {
  local source="$1"
  local name="$2"
  local destination="$skills_root/$name"

  if [[ -e "$destination" ]]; then
    printf 'SKIP %s (destination already exists: %s)\n' "$name" "$destination"
    return 0
  fi

  if [[ ! -f "$source/SKILL.md" ]]; then
    printf 'Refusing to install %s because SKILL.md was not found in %s\n' "$name" "$source" >&2
    return 1
  fi

  cp -R "$source" "$destination"
  printf 'INSTALLED %s -> %s\n' "$name" "$destination"
}

for bundled_skill in skill-library-router benchmark-models readmex; do
  install_directory_safely "$repo_root/skills/$bundled_skill" "$bundled_skill"
done

if [[ "$profile" == "hospitality-revenue" ]]; then
  for profile_skill in hospitality-revenue-analyst token-saver; do
    install_directory_safely "$repo_root/profiles/hospitality-revenue/skills/$profile_skill" "$profile_skill"
  done
fi

if [[ -n "$repository_list" ]]; then
  if [[ ! -f "$repository_list" ]]; then
    printf 'Repository list does not exist: %s\n' "$repository_list" >&2
    exit 1
  fi
  cp "$repository_list" "$skills_root/skill-library-router/references/repositories.json"
  printf 'CONFIGURED skill-library-router from %s\n' "$repository_list"
fi

if [[ "$skip_core" != "1" ]]; then
  for command_name in curl unzip; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
      printf 'Required command is missing: %s\n' "$command_name" >&2
      exit 1
    fi
  done

  while IFS=$'\t' read -r name repo commit path; do
    [[ "$name" == "name" || -z "$name" ]] && continue
    destination="$skills_root/$name"
    if [[ -e "$destination" ]]; then
      printf 'SKIP %s (destination already exists: %s)\n' "$name" "$destination"
      continue
    fi

    temp_path="$(mktemp -d "${TMPDIR:-/tmp}/codex-powerpack.XXXXXX")"
    cleanup_temp() {
      if [[ -n "${temp_path:-}" && -d "$temp_path" && "$(basename "$temp_path")" == codex-powerpack.* ]]; then
        rm -rf -- "$temp_path"
      fi
    }
    trap cleanup_temp EXIT

    archive="$temp_path/source.zip"
    extract="$temp_path/extract"
    mkdir -p "$extract"
    printf 'DOWNLOAD %s from %s@%s\n' "$name" "$repo" "$commit"
    curl -fsSL "https://codeload.github.com/$repo/zip/$commit" -o "$archive"
    unzip -q "$archive" -d "$extract"
    archive_root="$(find "$extract" -mindepth 1 -maxdepth 1 -type d -print -quit)"
    if [[ -z "$archive_root" ]]; then
      printf 'The archive for %s did not contain a root directory.\n' "$name" >&2
      exit 1
    fi

    if [[ "$path" == "." ]]; then
      source="$archive_root"
    else
      source="$archive_root/$path"
    fi
    install_directory_safely "$source" "$name"
    cleanup_temp
    trap - EXIT
  done < "$repo_root/config/core-skills.tsv"
fi

printf '\nCodex Powerpack is installed in %s\n' "$skills_root"
printf 'Open a new Codex chat before relying on newly installed skill discovery.\n'


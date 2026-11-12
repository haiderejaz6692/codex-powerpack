from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUNDLED_SKILLS = ("skill-library-router", "benchmark-models", "readmex")
PROFILE_SKILLS = ("hospitality-revenue-analyst", "token-saver")


class BundledSkillTests(unittest.TestCase):
    def run_skip_core_bootstrap(self, codex_home: Path) -> subprocess.CompletedProcess[str]:
        if os.name == "nt":
            command = [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "scripts" / "bootstrap.ps1"),
                "-CodexHome",
                str(codex_home),
                "-SkipCore",
            ]
            environment = None
        else:
            command = ["bash", str(ROOT / "scripts" / "bootstrap.sh")]
            environment = os.environ.copy()
            environment.update({"CODEX_HOME": str(codex_home), "SKIP_CORE": "1"})

        return subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_package_validator_reports_every_bundled_skill(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_package.py")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("3 bundled skills", result.stdout)
        self.assertIn("2 optional profile skills", result.stdout)

    def test_bundled_skill_manifests_match_directory_names(self) -> None:
        for name in BUNDLED_SKILLS:
            manifest = ROOT / "skills" / name / "SKILL.md"
            self.assertTrue(manifest.is_file(), f"missing bundled manifest: {manifest}")
            text = manifest.read_text(encoding="utf-8")
            self.assertIn(f"\nname: {name}\n", text, f"manifest name mismatch for {name}")

    def test_readmex_bundle_contains_runtime_resources(self) -> None:
        expected = (
            "LICENSE",
            "THIRD_PARTY_NOTICES",
            "bin/render-diagram.mjs",
            "scripts/scan.py",
            "schemas/architecture.schema.json",
            "renderers/architecture/render-architecture.mjs",
            "renderers/workflow/render-workflow.mjs",
        )
        for relative in expected:
            path = ROOT / "skills" / "readmex" / relative
            self.assertTrue(path.is_file(), f"incomplete ReadmeX bundle: {relative}")

    def test_benchmark_models_is_portable_and_attributed(self) -> None:
        root = ROOT / "skills" / "benchmark-models"
        expected = (
            "SKILL.md",
            "THIRD_PARTY_NOTICES",
            "agents/openai.yaml",
            "references/evaluation-rubric.md",
        )
        for relative in expected:
            self.assertTrue((root / relative).is_file(), f"missing benchmark resource: {relative}")

        manifest = (root / "SKILL.md").read_text(encoding="utf-8")
        forbidden = ("~/.claude/skills/gstack", "gstack-model-benchmark", "gstack-skill-start")
        for token in forbidden:
            self.assertNotIn(token, manifest, f"non-portable gstack dependency remains: {token}")
        self.assertIn("explicit", manifest.lower())
        self.assertIn("cost", manifest.lower())

    def test_hospitality_profile_is_self_contained_and_attributed(self) -> None:
        root = ROOT / "profiles" / "hospitality-revenue" / "skills" / "hospitality-revenue-analyst"
        expected = (
            "SKILL.md",
            "THIRD_PARTY_NOTICES",
            "agents/openai.yaml",
            "references/metrics-and-formulas.md",
            "references/analysis-workflows.md",
            "references/power-bi-and-presentations.md",
        )
        for relative in expected:
            self.assertTrue((root / relative).is_file(), f"missing hospitality resource: {relative}")

        manifest = (root / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("guest", manifest.lower())
        self.assertIn("personal", manifest.lower())
        self.assertIn("never invent", manifest.lower())

    def test_token_saver_is_dependency_free_and_non_destructive(self) -> None:
        root = ROOT / "profiles" / "hospitality-revenue" / "skills" / "token-saver"
        expected = ("SKILL.md", "THIRD_PARTY_NOTICES", "agents/openai.yaml")
        for relative in expected:
            self.assertTrue((root / relative).is_file(), f"missing token-saver resource: {relative}")

        manifest = (root / "SKILL.md").read_text(encoding="utf-8").lower()
        for forbidden in ("pip install", "npm install", "uv tool", "headroom wrap"):
            self.assertNotIn(forbidden, manifest, f"token-saver gained a runtime dependency: {forbidden}")
        self.assertIn("do not modify source files", manifest)
        self.assertIn("do not send", manifest)

    def test_hospitality_profile_installs_only_when_selected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="codex-powerpack-profile-") as temp:
            default_home = Path(temp) / "default-home"
            default_result = self.run_skip_core_bootstrap(default_home)
            self.assertEqual(0, default_result.returncode, default_result.stdout + default_result.stderr)
            self.assertFalse(
                (default_home / "skills" / PROFILE_SKILLS[0]).exists(),
                "hospitality skill should remain opt-in",
            )

            profile_home = Path(temp) / "profile-home"
            if os.name == "nt":
                command = [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(ROOT / "scripts" / "bootstrap.ps1"),
                    "-CodexHome",
                    str(profile_home),
                    "-SkipCore",
                    "-Profile",
                    "hospitality-revenue",
                ]
                environment = None
            else:
                command = ["bash", str(ROOT / "scripts" / "bootstrap.sh")]
                environment = os.environ.copy()
                environment.update(
                    {
                        "CODEX_HOME": str(profile_home),
                        "SKIP_CORE": "1",
                        "POWERPACK_PROFILE": "hospitality-revenue",
                    }
                )

            profile_result = subprocess.run(
                command,
                cwd=ROOT,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(
                0,
                profile_result.returncode,
                profile_result.stdout + profile_result.stderr,
            )
            for name in PROFILE_SKILLS:
                manifest = profile_home / "skills" / name / "SKILL.md"
                self.assertTrue(manifest.is_file(), f"hospitality profile did not install {name}")

    def test_skip_core_bootstrap_installs_complete_bundles_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory(prefix="codex-powerpack-test-") as temp:
            codex_home = Path(temp) / "codex-home"
            result = self.run_skip_core_bootstrap(codex_home)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            for name in BUNDLED_SKILLS:
                manifest = codex_home / "skills" / name / "SKILL.md"
                self.assertTrue(manifest.is_file(), f"bootstrap did not install {name}")

            nested_resources = (
                "skills/skill-library-router/references/catalog.tsv",
                "skills/benchmark-models/references/evaluation-rubric.md",
                "skills/readmex/renderers/architecture/render-architecture.mjs",
                "skills/readmex/renderers/workflow/render-workflow.mjs",
            )
            for relative in nested_resources:
                self.assertTrue(
                    (codex_home / relative).is_file(),
                    f"bootstrap did not recursively install {relative}",
                )

            sentinels: dict[Path, str] = {}
            for name in BUNDLED_SKILLS:
                sentinel = codex_home / "skills" / name / "preserve-existing.txt"
                expected = f"preserve {name}\n"
                sentinel.write_text(expected, encoding="utf-8")
                sentinels[sentinel] = expected

            second_result = self.run_skip_core_bootstrap(codex_home)
            self.assertEqual(
                0,
                second_result.returncode,
                second_result.stdout + second_result.stderr,
            )
            for name in BUNDLED_SKILLS:
                self.assertIn(f"SKIP {name}", second_result.stdout)
            for sentinel, expected in sentinels.items():
                self.assertEqual(expected, sentinel.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

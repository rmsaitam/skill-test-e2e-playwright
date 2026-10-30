import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_plugin import validate_plugin


SKILL_CONTENT = """---
name: test-e2e-playwright
description: Run Playwright end-to-end testing.
---

## Workflow

### Gate 1: Reconnaissance
### Gate 2: Browser startup
### Gate 3: Route inventory
### Gate 4: Test implementation
### Gate 5: Failure triage
### Gate 6: Verification

### Autonomous mode
### Guided mode

Use port 8931. Cover 100% of routes. Prefer page.getByRole(),
page.getByLabel(), and page.getByPlaceholder(); use
await expect(locator).toBeVisible(). Avoid textContent() for assertions
and do not use page.waitForTimeout(). Use Page Object Model and
storageState safely; configure on-first-retry and only-on-failure.
"""

PLUGIN_FILES = (
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
)
MARKETPLACE_FILES = (
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/marketplace.json",
    ".github/plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
)


def create_valid_package(root: Path) -> None:
    for relative in PLUGIN_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        manifest = {"name": "test-e2e-playwright"}
        if relative in (".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
            manifest["skills"] = "./skills/"
        if relative == ".cursor-plugin/plugin.json":
            manifest["commands"] = "./commands/"
        path.write_text(json.dumps(manifest), encoding="utf-8")

    for relative in MARKETPLACE_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"plugins": [{"name": "test-e2e-playwright"}]}),
            encoding="utf-8",
        )

    required = (
        "agents/openai.yaml",
        "commands/test-e2e-playwright.md",
        "skills/test-e2e-playwright/SKILL.md",
        "skills/test-e2e-playwright/references/browser-session.md",
        "skills/test-e2e-playwright/references/coverage-inventory.md",
        "skills/test-e2e-playwright/references/test-patterns.md",
        "skills/test-e2e-playwright/references/failure-triage.md",
        "README.md",
        "LICENSE",
        "Makefile",
    )
    for relative in required:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative.endswith("SKILL.md"):
            content = SKILL_CONTENT
        elif relative == "agents/openai.yaml":
            content = (
                "interface:\n"
                '  display_name: "Test E2E Playwright"\n'
                '  short_description: "Automate E2E tests"\n'
                '  default_prompt: "Use the test-e2e-playwright skill."\n'
            )
        elif relative == "README.md":
            content = (
                "# Test E2E Playwright\n\n"
                "### Modo automático\n"
                "### Modo acompanhado\n"
            )
        else:
            content = "present\n"
        path.write_text(content, encoding="utf-8")


class ValidatePluginTests(unittest.TestCase):
    def test_accepts_complete_cross_agent_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_package(root)

            self.assertEqual(validate_plugin(root), [])

    def test_reports_missing_required_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_package(root)
            (root / "agents/openai.yaml").unlink()

            errors = validate_plugin(root)

            self.assertTrue(any("agents/openai.yaml" in error for error in errors))

    def test_rejects_incomplete_skill_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_package(root)
            skill = root / "skills/test-e2e-playwright/SKILL.md"
            skill.write_text("---\nname: test-e2e-playwright\n---\n", encoding="utf-8")

            errors = validate_plugin(root)

            self.assertTrue(any("description" in error for error in errors))
            self.assertTrue(any("8931" in error or "port" in error for error in errors))

    def test_rejects_manifest_with_mismatched_plugin_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_package(root)
            (root / ".codex-plugin/plugin.json").write_text(
                json.dumps({"name": "wrong-name"}), encoding="utf-8"
            )

            errors = validate_plugin(root)

            self.assertTrue(any(".codex-plugin/plugin.json" in error for error in errors))

    def test_requires_shared_skill_path_in_agent_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_package(root)
            codex_manifest = root / ".codex-plugin/plugin.json"
            codex_manifest.write_text(
                json.dumps({"name": "test-e2e-playwright", "skills": "./other/"}),
                encoding="utf-8",
            )

            errors = validate_plugin(root)

            self.assertTrue(any("skills must point to ./skills/" in error for error in errors))

    def test_rejects_marketplace_without_the_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_package(root)
            (root / ".agents/plugins/marketplace.json").write_text(
                json.dumps({"plugins": [{"name": "another-skill"}]}),
                encoding="utf-8",
            )

            errors = validate_plugin(root)

            self.assertTrue(any(".agents/plugins/marketplace.json" in error for error in errors))

    def test_reports_malformed_json_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_package(root)
            (root / "plugin.json").write_text("{", encoding="utf-8")

            errors = validate_plugin(root)

            self.assertTrue(any("invalid or unreadable JSON" in error for error in errors))

    def test_requires_readme_to_explain_both_execution_modes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_valid_package(root)
            (root / "README.md").write_text(
                "# Test E2E Playwright\n\n## Modo automático\n",
                encoding="utf-8",
            )

            errors = validate_plugin(root)

            self.assertTrue(any("modo acompanhado" in error.lower() for error in errors))


if __name__ == "__main__":
    unittest.main()

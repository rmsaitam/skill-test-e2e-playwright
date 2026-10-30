#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PLUGIN_NAME = "test-e2e-playwright"
PLUGIN_MANIFESTS = (
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
)
MARKETPLACE_MANIFESTS = (
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/marketplace.json",
    ".github/plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
)
SKILL_DIRECTORY_MANIFESTS = (
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
)
COMMAND_DIRECTORY_MANIFESTS = (".cursor-plugin/plugin.json",)
REQUIRED_FILES = (
    *PLUGIN_MANIFESTS,
    *MARKETPLACE_MANIFESTS,
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
REQUIRED_HEADINGS = (
    "### Gate 1: Reconnaissance",
    "### Gate 2: Browser startup",
    "### Gate 3: Route inventory",
    "### Gate 4: Test implementation",
    "### Gate 5: Failure triage",
    "### Gate 6: Verification",
)
REQUIRED_TERMS = (
    "8931",
    "100%",
    "getByRole",
    "getByLabel",
    "getByPlaceholder",
    "toBeVisible",
    "textContent",
    "waitForTimeout",
    "Page Object Model",
    "storageState",
    "on-first-retry",
    "only-on-failure",
)
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


def _read_json(path: Path, errors: list[str]) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path}: invalid or unreadable JSON ({error})")
        return None
    if not isinstance(value, dict):
        errors.append(f"{path}: expected a JSON object")
        return None
    return value


def _check_skill_contract(path: Path, errors: list[str]) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        errors.append(f"{path}: cannot read skill ({error})")
        return

    match = FRONTMATTER_RE.match(content)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        frontmatter = ""
    else:
        frontmatter = match.group(1)

    fields = {}
    for line in frontmatter.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip().strip("\"'")
    if fields.get("name") != PLUGIN_NAME:
        errors.append(f"{path}: frontmatter name must be {PLUGIN_NAME}")
    if not fields.get("description"):
        errors.append(f"{path}: frontmatter description is required")

    for heading in REQUIRED_HEADINGS:
        if heading not in content:
            errors.append(f"{path}: missing required workflow section: {heading}")
    for term in REQUIRED_TERMS:
        if term.casefold() not in content.casefold():
            errors.append(f"{path}: missing required E2E guidance: {term}")

    for mode in ("Autonomous mode", "Guided mode"):
        if mode.casefold() not in content.casefold():
            errors.append(f"{path}: missing execution mode: {mode}")


def _check_readme_modes(path: Path, errors: list[str]) -> None:
    try:
        content = path.read_text(encoding="utf-8").casefold()
    except OSError as error:
        errors.append(f"{path}: cannot read README ({error})")
        return

    for mode in ("autonomous mode", "guided mode"):
        if mode not in content:
            errors.append(f"{path}: must document both execution modes; missing {mode}")


def validate_plugin(root: Path) -> list[str]:
    root = Path(root).resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")

    for relative in PLUGIN_MANIFESTS:
        path = root / relative
        if not path.is_file():
            continue
        manifest = _read_json(path, errors)
        if manifest is None:
            continue
        if manifest.get("name") != PLUGIN_NAME:
            errors.append(f"{relative}: plugin name must be {PLUGIN_NAME}")
        if relative in SKILL_DIRECTORY_MANIFESTS and manifest.get("skills") != "./skills/":
            errors.append(f"{relative}: skills must point to ./skills/")
        if relative in COMMAND_DIRECTORY_MANIFESTS and manifest.get("commands") != "./commands/":
            errors.append(f"{relative}: commands must point to ./commands/")

    for relative in MARKETPLACE_MANIFESTS:
        path = root / relative
        if not path.is_file():
            continue
        manifest = _read_json(path, errors)
        if manifest is None:
            continue
        plugins = manifest.get("plugins")
        if not isinstance(plugins, list) or not any(
            isinstance(plugin, dict) and plugin.get("name") == PLUGIN_NAME
            for plugin in plugins
        ):
            errors.append(f"{relative}: plugins must include {PLUGIN_NAME}")

    agent_manifest = root / "agents/openai.yaml"
    if agent_manifest.is_file():
        try:
            agent_text = agent_manifest.read_text(encoding="utf-8")
        except OSError as error:
            errors.append(f"{agent_manifest}: cannot read agent manifest ({error})")
        else:
            for field in ("display_name:", "short_description:", "default_prompt:"):
                if field not in agent_text:
                    errors.append(f"agents/openai.yaml: missing {field}")

    skill = root / "skills/test-e2e-playwright/SKILL.md"
    if skill.is_file():
        _check_skill_contract(skill, errors)

    readme = root / "README.md"
    if readme.is_file():
        _check_readme_modes(readme, errors)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the E2E Playwright skill package.")
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    args = parser.parse_args(argv)

    errors = validate_plugin(args.root)
    if errors:
        print("Plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Plugin validation passed: {args.root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
validate.py - Quality validation tool for ai-agent-prompt-engineering.

Validates prompt module schemas, agent configurations, and system JSON files
against the defined standards and constraints.

Usage:
    python tools/validate.py modules/prompts/auth/requirement
    python tools/validate.py agents/<scenario-name>
    python tools/validate.py systems/<system-name>/system.json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# ── Exit codes ──────────────────────────────────────────────────────────────
EXIT_OK = 0
EXIT_VALIDATION_FAILED = 1
EXIT_FILE_NOT_FOUND = 2


def _error(msg: str) -> None:
    print(f"  [ERROR] {msg}", file=sys.stderr)


def _warn(msg: str) -> None:
    print(f"  [WARN]  {msg}")


def _ok(msg: str) -> None:
    print(f"  [OK]    {msg}")


# ── Schema validation ────────────────────────────────────────────────────────

REQUIRED_SCHEMA_FIELDS = frozenset({"module", "version", "description", "parameters"})
REQUIRED_PARAM_FIELDS = frozenset({"type", "description", "required"})


def validate_schema(schema_path: Path) -> list[str]:
    """Validate a module schema JSON file. Returns a list of error messages."""
    errors = []
    try:
        with open(schema_path, encoding='utf-8') as f:
            schema = json.load(f)
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in {schema_path}: {exc}"]

    for field in REQUIRED_SCHEMA_FIELDS:
        if field not in schema:
            errors.append(f"Missing required top-level field '{field}' in {schema_path.name}")

    parameters = schema.get("parameters", {})
    if not isinstance(parameters, dict):
        errors.append("'parameters' must be an object")
        return errors

    for param_name, param_def in parameters.items():
        if not isinstance(param_def, dict):
            errors.append(f"Parameter '{param_name}' definition must be an object")
            continue
        for field in REQUIRED_PARAM_FIELDS:
            if field not in param_def:
                errors.append(f"Parameter '{param_name}' missing required field '{field}'")

    return errors


# ── Module validation ────────────────────────────────────────────────────────

def validate_module(module_path: Path) -> bool:
    """Validate a prompt or tool module directory. Returns True if valid."""
    print(f"\nValidating module: {module_path}")
    passed = True

    # Check for README
    if not (module_path / 'README.md').exists():
        _error("Missing README.md")
        passed = False
    else:
        _ok("README.md present")

    # Prompt module checks
    template_files = list(module_path.glob('*.template.md')) + list(module_path.glob('*.prompt'))
    schema_files = list(module_path.glob('*.schema.json'))

    if template_files:
        _ok(f"Template file found: {template_files[0].name}")

        # Each template should have a corresponding schema (unless it's a static .prompt)
        if template_files[0].suffix == '.md' and not schema_files:
            _error("Template module is missing a .schema.json file")
            passed = False

    if schema_files:
        schema_errors = validate_schema(schema_files[0])
        if schema_errors:
            for err in schema_errors:
                _error(err)
            passed = False
        else:
            _ok(f"Schema valid: {schema_files[0].name}")

    # Tool module checks
    workflow_files = list(module_path.glob('*.workflow.json'))
    if workflow_files:
        for wf_file in workflow_files:
            wf_errors = validate_workflow(wf_file)
            if wf_errors:
                for err in wf_errors:
                    _error(err)
                passed = False
            else:
                _ok(f"Workflow valid: {wf_file.name}")

    if not template_files and not workflow_files:
        _warn("No template or workflow files found — is this directory a module?")

    return passed


# ── Workflow validation ──────────────────────────────────────────────────────

REQUIRED_WORKFLOW_FIELDS = frozenset({"workflow", "version", "description", "parameters", "outputs"})


def validate_workflow(workflow_path: Path) -> list[str]:
    """Validate a workflow JSON file. Returns a list of error messages."""
    errors = []
    try:
        with open(workflow_path, encoding='utf-8') as f:
            workflow = json.load(f)
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in {workflow_path}: {exc}"]

    for field in REQUIRED_WORKFLOW_FIELDS:
        if field not in workflow:
            errors.append(f"Missing required field '{field}' in {workflow_path.name}")

    return errors


# ── Agent validation ─────────────────────────────────────────────────────────

REQUIRED_AGENT_FILES = frozenset({"prompt.md", "tools.json", "params.json", "README.md"})


def validate_agent(agent_path: Path) -> bool:
    """Validate an agent directory. Returns True if valid."""
    print(f"\nValidating agent: {agent_path}")
    passed = True

    for required_file in REQUIRED_AGENT_FILES:
        if not (agent_path / required_file).exists():
            _error(f"Missing required file: {required_file}")
            passed = False
        else:
            _ok(f"{required_file} present")

    # Validate tools.json structure
    tools_path = agent_path / 'tools.json'
    if tools_path.exists():
        try:
            with open(tools_path, encoding='utf-8') as f:
                tools_config = json.load(f)
            if 'tools' not in tools_config:
                _error("tools.json missing 'tools' array")
                passed = False
            else:
                repo_root = Path(__file__).parent.parent
                for tool in tools_config['tools']:
                    if 'module' not in tool:
                        _error("Tool entry missing 'module' field")
                        passed = False
                    else:
                        tool_path = repo_root / tool['module']
                        if not tool_path.exists():
                            _error(f"Referenced tool module not found: {tool['module']}")
                            passed = False
                        else:
                            _ok(f"Tool module exists: {tool['module']}")
        except json.JSONDecodeError as exc:
            _error(f"Invalid JSON in tools.json: {exc}")
            passed = False

    # Check that prompt.md does not contain hardcoded tool call syntax
    prompt_path = agent_path / 'prompt.md'
    if prompt_path.exists():
        prompt_content = prompt_path.read_text(encoding='utf-8')
        if re.search(r'<tool_call>|tool_call\(|invoke_tool\(', prompt_content):
            _warn("prompt.md may contain explicit tool call syntax — tools should be connected via canvas, not described in prompts")

    return passed


# ── System validation ────────────────────────────────────────────────────────

REQUIRED_SYSTEM_FIELDS = frozenset({"system", "version", "description", "agents", "orchestration"})


def validate_system_json(system_json_path: Path) -> bool:
    """Validate a system.json configuration file. Returns True if valid."""
    print(f"\nValidating system config: {system_json_path}")
    passed = True

    try:
        with open(system_json_path, encoding='utf-8') as f:
            system = json.load(f)
    except json.JSONDecodeError as exc:
        _error(f"Invalid JSON: {exc}")
        return False

    for field in REQUIRED_SYSTEM_FIELDS:
        if field not in system:
            _error(f"Missing required field: '{field}'")
            passed = False
        else:
            _ok(f"Field present: '{field}'")

    agents = system.get('agents', [])
    if not agents:
        _warn("No agents defined in system configuration")

    agent_ids = {a.get('id') for a in agents}
    entry_points = [a for a in agents if a.get('entry_point')]
    if not entry_points:
        _warn("No entry_point agent defined")

    # Validate orchestration references
    orchestration = system.get('orchestration', {})
    for flow in orchestration.get('flow', []):
        for direction in ('from', 'to'):
            if flow.get(direction) not in agent_ids:
                _error(f"Orchestration flow references unknown agent: '{flow.get(direction)}'")
                passed = False

    return passed


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description='Validate modules, agents, and system configurations'
    )
    parser.add_argument('target', help='Path to a module directory, agent directory, or system.json file')
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"Error: Target path does not exist: {target}", file=sys.stderr)
        return EXIT_FILE_NOT_FOUND

    if target.is_file() and target.name == 'system.json':
        passed = validate_system_json(target)
    elif target.is_dir() and (target / 'prompt.md').exists():
        passed = validate_agent(target)
    elif target.is_dir():
        passed = validate_module(target)
    else:
        print(f"Error: Cannot determine validation mode for: {target}", file=sys.stderr)
        return EXIT_FILE_NOT_FOUND

    if passed:
        print("\n✓ Validation passed")
        return EXIT_OK
    else:
        print("\n✗ Validation failed — see errors above")
        return EXIT_VALIDATION_FAILED


if __name__ == '__main__':
    sys.exit(main())

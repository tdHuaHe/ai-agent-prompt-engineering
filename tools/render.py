#!/usr/bin/env python3
"""
render.py - Template rendering engine for ai-agent-prompt-engineering.

Renders parameterized prompt templates and composes agent/system configurations
by substituting parameter values and assembling module outputs.

Usage:
    python tools/render.py modules/prompts/auth/requirement --params '{"verification_methods": ["SMS code"], "timeout_seconds": 180}'
    python tools/render.py agents/<scenario-name>
    python tools/render.py systems/<system-name>
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def render_template(template: str, params: dict) -> str:
    """Render a Handlebars-style template with the given parameters.

    Supports:
    - {{variable}} — simple variable substitution
    - {{#each list}} ... {{this}} ... {{/each}} — list iteration
    - {{join list "separator"}} — join a list with a separator
    """
    # Handle {{#each list}} ... {{/each}} blocks
    each_pattern = re.compile(
        r'\{\{#each (\w+)\}\}(.*?)\{\{/each\}\}',
        re.DOTALL
    )

    def replace_each(match: re.Match) -> str:
        var_name = match.group(1)
        block = match.group(2)
        items = params.get(var_name, [])
        if not isinstance(items, list):
            return ''
        rendered_items = []
        for item in items:
            if isinstance(item, dict):
                item_rendered = block
                for k, v in item.items():
                    item_rendered = item_rendered.replace('{{this.' + k + '}}', str(v))
            else:
                item_rendered = block.replace('{{this}}', str(item))
            rendered_items.append(item_rendered)
        return ''.join(rendered_items)

    result = each_pattern.sub(replace_each, template)

    # Handle {{join list "separator"}} expressions
    join_pattern = re.compile(r'\{\{join (\w+) "([^"]*)"\}\}')

    def replace_join(match: re.Match) -> str:
        var_name = match.group(1)
        separator = match.group(2)
        items = params.get(var_name, [])
        if not isinstance(items, list):
            return ''
        return separator.join(str(i) for i in items)

    result = join_pattern.sub(replace_join, result)

    # Handle simple {{variable}} substitutions
    simple_pattern = re.compile(r'\{\{(\w+)\}\}')

    def replace_simple(match: re.Match) -> str:
        var_name = match.group(1)
        value = params.get(var_name)
        if value is None:
            return match.group(0)  # Leave unresolved placeholders in place
        return str(value)

    result = simple_pattern.sub(replace_simple, result)

    return result


def render_module(module_path: Path, params: dict) -> str:
    """Render a single prompt module template with the given parameters."""
    # Find the template file
    template_files = list(module_path.glob('*.template.md')) + list(module_path.glob('*.prompt'))
    if not template_files:
        raise FileNotFoundError(f"No template file found in {module_path}")

    template_file = template_files[0]
    template_content = template_file.read_text(encoding='utf-8')
    return render_template(template_content, params)


def load_params(params_path: Path) -> dict:
    """Load parameters from a JSON file."""
    if not params_path.exists():
        return {}
    with open(params_path, encoding='utf-8') as f:
        return json.load(f)


def render_agent(agent_path: Path, output_path: Path | None = None) -> str:
    """Render a complete agent by composing its prompt modules."""
    params = load_params(agent_path / 'params.json')
    prompt_md_path = agent_path / 'prompt.md'

    if not prompt_md_path.exists():
        raise FileNotFoundError(f"No prompt.md found in {agent_path}")

    prompt_content = prompt_md_path.read_text(encoding='utf-8')
    repo_root = Path(__file__).parent.parent

    # Process <!-- include: module/path, params: key --> directives
    include_pattern = re.compile(
        r'<!--\s*include:\s*([^\s,]+)(?:,\s*params:\s*(\w+))?\s*-->'
    )

    def replace_include(match: re.Match) -> str:
        module_ref = match.group(1).strip()
        params_key = match.group(2).strip() if match.group(2) else None
        module_params = params.get(params_key, {}) if params_key else {}

        module_path = repo_root / 'modules' / 'prompts' / module_ref
        if not module_path.exists():
            print(f"Warning: Module not found: {module_path}", file=sys.stderr)
            return f'<!-- ERROR: module not found: {module_ref} -->'

        return render_module(module_path, module_params)

    rendered = include_pattern.sub(replace_include, prompt_content)

    if output_path:
        output_path.write_text(rendered, encoding='utf-8')
        print(f"Rendered agent prompt written to: {output_path}")

    return rendered


def render_system(system_path: Path) -> dict:
    """Render a complete system configuration, returning the final system dict."""
    params = load_params(system_path / 'params.json')
    system_config_path = system_path / 'system.json'

    if not system_config_path.exists():
        raise FileNotFoundError(f"No system.json found in {system_path}")

    with open(system_config_path, encoding='utf-8') as f:
        system_config = json.load(f)

    agents_dir = system_path / 'agents'
    if agents_dir.exists():
        for agent_dir in sorted(agents_dir.iterdir()):
            if agent_dir.is_dir():
                rendered_prompt = render_agent(agent_dir)
                for agent in system_config.get('agents', []):
                    if agent.get('id') == agent_dir.name:
                        agent['prompt'] = rendered_prompt
                        break

    return system_config


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Render prompt templates and agent/system configurations'
    )
    parser.add_argument('target', help='Path to a module, agent, or system directory')
    parser.add_argument('--params', help='JSON string of parameters (for module rendering)')
    parser.add_argument('--output', '-o', help='Output file path')
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"Error: Target path does not exist: {target}", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else None

    # Determine render mode based on directory contents
    if (target / 'system.json').exists():
        result = render_system(target)
        output = json.dumps(result, ensure_ascii=False, indent=2)
    elif (target / 'prompt.md').exists():
        output = render_agent(target, output_path)
        if output_path:
            return 0
    else:
        # Module rendering
        params = json.loads(args.params) if args.params else {}
        output = render_module(target, params)

    if output_path:
        output_path.write_text(output, encoding='utf-8')
        print(f"Output written to: {output_path}")
    else:
        print(output)

    return 0


if __name__ == '__main__':
    sys.exit(main())

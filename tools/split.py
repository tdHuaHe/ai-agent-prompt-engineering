#!/usr/bin/env python3
"""
split.py
Splits a platform system JSON export into editable YAML parts:

    templates/<industry>/
    ├── config/
  │   ├── manifest.yaml    # system metadata (all top-level fields except agents/variables/links)
  │   ├── links.yaml       # agent routing links
  │   └── variables.yaml   # all context variables
    ├── agents/
    │   ├── Coordinator.yaml
    │   ├── Account Balance and Transaction Agent.yaml
    │   ├── Authentication Agent.yaml
    │   └── ...
    └── eval/
      ├── env.yaml
      └── test_scenarios/

Usage:
    python3 tools/split.py                          # uses default SRC below
    python3 tools/split.py path/to/export.json      # custom source file
"""

import json, os, sys, re
import yaml

DEFAULT_SRC      = "systems/fsi-banking/imports/wafd-sb-AI-Agent-platform-SB - Trinity Voice Automation.json"
DEFAULT_INDUSTRY = "fsi-banking"

# ── YAML block-scalar representer ─────────────────────────────────────────────

class BlockDumper(yaml.Dumper):
    """Dumps multi-line strings as |- block scalars for readability."""
    pass

def _clean(s: str) -> str:
    """Strip trailing whitespace per line and remove non-printable control chars
    (anything below 0x20 except newline/tab) that would prevent block scalar format."""
    import re as _re
    s = _re.sub(r'[\x00-\x07\x08\x0b\x0c\x0e-\x1f\x7f]', '', s)
    return '\n'.join(line.rstrip() for line in s.splitlines())

def _str_representer(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', _clean(data), style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

BlockDumper.add_representer(str, _str_representer)

# ── Helpers ───────────────────────────────────────────────────────────────────

def file_name_from_agent(name: str) -> str:
    """Preserve agent naming style while removing filesystem-invalid characters."""
    # Keep original casing/spacing; just normalize spaces and strip invalid path chars.
    s = re.sub(r'[\\/:*?"<>|]', '', name).strip()
    return re.sub(r'\s+', ' ', s)

def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print(f"  wrote  {path}")

def write_yaml(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(obj, f, Dumper=BlockDumper, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f"  wrote  {path}")

# ── Main ──────────────────────────────────────────────────────────────────────

def split(src: str, industry: str = DEFAULT_INDUSTRY) -> None:
    base = f"templates/{industry}"

    with open(src, encoding='utf-8') as f:
        data = json.load(f)

    EXTRACTED = {"agents", "variables", "links"}

    # 1. config/manifest.yaml
    manifest = {k: v for k, v in data.items() if k not in EXTRACTED}
    write_yaml(f"{base}/config/manifest.yaml", manifest)

    # 2. config/links.yaml
    write_yaml(f"{base}/config/links.yaml", data.get("links", []))

    # 3. config/variables.yaml
    write_yaml(f"{base}/config/variables.yaml", data.get("variables", {}))

    # 4. agents/ -> all agents as YAML with instruction inline as |- block scalar
    for agent in data.get("agents", []):
        fname = file_name_from_agent(agent["agent_name"])
        if agent["role"] == "SUPERVISING_AGENT":
            write_yaml(f"{base}/agents/Coordinator.yaml", agent)
        elif agent["role"] == "ACTION_AGENT":
            write_yaml(f"{base}/agents/{fname}.yaml", agent)

    # 5. eval/ skeleton (skip if already exists)
    _scaffold_eval(base, industry, data.get("agents", []))

    print(f"\nSplit complete → {base}/")


def _scaffold_eval(base: str, industry: str, agents: list) -> None:
    """Create eval/ stub files (env.yaml + cases.yaml) only if they don't already exist."""
    KEY = industry.upper().replace("-", "_")
    action_agents = [a for a in agents if a.get("role") == "ACTION_AGENT"]

    # ── env.yaml ──────────────────────────────────────────────────────────────
    env_path = f"{base}/eval/env.yaml"
    if not os.path.exists(env_path):
        lines = [
            f"industry: {industry}",
            "",
            "environments:",
            "  test:",
            "    account_name: TODO",
            "    env_level: qa",
            "    agent_url: \"https://talkdeskchatsdk/chat.url\"",
            "    parallel_run: 2",
            "    dup_count: 2",
            "    aws_account: \"IND\"",
        ]
        os.makedirs(os.path.dirname(env_path), exist_ok=True)
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"  scaffolded {env_path}")

    # ── test_scenarios/ (empty, populated manually) ───────────────────────────
    tc_dir = f"{base}/eval/test_scenarios"
    if not os.path.isdir(tc_dir):
        os.makedirs(tc_dir, exist_ok=True)
        print(f"  scaffolded {tc_dir}/")


if __name__ == "__main__":
    src      = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    industry = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_INDUSTRY
    if not os.path.exists(src):
        print(f"Error: source file not found: {src}")
        sys.exit(1)
    split(src, industry)

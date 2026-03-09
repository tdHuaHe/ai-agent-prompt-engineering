#!/usr/bin/env python3
"""
split.py
Splits a platform system JSON export into editable parts:

  agents/<industry>/
  ├── Settings/
  │   ├── template.json       # all top-level fields except agents/variables/links
  │   └── links.json          # agent routing links
  ├── Variables/
  │   └── variables.json      # all context variables
  └── Coordinator/
      ├── coordinator.json              # SUPERVISING_AGENT
      └── Action-agents/
          ├── Account Balance and Transaction Agent/
          │   └── agent.json
          ├── Authentication Agent/
          │   └── agent.json
          └── ...

Usage:
    python3 tools/split.py                          # uses default SRC below
    python3 tools/split.py path/to/export.json      # custom source file
"""

import json, os, sys, re

DEFAULT_SRC      = "systems/fsi-banking/exports/wafd-sb-AI-Agent-platform-SB - Trinity Voice Automation.json"
DEFAULT_INDUSTRY = "fsi-banking"

# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """Keep letters, digits, spaces, hyphens; collapse whitespace."""
    s = re.sub(r'[^\w\s\-]', '', name).strip()
    return re.sub(r'\s+', ' ', s)

def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print(f"  wrote  {path}")

# ── Main ──────────────────────────────────────────────────────────────────────

def split(src: str, industry: str = DEFAULT_INDUSTRY) -> None:
    base = f"agents/{industry}"

    with open(src, encoding='utf-8') as f:
        data = json.load(f)

    EXTRACTED = {"agents", "variables", "links"}

    # 1. Settings/template.json
    template = {k: v for k, v in data.items() if k not in EXTRACTED}
    write_json(f"{base}/Settings/template.json", template)

    # 2. Settings/links.json
    write_json(f"{base}/Settings/links.json", data.get("links", []))

    # 3. Variables/variables.json
    write_json(f"{base}/Variables/variables.json", data.get("variables", {}))

    # 4. Coordinator agents
    for agent in data.get("agents", []):
        slug = slugify(agent["agent_name"])
        if agent["role"] == "SUPERVISING_AGENT":
            agent = _extract_text_fields(agent, f"{base}/Coordinator")
            write_json(f"{base}/Coordinator/Coordinator.json", agent)
        elif agent["role"] == "ACTION_AGENT":
            dest = f"{base}/Coordinator/Action-Agents/{slug}"
            agent = _extract_text_fields(agent, dest, fields=[("instruction", "instruction.md")])
            write_json(f"{dest}/agent.json", agent)

    # 5. Eval/ skeleton (skip if already exists)
    _scaffold_eval(base, industry, data.get("agents", []))

    print(f"\nSplit complete → {base}/")


def _extract_text_fields(agent: dict, dest_dir: str, fields=None) -> dict:
    """Extract long text fields to companion .md files.
    Returns a copy of the agent dict with those fields replaced by @filename refs."""
    if fields is None:
        fields = [
            ("instruction",       "Coordinator.instruction.md"),
            ("routing_condition", "Condition.instruction.md"),
        ]
    agent = dict(agent)
    for field, filename in fields:
        content = agent.get(field, "")
        if content and not content.startswith("@"):
            fpath = os.path.join(dest_dir, filename)
            os.makedirs(dest_dir, exist_ok=True)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  wrote {fpath}")
            agent[field] = f"@{filename}"
    return agent


def _scaffold_eval(base: str, industry: str, agents: list) -> None:
    """Create Eval/ stub files (env.yaml + cases.yaml) only if they don't already exist."""
    KEY = industry.upper().replace("-", "_")
    action_agents = [a for a in agents if a.get("role") == "ACTION_AGENT"]

    # ── env.yaml ──────────────────────────────────────────────────────────────
    env_path = f"{base}/Eval/env.yaml"
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
    tc_dir = f"{base}/Eval/test_scenarios"
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

#!/usr/bin/env python3
"""
build.py
Reassembles a full platform system JSON from the split parts under templates/<industry>/.

Reads:
    templates/<industry>/config/manifest.yaml         # system metadata
    templates/<industry>/config/links.yaml            # agent routing links
    templates/<industry>/config/variables.yaml        # all context variables
    templates/<industry>/agents/*.yaml                # SUPERVISING_AGENT + ACTION_AGENTs

Order: coordinator first, then action agents sorted alphabetically by agent_name.

Writes:
  systems/<industry>/builds/<account_name>_<env_level>_<system_name>_rebuilt.json

Usage:
    # Full rebuild for a named environment
    python3 tools/build.py <env_name>

    # Subset: only specific action agents (comma-separated)
    python3 tools/build.py <env_name> "Authentication Agent,FAQ Agent"

    # Different industry
    python3 tools/build.py <env_name> "" healthcare

Example:
    python3 tools/build.py pr-gate
    → reads templates/fsi-banking/eval/env.yaml → account_name=fsec, env_level=qa
    → systems/fsi-banking/builds/fsec_qa_SB - Trinity Voice Automation - Pre-Prod_rebuilt.json
"""

import json, os, sys, glob, yaml
from datetime import datetime

DEFAULT_INDUSTRY = "fsi-banking"


def load_json(path: str):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def load_yaml(path: str):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)

def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print(f"  wrote  {path}")


def _resolve_refs(agent: dict, agent_dir: str) -> dict:
    """Replace '@filename' string values with the file contents from agent_dir."""
    agent = dict(agent)
    for key, val in agent.items():
        if isinstance(val, str) and val.startswith("@"):
            fpath = os.path.join(agent_dir, val[1:])
            if os.path.exists(fpath):
                with open(fpath, encoding="utf-8") as f:
                    agent[key] = f.read()
    return agent


def build(env_name: str, include_action_agents: set | None = None, industry: str = DEFAULT_INDUSTRY) -> None:
    """
    env_name: key in templates/<industry>/eval/env.yaml  (e.g. 'pr-gate', 'nightly')
              provides account_name and env_level for the output filename.
    include_action_agents: if provided, only these ACTION_AGENT names are included.
                           SUPERVISING_AGENTs are always included.
                           Links to excluded agents are automatically dropped.
    Order: coordinator(s) first (alphabetically), then action agents (alphabetically by agent_name).
    """
    base    = f"templates/{industry}"
    out_dir = f"systems/{industry}/builds"

    # ── Read account_name + env_level from env.yaml ───────────────────────────
    env_yaml_path = f"{base}/eval/env.yaml"
    with open(env_yaml_path, encoding="utf-8") as f:
        env_config = yaml.safe_load(f)
    envs = env_config.get("environments", {})
    if env_name not in envs:
        print(f"Error: environment '{env_name}' not found in {env_yaml_path}")
        print(f"  Available: {list(envs.keys())}")
        sys.exit(1)
    tenant    = envs[env_name]["account_name"]
    env_level = envs[env_name]["env_level"]

    # ── Load parts ────────────────────────────────────────────────────────────
    template  = load_yaml(f"{base}/config/manifest.yaml")
    all_links = load_yaml(f"{base}/config/links.yaml")
    variables = load_yaml(f"{base}/config/variables.yaml")

    # ── Derive output filename from system name in template ───────────────────
    system_name = (
        template.get("agent_system_name")
        or template.get("agent_name")
        or template.get("name")
        or industry
    )
    safe_name   = system_name.replace("/", "-")
    timestamp   = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_name = f"{tenant}_{env_level}_{safe_name}_{timestamp}_rebuilt.json"

    # ── Load agent files by role ──────────────────────────────────────────────
    coordinators = []
    action_agents_all = []
    for path in sorted(glob.glob(f"{base}/agents/*.yaml")):
        a = load_yaml(path)
        if not isinstance(a, dict) or "agent_name" not in a:
            continue
        if a.get("role") == "SUPERVISING_AGENT":
            coordinators.append(a)
        elif a.get("role") == "ACTION_AGENT":
            action_agents_all.append(a)
    action_agents_all.sort(key=lambda a: a["agent_name"])

    # ── Filter action agents if subset requested ──────────────────────────────
    if include_action_agents is not None:
        requested = {name.casefold() for name in include_action_agents}
        action_agents_all = [a for a in action_agents_all if a["agent_name"].casefold() in requested]
        found = {a["agent_name"].casefold() for a in action_agents_all}
        for name in include_action_agents:
            if name.casefold() not in found:
                print(f"  WARNING: agent not found on disk: {name}")

    agents = coordinators + action_agents_all

    # ── Filter links so only included agents are referenced ──────────────────
    included_ids = {a["agent_id"] for a in agents}
    links = [
        lnk for lnk in all_links
        if lnk["source_agent_id"] in included_ids and lnk["target_agent_id"] in included_ids
    ]

    # ── Build final document — preserve original key order ───────────────────
    result = {}
    SKIP = {"_placeholder_agents", "_placeholder_variables", "_placeholder_links"}
    inserted_agents = False
    for k, v in template.items():
        if k in SKIP:
            continue
        result[k] = v
        if k == "welcome_text" and not inserted_agents:
            result["agents"] = agents
            inserted_agents = True
    if not inserted_agents:
        result["agents"] = agents

    result["links"]     = links
    result["markers"]   = template.get("markers", [])
    result["variables"] = variables

    for k, v in template.items():
        if k not in result and k not in SKIP:
            result[k] = v

    out_path = f"{out_dir}/{output_name}"
    write_json(out_path, result)

    agent_names = [a["agent_name"] for a in agents]
    print(f"\nBuild complete → {out_path}")
    print(f"  agents ({len(agents)}): {agent_names}")
    print(f"  links:  {len(links)}")
    print(f"  variables: {len(variables)} keys")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tools/build.py <env_name> [agents] [industry]")
        print("  env_name  environment key in eval/env.yaml  e.g. pr-gate, nightly")
        print("  agents    comma-separated action agent names (omit or '' for all)")
        print("  industry  e.g. fsi-banking, healthcare  (default: fsi-banking)")
        sys.exit(1)
    env_name = sys.argv[1]
    industry = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_INDUSTRY
    if len(sys.argv) > 2 and sys.argv[2].strip():
        include = {name.strip() for name in sys.argv[2].split(",")}
        print(f"  Subset mode: {include}")
    else:
        include = None
    build(env_name, include, industry)

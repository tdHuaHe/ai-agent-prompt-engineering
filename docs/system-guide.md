# How to Work with Multi-Agent Systems

## What Is a System?

A system is a complete multi-agent platform configuration that handles an end-to-end business process. In this repo, systems are stored as JSON exports from the AI Agent Platform under `systems/<industry>/`.

The system JSON is the **source of truth** — it defines every agent, every tool workflow, and the orchestration logic. Agent and module files in this repo are extracted from it.

## System Directory Structure

```
systems/<industry>/
├── exports/
│   └── <system-name>.json     # Full platform export (source of truth)
└── builds/
    └── <rebuilt>.json         # CI build output (not checked in)
```

There are no additional YAML, Markdown, or param files at the system level. Everything lives in the JSON.

## What the System JSON Contains

A platform export has the following top-level schema:

```json
{
  "agent_id": "...",
  "agent_name": "...",
  "role": "SUPERVISOR | ACTION_AGENT",
  "goal": "...",
  "instruction": "# Role\n...",
  "tools": [
    {
      "tool_name": "...",
      "input_params": { ... },
      "output_params": { ... },
      "execute_params": {
        "nodes": [ ... ],
        "edges": [ ... ],
        "variables": [ ... ]
      }
    }
  ]
}
```

Key fields:
- **`instruction`**: The agent's full prompt — maps to `instruction.prompt.md`
- **`tools[].input_params`**: Explicit inputs the agent passes to the tool — maps to `inputs:` in the workflow YAML
- **`tools[].execute_params.nodes`**: The workflow graph — `function` nodes contain JS that maps to `js_functions:` in the workflow YAML
- **`tools[].output_params`**: What the tool returns — maps to `outputs:` in the workflow YAML

## Extraction Workflow

### Step 1: Add the system JSON
Place the exported JSON under `systems/<industry>/exports/`. Use the platform's export or copy/paste from the canvas.

### Step 2: Extract agents
For each agent in the system, create an `agents/<agent-name>/` directory. See [agent-guide.md](./agent-guide.md) for the extraction process.

### Step 3: Identify reusable modules
After extracting all agents, review the instruction files and workflow YAMLs. Any pattern that appears in two or more agents is a candidate module. Extract to `modules/prompts/` or `modules/tools/` as appropriate.

### Step 4: Write the module guide
For each extracted module, add a `.guide.md` that explains the context it came from and what to change when reusing it.

## Multi-Agent Orchestration

In the current FSI Banking system, the orchestration pattern is:

```
[Supervisor / Coordinator]
        │
        ├── route → [FAQ Agent]
        ├── route → [Account Balance and Transactions Agent]
        └── escalate → [Session Summary Agent] → human handoff
```

Orchestration logic (routing conditions, escalation triggers) lives in the Supervisor's `instruction.prompt.md`. The reusable portions of that logic are extracted to `modules/prompts/orchestration/`.

## Current Systems

| System | Industry | File |
|--------|----------|------|
| Trinity Voice Automation | FSI Banking | `systems/fsi-banking/exports/wafd-sb-AI-Agent-platform-SB - Trinity Voice Automation.json` |


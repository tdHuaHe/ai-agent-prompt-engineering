# How to Define Agents

## What Is an Agent?

An agent is a combination of an instruction prompt and a set of tool workflows, assembled to handle a specific business role. Agents are defined in the `agents/` directory and represent the second layer of the composition hierarchy.

## Agent Directory Structure

```
agents/<agent-name>/
├── instruction.prompt.md            # The full agent instruction
├── <tool-name>.workflow.yaml        # One file per tool the agent uses
└── <tool-name>.workflow.yaml        # (repeat for each tool)
```

There is no `tools.json`, `params.json`, or `README.md`. The instruction and workflow files are self-contained.

## `instruction.prompt.md`

The agent instruction is stored verbatim — exactly as it appears on the AI Agent Platform. No template syntax, no parameter placeholders.

```
## Role
Retrieve account balance and transaction information for authenticated customers...

## CRITICAL RULES
- Customer MUST be authenticated before any data retrieval
...

## PROCESSING FLOW
### Step 0: Identify Intent
...
```

When a section of the instruction is reusable across agents, extract it to a prompt module in `modules/prompts/<category>/`. The module `.guide.md` then explains how to adapt it.

## `<tool-name>.workflow.yaml`

Each tool available to the agent has its own `.workflow.yaml`. The file name matches the tool name used in the platform.

Workflow YAMLs follow the format defined in [module-guide.md](./module-guide.md):
- `inputs:` — parameters the agent explicitly passes to the tool
- `internal:` — context variables the workflow reads from session state
- `outputs:` — what the tool writes back to context
- `logic:` — step-by-step description of what the workflow does
- `js_functions:` — verbatim JavaScript from the platform workflow nodes

## Extracting an Agent from a System JSON

### Step 1: Locate the agent JSON
Open the source system export in `systems/industries/<industry>/`. Find the agent block. The `instruction` field is the agent instruction; `tools` contains all workflow definitions.

### Step 2: Create the instruction file
Create `agents/<agent-name>/instruction.prompt.md`. Copy the `instruction` field content exactly.

### Step 3: Create workflow files
For each entry in `tools`, create `agents/<agent-name>/<tool-name>.workflow.yaml`:
- Map `input_params` → `inputs:`; context-read variables → `internal:`
- Document outputs from `output_params` and context writes in `outputs:`
- Summarize node sequence in `logic:`
- Copy JS from each `function` node verbatim into `js_functions:`

### Step 4: Extract reusable modules
If a section of the instruction appears in multiple agents, extract it to `modules/prompts/<category>/` with a `.guide.md`.

If a workflow is not specific to one agent's data model, move it to `modules/tools/<category>/`.

## Current Agents

| Agent | Tools |
|-------|-------|
| `account-balance-and-transactions-agent` | `query-customer-accounts`, `get-account-balance`, `get-account-transactions` |
| `session-summary-agent` | `gather-summary` |
| `faq-agent` | (no tools) |


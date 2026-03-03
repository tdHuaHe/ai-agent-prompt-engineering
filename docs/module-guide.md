# How to Design Good Modules

## What Is a Module?

A module is a self-contained, reusable building block extracted from a production agent. Modules come in two types:

- **Prompt modules** (`modules/prompts/`): Verbatim prompt text extracted from production agents, organized by role
- **Tool workflow modules** (`modules/tools/`): Workflow definitions with documented inputs, outputs, and implementation JS

---

## Prompt Module Design

### File Format

A prompt module is one or two files in a flat category directory:

```
modules/prompts/<category>/
├── <module-name>.prompt.md   # The verbatim prompt text
└── <module-name>.guide.md    # (optional) Reuse instructions
```

There is no template syntax and no parameter schema. The `.prompt.md` contains the actual production text.

#### Example: `modules/prompts/orchestration/supervisor-routing-priority.prompt.md`
```markdown
## Supported Scope
### Supported
- Questions about **guidance**.
- Questions about **products, services, policies, fees, and rates**.
...

## Request Handling Logic (Order of Priority)
### 1. Human Agent Requests (Highest Priority)
...
```

### The `.guide.md` File

The companion `.guide.md` explains what needs to change when adapting the module for a new context:

```markdown
# supervisor-routing-priority — Usage Guide

## Reuse Steps

1. Replace `### Supported` with what your skill agent handles
2. Replace `### Not Supported` with what is out of scope
3. Replace `FAQ Agent` with your downstream agent name
...
```

### Design Principles

#### Extract from production, don't author speculatively
A prompt module should come from a working agent. Copy the exact text first; generalize only what must change across use cases, and document those points in the `.guide.md`.

#### One concern per module
Each module covers one cross-cutting behavior: routing logic, escalation flow, safety rules, output format, etc. If a module covers two distinct behaviors, split it.

#### Generality threshold
Only extract to a module if the pattern plausibly applies in at least two different agents. Agent-specific logic stays in `agents/`.

### Categories

| Category | Purpose |
|----------|---------|
| `auth/` | Identity verification requirements |
| `input/` | Intent parsing and entity extraction |
| `orchestration/` | Supervisor routing, escalation flows |
| `output/` | Response format rules |
| `safety/` | PII protection, data handling rules |

---

## Tool Workflow Module Design

### File Format

```
modules/tools/<category>/
└── <workflow-name>.workflow.yaml
```

A single `.workflow.yaml` per workflow. No README — the YAML is self-documenting.

### YAML Structure

```yaml
tool: <category>/<workflow-name>
description: >
  One or two sentences describing what this workflow does.

# ─── Input ────────────────────────────────────────────────────────────────────
inputs:
  <param_name>:
    required: true|false
    description: What this parameter is and where it comes from.
  # Use `inputs: none` if there are no external inputs.

# ─── Internal context vars (resolved inside workflow) ─────────────────────────
internal:
  <var_name>: Where this variable comes from and how it is used.

# ─── Output ───────────────────────────────────────────────────────────────────
outputs:
  <output_name>:
    context_var: <context variable name>
    description: |
      Description with example values for each scenario.
  skill_execution_result:
    context_var: skill_execution_result
    description: "{ skill_name, skill_result: success|warning|error, skill_message }"

# ─── Logic ────────────────────────────────────────────────────────────────────
logic:
  - step: 1
    name: <Node name from platform>
    description: >
      Plain-English description of what this step does, including branch conditions.

# ─── JS functions ─────────────────────────────────────────────────────────────
js_functions:
  <function_name>: |
    // verbatim JS from the platform workflow node
    function example() { ... }
```

### Key Conventions

#### `inputs` vs `internal`
- **`inputs:`** — parameters that the agent explicitly passes in when calling the tool (defined in `input_params` in the platform JSON)
- **`internal:`** — context variables that the workflow reads from session context (set by earlier steps, not passed as explicit inputs)

This distinction matters: `inputs` are the tool's public interface; `internal` are implicit runtime dependencies.

#### `js_functions`
Paste the JS verbatim from the platform workflow node. Do not rewrite or pseudocode it. The function name is the node name (lowercased, underscored). When one node contains multiple functions, group them under one key.

#### `skill_execution_result`
Every tool workflow outputs a `skill_execution_result` context variable. The schema is always:
```json
{ "skill_name": "<tool_name>", "skill_result": "success|warning|error", "skill_message": "..." }
```

### When to Put Workflows in `modules/tools/` vs `agents/`

Workflows that are specific to one agent's data model or business logic belong in `agents/<agent-name>/`. Extract to `modules/tools/<category>/` when the workflow pattern could serve multiple agents (e.g., a generic SMS verification flow, a date parser, an HTTP caller).


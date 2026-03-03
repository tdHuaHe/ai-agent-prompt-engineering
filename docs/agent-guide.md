# How to Compose Modules into Agents

## What Is an Agent?

An agent is a combination of a Prompt and a set of Tools, assembled to handle a specific business scenario. Agents are defined in the `agents/` directory and represent the second layer of the composition hierarchy.

## Agent Directory Structure

```
agents/<scenario-name>/
├── prompt.md           # Composed agent prompt
├── tools.json          # List of tool modules used
├── params.json         # Parameter values for all modules
└── README.md           # Agent description, usage, and composition notes
```

## Composition Workflow

### Step 1: Identify Required Capabilities

Start by listing what the agent needs to do:
- What does the user ask the agent?
- What does the agent need to verify or check?
- What format should the output be in?
- What safety rules must be enforced?

### Step 2: Find Matching Modules

Search `modules/prompts/` for modules that cover each capability:

```
modules/prompts/auth/     → identity and authorization requirements
modules/prompts/input/    → understanding and parsing user input
modules/prompts/output/   → response format control
modules/prompts/safety/   → safety rules and PII protection
```

Similarly, search `modules/tools/` for required workflows.

### Step 3: Compose the Prompt

The agent prompt is assembled by including the selected module templates. Each module is rendered with scenario-specific parameter values.

**Example `prompt.md`**:
```markdown
<!-- include: modules/prompts/auth/requirement, params: auth -->
<!-- include: modules/prompts/input/intent-parsing, params: input -->

## Business Logic

You are a loan application assistant. Guide the user through the application process...

<!-- include: modules/prompts/output/json-strict, params: output -->
<!-- include: modules/prompts/safety/pii-protection, params: safety -->
```

### Step 4: Define Tool References

The `tools.json` file lists all tool modules used by this agent:

```json
{
  "tools": [
    {
      "module": "modules/tools/auth/phone-sms",
      "alias": "verify_phone"
    },
    {
      "module": "modules/tools/data/web-scraping",
      "alias": "fetch_product_info"
    }
  ]
}
```

Tools are connected to the agent via canvas nodes. The prompt does not need to describe tool-calling logic explicitly.

### Step 5: Set Parameter Values

The `params.json` file provides values for all module parameters:

```json
{
  "auth": {
    "verification_methods": ["SMS code"],
    "timeout_seconds": 180
  },
  "input": {
    "domain": "loan application",
    "supported_languages": ["zh-CN", "en"]
  },
  "output": {
    "schema_reference": "loan_application_schema"
  },
  "safety": {
    "pii_fields": ["id_number", "bank_account", "phone_number"]
  }
}
```

## Design Constraints

### Must Compose First
- Always start from modules. Only add custom logic after confirming no existing module meets the need.
- If you write more than 20% custom prompt logic, consider whether new modules should be extracted.

### No Tool Logic in Prompts
- Prompts describe **what** the agent does, not **how** tools are called.
- Tool-calling logic is handled by canvas connections and the platform runtime.

### No Module Rewriting
- Never copy a module's content into an agent and modify it inline.
- If a module doesn't fit your needs exactly, either use parameters to adapt it or propose a new module.

### Thin Custom Layer
- Business-specific content (product names, domain terminology, specific rules) belongs in the agent layer.
- Generic logic (authorization patterns, safety rules, output formats) belongs in modules.

## Agent README Template

```markdown
# Agent: <Name>

## Purpose
One-paragraph description of what this agent does and for whom.

## Modules Used
| Module | Purpose |
|--------|---------|
| `auth/requirement` | Verify user identity via SMS |
| `output/json-strict` | Return structured JSON responses |

## Tools Used
| Tool | Alias | Purpose |
|------|-------|---------|
| `tools/auth/phone-sms` | verify_phone | SMS verification |

## Custom Logic
Description of any business-specific logic added beyond modules.

## Parameters
Link to or inline the params.json content.
```

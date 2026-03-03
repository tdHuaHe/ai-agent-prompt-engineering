# How to Design Good Modules

## What Is a Module?

A module is a self-contained, reusable building block that encapsulates a single, well-defined capability. Modules come in two types:

- **Prompt modules** (`modules/prompts/`): Parameterized prompt snippets that express agent behavior
- **Tool modules** (`modules/tools/`): Workflow definitions that give agents access to external systems

## Prompt Module Design

### Directory Structure

Each prompt module lives in its own directory under the relevant category:

```
modules/prompts/<category>/<module-name>/
├── <module-name>.template.md   # Parameterized prompt template
├── <module-name>.schema.json   # Parameter definitions and validation
└── README.md                   # Usage instructions and examples
```

### Template Format

Prompt templates use `{{parameter_name}}` syntax for variable substitution:

```markdown
## Authorization Requirements

You must verify the user's identity before proceeding. Accepted verification methods:
{{#each verification_methods}}
- {{this}}
{{/each}}

Verification timeout: {{timeout_seconds}} seconds.
```

### Schema Format

Each template must have a corresponding JSON schema:

```json
{
  "module": "auth/requirement",
  "version": "1.0.0",
  "description": "Defines authorization requirements for an agent",
  "parameters": {
    "verification_methods": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of accepted verification methods",
      "required": true,
      "examples": [["SMS code", "bank card"]]
    },
    "timeout_seconds": {
      "type": "integer",
      "description": "Verification timeout in seconds",
      "required": false,
      "default": 300
    }
  }
}
```

### Design Principles

#### Atomicity
Each module solves exactly one problem. If you find yourself writing "and also..." in a module description, split it into two modules.

#### Generality
A module should be applicable across at least two distinct business scenarios. If a module only makes sense in one context, it belongs in the `agents/` layer instead.

#### Parameterization
Abstract all business-specific details into parameters. The template contains the general logic; parameters provide the specifics.

#### Clarity
The module README should answer:
- What problem does this module solve?
- What are the required and optional parameters?
- What does the rendered output look like?
- Which agents currently use this module?

## Tool Module Design

### Directory Structure

```
modules/tools/<category>/<workflow-name>/
├── <workflow-name>.workflow.json   # Workflow definition
└── README.md                       # Usage instructions
```

Alternatively, for simple single-file workflows:
```
modules/tools/<category>/
├── <workflow-name>.workflow.json
└── README.md
```

### Workflow Definition Format

```json
{
  "workflow": "auth/phone-sms",
  "version": "1.0.0",
  "description": "Sends and verifies an SMS verification code",
  "parameters": {
    "phone_number_variable": {
      "type": "string",
      "description": "Canvas variable name holding the user's phone number"
    }
  },
  "nodes": []
}
```

### Design Principles

#### Single Responsibility
Each workflow performs one logical operation (e.g., "send and verify SMS code", not "do all auth").

#### Platform Compatibility
Workflows must be compatible with the internal Workflow system. Use only supported node types and connection patterns.

#### Parameter-Driven
Hardcoded values should be replaced with parameters wherever the value might differ between deployments.

## Quality Checklist

Before adding a module, verify:

- [ ] The module solves a single, clearly defined problem
- [ ] It is applicable in at least two business scenarios
- [ ] All variable parts are parameterized
- [ ] A schema file defines and validates all parameters
- [ ] A README explains usage with at least one example
- [ ] The module has been tested in at least one agent context

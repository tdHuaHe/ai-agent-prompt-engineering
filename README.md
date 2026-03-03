# ai-agent-prompt-engineering

An engineering assembly system for Multi-agent Systems, designed to achieve reuse, composition, and quality management of prompts and tools through modular design.

## Overview

This repository provides a structured framework for building AI agents and multi-agent systems on top of an internal AI Agent Platform (low-code canvas). The final output is a **Multi-agent Template** (JSON configuration file). Each agent is composed of a **Prompt** and a set of **Tools**, where Tools are backed by a Workflow system.

**Core Philosophy**:
- **Modular Reuse**: Provide parameterizable prompt and tool building blocks
- **Composition over Authoring**: Prioritize composing from modules, then fine-tune
- **Layered Design**: From low-level modules to top-level multi-agent templates
- **Engineering Management**: Standardized design, evaluation, and tooling support

---

## Repository Structure

```
ai-agent-prompt-engineering/
│
├── docs/                    # 📘 Design standards and guidelines
│   ├── philosophy.md        # Why engineering-based assembly
│   ├── module-guide.md      # How to design good modules
│   ├── agent-guide.md       # How to compose modules into agents
│   └── system-guide.md      # How to design multi-agent systems
│
├── modules/                 # 🧱 Reusable component building blocks
│   ├── prompts/            # Prompt building block library
│   │   ├── auth/           # Authorization-related prompt capabilities
│   │   ├── input/          # Input understanding capabilities
│   │   ├── output/         # Output format control
│   │   └── safety/         # Safety and governance
│   └── tools/              # Tool/Workflow building block library
│       ├── auth/           # Authorization verification workflows
│       ├── data/           # Data processing workflows
│       └── integration/    # Third-party integration workflows
│
├── agents/                 # 🤖 Agent templates (Prompt + Tools composition)
│   └── [specific business scenario]/
│
├── systems/                # 🏗️ Multi-agent templates (final deliverables)
│   └── [complete business system]/
│
├── eval/                   # 🧪 Quality evaluation framework
│   ├── modules/           # Module-level tests
│   ├── agents/            # Agent-level tests
│   └── systems/           # System-level tests
│
└── tools/                  # 🛠️ Engineering tools
    ├── render.py          # Template rendering
    └── validate.py        # Quality validation
```

---

## Layers

### 1. `modules/` — Reusable Component Library

The foundation of the system. Each module is a validated, parameterizable building block.

**Prompt modules** (`modules/prompts/`) solve specific prompt-level problems:
- `auth/requirement` — Enforces mandatory identity verification
- `input/intent-parsing` — Guides intent identification and entity extraction
- `output/json-strict` — Forces strict JSON output conforming to a schema
- `output/structured` — Human-readable structured response format
- `safety/pii-protection` — Enforces PII handling and data minimization rules

**Tool modules** (`modules/tools/`) define reusable workflow definitions:
- `auth/phone-sms` — SMS verification code workflow
- `auth/bank-card` — Bank card identity verification workflow
- `data/web-scraping` — Web page content extraction workflow
- `data/date-parser` — Natural language date parsing workflow
- `integration/api-caller` — Generic HTTP API caller workflow

Each module contains:
- A template file (`.template.md` or `.prompt`) with `{{parameter}}` placeholders
- A schema file (`.schema.json`) defining and validating parameters
- A `README.md` with usage instructions and examples

### 2. `agents/` — Agent Templates

Business-scenario-specific agents assembled by composing prompt and tool modules. Each agent defines:
- `prompt.md` — Composed prompt with module include directives
- `tools.json` — Tool module references
- `params.json` — Parameter values for all included modules
- `README.md` — Agent description and composition notes

> See [docs/agent-guide.md](docs/agent-guide.md) before creating a new agent.

### 3. `systems/` — Multi-Agent Templates

Complete multi-agent system configurations — the final deliverables. Each system contains:
- `system.json` — Full orchestration configuration (importable into the AI Agent Platform)
- Per-agent prompt, tools, and parameter configurations
- System-level parameters and environment configuration

> See [docs/system-guide.md](docs/system-guide.md) before creating a new system.

### 4. `eval/` — Quality Evaluation Framework

Layered quality assurance covering the full chain:
- `eval/modules/` — Module rendering and parameter validation tests
- `eval/agents/` — Agent functional and safety tests
- `eval/systems/` — End-to-end business flow tests

### 5. `tools/` — Engineering Tools

- **`render.py`** — Renders parameterized templates into final configurations
- **`validate.py`** — Validates module schemas, agent configs, and system JSON files

---

## Quick Start

### Render a prompt module

```bash
python tools/render.py modules/prompts/auth/requirement \
  --params '{"verification_methods": ["SMS code"], "timeout_seconds": 180}'
```

### Validate a module

```bash
python tools/validate.py modules/prompts/auth/requirement
```

### Render and validate an agent

```bash
python tools/render.py agents/my-agent --output /tmp/my-agent-prompt.md
python tools/validate.py agents/my-agent
```

### Render a system configuration

```bash
python tools/render.py systems/my-system --output systems/my-system/system.rendered.json
python tools/validate.py systems/my-system/system.json
```

---

## Design Guidelines

| Document | Description |
|----------|-------------|
| [docs/philosophy.md](docs/philosophy.md) | Why we use engineering-based assembly |
| [docs/module-guide.md](docs/module-guide.md) | How to design good reusable modules |
| [docs/agent-guide.md](docs/agent-guide.md) | How to compose modules into agents |
| [docs/system-guide.md](docs/system-guide.md) | How to design multi-agent systems |

---

## Contributing

1. **Adding a module**: Follow [docs/module-guide.md](docs/module-guide.md). Include a schema, README, and at least one eval test.
2. **Adding an agent**: Follow [docs/agent-guide.md](docs/agent-guide.md). Compose from existing modules first.
3. **Adding a system**: Follow [docs/system-guide.md](docs/system-guide.md). Render and validate before submitting.
4. **All contributions** must pass `tools/validate.py` before merging.

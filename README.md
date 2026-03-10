# ai-agent-prompt-engineering

An engineering repository for building, governing, and reusing multi-agent templates on our internal AI Agent Platform.

## Overview

This repo is the production assembly line for multi-agent template delivery.

It serves three purposes:

1. `templates/`: manage industry-specific basic templates in a split, reviewable format.
2. `modules/`: maintain cross-industry reusable best practices for `prompts` and `tools`.
3. `docs/`: provide platform rules, usage guidance, and context for both humans and Copilot.

The final output is a complete platform-importable system JSON.

## Core Principles

- Modular reuse over rewriting.
- Composition over ad hoc authoring.
- Git-based engineering management (diff, review, rollback, traceability).
- Quality-gated merge through automated build and E2E validation.

---

## Repository Structure

```text
ai-agent-prompt-engineering/
├── templates/                               # Industry-specific editable assets
│   ├── fsi-banking/
│   │   ├── config/
│   │   │   ├── manifest.yaml                # Top-level system metadata
│   │   │   ├── links.yaml                   # Inter-agent routing links
│   │   │   └── variables.yaml               # Shared context variables
│   │   ├── agents/
│   │   │   ├── coordinator.yaml             # Supervisor agent (instruction inline |-block)
│   │   │   ├── faq agent.yaml
│   │   │   └── <action agent name>.yaml
│   │   └── eval/
│   │       ├── env.yaml
│   │       └── test_scenarios/
│   ├── healthcare/
│   └── retail/
├── modules/                                 # Cross-industry reusable library
│   ├── prompts/                             # Prompt patterns and best practices
│   │   ├── auth/
│   │   ├── input/
│   │   ├── orchestration/
│   │   ├── output/
│   │   └── safety/
│   └── tools/                               # Reusable tool/workflow/function patterns
│       ├── auth/
│       ├── data/
│       └── integration/
├── docs/                                    # Knowledge base and platform rules
│   ├── philosophy.md
│   ├── module-guide.md
│   ├── agent-guide.md
│   ├── system-guide.md
│   └── platform-prompt/
├── systems/                                 # Raw imports and rebuilt outputs
│   └── <industry>/
│       ├── imports/
│       └── builds/
└── tools/
    ├── split.py                             # Import JSON -> templates/<industry>/ split files
    └── build.py                             # templates/<industry>/ -> rebuilt system JSON
```

---

## Standard Workflow

### 1. Update Source Export

Put an updated full platform import file under:

- `systems/<industry>/imports/*.json`

### 2. Split into Reviewable Files

Use `ai-agent-templates decompose` to extract editable YAML files into `templates/<industry>/`:

```bash
./ai-agent-templates decompose "systems/fsi-banking/imports/<import-file>.json" --industry fsi-banking
```

Each agent is written as a single lowercase `<agent name>.yaml` with instruction rendered as a `|-` block scalar for readability. System metadata, links, and variables are written to `config/`.

### 3. Open PR on `templates/` Changes

PR review is done on split files so change scope is clear at file level.

### 4. Scope-Aware Test Trigger

CI detects changed paths and triggers different levels of tests:

- Action-agent-only changes: targeted tests + smoke tests.
- Coordinator/config changes: full regression.
- Docs-only changes: docs checks only.

### 5. Build Before E2E

Workflow rebuilds full JSON from `templates/<industry>/` to verify assembly integrity:

```bash
./ai-agent-templates compose test --industry fsi-banking
```

Output is written to:

- `systems/<industry>/builds/*_rebuilt.json`

### 6. Import and Run E2E Tests

Rebuilt JSON is auto-imported into the platform test environment and validated with the existing agentic chat automation framework.

### 7. Quality Gate and Review

Only PRs that pass quality gates proceed to human review and merge.

---

## Quick Start

### Split a system export

```bash
./ai-agent-templates decompose "systems/fsi-banking/imports/<import-file>.json" --industry fsi-banking
```

### Rebuild a full industry system

```bash
./ai-agent-templates compose test --industry fsi-banking
```

`test` here is the environment key from `templates/<industry>/eval/env.yaml`.

### Rebuild with selected action agents (debug mode)

```bash
./ai-agent-templates compose test --industry fsi-banking --agents "Authentication Agent,FAQ Agent"
```

`--agents` is the parameter used to select an action-agent subset for composition.
The coordinator agent is always included automatically.

### FSI Banking common examples

Split a specific banking import file:

```bash
./ai-agent-templates decompose "systems/fsi-banking/imports/fsec-AI-Agent-platform-FSI Providers Multi Agent - hehua-2026-03-09T18-17.json" --industry fsi-banking
```

Build with selected action agents (`Member Search`, `Account Balance`, `FAQ`):

```bash
./ai-agent-templates compose test --industry fsi-banking --agents "Member Search Agent,Account Balance and Transaction Agent,FAQ Agent"
```

---

## Quality Gate (Recommended Baseline)

Merge should require all of the following:

1. Build succeeds and produces rebuilt JSON.
2. Rebuilt JSON imports successfully in test environment.
3. All P0/P1 business scenarios pass.
4. Overall pass rate meets threshold.
5. No blocker-level safety/compliance issues.

---

## Phased Plan

### Phase 1: Engineerized Basic Template Governance

- Standardize split-file management in `templates/`.
- Use Git PR workflow for diff, review, and controlled merge.
- Enforce automated build + E2E + quality gates.

### Phase 2: Reusable Module Library

- Extract stable cross-industry patterns into `modules/prompts` and `modules/tools`.
- Reduce duplication and improve consistency.
- Default to module reuse when creating new capabilities.

### Phase 3: Copilot-Assisted Template Assembly

- Use `docs/` as platform context and policy knowledge.
- Reuse existing industry basic templates from `templates/`.
- Reuse best-practice modules from `modules/`.
- Generate import-ready full template JSON for rapid testing and tuning.

---

## Design Docs

- [docs/philosophy.md](docs/philosophy.md)
- [docs/module-guide.md](docs/module-guide.md)
- [docs/agent-guide.md](docs/agent-guide.md)
- [docs/system-guide.md](docs/system-guide.md)

---

## Contributing

1. Start from `systems/<industry>/imports`, then split to `templates/<industry>/`.
2. Keep PR scope explicit and industry-focused.
3. Ensure build and required tests pass before requesting merge.
4. Promote proven reusable logic into `modules/`.
5. Update `docs/` when platform rules or conventions change.

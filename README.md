# ai-agent-prompt-engineering

An engineering repository for building, governing, and reusing multi-agent templates on our internal AI Agent Platform.

## Overview

This repo is the production assembly line for multi-agent template delivery.

It serves three purposes:

1. `agents/`: manage industry-specific basic templates in a split, reviewable format.
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
├── agents/                                  # Industry-specific editable assets
│   ├── fsi-banking/
│   │   ├── Settings/
│   │   │   ├── template.json                # Top-level system fields
│   │   │   └── links.json                   # Inter-agent routing links
│   │   ├── Variables/
│   │   │   └── variables.json               # Shared variables
│   │   ├── Coordinator/
│   │   │   ├── Coordinator.json             # Supervisor agent config
│   │   │   ├── Coordinator.instruction.md   # Supervisor instruction
│   │   │   ├── Condition.instruction.md     # Routing condition instruction
│   │   │   └── Action-Agents/
│   │   │       └── <Action Agent Name>/
│   │   │           ├── agent.json
│   │   │           └── instruction.md
│   │   └── Eval/
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
├── systems/                                 # Full exports and rebuilt outputs
│   └── <industry>/
│       ├── exports/
│       └── builds/
└── tools/
    ├── split.py                             # Export JSON -> agents/<industry>/ split files
    └── build.py                             # agents/<industry>/ -> rebuilt system JSON
```

---

## Standard Workflow

### 1. Update Source Export

Put an updated full platform export under:

- `systems/<industry>/exports/*.json`

### 2. Split into Reviewable Files

Use `split.py` to extract editable files into `agents/<industry>/`:

```bash
python3 tools/split.py systems/fsi-banking/exports/<export-file>.json fsi-banking
```

### 3. Open PR on `agents/` Changes

PR review is done on split files so change scope is clear at file level.

### 4. Scope-Aware Test Trigger

CI detects changed paths and triggers different levels of tests:

- Action-agent-only changes: targeted tests + smoke tests.
- Coordinator/settings/links/variables changes: full regression.
- Docs-only changes: docs checks only.

### 5. Build Before E2E

Workflow rebuilds full JSON from `agents/<industry>/` to verify assembly integrity:

```bash
python3 tools/build.py test "" fsi-banking
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
python3 tools/split.py systems/fsi-banking/exports/<export-file>.json fsi-banking
```

### Rebuild a full industry system

```bash
python3 tools/build.py test "" fsi-banking
```

### Rebuild with selected action agents (debug mode)

```bash
python3 tools/build.py test "Authentication Agent,FAQ Agent" fsi-banking
```

### FSI Banking common examples

Split a specific banking export file:

```bash
python3 tools/split.py "systems/fsi-banking/exports/fsec-AI-Agent-platform-FSI Providers Multi Agent - hehua-2026-03-09T18-17.json" fsi-banking
```

Build with selected action agents (`Member Search`, `Account Balance`, `FAQ`):

```bash
python3 tools/build.py test "Member Search Agent,Account Balance and Transaction Agent,FAQ Agent" fsi-banking
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

- Standardize split-file management in `agents/`.
- Use Git PR workflow for diff, review, and controlled merge.
- Enforce automated build + E2E + quality gates.

### Phase 2: Reusable Module Library

- Extract stable cross-industry patterns into `modules/prompts` and `modules/tools`.
- Reduce duplication and improve consistency.
- Default to module reuse when creating new capabilities.

### Phase 3: Copilot-Assisted Template Assembly

- Use `docs/` as platform context and policy knowledge.
- Reuse existing industry basic templates from `agents/`.
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

1. Start from `systems/<industry>/exports`, then split to `agents/<industry>/`.
2. Keep PR scope explicit and industry-focused.
3. Ensure build and required tests pass before requesting merge.
4. Promote proven reusable logic into `modules/`.
5. Update `docs/` when platform rules or conventions change.

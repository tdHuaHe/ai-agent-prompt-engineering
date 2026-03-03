# Systems

This directory contains multi-agent system templates — the final deliverables of the engineering framework. Each system orchestrates multiple agents to handle a complete business process.

## Structure

Each system lives in its own subdirectory:

```
systems/<system-name>/
├── system.json         # Full system configuration (final deliverable)
├── agents/             # Per-agent configurations for this system
│   └── <agent-name>/
│       ├── prompt.md
│       ├── tools.json
│       └── params.json
├── params.json         # System-level parameters
└── README.md           # System architecture and data flow
```

## Creating a New System

1. Read [docs/system-guide.md](../docs/system-guide.md) before starting.
2. Map the complete business process and identify agent boundaries.
3. Compose each agent following [docs/agent-guide.md](../docs/agent-guide.md).
4. Define orchestration logic in `system.json`.
5. Render the final configuration: `python tools/render.py systems/<system-name>`.
6. Validate: `python tools/validate.py systems/<system-name>/system.json`.
7. Add end-to-end tests in `eval/systems/<system-name>/`.

## Existing Systems

| System | Description |
|--------|-------------|
| *(none yet — add your first system!)* | |

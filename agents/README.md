# Agents

This directory contains agent templates — combinations of prompt modules and tool modules assembled to handle specific business scenarios.

## Structure

Each agent lives in its own subdirectory:

```
agents/<scenario-name>/
├── prompt.md       # Composed agent prompt (references modules)
├── tools.json      # Tool modules used by this agent
├── params.json     # Parameter values for all included modules
└── README.md       # Agent description and composition notes
```

## Creating a New Agent

1. Read [docs/agent-guide.md](../docs/agent-guide.md) before starting.
2. Identify which modules from `modules/prompts/` and `modules/tools/` cover your requirements.
3. Create a new subdirectory under `agents/` with the scenario name.
4. Compose the prompt, define tool references, and set parameter values.
5. Run `python tools/validate.py agents/<scenario-name>` to validate.
6. Add eval tests in `eval/agents/<scenario-name>/`.

## Existing Agents

| Agent | Description |
|-------|-------------|
| *(none yet — add your first agent!)* | |

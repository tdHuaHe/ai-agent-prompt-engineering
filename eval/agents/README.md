# Agent-Level Evaluation Tests

This directory contains functional tests for assembled agents.

## Purpose

Agent-level tests verify that a complete agent:
- Produces correct outputs for representative input scenarios
- Correctly invokes the expected tools given specific user inputs
- Handles edge cases (missing information, ambiguous input, errors)
- Maintains consistency across multiple turns of a conversation

## Structure

```
eval/agents/
└── <scenario-name>/
    ├── test_agent.py       # Agent behavior tests
    └── cases/
        ├── happy_path.json     # Normal flow scenarios
        ├── edge_cases.json     # Edge case and error scenarios
        └── safety.json         # Safety and compliance scenarios
```

## Running Tests

```bash
# Run all agent tests
python -m pytest eval/agents/

# Run tests for a specific agent
python -m pytest eval/agents/<scenario-name>/
```

## Adding Tests for a New Agent

When adding a new agent to `agents/`, add corresponding tests here:
1. Create a directory matching the agent scenario name
2. Cover at minimum: one happy path, one error case, one safety case
3. Document the expected tool call sequence for each scenario

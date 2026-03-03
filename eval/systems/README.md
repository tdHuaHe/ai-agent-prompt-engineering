# System-Level Evaluation Tests

This directory contains end-to-end tests for complete multi-agent systems.

## Purpose

System-level tests verify that a complete multi-agent system:
- Successfully handles representative end-to-end business flows
- Correctly routes between agents based on orchestration logic
- Maintains data integrity as information passes between agents
- Meets overall system-level performance and quality requirements

## Structure

```
eval/systems/
└── <system-name>/
    ├── test_system.py      # End-to-end system tests
    └── cases/
        ├── e2e_happy.json      # Complete happy-path flows
        ├── e2e_errors.json     # Error handling and recovery flows
        └── e2e_boundary.json   # Boundary and stress test scenarios
```

## Running Tests

```bash
# Run all system tests
python -m pytest eval/systems/

# Run tests for a specific system
python -m pytest eval/systems/<system-name>/
```

## Adding Tests for a New System

When adding a new system to `systems/`, add corresponding tests here:
1. Create a directory matching the system name
2. Cover at minimum: one complete happy-path flow through all agents
3. Test agent handoff conditions (what happens when Agent A returns different results)
4. Test system-level error recovery

# Module-Level Evaluation Tests

This directory contains quality tests for individual prompt and tool modules.

## Purpose

Module-level tests verify that each module:
- Renders correctly with valid parameter inputs
- Fails gracefully with invalid parameters
- Produces output that meets the documented quality standard
- Enforces any safety or compliance rules

## Structure

```
eval/modules/
└── <category>/<module-name>/
    ├── test_render.py      # Rendering and schema validation tests
    └── cases/
        ├── valid.json      # Valid parameter inputs and expected outputs
        └── invalid.json    # Invalid inputs and expected error conditions
```

## Running Tests

```bash
# Run all module tests
python -m pytest eval/modules/

# Run tests for a specific module
python -m pytest eval/modules/auth/requirement/
```

## Adding Tests for a New Module

When adding a new module to `modules/`, add corresponding tests here:
1. Create a directory matching the module path
2. Add `test_render.py` with at minimum:
   - A test for each example in the module's schema
   - A test for missing required parameters
   - A test for invalid parameter types

# Module: output/

## Purpose

Output modules control how the agent formats its responses. Choose the appropriate output module based on the integration requirements of the consuming system.

## Available Modules

| File | Description |
|------|-------------|
| `json-strict.prompt` | Forces strict JSON output conforming to a specified schema |
| `structured.template.md` | Human-readable structured response with configurable sections |

## When to Use Which

| Use Case | Module |
|----------|--------|
| API response consumed by code | `json-strict.prompt` |
| Human-readable chat response | `structured.template.md` |

## json-strict.prompt

A static prompt (no parameters). Include it verbatim and set `schema_reference` to the name of the JSON schema the output must conform to.

**Usage note**: When using `json-strict`, the agent prompt should also define the exact schema structure, or reference it by name if the platform resolves schema references automatically.

## structured.template.md

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `summary_instruction` | `string` | Yes | Instruction for what to include in the summary |
| `detail_sections` | `object[]` | Yes | Array of `{title, instruction}` section definitions |

## Used By

- *(Add agent references here as they are created)*

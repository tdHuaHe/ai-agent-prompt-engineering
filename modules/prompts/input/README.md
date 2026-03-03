# Module: input/intent-parsing

## Purpose

Provides a standardized approach for the agent to parse user input: identify intent, extract entities, handle ambiguity, and respond to out-of-scope requests. Use this module in any conversational agent that needs to understand free-form user messages.

## Files

| File | Description |
|------|-------------|
| `intent-parsing.template.md` | Parameterized prompt template |
| `intent-parsing.schema.json` | Parameter schema and validation rules |

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `domain` | `string` | Yes | — | Business domain the agent operates in |
| `supported_intents` | `object[]` | Yes | — | List of `{id, description}` intent definitions |
| `supported_languages` | `string[]` | No | `["zh-CN", "en"]` | Accepted input languages (BCP-47) |

## Example Usage

**params.json**:
```json
{
  "input": {
    "domain": "loan application",
    "supported_intents": [
      { "id": "apply_loan", "description": "User wants to submit a new loan application" },
      { "id": "check_status", "description": "User wants to check the status of an existing application" },
      { "id": "cancel_application", "description": "User wants to cancel a pending application" }
    ],
    "supported_languages": ["zh-CN", "en"]
  }
}
```

## Used By

- *(Add agent references here as they are created)*

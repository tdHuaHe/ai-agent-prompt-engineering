# Module: auth/requirement

## Purpose

Enforces mandatory user identity verification before the agent proceeds with any sensitive action. Use this module in any agent that handles personal data, financial transactions, or account changes.

## Files

| File | Description |
|------|-------------|
| `requirement.template.md` | Parameterized prompt template |
| `requirement.schema.json` | Parameter schema and validation rules |

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `verification_methods` | `string[]` | Yes | — | List of accepted verification methods |
| `timeout_seconds` | `integer` | No | `300` | Session inactivity timeout in seconds |

## Example Usage

**params.json**:
```json
{
  "auth": {
    "verification_methods": ["SMS verification code", "bank card last 4 digits"],
    "timeout_seconds": 180
  }
}
```

**Rendered output**:
```
Before proceeding with any action, you must verify the user's identity...

Accepted verification methods:
- SMS verification code
- Bank card last 4 digits

Verification expires after 180 seconds of inactivity.
```

## Used By

- *(Add agent references here as they are created)*

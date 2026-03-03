# Module: safety/

## Purpose

Safety modules enforce governance rules, compliance requirements, and ethical guardrails. Every agent should include at least one safety module.

## Available Modules

| File | Description |
|------|-------------|
| `pii-protection.prompt` | Enforces PII handling rules and data minimization |

## pii-protection.prompt

Protects personally identifiable information (PII) by instructing the agent to:
- Never repeat or store PII unnecessarily
- Mask PII in any output
- Minimize PII collection to what is strictly required

**Parameters** (via template substitution):

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pii_fields` | `string[]` | Yes | List of field names considered PII in this context |

**Example**:
```json
{
  "safety": {
    "pii_fields": [
      "ID card number",
      "bank account number",
      "phone number",
      "home address"
    ]
  }
}
```

## Adding New Safety Modules

When adding a safety module:
1. Get review from the compliance or security team before merging
2. Clearly document which regulations or policies the module addresses
3. Include at least one test case in `eval/modules/` that verifies the safety behavior

## Used By

- *(Add agent references here as they are created)*

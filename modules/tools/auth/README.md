# Module: tools/auth/

## Purpose

Authorization verification workflows. Use these tools to verify a user's identity before allowing access to sensitive operations.

## Available Workflows

| File | Description |
|------|-------------|
| `phone-sms.workflow.json` | Send and verify an SMS code to the user's phone number |
| `bank-card.workflow.json` | Verify identity via bank card details |

## phone-sms

Sends a one-time verification code via SMS and confirms the code entered by the user.

**Canvas alias suggestion**: `verify_phone`

**Key outputs**:
- `verified` (boolean): `true` if the user entered the correct code within the time limit
- `error_code` (string | null): reason for failure if `verified` is `false`

## bank-card

Verifies the user's identity by matching provided bank card details against their account record.

**Canvas alias suggestion**: `verify_bank_card`

**Key outputs**:
- `verified` (boolean): `true` if the card details matched
- `error_code` (string | null): reason for failure if `verified` is `false`

## Combining Auth Methods

For higher-assurance scenarios, compose both tools and require both to return `verified: true` before proceeding. The agent prompt should use the `auth/requirement` prompt module with both methods listed.

## Used By

- *(Add agent references here as they are created)*

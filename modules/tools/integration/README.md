# Module: tools/integration/

## Purpose

Third-party integration workflows for connecting agents to external systems and APIs.

## Available Workflows

| File | Description |
|------|-------------|
| `api-caller.workflow.json` | Generic HTTP API caller with configurable endpoint, method, and auth |

## api-caller

A flexible, parameterized HTTP client that can call any REST API endpoint. Suitable for integrations where no specialized workflow exists.

**Canvas alias suggestion**: `call_api`

**Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `endpoint_url` | `string` | Yes | — | Full URL of the API endpoint |
| `method` | `string` | No | `POST` | HTTP method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) |
| `payload_variable` | `string` | No | — | Canvas variable holding the request body |
| `headers` | `object` | No | `{}` | Static headers (no secrets) |
| `timeout_seconds` | `integer` | No | `30` | Request timeout |
| `auth_secret_key` | `string` | No | — | Platform secret store key for Bearer token |

**Key outputs**:
- `status_code` (integer): HTTP response status
- `response_body` (object): Parsed response
- `success` (boolean): `true` if status code is 2xx
- `error_code` (string | null): Failure reason

**Security note**: Never hardcode API keys or secrets in `headers`. Use the `auth_secret_key` parameter to reference a key in the platform's secret store.

## Used By

- *(Add agent references here as they are created)*

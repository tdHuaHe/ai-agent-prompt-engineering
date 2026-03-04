# query_customer_accounts — Workflow Reference

Queries all accounts for the authenticated customer. Performs an auth check first, then calls the Account Search API, and formats the results as a numbered list for TTS or agent routing logic.

---

## Inputs

This workflow takes no external inputs. All variables are resolved internally from session context.

## Internal Context Variables

| Variable | Description |
|----------|-------------|
| `authentication_status` | Read from context; if `false`, workflow exits immediately with an error result |
| `id_authenticated_user` | Resolved at runtime via `getCustomerId()` (3-level fallback) |

## Outputs

| Variable | Description |
|----------|-------------|
| `account_list` | Array of account objects. Fields: `id`, `type`, `nickname`, `accountNumber`, `balance`, `availableBalance`, `currency`, `accountAccess` |
| `account_number_list` | Numbered list for TTS, e.g. `"1. Checking ending in 4427\n2. Savings ending in 8831"` |
| `account_total_count` | `0` = no accounts found; `1` = auto-select; `>1` = ask customer to choose |
| `skill_execution_result` | `{ skill_name, skill_result: "success"\|"warning"\|"error", skill_message }` |

---

## Logic

**Step 1 — Auth Gate**

- Read `authentication_status` from context
- If `false` → set error result and stop

**Step 2 — Resolve UID**

- Call `getCustomerId()` with 3-level fallback:
  1. `private_detail_object.active_id`
  2. `Application Input.Uid`
  3. Context var `Uid`
- Set `id_authenticated_user`

**Step 3 — Call API**

- POST Account Search API with `{ uid: id_authenticated_user }`
- Store returned accounts array as `account_list` in context

**Step 4 — Format and Set Outputs**

- Build `account_number_list` via `formatAccountList()` (numbered, last-4 digits)
- Set `account_total_count` = number of accounts
- If 0 accounts → set warning result; otherwise → set success result

---

## JS Functions

### `getCustomerId`

Resolves the authenticated customer ID from session context using a 3-level fallback chain.

```js
function getCustomerId() {
  const privateDetail = Context.getVariable("private_detail_object");
  if (privateDetail && privateDetail.active_id) return privateDetail.active_id;
  const appInputUid = Context.getVariable("Application Input.Uid");
  if (appInputUid) return appInputUid;
  return Context.getVariable("Uid");
}
```

### `formatAccountList`

Formats the accounts array into a numbered string for TTS or display.

```js
function formatAccountList(accounts) {
  return accounts.map((acct, i) =>
    `${i + 1}. ${acct.type} ending in ${acct.accountNumber.slice(-4)}`
  ).join("\n");
}
```

### `set_outputs`

Sets `account_number_list`, `account_total_count`, and `skill_execution_result` based on the API response.

```js
const accounts = Context.getVariable("account_list") || [];
Context.setVariable("account_number_list", formatAccountList(accounts));
Context.setVariable("account_total_count", accounts.length);
const result = accounts.length === 0
  ? { skill_name: "query_customer_accounts", skill_result: "warning", skill_message: "No accounts found." }
  : { skill_name: "query_customer_accounts", skill_result: "success", skill_message: `${accounts.length} account(s) found.` };
Context.setVariable("skill_execution_result", result);
```

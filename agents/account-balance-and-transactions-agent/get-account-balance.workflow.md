# get_account_balance — Workflow Reference

Reads balance from `account_list` already in context. No separate Balance API call is made. Verifies access rights, handles credit/loan account routing, and formats the output for voice or digital channel.

---

## Inputs

| Variable | Required | Description |
|----------|----------|-------------|
| `account_number` | yes | Last 4+ digits provided by the customer, used to match account in `account_list` |

## Internal Context Variables

| Variable | Description |
|----------|-------------|
| `account_list` | Populated by `query_customer_accounts` earlier in the session |
| `Channel Type` | `"digital"` → symbol + line-break format; anything else → voice prose |
| `id_authenticated_user` | Resolved via `getCustomerId()` inside `getAccountDetails()` |

## Outputs

| Variable | Description |
|----------|-------------|
| `account_balance_information` | Formatted balance string, or a special value (see below) |
| `skill_execution_result` | `{ skill_name, skill_result: "success"\|"error", skill_message }` |

**`account_balance_information` special values:**

| Condition | Value |
|-----------|-------|
| Account not found | `"ACCOUNT_NOT_FOUND"` |
| No authenticated customer ID | `"Customer is not authenticated."` |
| Access denied | `"You do not have access to the account balance of this account."` |
| Credit account | `"I can't provide balance information for credit accounts. Please route to Credit Card Agent."` |
| Loan account | `"I can't provide balance information for loan accounts. Please route to Loan Services Agent."` |

**`account_balance_information` formatted values:**

| Channel | Example |
|---------|---------|
| Voice | `"For your Rewards Checking account ending in 4427, your available balance is $232.61, and your current balance is $232.61."` |
| Digital | `"Your active checking account Rewards Checking ending in 4427:\n- Available balance: $232.61\n- Current balance: $232.61"` |

---

## Logic

**Step 1 — Get Balance Details**

1. Read `account_number` from context, extract last 4 digits
2. Find matching account in `account_list`; if not found → set `ACCOUNT_NOT_FOUND` and return
3. If account type is `credit` → set credit redirect message and return
4. If account type is `loan` → set loan redirect message and return
5. Resolve customer ID via `getCustomerId()` (3-level fallback: `private_detail_object.active_id` → `Application Input.Uid` → context var `Uid`); if none found → set "not authenticated" and return
6. Check `account.accountAccess[]` for an entry where `customerId` matches and `accessType` is `OTAX`, `OWN`, or `HOLDER`; if no match → set no-access message and return
7. Format `availableBalance` and `balance` using `Channel Type`; set `account_balance_information`

**Step 2 — Set Result**

- Step 1 succeeded → `skill_result: "success"`
- Step 1 threw an error → `skill_result: "error"`

---

## JS Functions

### `getAccountDetails`

Drives all of Step 1. Reads `account_number` and `account_list` from context, runs the account lookup, access check, and balance formatting. Delegates customer ID resolution to `getCustomerId()`.

```js
function parseIfJson(value) {
    if (typeof value === "string") {
        try { return JSON.parse(value); } catch (e) { return {}; }
    }
    if (typeof value === "object" && value !== null) return value;
    return {};
}

function getCustomerId() {
    let customerObj = parseIfJson(Context.getVariable("private_detail_object"));
    let customer_id = customerObj.active_id;
    if (!customer_id) {
        const appInput = parseIfJson(Context.getVariable("Application Input"));
        customer_id = appInput.Uid;
    }
    if (!customer_id) {
        const agentUid = Context.getVariable("Uid");
        if (typeof agentUid === "string" && agentUid !== "null") customer_id = agentUid;
    }
    return customer_id;
}

function getAccountDetails(selectedAccountNumber) {
    const accountList = Context.getVariable("account_list") || [];
    const last4 = String(selectedAccountNumber).slice(-4);
    const channelType = Context.getVariable("Channel Type");
    const isDigital = typeof channelType === "string" && channelType.trim().toLowerCase() === "digital";
    const currencyMap = { USD: "$", EUR: "€", GBP: "£", JPY: "¥", CNY: "¥", AUD: "A$", CAD: "C$" };

    const account = accountList.find(acc => acc.accountNumber.endsWith(last4));
    if (!account) { Context.setVariable("account_balance_information", "ACCOUNT_NOT_FOUND"); return; }

    const last4digits = account.accountNumber.slice(-4);
    Context.setVariable("account_id", account.id);
    const account_type = account.type?.toLowerCase();
    const account_status = account.status?.toLowerCase();
    const account_nickname = account.nickname || "";
    const currencySymbol = currencyMap[account.currency] || account.currency || "";

    let account_balance_information;
    if (account_type && account_type.includes("credit")) {
        account_balance_information = "I can't provide balance information for credit accounts. Please route to Credit Card Agent.";
    } else if (account_type && account_type.includes("loan")) {
        account_balance_information = "I can't provide balance information for loan accounts. Please route to Loan Services Agent.";
    } else {
        const customer_id = getCustomerId();
        if (!customer_id) { Context.setVariable("account_balance_information", "Customer is not authenticated."); return; }

        const hasAccess = (account.accountAccess || []).some(item =>
            item.customerId === customer_id &&
            (item.accessType === "OTAX" || item.accessType === "OWN" || item.accessType === "HOLDER")
        );
        if (!hasAccess) { Context.setVariable("account_balance_information", "You do not have access to the account balance of this account."); return; }

        const available = account.availableBalance;
        const current = account.balance;
        account_balance_information = isDigital
            ? `Your ${account_status} ${account_type} account ${account_nickname} ending in ${last4digits}:\n- Available balance: ${currencySymbol}${available}\n- Current balance: ${currencySymbol}${current}`
            : `For your ${account_nickname} account ending in ${last4digits}, your available balance is ${currencySymbol}${available}, and your current balance is ${currencySymbol}${current}.`;
    }
    Context.setVariable("account_balance_information", account_balance_information);
}

const selectedAccountNumber = Context.getVariable("account_number");
getAccountDetails(selectedAccountNumber);
```

### `set_result_success`

```js
Context.setVariable("skill_execution_result", {
    skill_name: "get_account_balance",
    skill_result: "success",
    skill_message: "get account balance successfully"
});
```

### `set_result_error`

```js
Context.setVariable("skill_execution_result", {
    skill_name: "get_account_balance",
    skill_result: "error",
    skill_message: "error while getting account balance"
});
```

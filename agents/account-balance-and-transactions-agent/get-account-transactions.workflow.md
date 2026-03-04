# get_account_transactions — Workflow Reference

Resolves an account by last 4 digits, verifies access, paginates using `skipped_count`, calls the Transaction API, and formats the result as voice prose or digital bullet lines.

---

## Inputs

| Variable | Required | Description |
|----------|----------|-------------|
| `account_number` | yes | Last 4+ digits provided by the customer, used to match account in `account_list` |
| `transaction_batch_index` | yes | Which batch of transactions to return (1-based). Batch 1 = most recent 5; each increment skips 5 more. Never ask the customer for this — the agent manages it internally |

## Internal Context Variables

| Variable | Description |
|----------|-------------|
| `account_list` | Populated by `query_customer_accounts` earlier in the session |
| `Channel Type` | `"voice"` → spoken prose sentences; `"digital"` → bullet/symbol format |
| `account_id` | Resolved from `account_list` via `account.id`; passed to the Transaction API |
| `id_authenticated_user` | Resolved via `getCustomerId()` inside `getAccountDetails()` |
| `selected_account` | Set internally after account lookup; used by the formatting function |
| `skipped_count` | Computed as `(transaction_batch_index - 1) * 5`; passed to Transaction API as `skip` |

## Outputs

| Variable | Description |
|----------|-------------|
| `transaction_information` | Formatted transaction string (see examples below) |
| `skill_execution_result` | `{ skill_name, skill_result: "success"\|"warning"\|"error", skill_message }` |

**`transaction_information` output examples:**

| Condition | Example |
|-----------|---------|
| Voice | `"Here are your 5 transactions for your account:\nRewards Checking ending in 4427\nYou spent $232.61 at Square on 2025-12-18.\n..."` |
| Digital | `"Rewards Checking > 4427\n\n> Dec 18 2025 | Square\n   - $232.61\n\n> Dec 8 2025 | Square\n   + $98.41"` |
| No transactions (first batch) | `"There are no recent transactions for this account Rewards Checking ending in 4427."` |
| No transactions (paginated) | `"There are no more transactions for this account Rewards Checking ending in 4427."` |

---

## Logic

**Step 1 — Get Account Id and Batch Index**

1. Read `account_number` from context, extract last 4 digits
2. Find matching account in `account_list`; if not found → set error result and return
3. Set `selected_account` and `account_id` from the matched account object
4. Resolve customer ID via `getCustomerId()` (3-level fallback: `private_detail_object.active_id` → `Application Input.Uid` → context var `Uid`); set `id_authenticated_user`
5. Check `account.accountAccess[]` for an entry matching `customerId` with `accessType` of `OTAX`, `OWN`, or `HOLDER`; set `has_access`
6. If no access → set no-access result and return
7. Parse `transaction_batch_index`; default to 1 if missing or invalid. Compute `skipped_count = (index - 1) * 5`; set in context

**Step 2 — Account Transactions (API call)**

1. Call Transaction API with `{ uid: id_authenticated_user, account_id, skip: skipped_count, limit: 5 }`
2. Store result in context var `transaction_list`
3. On API error → set api-error result; on timeout → set timeout result

**Step 3 — Get Last 5 Transactions**

1. Read `transaction_list` and `selected_account` from context
2. Format transactions via `formatLatestTransactionsV2` (voice: prose sentences; digital: `> date | merchant \n amount` lines)
3. Build final string via `buildTransactionSummaryV2` (includes account header and empty-state handling)
4. Set `transaction_information` in context
5. On success → set success result; on error → set format-error result

---

## JS Functions

### `getAccountDetails`

Runs Step 1. Finds the account in `account_list`, sets `selected_account`, `account_id`, `id_authenticated_user`, and `has_access`. Also parses `transaction_batch_index` and computes `skipped_count`.

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
    let accountList = Context.getVariable("account_list");
    if (typeof accountList === "string") {
        try { accountList = JSON.parse(accountList); } catch (e) {
            Context.setVariable("account_balance_information", "ACCOUNT_LIST_PARSE_ERROR");
            return;
        }
    }

    const last4 = String(selectedAccountNumber).slice(-4);
    const account = accountList.find(acc => acc.accountNumber.endsWith(last4));
    if (!account) {
        Context.setVariable("account_balance_information", "ACCOUNT_NOT_FOUND");
        return;
    }

    Context.setVariable("selected_account", account);
    const account_id = account.id;
    Context.setVariable("account_id", account_id);

    const customer_id = getCustomerId();
    Context.setVariable("id_authenticated_user", customer_id);

    const accountAccess = account.accountAccess || [];
    const hasAccess = accountAccess.some(item =>
        item.customerId === customer_id &&
        (item.accessType === "OTAX" || item.accessType === "OWN" || item.accessType === "HOLDER")
    );
    Context.setVariable("has_access", hasAccess);
}

const selectedAccountNumber = Context.getVariable("account_number");
getAccountDetails(selectedAccountNumber);

const raw_batch_index = Context.getVariable("transaction_batch_index");
let transaction_batch_index = Number.parseInt(String(raw_batch_index ?? '').trim(), 10);
if (!Number.isFinite(transaction_batch_index) || transaction_batch_index < 1) {
    transaction_batch_index = 1;
}
const BATCH_SIZE = 5;
const skipped_count = (transaction_batch_index - 1) * BATCH_SIZE;
Context.setVariable("skipped_count", skipped_count);
```

### `formatLatestTransactionsV2_and_buildSummary`

Runs Step 3. Formats up to 5 transactions for the appropriate channel, then assembles the final `transaction_information` string including account header and empty-state messages.

```js
const AMOUNT_INDENT = "   ";
const BULLET = ">";
const SEP_DOT = " | ";

function formatLatestTransactionsV2(transactionList) {
  const transactionArray = typeof transactionList === "string" ? JSON.parse(transactionList) : transactionList;
  if (!transactionArray || transactionArray.length === 0) return [];

  const channelType = Context.getVariable("Channel Type");
  const isDigital = typeof channelType === "string" && channelType.trim().toLowerCase() === "digital";

  const currencyMap = {
    USD: "$", EUR: "€", GBP: "£", JPY: "¥", CNY: "¥", AUD: "A$", CAD: "C$"
  };
  const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  function formatMonthDay(dateStr) {
    if (!dateStr || typeof dateStr !== "string") return "";
    const parts = dateStr.split("-");
    if (parts.length !== 3) return dateStr;
    const [yearStr, monthStr, dayStr] = parts;
    const mIdx = Math.max(0, Math.min(11, Number(monthStr) - 1));
    return `${monthNames[mIdx]} ${Number(dayStr)} ${yearStr}`;
  }

  function merchantLabel(desc) { return (desc || "").trim(); }

  const latestFive = transactionArray.slice(-5);

  if (!isDigital) {
    return latestFive.map((tx, idx) => {
      const currencySymbol = currencyMap[tx.currency] || tx.currency || "";
      const rawAmount = (tx.amount ?? "").toString().trim();
      const unsignedAmount = rawAmount.replace(/^[+-]\s*/, '');
      const txType = ((tx.transactionType ?? '') + '').trim().toUpperCase();
      const num = Number(rawAmount.replace(/,/g, ''));
      const kind = txType === 'DEBIT' ? 'Debit' : txType === 'CREDIT' ? 'Credit' : (num < 0 ? 'Debit' : 'Credit');
      const isoDate = tx.effectiveDate || tx.postDate || "";
      const merchant = merchantLabel(tx.description);
      if (kind === 'Debit') {
        return `You spent ${currencySymbol}${unsignedAmount} at ${merchant} on ${isoDate}.`;
      } else {
        return `You received ${currencySymbol}${unsignedAmount} from ${merchant} on ${isoDate}.`;
      }
    }).reverse();
  }

  return latestFive.map(tx => {
    const currencySymbol = currencyMap[tx.currency] || tx.currency || "";
    const dateLabel = formatMonthDay(tx.effectiveDate || tx.postDate || "");
    const merchant = merchantLabel(tx.description);
    const rawAmount = (tx.amount ?? "").toString().trim();
    const signMatch = rawAmount.match(/^([+-])/);
    let signPrefix = signMatch ? signMatch[1] : '';
    const txType = ((tx.transactionType ?? '') + '').trim().toUpperCase();
    if (txType === 'DEBIT') {
      signPrefix = '-';
    } else if (txType === 'CREDIT') {
      signPrefix = '+';
    } else if (!signPrefix) {
      const num = Number(rawAmount.replace(/,/g, ''));
      if (!isNaN(num) && num !== 0) signPrefix = '+';
    }
    const unsignedAmount = signMatch ? rawAmount.slice(1).trim() : rawAmount;
    const line1 = `${BULLET} ${dateLabel} ${SEP_DOT} ${merchant}`;
    const line2 = `${AMOUNT_INDENT}${signPrefix ? signPrefix + ' ' : ''}${currencySymbol}${unsignedAmount}`;
    return `${line1}\n${line2}`;
  });
}

function buildTransactionSummaryV2(accountJson, formattedTransactions) {
  const account = typeof accountJson === "string" ? JSON.parse(accountJson) : accountJson;
  const nickname = (account?.nickname || "").trim();
  const last4 = (account?.accountNumber || "").slice(-4);
  const channelType = Context.getVariable("Channel Type");
  const isDigital = typeof channelType === "string" && channelType.trim().toLowerCase() === "digital";
  const header = isDigital
    ? `${nickname} ${BULLET} ${last4}`
    : `${nickname} ending in ${last4}`;
  if (formattedTransactions.length === 0) {
    const skippedCount = Context.getVariable("skipped_count");
    if (skippedCount === 0 || skippedCount === "0") {
      return `There are no recent transactions for this account ${nickname} ending in ${last4}.`;
    } else {
      return `There are no more transactions for this account ${nickname} ending in ${last4}.`;
    }
  }
  const joiner = isDigital ? "\n\n" : "\n";
  if (!isDigital) {
    const count = formattedTransactions.length;
    const intro = `Here ${count === 1 ? 'is' : 'are'} your ${count} transaction${count === 1 ? '' : 's'} for your account:`;
    return `${intro}\n${header}${joiner}${formattedTransactions.join(joiner)}`;
  }
  return `${header}${joiner}${formattedTransactions.join(joiner)}`;
}

let transactionList = Context.getVariable("transaction_list");
const lastFiveTransactions = formatLatestTransactionsV2(transactionList);
const selectedAccountJson = Context.getVariable("selected_account");
const transactionSummary = buildTransactionSummaryV2(selectedAccountJson, lastFiveTransactions);
Context.setVariable("transaction_information", transactionSummary);
```

### `set_result_success`

```js
Context.setVariable("skill_execution_result", {
    skill_name: "get_account_transactions",
    skill_result: "success",
    skill_message: "get the transaction list successfully"
});
```

### `set_result_no_access`

```js
Context.setVariable("skill_execution_result", {
    skill_name: "get_account_transactions",
    skill_result: "warning",
    skill_message: "user do not have access to the account transactions of this account"
});
```

### `set_result_api_error`

```js
Context.setVariable("skill_execution_result", {
    skill_name: "get_account_transactions",
    skill_result: "error",
    skill_message: "error while getting the transaction list"
});
```

### `set_result_api_timeout`

```js
Context.setVariable("skill_execution_result", {
    skill_name: "get_account_transactions",
    skill_result: "error",
    skill_message: "timeout while getting the transaction list"
});
```

### `set_result_account_id_error`

```js
Context.setVariable("skill_execution_result", {
    skill_name: "get_account_transactions",
    skill_result: "error",
    skill_message: "error while getting the account id and batch index"
});
```

### `set_result_format_error`

```js
Context.setVariable("skill_execution_result", {
    skill_name: "get_account_transactions",
    skill_result: "error",
    skill_message: "error while getting the transactions"
});
```

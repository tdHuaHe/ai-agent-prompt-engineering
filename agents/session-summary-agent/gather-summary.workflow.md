# gather_summary — Workflow Reference

Checks whether a `conversation_summary` has been set in context before live-agent escalation. Returns success if it exists and is non-empty, error if it is missing or blank.

---

## Inputs

| Variable | Required | Source | Description |
|----------|----------|--------|-------------|
| `conversation_summary` | yes | context var | The conversation summary written by the Coordinator before escalation |

## Outputs

| Variable | Description |
|----------|-------------|
| `conversation_summary` | Passed through unchanged |
| `skill_execution_result` | `{ skill_name, skill_result: "success"\|"error", skill_message }` |

**`skill_execution_result` values:**

| Condition | `skill_result` | `skill_message` |
|-----------|----------------|-----------------|
| Summary is present and non-empty | `"success"` | `"Escalate directly to the live agent"` |
| Summary is missing or blank | `"error"` | `"Please provide a summary of the conversation history"` |

---

## Logic

**Step 1 — Check Summary**

1. Read `conversation_summary` from context
2. If non-empty → set success result
3. If empty or missing → set error result

---

## JS Functions

### `js_function`

```js
var conversation_summary = Context.getVariable("conversation_summary");

var skill_execution_result;

if (conversation_summary && conversation_summary.trim() !== "") {
    skill_execution_result = {
        skill_name: "gather_summary",
        skill_result: "success",
        skill_message: "Escalate directly to the live agent"
    };
} else {
    skill_execution_result = {
        skill_name: "gather_summary",
        skill_result: "error",
        skill_message: "Please provide a summary of the conversation history"
    };
}

Context.setVariable("skill_execution_result", skill_execution_result);
```

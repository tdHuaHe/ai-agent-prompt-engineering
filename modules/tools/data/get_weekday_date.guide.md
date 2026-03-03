# get_weekday_date — Usage Guide

## What It Does

When a user mentions a date like "next Monday", an upstream NLP node parses a `start_date` but may not align it to the correct weekday. This script:

1. Adjusts `start_date` to the nearest occurrence of `preferred_weekday` (within ±3 days)
2. If the date was changed, writes a human-readable correction to `workflow_status`

---

## Required Inputs (set in context before running)

| Variable | Description |
|----------|-------------|
| `start_date` | The parsed date in `YYYY-MM-DD` format. Defaults to today if empty. |
| `preferred_weekday` | The weekday the user mentioned, e.g. `"monday"` or `"mon"`. If empty, no adjustment is made. |
| `date_matched_weekday` | Set by the upstream node. If `"No"`, the script writes a correction to `workflow_status`. |

---

## Outputs (written to context after running)

| Variable | Description |
|----------|-------------|
| `start_date` | The adjusted date, or unchanged if no adjustment was needed. |
| `workflow_status` | Written only when `date_matched_weekday === "No"`. Example: `"The date for Monday should be January 6th. So the correct match is: on Monday, January 6th"` |

---

## Examples

**Date needs adjustment**: User says "next Monday". Upstream sets `start_date = "2025-01-09"` (Thursday), `preferred_weekday = "monday"`, `date_matched_weekday = "No"`.
- `start_date` → `"2025-01-06"` (nearest Monday, 3 days back)
- `workflow_status` → `"The date for Monday should be January 6th. So the correct match is: on Monday, January 6th"`

**No adjustment needed**: `preferred_weekday` is empty, or `start_date` is already the correct weekday — `start_date` is unchanged and `workflow_status` is not written.

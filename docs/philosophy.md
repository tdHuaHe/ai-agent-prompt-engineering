# Why This Repo Exists

## Short Answer

We treat AI agent templates as engineering assets, not one-off prompt files.

## Problems We Solve

- Repeated work across industries
- Hard-to-review monolithic JSON changes
- Low reuse of proven prompt/tool patterns
- Weak quality control before merge

## Our Approach

1. Keep full exports in `systems/<industry>/exports/`.
2. Split exports into reviewable files in `agents/<industry>/`.
3. Rebuild from split files with `tools/build.py`.
4. Run scope-based tests and quality gates before merge.
5. Extract reusable patterns into `modules/prompts` and `modules/tools`.

## Design Principles

- `systems/` is source-of-truth input and final delivery output.
- `agents/` is the editable and reviewable working layer.
- `modules/` is for cross-industry reuse only.
- `docs/` is the knowledge context for both humans and Copilot.

## Rule of Thumb

- If logic is industry-specific, keep it in `agents/`.
- If logic is reusable across industries, move it to `modules/`.

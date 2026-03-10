# Agent Guide (Short)

## What Is in `agents/`

`agents/<industry>/` is the editable layer used for PR review and testing.

Typical structure:

```text
agents/<industry>/
├── Settings/{template.json,links.json}
├── Variables/variables.json
├── Coordinator/
│   ├── Coordinator.json
│   ├── Coordinator.instruction.md
│   ├── Condition.instruction.md
│   └── Action-Agents/<Agent Name>/{agent.json,instruction.md}
└── Eval/{env.yaml,test_scenarios/}
```

## How to Update an Agent

1. Start from a new export JSON in `systems/<industry>/exports/`.
2. Run `tools/split.py` into `agents/<industry>/`.
3. Make targeted edits in split files.
4. Rebuild with `tools/build.py`.
5. Run required tests and open PR.

## Editing Rules

- Keep `agent_name` and `agent_id` stable unless migration requires changes.
- Keep instructions in `.md` files when extracted with `@filename` refs.
- Prefer minimal, scoped edits to keep PR diff readable.
- If logic becomes cross-industry, move it to `modules/`.

## Build Command Example

```bash
./ai-agent-templates build test --industry fsi-banking
```

Subset build example:

```bash
./ai-agent-templates build test --industry fsi-banking --agents "Member Search Agent,Account Balance and Transaction Agent,FAQ Agent"
```


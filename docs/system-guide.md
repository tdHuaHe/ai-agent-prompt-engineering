# System Guide (Short)

## What Is a System in This Repo?

A system is a full platform export JSON plus a rebuilt JSON generated from split agent files.

Location:

```text
systems/<industry>/
├── exports/   # incoming source exports
└── builds/    # rebuilt outputs from tools/build.py
```

## Recommended Flow

1. Add/update export in `systems/<industry>/exports/`.
2. Split into `agents/<industry>/` with `tools/split.py`.
3. Edit split files as needed.
4. Rebuild with `tools/build.py`.
5. Import rebuilt JSON to test environment.
6. Run E2E tests and quality gates.
7. Merge after review.

## Commands

Split:

```bash
./ai-agent-templates decompose "systems/fsi-banking/exports/<export-file>.json" --industry fsi-banking
```

Build full:

```bash
./ai-agent-templates build test --industry fsi-banking
```

Build subset:

```bash
./ai-agent-templates build test --industry fsi-banking --agents "Member Search Agent,Account Balance and Transaction Agent,FAQ Agent"
```

## Quality Gate (Minimum)

- Build succeeds.
- Rebuilt JSON imports successfully.
- Critical test scenarios pass.
- No blocker safety/compliance issues.

## Notes

- `systems/exports` is the intake source.
- `agents/` is the editable review layer.
- `systems/builds` is the CI/test artifact.


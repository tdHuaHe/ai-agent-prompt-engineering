# Module Guide (Short)

## What Is a Module?

A module is a reusable pattern that is not tied to one industry template.

Two module types:

- `modules/prompts/`: reusable prompt snippets and policies
- `modules/tools/`: reusable tool/workflow/function patterns

## When to Create a Module

Create a module only when all are true:

1. The pattern appears in at least two agents or industries.
2. The behavior is stable and already validated.
3. It can be reused with small adaptations.

If not, keep it in `agents/` first.

## Suggested Structure

```text
modules/
├── prompts/<category>/<name>.prompt.md
├── prompts/<category>/<name>.guide.md   # optional, recommended
└── tools/<category>/<name>.workflow.yaml
```

## Minimal Content Rules

- Prompt module: keep text concise and production-oriented.
- Tool module: document input, output, core logic, and required context vars.
- Guide file: explain what to change and what not to change during reuse.

## Quality Checklist

- Name is clear and behavior-focused.
- Scope is single concern (do one thing well).
- No industry-specific hardcoding unless clearly marked.
- Example usage is provided.
- Referenced from at least one agent.


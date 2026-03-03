# Why Engineering-Based Assembly

## The Problem with Traditional Agent Development

In traditional agent development, prompts and tool workflows are written from scratch for each use case. This leads to:

- **Duplicated effort**: Similar routing logic, safety rules, and workflow patterns are rewritten across agents
- **Inconsistent quality**: No shared standards or battle-tested baselines
- **Poor maintainability**: Changing common logic requires editing every agent that contains it
- **Lost knowledge**: Patterns that work in production stay buried inside monolithic JSON exports

## The Engineering Approach

This repo treats production-proven prompts and tool workflows as extractable, reusable building blocks — similar to how engineers treat shared libraries. Instead of authoring from scratch, you:

1. Extract stable patterns from production system exports into named modules
2. Compose agents from those modules
3. Assemble systems from those agents

### Core Principles

#### 1. Extract Before Authoring
The primary source of modules is production system JSON exports in `systems/`. Patterns are extracted when they prove themselves at scale, not designed speculatively. Every module has real provenance.

#### 2. Flat Files, Not Frameworks
Modules are plain `.prompt.md` and `.workflow.yaml` files. No build steps, no rendering pipelines, no template engines. The format is readable and editable without tooling.

#### 3. Layered Design
The repo is organized into three layers:
- **Module Layer** (`modules/`): Atomic, reusable prompt snippets and tool workflow definitions
- **Agent Layer** (`agents/`): Instruction prompts and tool files assembled for a specific agent role
- **System Layer** (`systems/`): Complete multi-agent platform exports (source of truth)

Extraction flows upward: system JSON → agent files → module files.

#### 4. Guide Over Schema
Rather than enforcing parameterization schemas, modules ship with a `.guide.md` that explains what to adapt when reusing. This keeps modules lightweight and avoids over-abstraction.

## Benefits

| Aspect | Without Engineering | With Engineering |
|--------|---------------------|------------------|
| Development speed | Slow (rewrite each time) | Fast (adapt from modules) |
| Consistency | Low | High (shared, proven modules) |
| Knowledge retention | Lost in JSON exports | Surfaced as named modules |
| Maintainability | Hard | Easy (single source per pattern) |
| Onboarding | Hard (no standards) | Easy (clear structure + guides) |

## When Agent-Specific Logic Is Appropriate

Not everything belongs in a module. Keep logic in `agents/` when:
- It is tightly coupled to a specific business domain or data schema
- It has no plausible reuse across more than one agent
- It captures a workflow that is not yet proven stable enough to generalize

In these cases, the agent file is the right home — not a forced abstraction into a module.

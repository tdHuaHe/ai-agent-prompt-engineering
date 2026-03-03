# Why Engineering-Based Assembly

## The Problem with Traditional Prompt Development

In traditional agent development, prompts are written from scratch for each use case. This leads to:

- **Duplicated effort**: Similar logic is rewritten across agents
- **Inconsistent quality**: No shared best practices or standards
- **Poor maintainability**: Changes to common logic require updating many places
- **No reuse**: Knowledge accumulated in one agent cannot be transferred to another

## The Engineering Approach

The engineering-based assembly approach treats prompts and tools as reusable, versionable, and composable building blocks — similar to how software engineers treat libraries and components.

### Core Principles

#### 1. Modular Reuse
Every prompt snippet and tool workflow that solves a general problem should be encapsulated as a module. Modules are:
- Independently testable
- Parameterizable to adapt to different scenarios
- Documented with clear usage instructions
- Validated against quality standards

#### 2. Composition over Authoring
When building a new agent, the first step is to identify which existing modules cover the required capabilities. Only after exhausting reuse options should new logic be authored. This ensures:
- Faster agent development
- Higher baseline quality (reusing proven modules)
- Reduced maintenance burden

#### 3. Layered Design
The system is organized into distinct layers:
- **Module Layer**: Atomic, reusable prompt and tool components
- **Agent Layer**: Business-scenario-specific composition of modules
- **System Layer**: Multi-agent orchestration for complete business systems

Each layer builds on the layer below, and changes at one layer have clear, bounded impact.

#### 4. Engineering Management
Quality is enforced through:
- Parameterization schemas that validate module inputs
- Automated evaluation frameworks at each layer
- Tooling for rendering templates and validating configurations
- Standardized directory structure and naming conventions

## Benefits

| Aspect | Without Engineering | With Engineering |
|--------|---------------------|-----------------|
| Development speed | Slow (rewrite each time) | Fast (compose from modules) |
| Consistency | Low | High (shared modules) |
| Quality | Variable | Controlled (validated modules) |
| Maintainability | Hard | Easy (single source of truth) |
| Onboarding | Hard (no standards) | Easy (clear structure) |

## When to Break the Rules

Modules should be general enough to avoid the need for overrides, but there are legitimate cases for agent-specific customization:
- Business terminology that cannot be generalized
- Compliance requirements specific to a single domain
- Experimental capabilities not yet ready for module extraction

In these cases, customization should be applied as thin layers on top of composed modules, not by rewriting the modules themselves.

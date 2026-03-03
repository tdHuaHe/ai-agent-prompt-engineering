# How to Design Multi-Agent Systems

## What Is a Multi-Agent System?

A multi-agent system (MAS) is the top-level deliverable of this engineering framework. It consists of multiple coordinated agents working together to handle a complete business process. Systems are defined in the `systems/` directory.

## System Directory Structure

```
systems/<system-name>/
├── system.json         # Full system configuration (final deliverable)
├── agents/             # Agent configurations specific to this system
│   └── <agent-name>/
│       ├── prompt.md
│       ├── tools.json
│       └── params.json
├── params.json         # System-level parameters
└── README.md           # System description and architecture
```

## System Configuration Format

The `system.json` is the final deliverable — a JSON configuration file that can be imported into the AI Agent Platform:

```json
{
  "system": "loan-application-system",
  "version": "1.0.0",
  "description": "End-to-end loan application processing system",
  "agents": [
    {
      "id": "intake_agent",
      "name": "Application Intake Agent",
      "prompt": "<rendered prompt content>",
      "tools": ["verify_phone", "fetch_credit_score"],
      "entry_point": true
    },
    {
      "id": "review_agent",
      "name": "Application Review Agent",
      "prompt": "<rendered prompt content>",
      "tools": ["fetch_applicant_history", "submit_decision"]
    }
  ],
  "orchestration": {
    "flow": [
      { "from": "intake_agent", "to": "review_agent", "condition": "application_complete" }
    ]
  },
  "environment": {
    "timeout_global": 3600,
    "retry_policy": "exponential_backoff"
  }
}
```

## System Design Workflow

### Step 1: Map the Business Process

Before defining agents, map the complete business flow:
- What are the distinct stages of the process?
- What information is passed between stages?
- What are the decision points and branching conditions?
- What are the entry and exit points?

### Step 2: Define Agent Responsibilities

Each agent should own one stage or responsibility. Principles:
- **Single responsibility**: One agent, one clear job
- **Clear handoffs**: Define what data passes between agents
- **Minimal coupling**: Agents communicate through defined interfaces, not shared state

### Step 3: Compose Each Agent

Follow the agent composition process in [agent-guide.md](./agent-guide.md) for each agent in the system.

### Step 4: Define Orchestration Logic

The orchestration section defines how agents hand off to each other:
- **Sequential**: Agent A completes, then Agent B starts
- **Conditional**: Agent B starts only if Agent A produces a specific result
- **Parallel**: Multiple agents run simultaneously, results merged

### Step 5: Set System Parameters

System-level parameters apply across all agents:
- Environment configuration (timeouts, retry policies)
- Shared context (session ID, user profile)
- Feature flags

### Step 6: Render and Validate

Use the engineering tools to produce the final `system.json`:

```bash
python tools/render.py systems/<system-name>
python tools/validate.py systems/<system-name>/system.json
```

## System README Template

```markdown
# System: <Name>

## Purpose
Description of the complete business process this system handles.

## Architecture

```
[intake_agent] → [review_agent] → [decision_agent]
```

## Agents
| Agent | Responsibility | Entry Point |
|-------|---------------|-------------|
| `intake_agent` | Collect and verify application data | Yes |
| `review_agent` | Evaluate application against criteria | No |
| `decision_agent` | Issue final decision and notification | No |

## Data Flow
Description of what data is passed between agents.

## System Parameters
Link to or inline the system params.json content.

## Deployment Notes
Any platform-specific setup required.
```

## Quality Standards

Before delivering a system, verify:

- [ ] Every agent is composed from modules (not written from scratch)
- [ ] Orchestration logic is fully defined with explicit conditions
- [ ] `system.json` passes validation (`tools/validate.py`)
- [ ] System-level eval tests pass (`eval/systems/`)
- [ ] README documents the architecture and data flow

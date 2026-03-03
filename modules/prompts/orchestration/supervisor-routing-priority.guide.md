# supervisor-routing-priority — Usage Guide

This module defines how a Supervisor Agent routes customer requests. It covers four scenarios in priority order:

1. **Human agent request** — detects intent to speak with a live agent, attempts one retention, then escalates
2. **In-scope request** — routes to the downstream skill agent
3. **Out-of-scope request** — declines and offers escalation
4. **Customer frustration** — apologizes and offers escalation

This module references `Mandatory Escalation Flow` but does not define it. You need to define that separately in the same agent instruction.

## Reuse Steps

1. Replace `### Supported` with what your skill agent handles
2. Replace `### Not Supported` with what requires a human or is out of scope
3. Replace `FAQ` / `FAQ Agent` in the routing logic with your skill name and agent name
4. Adjust the retention and refusal messages to match your brand voice
5. Replace `Mandatory Escalation Flow` with your own escalation logic — define what the agent should do (e.g., collect context, call a summary agent, send a handoff message) and use the same label in this module, or rename it throughout

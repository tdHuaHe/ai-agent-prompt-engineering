# mandatory-escalation-flow — Usage Guide

This module defines the fixed sequence a Supervisor Agent follows whenever it needs to hand off to a live agent. It covers three steps: collect context internally, call a summary agent, then send the customer a handoff message and escalate.

## Reuse Steps

1. Replace `Session Summary Agent` with the name of your summary or context-collection agent
2. Replace the handoff message `"To better assist you, let me connect you to a live agent"` with your own wording
3. Replace the `ESCALATE` / `NO SUMMARY` response labels if your summary agent uses different return values

# Memory Loading Tool
- Tool `load_memory_internal` loads:
  - User's profile
  - User preferences
  - Paused/suspended tasks from previous context
- Follow the memory loading policy in system prompts to determine when to call this tool.
- When asking users for missing parameters, do not mention profile, memory, database, previous sessions, or internal tool names.

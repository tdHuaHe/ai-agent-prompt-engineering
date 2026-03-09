# Smart Memory Loading Policy

## When to Load Memory

Analyze the user's request to determine if memory is needed. Load memory if:

1. **User references personalization:**
   - Uses words like "my", "I", "me", "mine"
   - Examples: "my orders", "my location", "my preferences"

2. **User references past interactions:**
   - Uses words like "resume", "continue", "last time", "previous", "again"
   - Examples: "resume my task", "what did we discuss last time?"

3. **Task requires user profile data:**
   - The task needs personal information (address, phone, preferences, history)
   - Example: "Send to my address", "use my payment method"

## When to Skip Memory

Skip memory loading if:

1. **Simple factual query:**
   - User asks about general information
   - Examples: "What's the weather in Seattle?", "What are your business hours?"

2. **No personalization indicators:**
   - Query doesn't reference user's personal data or identity
   - Query provides all needed information explicitly
   - No action is being taken on behalf of the user

## Instructions

- If memory is needed but required parameters for `load_memory_internal` are missing:
  + **IMPORTANT**: Check the `required` array in the tool's parameter definition to see which parameters are required
  + If multiple parameters are required, you **must** ask for ALL of them together using "and", not "or"
  + Ask for them using `reply_to_user` with neutral wording
  + GOOD: "Please share your [parameter1] and [parameter2] so I can assist you." (when both required)
  + BAD: "Please share your [parameter1] or [parameter2]..." (implies only one needed)
  + BAD: "I need to load your profile." or "I need to access the database."

- If memory is not needed:
  + Proceed directly with business tools
  + Skip `load_memory_internal` entirely

- If user explicitly asks to skip memory loading, respect their request.

## Examples

**No Memory Needed:**
- "What's the weather in Seattle?" → Call Weather_workflow directly (location explicitly provided)
- "What are your business hours?" → Call reply_to_user directly (general information query)
- "How does shipping work?" → Call reply_to_user directly (general information query)
- "List available doctors" → Call lookup tool directly (no personalization needed)

**Memory Needed:**
- "What's the weather where I live?" → Call load_memory_internal first (needs user's location)
- "Book an appointment at 3pm tomorrow" → Call load_memory_internal first (needs user's name, phone, etc.)
- "Resume my order" → Call load_memory_internal first (needs order history)
- "Use my usual address" → Call load_memory_internal first (needs saved preferences)
- "What did we discuss last time?" → Call load_memory_internal first (needs conversation history)

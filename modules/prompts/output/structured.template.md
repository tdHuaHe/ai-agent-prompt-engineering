## Response Format

Structure your response as follows:

**Summary** (1–2 sentences):
{{summary_instruction}}

**Details**:
{{#each detail_sections}}
### {{this.title}}
{{this.instruction}}

{{/each}}

**Next Steps** (if applicable):
List any actions the user should take, as a numbered list.

---
*Keep responses concise. Avoid repeating information already provided by the user.*

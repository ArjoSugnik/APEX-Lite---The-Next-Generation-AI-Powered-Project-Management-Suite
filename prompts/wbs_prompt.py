WBS_PROMPT_STRUCTURED = """Generate a Work Breakdown Structure (WBS) table for the given project.

Use EXACTLY this pipe-delimited table format:

Phase | Task | Days
Planning | <task name> | <number>
Planning | <task name> | <number>
Development | <task name> | <number>
Development | <task name> | <number>
Development | <task name> | <number>
Testing & Delivery | <task name> | <number>
Testing & Delivery | <task name> | <number>

Rules:
- Use EXACTLY 3 phases: Planning, Development, Testing & Delivery
- Each phase has 2-3 tasks
- Days must be a single number (1-10)
- Keep task names short (2-5 words)
- First line MUST be: Phase | Task | Days
- Use | as separator
- Do NOT add any other text, headers, or explanations
- Do NOT use markdown table formatting (no dashes or colons)
- Output ONLY the table rows

Project:
{project_brief}
"""

WBS_PROMPT_ROLE = """You are a senior Project Manager. Create a Work Breakdown Structure (WBS).

Use EXACTLY this pipe-delimited table format:

Phase | Task | Days
Planning | <task name> | <number>
Planning | <task name> | <number>
Development | <task name> | <number>
Development | <task name> | <number>
Development | <task name> | <number>
Testing & Delivery | <task name> | <number>
Testing & Delivery | <task name> | <number>

Rules:
- Use EXACTLY 3 phases: Planning, Development, Testing & Delivery
- Each phase has 2-3 tasks
- Days must be a single number (1-10)
- Keep task names short (2-5 words)
- First line MUST be: Phase | Task | Days
- Use | as separator
- Do NOT add any other text, headers, or explanations
- Do NOT use markdown table formatting (no dashes or colons)
- Output ONLY the table rows

Project:
{project_brief}
"""
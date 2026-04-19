COST_PROMPT_STRUCTURED = """Generate a Cost Estimation table for the project.

Use EXACTLY this pipe-delimited table format:

Category | Resource/Item | Estimated Cost
Personnel | <role name or team> | $<number>
Personnel | <role name or team> | $<number>
Software | <tool or license> | $<number>
Hardware | <equipment> | $<number>
Miscellaneous | <expense> | $<number>

Rules:
- Include at least 5 cost items
- Values in 'Estimated Cost' MUST begin with $ and be a number (e.g. $5000)
- First line MUST be: Category | Resource/Item | Estimated Cost
- Use | as separator
- Do NOT add any other text, headers, or explanations
- Do NOT use markdown table formatting (no dashes or colons)
- Output ONLY the table rows

Project:
{project_brief}
"""

COST_PROMPT_ROLE = """You are a senior Financial Analyst and Project Manager. Your job is to build a Cost Estimation sheet based on anticipated resources and duration for the project below.

Output your findings using EXACTLY this pipe-delimited table format:

Category | Resource/Item | Estimated Cost
Personnel | <role name or team> | $<number>
Personnel | <role name or team> | $<number>
Software | <tool or license> | $<number>
Hardware | <equipment> | $<number>
Miscellaneous | <expense> | $<number>

Rules:
- Include at least 5 cost items across different categories (Personnel, Software, Hardware, etc)
- Values in 'Estimated Cost' MUST begin with $ and be a number (e.g. $15000)
- First line MUST be: Category | Resource/Item | Estimated Cost
- Use | as separator
- Do NOT add any other text, headers, or explanations
- Do NOT use markdown table formatting (no dashes or colons)
- Output ONLY the table rows

Project:
{project_brief}
"""

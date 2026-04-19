AGILE_PROMPT_STRUCTURED = """Generate an Agile Backlog (User Stories) for the given project.

Use EXACTLY this pipe-delimited table format:

Epic | User Story | Story Points | Acceptance Criteria
<Epic Name> | As a <user>, I want to <feature> so that <benefit> | 3 | 1. <crit> 2. <crit>
<Epic Name> | As a <user>, I want to <feature> so that <benefit> | 5 | 1. <crit> 2. <crit>

Rules:
- Include at least 5 user stories
- Story Points must be a single number (e.g. 1, 2, 3, 5, 8)
- First line MUST be: Epic | User Story | Story Points | Acceptance Criteria
- Use | as separator
- Do NOT add any other text, headers, or explanations
- Do NOT use markdown table formatting (no dashes or colons)
- Output ONLY the table rows

Project:
{project_brief}
"""

AGILE_PROMPT_ROLE = """You are a senior Agile Product Owner. Your job is to analyze the project below and write a backlog of User Stories.

Output your findings using EXACTLY this pipe-delimited table format:

Epic | User Story | Story Points | Acceptance Criteria
<Epic Name> | As a <user>, I want to <feature> so that <benefit> | 3 | 1. <crit> 2. <crit>
<Epic Name> | As a <user>, I want to <feature> so that <benefit> | 5 | 1. <crit> 2. <crit>

Rules:
- Include at least 5 well-defined user stories across multiple Epics
- Story Points must be a single number (e.g. 1, 2, 3, 5, 8)
- First line MUST be: Epic | User Story | Story Points | Acceptance Criteria
- Use | as separator
- Do NOT add any other text, headers, or explanations
- Do NOT use markdown table formatting (no dashes or colons)
- Output ONLY the table rows

Project:
{project_brief}
"""

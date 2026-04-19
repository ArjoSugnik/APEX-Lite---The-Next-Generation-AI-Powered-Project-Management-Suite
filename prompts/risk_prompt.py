RISK_PROMPT_STRUCTURED = """Generate a Risk Register for the project.

Use EXACTLY this pipe-delimited table format:

Category | Risk Description | Mitigation
Technical | <describe risk> | <describe mitigation>
Technical | <describe risk> | <describe mitigation>
Business | <describe risk> | <describe mitigation>
Operational | <describe risk> | <describe mitigation>
Operational | <describe risk> | <describe mitigation>

Rules:
- Include at least 5 risks
- First line MUST be: Category | Risk Description | Mitigation
- Use | as separator
- Do NOT add any other text, headers, or explanations
- Do NOT use markdown table formatting (no dashes or colons)
- Output ONLY the table rows

Project:
{project_brief}
"""

RISK_PROMPT_ROLE = """You are a senior Risk Manager. Your job is to analyze the project below and identify potential risks and mitigations.

Output your findings using EXACTLY this pipe-delimited table format:

Category | Risk Description | Mitigation
Technical | <describe risk> | <describe mitigation>
Technical | <describe risk> | <describe mitigation>
Business | <describe risk> | <describe mitigation>
Operational | <describe risk> | <describe mitigation>

Rules:
- Include at least 5 risks across different categories (e.g. Technical, Business, Operational)
- First line MUST be: Category | Risk Description | Mitigation
- Use | as separator
- Do NOT add any other text, headers, or explanations
- Do NOT use markdown table formatting (no dashes or colons)
- Output ONLY the table rows

Project:
{project_brief}
"""

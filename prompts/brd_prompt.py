BRD_PROMPT_STRUCTURED = """Generate a Business Requirements Document (BRD) for the given project.

Use EXACTLY this format with these EXACT section headers:

## Project Title
<Write a clear project title>

## Stakeholders
- <Stakeholder 1>
- <Stakeholder 2>
- <Stakeholder 3>

## Functional Requirements
- <Requirement 1>
- <Requirement 2>
- <Requirement 3>
- <Requirement 4>
- <Requirement 5>

## Non-Functional Requirements
- <Requirement 1>
- <Requirement 2>
- <Requirement 3>

Rules:
- Use exactly these section headers with ## prefix
- Use bullet points with - prefix
- Keep each point to one sentence
- Do NOT add any other sections
- Do NOT add explanations or commentary

Project:
{project_brief}
"""

BRD_PROMPT_ROLE = """You are a senior Business Analyst. Write a Business Requirements Document (BRD).

Use EXACTLY this format with these EXACT section headers:

## Project Title
<Write a clear project title>

## Stakeholders
- <Stakeholder 1>
- <Stakeholder 2>
- <Stakeholder 3>

## Functional Requirements
- <Requirement 1>
- <Requirement 2>
- <Requirement 3>
- <Requirement 4>
- <Requirement 5>

## Non-Functional Requirements
- <Requirement 1>
- <Requirement 2>
- <Requirement 3>

Rules:
- Use exactly these section headers with ## prefix
- Use bullet points with - prefix
- Keep each point to one sentence
- Do NOT add any other sections
- Do NOT add explanations or commentary
- Be specific and professional

Project:
{project_brief}
"""
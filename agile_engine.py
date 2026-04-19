"""
Agile Engine — generates the Agile Backlog via Ollama.
"""

import ollama
from prompts.agile_prompt import AGILE_PROMPT_ROLE, AGILE_PROMPT_STRUCTURED

MODEL_NAME = "phi"


def generate_agile(project_brief: str, prompt_strategy: str = "structured") -> str:
    """
    Call the local LLM to produce a pipe-delimited Agile User Story table.
    """
    if not project_brief or not project_brief.strip():
        raise ValueError("Project brief cannot be empty.")

    if prompt_strategy.lower().startswith("role"):
        prompt = AGILE_PROMPT_ROLE.format(project_brief=project_brief.strip())
        system_content = "You are a senior agile product owner. Follow the requested format exactly."
    else:
        prompt = AGILE_PROMPT_STRUCTURED.format(project_brief=project_brief.strip())
        system_content = "You are an AI assistant. Output ONLY a pipe-delimited table. Follow the requested format exactly."

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt},
            ],
        )
        content = response["message"]["content"]
        if not content or not content.strip():
            raise RuntimeError("The model returned an empty response.")
        return content.strip()

    except Exception as exc:
        raise RuntimeError(f"Failed to generate Agile Backlog: {exc}") from exc

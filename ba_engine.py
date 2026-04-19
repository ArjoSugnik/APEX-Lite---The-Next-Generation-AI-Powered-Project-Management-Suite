"""
BA Engine — generates the Business Requirements Document via Ollama.
"""

import ollama
from prompts.brd_prompt import BRD_PROMPT_ROLE, BRD_PROMPT_STRUCTURED

MODEL_NAME = "phi"


def generate_brd(project_brief: str, prompt_strategy: str = "structured") -> str:
    """
    Call the local LLM to produce a structured BRD.

    Raises RuntimeError on communication failure so the UI can
    show a user-friendly message.
    """
    if not project_brief or not project_brief.strip():
        raise ValueError("Project brief cannot be empty.")

    if prompt_strategy.lower().startswith("role"):
        prompt = BRD_PROMPT_ROLE.format(project_brief=project_brief.strip())
        system_content = (
            "You are a senior business analyst. "
            "Follow the requested format exactly. "
            "Do not add commentary. Be concise and professional."
        )
    else:
        prompt = BRD_PROMPT_STRUCTURED.format(project_brief=project_brief.strip())
        system_content = (
            "You are an AI assistant. "
            "Follow the requested format exactly. "
            "Do not add commentary."
        )

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_content,
                },
                {"role": "user", "content": prompt},
            ],
        )
        content = response["message"]["content"]
        if not content or not content.strip():
            raise RuntimeError("The model returned an empty response.")
        return content.strip()

    except Exception as exc:
        raise RuntimeError(f"Failed to generate BRD: {exc}") from exc
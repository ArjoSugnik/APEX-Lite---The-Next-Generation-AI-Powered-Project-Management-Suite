"""
PM Engine — generates the Work Breakdown Structure via Ollama.
"""

import ollama
from prompts.wbs_prompt import WBS_PROMPT_ROLE, WBS_PROMPT_STRUCTURED

MODEL_NAME = "phi"


def generate_wbs(project_brief: str, prompt_strategy: str = "structured") -> str:
    """
    Call the local LLM to produce a pipe-delimited WBS table.

    Raises RuntimeError on communication failure so the UI can
    show a user-friendly message.
    """
    if not project_brief or not project_brief.strip():
        raise ValueError("Project brief cannot be empty.")

    if prompt_strategy.lower().startswith("role"):
        prompt = WBS_PROMPT_ROLE.format(project_brief=project_brief.strip())
        system_content = (
            "You are a senior project manager. "
            "Output ONLY a pipe-delimited table. "
            "No explanations. No markdown formatting. "
            "Follow the requested format exactly."
        )
    else:
        prompt = WBS_PROMPT_STRUCTURED.format(project_brief=project_brief.strip())
        system_content = (
            "You are an AI assistant. "
            "Output ONLY a pipe-delimited table. "
            "No explanations. No markdown formatting. "
            "Follow the requested format exactly."
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
        raise RuntimeError(f"Failed to generate WBS: {exc}") from exc
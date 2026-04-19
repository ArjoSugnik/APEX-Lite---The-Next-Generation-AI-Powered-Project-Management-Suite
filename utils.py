"""
Utility functions for parsing and formatting BRD/WBS output.
"""

import re
import pandas as pd


# ---------------------------------------------------------------------------
# WBS Parsing
# ---------------------------------------------------------------------------

def parse_wbs_to_table(wbs_text: str) -> pd.DataFrame:
    """
    Parse pipe-delimited WBS text into a structured DataFrame.

    Expected format per line:
        Phase | Task Name | Days

    Returns an empty DataFrame on failure so the caller can fall back
    to displaying the raw text.
    """
    rows: list[dict] = []

    for line in wbs_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        # Skip the header row
        if _is_header_row(line):
            continue

        # Skip markdown table separator rows (e.g. ---|---|---)
        if re.match(r"^[\s|:-]+$", line):
            continue

        # Strip leading/trailing pipes if present from markdown format
        line = line.strip('|').strip()
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            phase = _clean_text(parts[0])
            task = _clean_text(parts[1])
            days = _extract_days(parts[2])

            if phase and task:
                rows.append({
                    "Phase": phase,
                    "Task": task,
                    "Estimated Days": days,
                })

    # Fallback: try the old dash-based format if pipe parsing found nothing
    if not rows:
        rows = _parse_dash_format(wbs_text)

    return pd.DataFrame(rows)


def _is_header_row(line: str) -> bool:
    """Return True if the line looks like a table header."""
    lower = line.lower()
    return "phase" in lower and "task" in lower and "day" in lower


def _extract_days(text: str) -> str:
    """Extract the first integer from a string, or return 'N/A'."""
    match = re.search(r"(\d+)", text)
    return match.group(1) if match else "N/A"


def _clean_text(text: str) -> str:
    """Strip leading bullets, numbers, dashes, and whitespace."""
    return re.sub(r"^[-•*\d.)\s]+", "", text).strip()


def _parse_dash_format(wbs_text: str) -> list[dict]:
    """
    Legacy parser for dash-based WBS output:
        Phase: <name>
        - Task: <name> - <N> days
    """
    rows: list[dict] = []
    current_phase = "General"

    for line in wbs_text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Detect phase headers
        phase_match = re.match(r"(?:phase[:\s]*)?(.+)", line, re.IGNORECASE)
        if "phase" in line.lower() and ":" in line:
            current_phase = line.split(":", 1)[-1].strip() or line
            continue

        # Detect task lines
        task_match = re.match(
            r"[-•*]\s*(?:Task:\s*)?(.+?)\s*[-–:]\s*(\d+)\s*days?",
            line,
            re.IGNORECASE,
        )
        if task_match:
            rows.append({
                "Phase": current_phase,
                "Task": task_match.group(1).strip(),
                "Estimated Days": task_match.group(2),
            })

    return rows


# ---------------------------------------------------------------------------
# BRD Parsing
# ---------------------------------------------------------------------------

def parse_brd_sections(brd_text: str) -> dict[str, str]:
    """
    Split a BRD into its named sections.

    Handles multiple header formats produced by different models:
      - Markdown:  ## Project Title
      - Colon:     Project Title: <value>
      - Bold:      **Project Title**

    Returns a dict like:
        {
            "Project Title": "...",
            "Stakeholders": "- ...\n- ...",
            "Functional Requirements": "...",
            "Non-Functional Requirements": "...",
        }
    If parsing fails the returned dict will contain a single key "raw"
    with the full text so the UI can still display something.
    """
    # Known BRD section keywords (order matters for display)
    _KNOWN_SECTIONS = [
        "Project Title",
        "Stakeholders",
        "Non-Functional Requirements",
        "Functional Requirements",
    ]

    sections: dict[str, str] = {}
    current_key: str | None = None
    buffer: list[str] = []

    for line in brd_text.splitlines():
        detected_key = _detect_section_header(line, _KNOWN_SECTIONS)

        if detected_key:
            # Flush the previous section
            if current_key is not None:
                sections[current_key] = "\n".join(buffer).strip()

            current_key = detected_key
            buffer = []

            # If the header line also contains inline content after ":"
            # e.g. "Project Title: My Cool App"
            inline = _extract_inline_value(line, detected_key)
            if inline:
                buffer.append(inline)
        else:
            buffer.append(line)

    # Flush the last section
    if current_key is not None:
        sections[current_key] = "\n".join(buffer).strip()

    # If we found nothing, return raw
    if not sections:
        sections["raw"] = brd_text.strip()

    return sections


def _detect_section_header(line: str, known_sections: list[str]) -> str | None:
    """
    Check if a line is a section header.
    Returns the canonical section name or None.
    """
    stripped = line.strip()
    if not stripped:
        return None

    # Pattern 1:  ## Header  or  # Header
    md_match = re.match(r"^#{1,3}\s+(.+)", stripped)
    if md_match:
        header_text = md_match.group(1).strip().rstrip(":")
        return _match_known_section(header_text, known_sections)

    # Pattern 2:  **Header** or **Header:**
    bold_match = re.match(r"^\*\*(.+?)\*\*\s*:?\s*$", stripped)
    if bold_match:
        header_text = bold_match.group(1).strip().rstrip(":")
        return _match_known_section(header_text, known_sections)

    # Pattern 3:  "Project Title:" or "Functional Requirements:" at line start
    # Only match if the text before the colon closely matches a known section
    colon_match = re.match(r"^([A-Za-z][A-Za-z\s\-/]+?):\s*(.*)", stripped)
    if colon_match:
        header_text = colon_match.group(1).strip()
        return _match_known_section(header_text, known_sections)

    return None


def _match_known_section(text: str, known_sections: list[str]) -> str | None:
    """Fuzzy-match text against known section names."""
    text_lower = text.lower().strip()

    # Exact match first
    for section in known_sections:
        if text_lower == section.lower():
            return section

    # Keyword-based matching (check more-specific terms first)
    if "non-functional" in text_lower or "non functional" in text_lower:
        return "Non-Functional Requirements"
    if "title" in text_lower and "project" in text_lower:
        return "Project Title"
    if "stakeholder" in text_lower:
        return "Stakeholders"
    if "functional" in text_lower and "requirement" in text_lower:
        return "Functional Requirements"

    # Substring containment (order: longest first to avoid false matches)
    for section in known_sections:
        if section.lower() in text_lower:
            return section

    return None


def _extract_inline_value(line: str, section_name: str) -> str | None:
    """Extract any value that appears on the same line as the header."""
    # Handle "Project Title: My Cool App"
    colon_match = re.match(r"^[#*\s]*" + re.escape(section_name) + r"\s*:?\s*\*?\*?\s*(.*)", line, re.IGNORECASE)
    if colon_match:
        value = colon_match.group(1).strip().rstrip(":")
        return value if value else None
    # Handle "## Project Title" lines (the content is on the same line in colon format)
    general_match = re.search(r":\s*(.+)$", line)
    if general_match:
        value = general_match.group(1).strip()
        return value if value else None
    return None


# ---------------------------------------------------------------------------
# Risk & Cost Parsing
# ---------------------------------------------------------------------------

def parse_risk_to_table(risk_text: str) -> pd.DataFrame:
    rows: list[dict] = []
    for line in risk_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if _is_risk_header_row(line):
            continue
        if re.match(r"^[\s|:-]+$", line):
            continue
        line = line.strip('|').strip()
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            cat = _clean_text(parts[0])
            desc = _clean_text(parts[1])
            mitig = _clean_text("|".join(parts[2:]))
            if cat and desc:
                rows.append({"Category": cat, "Risk Description": desc, "Mitigation": mitig})
    return pd.DataFrame(rows)

def _is_risk_header_row(line: str) -> bool:
    lower = line.lower()
    return "category" in lower and "risk" in lower and "mitigation" in lower

def parse_cost_to_table(cost_text: str) -> pd.DataFrame:
    rows: list[dict] = []
    for line in cost_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if _is_cost_header_row(line):
            continue
        if re.match(r"^[\s|:-]+$", line):
            continue
        line = line.strip('|').strip()
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            cat = _clean_text(parts[0])
            item = _clean_text(parts[1])
            cost_val = _clean_text("|".join(parts[2:]))
            if cat and item:
                rows.append({"Category": cat, "Resource/Item": item, "Estimated Cost": cost_val})
    return pd.DataFrame(rows)

def _is_cost_header_row(line: str) -> bool:
    lower = line.lower()
    return "category" in lower and "cost" in lower

# ---------------------------------------------------------------------------
# Agile & Viz Parsing
# ---------------------------------------------------------------------------

def parse_agile_to_table(agile_text: str) -> pd.DataFrame:
    rows: list[dict] = []
    for line in agile_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if _is_agile_header_row(line):
            continue
        if re.match(r"^[\s|:-]+$", line):
            continue
        line = line.strip('|').strip()
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            epic = _clean_text(parts[0])
            story = _clean_text(parts[1])
            points = _extract_days(parts[2])
            criteria = _clean_text("|".join(parts[3:]))
            if epic and story:
                rows.append({
                    "Epic": epic,
                    "User Story": story,
                    "Story Points": points,
                    "Acceptance Criteria": criteria
                })
    return pd.DataFrame(rows)

def _is_agile_header_row(line: str) -> bool:
    lower = line.lower()
    return "epic" in lower and "story" in lower

def generate_gantt_chart(wbs_df: pd.DataFrame):
    """
    Generate a Plotly Gantt Chart object from the WBS DataFrame.
    Calculates Start/Finish dates sequentially based on Estimated Days.
    """
    try:
        import plotly.express as px
        from datetime import datetime
        
        if wbs_df is None or wbs_df.empty:
            return None
            
        df = wbs_df.copy()
        start_date = datetime.today()
        
        starts = []
        finishes = []
        
        current_date = start_date
        for idx, row in df.iterrows():
            try:
                days = int(row['Estimated Days'])
            except (ValueError, TypeError):
                days = 1 # default
                
            finish_date = current_date + pd.Timedelta(days=days)
            starts.append(current_date)
            finishes.append(finish_date)
            current_date = finish_date
            
        df['Start'] = starts
        df['Finish'] = finishes
        
        fig = px.timeline(
            df, 
            x_start="Start", 
            x_end="Finish", 
            y="Task", 
            color="Phase",
            title="Project Timeline (Gantt Chart)"
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#e4eaf6")
        )
        return fig
    except ImportError:
        return None
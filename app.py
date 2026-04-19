"""
APEX Lite — AI-Powered Project Planner
=======================================
Premium Streamlit dashboard for generating BRD & WBS documents
using a local Ollama LLM.
"""

import streamlit as st
import pandas as pd
import ollama

from ba_engine import generate_brd
from pm_engine import generate_wbs
from agile_engine import generate_agile
from risk_engine import generate_risk
from cost_engine import generate_cost
from utils import parse_wbs_to_table, parse_brd_sections, parse_risk_to_table, parse_cost_to_table, parse_agile_to_table, generate_gantt_chart
from docx_writer import create_docx

# ─────────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="APEX Lite — AI Project Planner",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# Custom CSS — premium dark theme
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* ---------- Import Google Font ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ---------- Global ---------- */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #101829 40%, #0d1422 100%);
    }

    /* ---------- Hide Streamlit defaults ---------- */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* ---------- Hero header ---------- */
    .hero-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        margin-bottom: 1rem;
    }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #387aff22, #7c3aed22);
        border: 1px solid #387aff44;
        color: #93b4ff;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        padding: 0.35rem 1rem;
        border-radius: 999px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #387aff 50%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.25rem 0;
        line-height: 1.15;
    }
    .hero-subtitle {
        color: #8899bb;
        font-size: 1.05rem;
        font-weight: 400;
        max-width: 640px;
        margin: 0.5rem auto 0 auto;
        line-height: 1.6;
    }

    /* ---------- Glass cards ---------- */
    .glass-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(12px);
    }

    /* ---------- Section headers ---------- */
    .section-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #387aff;
        margin-bottom: 0.5rem;
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #e4eaf6;
        margin-bottom: 0.15rem;
    }
    .section-desc {
        font-size: 0.88rem;
        color: #7888a8;
        margin-bottom: 1rem;
    }

    /* ---------- BRD sections ---------- */
    .brd-heading {
        font-size: 1.1rem;
        font-weight: 700;
        color: #387aff;
        margin: 1.2rem 0 0.4rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid #387aff33;
    }
    .brd-item {
        color: #c5d0e6;
        font-size: 0.92rem;
        padding: 0.25rem 0 0.25rem 1rem;
        border-left: 2px solid #387aff33;
        margin-bottom: 0.3rem;
        line-height: 1.5;
    }
    .brd-text {
        color: #b0bdd4;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ---------- Stats row ---------- */
    .stat-card {
        background: rgba(56,122,255,0.08);
        border: 1px solid rgba(56,122,255,0.15);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #387aff;
    }
    .stat-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #7888a8;
        margin-top: 0.15rem;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 0.35rem;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #7888a8;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 0.55rem 1.5rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #387aff20, #7c3aed20) !important;
        color: #387aff !important;
        border: 1px solid #387aff44 !important;
    }

    /* ---------- Data-frame ---------- */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ---------- Buttons ---------- */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #387aff, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(56,122,255,0.35) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #387aff, #5e5cff) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(56,122,255,0.4) !important;
    }

    /* ---------- Text area ---------- */
    .stTextArea textarea {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: #c5d0e6 !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #387aff !important;
        box-shadow: 0 0 0 2px rgba(56,122,255,0.15) !important;
    }

    /* ---------- Alerts / Messages ---------- */
    .stAlert {
        border-radius: 12px !important;
    }

    /* ---------- Divider ---------- */
    .divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Hero Header
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ Powered by Ollama LLM</div>
    <div class="hero-title">APEX Lite</div>
    <div class="hero-subtitle">
        Generate professional Business Requirements Documents and
        Work Breakdown Structures in seconds — powered by your local LLM.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Input Section
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="glass-card">
    <div class="section-label">📋 Input</div>
    <div class="section-title">Describe Your Project</div>
    <div class="section-desc">
        Provide a brief description and APEX Lite will generate a full
        BRD and WBS plan for you.
    </div>
</div>
""", unsafe_allow_html=True)

project_brief = st.text_area(
    "Project Description",
    placeholder="e.g. Build a mobile app for tracking daily fitness goals with social features and gamification...",
    height=130,
    label_visibility="collapsed",
)

col_opt1, col_opt2 = st.columns(2)
with col_opt1:
    project_methodology = st.selectbox(
        "Project Methodology",
        ["Waterfall (WBS & Timeline)", "Agile (Scrum Backlog)"]
    )
with col_opt2:
    prompt_type = st.selectbox(
        "Select Prompt Strategy",
        [
            "Role Prompting (acts as project manager)", 
            "Structured Prompting (enforces strict document format)"
        ]
    )

col_btn, col_space = st.columns([1, 3])
with col_btn:
    generate_clicked = st.button("🚀  Generate Plan")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────

if "brd_text" not in st.session_state:
    st.session_state.brd_text = None
if "wbs_text" not in st.session_state:
    st.session_state.wbs_text = None
if "wbs_df" not in st.session_state:
    st.session_state.wbs_df = None
if "agile_text" not in st.session_state:
    st.session_state.agile_text = None
if "agile_df" not in st.session_state:
    st.session_state.agile_df = None
if "risk_df" not in st.session_state:
    st.session_state.risk_df = None
if "risk_text" not in st.session_state:
    st.session_state.risk_text = None
if "cost_df" not in st.session_state:
    st.session_state.cost_df = None
if "cost_text" not in st.session_state:
    st.session_state.cost_text = None
if "methodology" not in st.session_state:
    st.session_state.methodology = None

# ─────────────────────────────────────────────────────────────
# Generation Logic
# ─────────────────────────────────────────────────────────────

if generate_clicked:
    if not project_brief or not project_brief.strip():
        st.warning("⚠️  Please enter a project description to continue.")
    else:
        try:
            with st.spinner("🔍  Generating BRD..."):
                st.session_state.brd_text = generate_brd(project_brief, prompt_type)

            st.session_state.methodology = project_methodology
            if st.session_state.methodology.startswith("Waterfall"):
                with st.spinner("🔍  Generating WBS..."):
                    wbs_content = generate_wbs(project_brief, prompt_type)
                    st.session_state.wbs_text = wbs_content
                    st.session_state.wbs_df = parse_wbs_to_table(wbs_content)
                    st.session_state.agile_df = None
            else:
                with st.spinner("🔍  Generating Agile Backlog..."):
                    agile_content = generate_agile(project_brief, prompt_type)
                    st.session_state.agile_text = agile_content
                    st.session_state.agile_df = parse_agile_to_table(agile_content)
                    st.session_state.wbs_df = None

            with st.spinner("🔍  Generating Risk Register..."):
                risk_content = generate_risk(project_brief, prompt_type)
                st.session_state.risk_text = risk_content
                st.session_state.risk_df = parse_risk_to_table(risk_content)

            with st.spinner("🔍  Generating Cost Estimates..."):
                cost_content = generate_cost(project_brief, prompt_type)
                st.session_state.cost_text = cost_content
                st.session_state.cost_df = parse_cost_to_table(cost_content)

            st.success("✅  Plan generated successfully!")

        except RuntimeError as e:
            st.error(f"❌  {e}")
        except Exception as e:
            st.error(
                "❌  An unexpected error occurred. "
                "Please make sure Ollama is running and the **phi** model is available.\n\n"
                f"`{e}`"
            )

# ─────────────────────────────────────────────────────────────
# Results Display
# ─────────────────────────────────────────────────────────────

if st.session_state.brd_text or st.session_state.wbs_df is not None or st.session_state.agile_df is not None:
    tab2_name = "📊 WBS & Timeline" if st.session_state.methodology and st.session_state.methodology.startswith("Waterfall") else "🏃 Agile Backlog"
    tab_brd, tab_plan, tab_risk, tab_cost, tab_download = st.tabs([
        "📄  BRD",
        tab2_name,
        "⚠️  Risks",
        "💰  Costs",
        "📥  Download",
    ])

    # ── TAB 1: BRD ──────────────────────────────────────────
    with tab_brd:
        st.markdown("""
        <div class="glass-card">
            <div class="section-label">📄 Document</div>
            <div class="section-title">Business Requirements Document</div>
            <div class="section-desc">Auto-generated from your project brief.</div>
        </div>
        """, unsafe_allow_html=True)

        brd_text = st.session_state.brd_text or ""
        sections = parse_brd_sections(brd_text)

        if "raw" in sections:
            # Could not parse — display nicely formatted raw text
            st.markdown(brd_text)
        else:
            for heading, body in sections.items():
                st.markdown(
                    f'<div class="brd-heading">{heading}</div>',
                    unsafe_allow_html=True,
                )
                for line in body.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("- ") or line.startswith("• "):
                        cleaned = line.lstrip("-•").strip()
                        st.markdown(
                            f'<div class="brd-item">● {cleaned}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<div class="brd-text">{line}</div>',
                            unsafe_allow_html=True,
                        )

    # ── TAB 2: Plan / Agile ──────────────────────────────────────────
    with tab_plan:
        if st.session_state.methodology and st.session_state.methodology.startswith("Waterfall"):
            st.markdown("""
            <div class="glass-card">
                <div class="section-label">📊 Plan</div>
                <div class="section-title">Work Breakdown Structure</div>
                <div class="section-desc">Tasks organized by phase with time estimates.</div>
            </div>
            """, unsafe_allow_html=True)
    
            wbs_df = st.session_state.wbs_df
    
            if wbs_df is not None and not wbs_df.empty:
                # Stats row
                total_tasks = len(wbs_df)
                total_phases = wbs_df["Phase"].nunique()
    
                total_days = 0
                for v in wbs_df["Estimated Days"]:
                    try:
                        total_days += int(v)
                    except (ValueError, TypeError):
                        pass
    
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(
                        '<div class="stat-card">'
                        f'<div class="stat-value">{total_phases}</div>'
                        '<div class="stat-label">Phases</div>'
                        '</div>',
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown(
                        '<div class="stat-card">'
                        f'<div class="stat-value">{total_tasks}</div>'
                        '<div class="stat-label">Tasks</div>'
                        '</div>',
                        unsafe_allow_html=True,
                    )
                with c3:
                    st.markdown(
                        '<div class="stat-card">'
                        f'<div class="stat-value">{total_days}</div>'
                        '<div class="stat-label">Total Days</div>'
                        '</div>',
                        unsafe_allow_html=True,
                    )
    
                st.markdown("<br>", unsafe_allow_html=True)
    
                # Styled dataframe
                st.dataframe(
                    wbs_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Phase": st.column_config.TextColumn("Phase", width="medium"),
                        "Task": st.column_config.TextColumn("Task", width="large"),
                        "Estimated Days": st.column_config.TextColumn("Est. Days", width="small"),
                    },
                )
                
                # Render Gantt Chart
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 📅 Project Timeline")
                gantt_fig = generate_gantt_chart(wbs_df)
                if gantt_fig:
                    st.plotly_chart(gantt_fig, use_container_width=True)
                else:
                    st.info("💡 Gantt chart could not be generated.")
            else:
                st.warning(
                    "⚠️  Could not parse WBS into a table. Showing raw output below."
                )
                st.code(st.session_state.wbs_text or "No WBS data available.")
        
        else:
            # Agile Mode
            st.markdown("""
            <div class="glass-card">
                <div class="section-label">🏃 Agile</div>
                <div class="section-title">Product Backlog</div>
                <div class="section-desc">User stories parsed by Epic with assigned Story Points.</div>
            </div>
            """, unsafe_allow_html=True)
    
            agile_df = st.session_state.agile_df
            
            if agile_df is not None and not agile_df.empty:
                # Stats row
                total_stories = len(agile_df)
                total_epics = agile_df["Epic"].nunique()
    
                total_points = 0
                for v in agile_df["Story Points"]:
                    try:
                        total_points += int(v)
                    except (ValueError, TypeError):
                        pass
    
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(
                        '<div class="stat-card">'
                        f'<div class="stat-value">{total_epics}</div>'
                        '<div class="stat-label">Epics</div>'
                        '</div>',
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown(
                        '<div class="stat-card">'
                        f'<div class="stat-value">{total_stories}</div>'
                        '<div class="stat-label">User Stories</div>'
                        '</div>',
                        unsafe_allow_html=True,
                    )
                with c3:
                    st.markdown(
                        '<div class="stat-card">'
                        f'<div class="stat-value">{total_points}</div>'
                        '<div class="stat-label">Story Points</div>'
                        '</div>',
                        unsafe_allow_html=True,
                    )
    
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.dataframe(
                    agile_df,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.warning("⚠️  Could not parse Agile data into a table. Showing raw output below.")
                st.code(st.session_state.agile_text or "No Agile Backlog data available.")

    # ── TAB 3: Risks ─────────────────────────────────────────
    with tab_risk:
        st.markdown("""
        <div class="glass-card">
            <div class="section-label">⚠️ Risks</div>
            <div class="section-title">Risk Register</div>
            <div class="section-desc">Identified risks and mitigation strategies.</div>
        </div>
        """, unsafe_allow_html=True)

        risk_df = st.session_state.risk_df

        if risk_df is not None and not risk_df.empty:
            st.dataframe(
                risk_df,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning("⚠️  Could not parse Risk data into a table. Showing raw output below.")
            st.code(st.session_state.risk_text or "No Risk data available.")

    # ── TAB 4: Costs ─────────────────────────────────────────
    with tab_cost:
        st.markdown("""
        <div class="glass-card">
            <div class="section-label">💰 Costs</div>
            <div class="section-title">Cost Estimation</div>
            <div class="section-desc">Estimated project resource costs.</div>
        </div>
        """, unsafe_allow_html=True)

        cost_df = st.session_state.cost_df

        if cost_df is not None and not cost_df.empty:
            st.dataframe(
                cost_df,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.warning("⚠️  Could not parse Cost data into a table. Showing raw output below.")
            st.code(st.session_state.cost_text or "No Cost data available.")

    # ── TAB 5: Download ─────────────────────────────────────
    with tab_download:
        st.markdown("""
        <div class="glass-card">
            <div class="section-label">📥 Export</div>
            <div class="section-title">Download Report</div>
            <div class="section-desc">
                Export a professionally formatted Word document containing
                your BRD, WBS, Risk Register, and Cost Estimation.
            </div>
        </div>
        """, unsafe_allow_html=True)

        brd_for_doc = st.session_state.brd_text or ""
        wbs_for_doc = st.session_state.wbs_df if st.session_state.wbs_df is not None else pd.DataFrame()
        agile_for_doc = st.session_state.agile_df if st.session_state.agile_df is not None else pd.DataFrame()
        risk_for_doc = st.session_state.risk_df if st.session_state.risk_df is not None else pd.DataFrame()
        cost_for_doc = st.session_state.cost_df if st.session_state.cost_df is not None else pd.DataFrame()
        methodology = st.session_state.methodology or "Waterfall"

        try:
            docx_buffer = create_docx(project_brief, brd_for_doc, wbs_for_doc, agile_for_doc, risk_for_doc, cost_for_doc, methodology)

            col_dl, _ = st.columns([1, 3])
            with col_dl:
                st.download_button(
                    label="📥  Download DOCX Report",
                    data=docx_buffer,
                    file_name="APEX_Lite_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )

            st.info(
                "💡 The report includes a styled title page, structured BRD sections, "
                "WBS Planning/Agile Backlog, Risk, and Cost tables."
            )
        except Exception as e:
            st.error(f"❌  Failed to generate DOCX: {e}")

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem; color: #556080;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📋</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #7888a8;">
            No plan generated yet
        </div>
        <div style="font-size: 0.88rem; margin-top: 0.3rem; color: #556080;">
            Enter a project description above and click <b>Generate Plan</b> to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)
"""
Inject per-stage CSS theme and render the stage context banner.
Call apply_stage_theme() once per page, after render_chat_panel().
"""
import streamlit as st
from utils.session_manager import get_education_stage
from utils.stage_config import get_stage_config


def apply_stage_theme():
    """Inject stage CSS and render the page-top stage banner."""
    stage = get_education_stage()
    cfg = get_stage_config(stage)
    color = cfg["color"]
    bg = cfg["bg"]
    dark = cfg["dark"]

    st.markdown(f"""
<style>
/* ── Sidebar accent ───────────────────────────────────── */
section[data-testid="stSidebar"] {{
    border-right: 4px solid {color} !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    background: linear-gradient(180deg, {bg}60 0%, transparent 120px) !important;
}}

/* ── Primary buttons ──────────────────────────────────── */
div.stButton > button[kind="primary"],
div.stButton > button[data-testid*="primary"] {{
    background-color: {color} !important;
    border-color: {color} !important;
    color: white !important;
}}

/* ── Expander left accent ─────────────────────────────── */
details > summary {{
    border-left: 3px solid {color};
    padding-left: 10px;
}}

/* ── Metric label color ───────────────────────────────── */
div[data-testid="stMetricLabel"] {{
    color: {dark} !important;
}}

/* ── Tab active underline ─────────────────────────────── */
button[data-baseweb="tab"][aria-selected="true"] {{
    border-bottom: 3px solid {color} !important;
    color: {color} !important;
}}

/* ── Info boxes ───────────────────────────────────────── */
div[data-testid="stInfo"] {{
    border-left: 4px solid {color} !important;
}}

/* ── Stage banner ─────────────────────────────────────── */
.stage-banner {{
    background: linear-gradient(135deg, {color}18, {bg}80);
    border-left: 5px solid {color};
    border-radius: 0 8px 8px 0;
    padding: 10px 16px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.stage-banner strong {{
    color: {dark};
    font-size: 0.95em;
}}
.stage-banner span {{
    color: {dark}99;
    font-size: 0.82em;
}}
</style>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="stage-banner">
    <strong>{cfg['label']}</strong>
    <span>·&nbsp;{cfg['subtitle']}</span>
</div>
""", unsafe_allow_html=True)

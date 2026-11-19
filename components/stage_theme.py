"""
SGDS-inspired theme + per-stage accent banner.
"""
import streamlit as st
from utils.session_manager import get_education_stage
from utils.stage_config import get_stage_config


def apply_stage_theme():
    stage = get_education_stage()
    cfg = get_stage_config(stage)
    color = cfg["color"]
    bg = cfg["bg"]
    dark = cfg["dark"]

    st.markdown(f"""
<style>
/* ── Google Fonts ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* ── Base typography ──────────────────────────────────── */
html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}}
h1, h2, h3 {{ font-weight: 700; color: #0E0E0E; }}
h4, h5, h6 {{ font-weight: 600; color: #3B3B3B; }}

/* ── Hide Streamlit default page nav ──────────────────── */
[data-testid="stSidebarNav"] {{display: none !important;}}

/* ── Sidebar (gov.sg clean) ───────────────────────────── */
section[data-testid="stSidebar"] {{
    background-color: #F7F7F7 !important;
    border-right: 1px solid #DFDFDF !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    background: #F7F7F7 !important;
}}

/* ── Primary buttons (gov.sg blue) ────────────────────── */
div.stButton > button[kind="primary"],
div.stButton > button[data-testid*="primary"] {{
    background-color: #0269D0 !important;
    border-color: #0269D0 !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
}}
div.stButton > button[kind="primary"]:hover {{
    background-color: #0151A0 !important;
}}

/* ── Secondary buttons ────────────────────────────────── */
div.stButton > button:not([kind="primary"]) {{
    border: 1px solid #DFDFDF !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}}

/* ── Info boxes (SGDS style) ──────────────────────────── */
div[data-testid="stAlert"] > div {{
    border-radius: 4px !important;
}}

/* ── Tab active underline (gov.sg blue) ───────────────── */
button[data-baseweb="tab"][aria-selected="true"] {{
    border-bottom: 3px solid #0269D0 !important;
    color: #0269D0 !important;
    font-weight: 600 !important;
}}

/* ── Expanders (clean gov.sg style) ───────────────────── */
details {{
    border: 1px solid #DFDFDF !important;
    border-radius: 8px !important;
    margin-bottom: 8px;
}}
details > summary {{
    font-weight: 600;
    color: #3B3B3B;
}}

/* ── Dataframes ───────────────────────────────────────── */
div[data-testid="stDataFrame"] {{
    border: 1px solid #DFDFDF;
    border-radius: 8px;
}}

/* ── Stage accent (subtle) ────────────────────────────── */
.stage-banner {{
    background: {bg}40;
    border-left: 4px solid {color};
    border-radius: 0 6px 6px 0;
    padding: 8px 16px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.stage-banner strong {{
    color: {dark};
    font-size: 0.9em;
}}
.stage-banner span {{
    color: {dark}99;
    font-size: 0.8em;
}}

/* ── Gov.sg footer style ──────────────────────────────── */
.gov-footer {{
    background: #F3F3F3;
    border-top: 1px solid #DFDFDF;
    padding: 16px 24px;
    margin-top: 40px;
    border-radius: 4px;
    font-size: 0.8em;
    color: #6B6B6B;
    text-align: center;
}}
.gov-footer a {{ color: #0269D0; text-decoration: none; }}
.gov-footer a:hover {{ text-decoration: underline; }}
</style>
""", unsafe_allow_html=True)

    # Stage banner
    st.markdown(f"""
<div class="stage-banner">
    <strong>{cfg['label']}</strong>
    <span>&middot;&nbsp;{cfg['subtitle']}</span>
</div>
""", unsafe_allow_html=True)

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

/* ── Tab active underline (stage color) ──────────────── */
button[data-baseweb="tab"][aria-selected="true"] {{
    border-bottom: 3px solid {color} !important;
    color: {dark} !important;
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

/* ── Error / warning animations ──────────────────────── */
@keyframes ep-shake {{
    0%, 100% {{ transform: translateX(0); }}
    10%, 30%, 50%, 70%, 90% {{ transform: translateX(-4px); }}
    20%, 40%, 60%, 80% {{ transform: translateX(4px); }}
}}
@keyframes ep-fade-slide-in {{
    from {{ opacity: 0; transform: translateY(-8px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes ep-pulse-border {{
    0%   {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }}
    70%  {{ box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
}}
@keyframes ep-warning-pulse {{
    0%   {{ box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }}
    70%  {{ box-shadow: 0 0 0 6px rgba(245, 158, 11, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }}
}}

/* Error alerts — shake + fade in + pulse glow */
div[data-testid="stAlert"][data-baseweb*="negative"],
div[data-testid="stNotification"][kind="error"],
div.stAlert > div[role="alert"]:has(> svg[data-testid="stErrorIcon"]) {{
    animation: ep-fade-slide-in 0.4s ease-out, ep-shake 0.5s ease-in-out 0.1s, ep-pulse-border 1.5s ease-out 0.6s;
    border-radius: 6px !important;
}}

/* Warning alerts — softer fade + pulse */
div[data-testid="stAlert"][data-baseweb*="warning"],
div[data-testid="stNotification"][kind="warning"] {{
    animation: ep-fade-slide-in 0.4s ease-out, ep-warning-pulse 1.5s ease-out 0.4s;
    border-radius: 6px !important;
}}

/* Success & info alerts — smooth fade in */
div[data-testid="stAlert"][data-baseweb*="positive"],
div[data-testid="stAlert"][data-baseweb*="informational"],
div[data-testid="stNotification"][kind="success"],
div[data-testid="stNotification"][kind="info"] {{
    animation: ep-fade-slide-in 0.4s ease-out;
    border-radius: 6px !important;
}}

/* ── Stage accent card ────────────────────────────────── */
.stage-banner {{
    background: linear-gradient(135deg, {bg}, {bg}90);
    border-left: 5px solid {color};
    border-radius: 0 10px 10px 0;
    padding: 14px 20px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    box-shadow: 0 2px 8px {color}18;
    animation: ep-fade-slide-in 0.4s ease-out;
}}
.stage-banner-icon {{
    font-size: 1.6em;
    line-height: 1;
    flex-shrink: 0;
}}
.stage-banner-text {{
    display: flex;
    flex-direction: column;
    gap: 2px;
}}
.stage-banner strong {{
    color: {dark};
    font-size: 0.95em;
}}
.stage-banner .stage-sub {{
    color: {dark}99;
    font-size: 0.78em;
}}
.stage-banner .stage-action {{
    color: {dark}cc;
    font-size: 0.78em;
    font-style: italic;
    margin-top: 2px;
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
    banner_icon = cfg.get("banner_icon", "📋")
    banner_action = cfg.get("banner_action", "")
    action_html = f'<div class="stage-action">💡 {banner_action}</div>' if banner_action else ""
    st.markdown(f"""
<div class="stage-banner">
    <div class="stage-banner-icon">{banner_icon}</div>
    <div class="stage-banner-text">
        <strong>{cfg['label']}</strong>
        <div class="stage-sub">{cfg['subtitle']}</div>
        {action_html}
    </div>
</div>
""", unsafe_allow_html=True)

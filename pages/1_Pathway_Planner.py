import streamlit as st

st.set_page_config(page_title="Pathway Planner — EduPath SG", page_icon="🗺️", layout="wide")

import plotly.graph_objects as go
import pandas as pd

from utils.session_manager import require_login
from utils.config import DISCLAIMER
from components.sidebar import render_sidebar
from services.pathway_service import get_stages, get_pathway_for_profile

user = require_login()
render_sidebar()

st.title("🗺️ Singapore Education Pathway Planner")
st.caption("Visualise your complete education journey from any stage to graduation and beyond.")
st.warning(f"⚠️ {DISCLAIMER}", icon="⚠️")

STAGE_ID_MAP = {
    "Early Childhood (0–6)": "early_childhood",
    "Primary School": "primary",
    "Secondary School": "secondary_express",
    "Post-Secondary (JC/Poly/ITE)": "junior_college",
    "University": "university",
    "Post-Graduate": "postgrad",
}

ALL_STAGES_META = [
    {"id": "early_childhood", "name": "Early Childhood", "age": "0–6"},
    {"id": "primary",         "name": "Primary School",   "age": "7–12"},
    {"id": "secondary_express","name": "Secondary School", "age": "13–16/17"},
    {"id": "junior_college",  "name": "Post-Secondary",   "age": "17–19"},
    {"id": "university",      "name": "University",        "age": "19–23"},
    {"id": "postgrad",        "name": "Post-Grad / SkillsFuture", "age": "23+"},
]

# ── INPUT FORM ──────────────────────────────────────────────────────────────
with st.form("pathway_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        stage_label = st.selectbox("Current stage:", list(STAGE_ID_MAP.keys()))
    with col2:
        citizenship = st.selectbox("Citizenship:", ["Singapore Citizen", "Permanent Resident", "International Student"])
    with col3:
        age = st.number_input("Child's current age:", min_value=0, max_value=25, value=7)

    interests = st.multiselect(
        "Areas of interest (optional):",
        ["STEM / Engineering", "Business / Finance", "Arts / Design / Media",
         "Healthcare / Medicine", "Law", "Education / Social Work", "IT / Computing", "Vocational / Technical"],
    )
    submitted = st.form_submit_button("🗺️ Show My Pathway", type="primary", use_container_width=True)

if submitted or st.session_state.get("pathway_shown"):
    st.session_state["pathway_shown"] = True
    stage_id = STAGE_ID_MAP[stage_label]
    pathway = get_pathway_for_profile(stage_id, interests, citizenship)

    # ── VISUAL TIMELINE ─────────────────────────────────────────────────────
    st.divider()
    st.subheader("📍 Your Education Timeline")

    current_idx = next((i for i, s in enumerate(ALL_STAGES_META) if s["id"] == stage_id), 0)
    n = len(ALL_STAGES_META)
    xs = list(range(n))
    ys = [0] * n

    colours = []
    for i in range(n):
        if i < current_idx:
            colours.append("#90A4AE")   # past – grey
        elif i == current_idx:
            colours.append("#1565C0")   # current – deep blue
        else:
            colours.append("#42A5F5")   # upcoming – light blue

    labels = [f"<b>{s['name']}</b><br>{s['age']} yrs" for s in ALL_STAGES_META]

    fig = go.Figure()

    # Connecting line
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="lines",
        line=dict(color="#B0BEC5", width=3),
        hoverinfo="skip",
        showlegend=False,
    ))

    # Stage nodes
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="markers+text",
        marker=dict(size=36, color=colours, line=dict(color="white", width=2)),
        text=labels,
        textposition="bottom center",
        hovertext=[f"{s['name']} ({s['age']} yrs)" for s in ALL_STAGES_META],
        hoverinfo="text",
        showlegend=False,
    ))

    # Stage number inside node
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="text",
        text=[str(i + 1) for i in range(n)],
        textfont=dict(color="white", size=14),
        hoverinfo="skip",
        showlegend=False,
    ))

    fig.update_layout(
        height=200,
        margin=dict(t=20, b=80, l=20, r=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 0.5]),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    # Legend annotation
    fig.add_annotation(x=current_idx, y=0.35, text="▼ You are here", showarrow=False,
                       font=dict(color="#1565C0", size=12))

    st.plotly_chart(fig, use_container_width=True)

    # Colour legend
    lcol1, lcol2, lcol3 = st.columns(3)
    lcol1.markdown("🔵 **Current stage**")
    lcol2.markdown("🩵 **Upcoming stages**")
    lcol3.markdown("⬜ **Previous stages**")

    # ── CITIZENSHIP NOTES ───────────────────────────────────────────────────
    if pathway.get("citizenship_notes"):
        st.divider()
        st.subheader(f"🌐 Notes for {citizenship}")
        for note in pathway["citizenship_notes"]:
            st.info(note)

    # ── STAGE DETAILS ───────────────────────────────────────────────────────
    st.divider()
    st.subheader("📋 Stage-by-Stage Details")

    for stage in pathway.get("stages", []):
        age_range = stage.get("age_range", "")
        with st.expander(f"**{stage.get('name', '')}** — Age {age_range}", expanded=False):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Description:** {stage.get('description', '')}")
                st.markdown(f"**Entry criteria:** {stage.get('entry_criteria', '')}")
            with col_b:
                st.markdown(f"**Exit process:** {stage.get('exit_process', '')}")
                st.markdown(f"**Governing body:** {stage.get('governing_body', '')}")
            if stage.get("official_url"):
                st.markdown(f"🔗 [Official information]({stage['official_url']})")
            if stage.get("key_facts"):
                st.markdown("**Key facts:**")
                for fact in stage["key_facts"]:
                    st.markdown(f"- {fact}")

    # ── FORKS ───────────────────────────────────────────────────────────────
    if pathway.get("forks"):
        st.divider()
        st.subheader("🔀 Key Decision Points")
        for fork in pathway["forks"]:
            st.markdown(f"### Fork at: **{fork['at']}**")
            for i, opt in enumerate(fork["options"]):
                colour_fn = st.success if i == 0 else (st.info if i == 1 else st.warning)
                colour_fn(f"**{opt['name']}** — _{opt['criteria']}_ → {opt['leads_to']}")
            st.divider()

    # ── QUICK LINK ──────────────────────────────────────────────────────────
    st.divider()
    st.markdown("**🎯 Want to check specific school eligibility based on scores?**")
    st.page_link("pages/2_Score_Matcher.py", label="→ Go to Score & School Matcher", icon="🎯")

import streamlit as st
from utils.session_manager import (
    get_user, clear_user, get_education_stage, set_education_stage,
    get_career_goal, set_career_goal,
)
from utils.stage_config import STAGES, STAGE_ORDER
from components.role_context import get_role_labels


def render_sidebar():
    user = get_user()
    if not user:
        return

    role = user["role"]
    labels = get_role_labels(role)

    with st.sidebar:
        st.markdown("## 🎓 EduPath SG")
        st.caption("Singapore Education Journey Navigator")
        st.divider()

        # User info
        st.markdown(f"**{user['full_name'].split()[0]}** {labels['home_icon']}")
        st.caption(f"Role: {role.capitalize()}")
        st.divider()

        # ── Stage selector ────────────────────────────────────
        st.markdown("**Your Education Stage**")
        current = get_education_stage()

        for key in STAGE_ORDER:
            s = STAGES[key]
            is_active = key == current
            bg_color = s['color'] if is_active else "transparent"
            text_color = "white" if is_active else s['dark']
            border = f"2px solid {s['color']}"
            st.markdown(f"""
<div style="
    background:{bg_color};
    border:{border};
    border-radius:6px;
    padding:5px 10px;
    margin:3px 0;
    font-size:0.85em;
    color:{text_color};
    line-height:1.4;
">
{s['label']}<br><small style="opacity:0.75">{s['subtitle']}</small>
</div>
""", unsafe_allow_html=True)
            if st.button(
                "✓ Selected" if is_active else "Select",
                key=f"stage_btn_{key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                set_education_stage(key)
                st.rerun()

        st.divider()

        # ── Career goal selector ──────────────────────────────
        st.markdown(f"**{labels['career_question']}**")
        try:
            from services.career_service import get_career_list
            careers = get_career_list()
            career_options = ["🔍 Exploring (no specific goal)"] + [
                f"{c['icon']} {c['career']}" for c in careers
            ]
            current_goal = get_career_goal()
            idx = 0
            if current_goal:
                for i, opt in enumerate(career_options):
                    if current_goal in opt:
                        idx = i
                        break
            selected = st.selectbox(
                "Career aspiration:",
                career_options,
                index=idx,
                key="sidebar_career_select",
                label_visibility="collapsed",
            )
            if selected and selected != "🔍 Exploring (no specific goal)":
                career_name = selected.split(" ", 1)[1] if " " in selected else selected
                if career_name != current_goal:
                    set_career_goal(career_name)
                    st.rerun()
                st.caption(f"🎯 Goal: **{career_name}**")
            elif current_goal:
                set_career_goal(None)
                st.rerun()
        except Exception:
            st.caption("Career data loading…")

        st.divider()

        # ── Nav links (role-filtered) ─────────────────────────
        st.markdown("**Explore**")
        if role == "teacher":
            st.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner (Full Data)")
            st.page_link("pages/2_Score_Matcher.py", label="🎯 Score Matcher (Full Data)")
        else:
            st.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner")
            st.page_link("pages/2_Score_Matcher.py", label="🎯 Score & School Matcher")
        st.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Guide")
        st.page_link("pages/4_AI_Guide.py", label="🤖 AI Education Guide")
        if role in ("parent", "teacher"):
            st.page_link("pages/8_Primary_Hub.py", label="🏫 Primary School Hub")
        st.page_link("pages/7_Support_Hub.py", label="🤝 Support Hub")

        st.divider()
        st.markdown("**Info**")
        st.page_link("pages/5_About_Us.py", label="ℹ️ About Us")
        st.page_link("pages/6_Methodology.py", label="📖 Methodology")

        st.divider()

        # Role hint styled in stage color
        color = STAGES[current]["color"]
        hint_bg = STAGES[current]["bg"]
        st.markdown(f"""
<div style="background:{hint_bg};border-left:3px solid {color};border-radius:4px;padding:8px 10px;font-size:0.82em;">
{labels['home_icon']} {role.capitalize()} View<br>{labels['welcome_action']}
</div>
""", unsafe_allow_html=True)

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            clear_user()
            st.rerun()

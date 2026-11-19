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
        st.caption(f"{labels['home_icon']} {role.capitalize()} · {labels['welcome_action']}")
        st.divider()

        # ── Stage selector (compact dropdown) ─────────────────
        visible_stages = [k for k in STAGE_ORDER if not (role == "student" and k == "early_childhood")]
        current = get_education_stage()
        if role == "student" and current == "early_childhood":
            set_education_stage("primary")
            current = "primary"

        stage_labels = {k: STAGES[k]["label"] for k in visible_stages}
        current_label = stage_labels.get(current, stage_labels[visible_stages[0]])
        selected_label = st.selectbox(
            "Education Stage:",
            list(stage_labels.values()),
            index=list(stage_labels.values()).index(current_label),
            key="stage_select",
        )
        for k, v in stage_labels.items():
            if v == selected_label and k != current:
                set_education_stage(k)
                st.rerun()

        # ── Career goal selector ──────────────────────────────
        try:
            from services.career_service import get_career_list
            careers = get_career_list()
            career_options = ["🔍 Exploring"] + [f"{c['icon']} {c['career']}" for c in careers]
            current_goal = get_career_goal()
            idx = 0
            if current_goal:
                for i, opt in enumerate(career_options):
                    if current_goal in opt:
                        idx = i
                        break
            selected = st.selectbox("Career Goal:", career_options, index=idx, key="sidebar_career")
            if selected and selected != "🔍 Exploring":
                career_name = selected.split(" ", 1)[1] if " " in selected else selected
                if career_name != current_goal:
                    set_career_goal(career_name)
                    st.rerun()
            elif current_goal:
                set_career_goal(None)
                st.rerun()
        except Exception:
            pass

        st.divider()

        # ── Nav links ─────────────────────────────────────────
        st.page_link("app.py", label="🏠 Home")
        st.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner")
        st.page_link("pages/2_Score_Matcher.py", label="🎯 Score & School Matcher")
        st.page_link("pages/3_Fallback_Support.py", label="🔄 Fallback & Support")
        st.divider()
        st.page_link("pages/4_About_Us.py", label="ℹ️ About Us")
        st.page_link("pages/5_Methodology.py", label="📖 Methodology")

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            clear_user()
            st.rerun()

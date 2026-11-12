import streamlit as st
from utils.session_manager import get_user, clear_user, get_education_stage, set_education_stage
from utils.stage_config import STAGES, STAGE_ORDER


def render_sidebar():
    user = get_user()
    if not user:
        return

    with st.sidebar:
        st.markdown("## 🎓 EduPath SG")
        st.caption("Singapore Education Journey Navigator")
        st.divider()

        # User info
        st.markdown(f"**{user['full_name'].split()[0]}**")
        st.caption(f"Role: {user['role'].capitalize()}")
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

        # ── Nav links ─────────────────────────────────────────
        st.markdown("**Explore**")
        st.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner")
        st.page_link("pages/2_Score_Matcher.py", label="🎯 Score & School Matcher")
        st.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Guide")
        st.page_link("pages/4_AI_Guide.py", label="🤖 AI Education Guide")
        st.page_link("pages/8_Primary_Hub.py", label="🏫 Primary School Hub")
        st.page_link("pages/7_Support_Hub.py", label="🤝 Support Hub")

        st.divider()
        st.markdown("**Info**")
        st.page_link("pages/5_About_Us.py", label="ℹ️ About Us")
        st.page_link("pages/6_Methodology.py", label="📖 Methodology")

        st.divider()

        # Role hint styled in stage color
        role_hints = {
            "parent": "👨‍👩‍👧 Parent View\nPlan your child's journey.",
            "student": "🎒 Student View\nCheck scores and find schools.",
            "teacher": "👩‍🏫 Teacher View\nFull pathway data for counselling.",
        }
        hint = role_hints.get(user["role"], "")
        if hint:
            color = STAGES[current]["color"]
            hint_bg = STAGES[current]["bg"]
            st.markdown(f"""
<div style="background:{hint_bg};border-left:3px solid {color};border-radius:4px;padding:8px 10px;font-size:0.82em;">
{hint}
</div>
""", unsafe_allow_html=True)

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            clear_user()
            st.rerun()

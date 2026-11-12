import streamlit as st
from utils.session_manager import get_user, clear_user


def render_sidebar():
    user = get_user()
    if not user:
        return

    with st.sidebar:
        st.markdown("## 🎓 EduPath SG")
        st.caption("Singapore Education Journey Navigator")
        st.divider()
        st.markdown(f"**{user['full_name'].split()[0]}**")
        st.caption(f"Role: {user['role'].capitalize()}")
        st.divider()

        role = user["role"]

        st.markdown("**Explore**")
        st.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner")
        st.page_link("pages/2_Score_Matcher.py", label="🎯 Score & School Matcher")
        st.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Guide")
        st.page_link("pages/4_AI_Guide.py", label="🤖 AI Education Guide")

        st.divider()
        st.markdown("**Info**")
        st.page_link("pages/5_About_Us.py", label="ℹ️ About Us")
        st.page_link("pages/6_Methodology.py", label="📖 Methodology")

        st.divider()

        if role == "parent":
            st.info("👨‍👩‍👧 Parent View\nPlan your child's journey from any stage.")
        elif role == "student":
            st.info("🎒 Student View\nCheck your score and find matching schools.")
        elif role == "teacher":
            st.info("👩‍🏫 Teacher View\nFull pathway data for student counselling.")

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            clear_user()
            st.rerun()

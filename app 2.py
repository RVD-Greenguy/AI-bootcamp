import streamlit as st

st.set_page_config(
    page_title="EduPath SG — Singapore Education Journey Navigator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.session_manager import get_user, set_user, clear_user
from utils.config import DISCLAIMER
from services.auth_service import login_user, register_user

user = get_user()

if user:
    st.title("🎓 EduPath SG")
    st.caption("Singapore Education Journey Navigator")
    st.info(f"⚠️ {DISCLAIMER}")
    st.divider()

    role = user["role"]
    name = user["full_name"].split()[0]

    if role == "parent":
        st.markdown(f"### Welcome back, {name}! 👨‍👩‍👧")
        st.markdown("Plan your child's complete education journey — from preschool registration through to university and beyond.")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner", use_container_width=True)
        with col2:
            st.page_link("pages/2_Score_Matcher.py", label="🎯 Score Matcher", use_container_width=True)
        with col3:
            st.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Guide", use_container_width=True)
        with col4:
            st.page_link("pages/4_AI_Guide.py", label="🤖 AI Guide", use_container_width=True)

    elif role == "student":
        st.markdown(f"### Welcome, {name}! 🎒")
        st.markdown("Check your score, find schools that match, and plan your next steps in Singapore's education system.")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.page_link("pages/2_Score_Matcher.py", label="🎯 Check My Scores", use_container_width=True)
        with col2:
            st.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Options", use_container_width=True)
        with col3:
            st.page_link("pages/4_AI_Guide.py", label="🤖 Ask the Guide", use_container_width=True)

    elif role == "teacher":
        st.markdown(f"### Welcome, {name}! 👩‍🏫")
        st.markdown("Full Singapore education pathway data for student counselling — from PSLE to post-graduation.")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner", use_container_width=True)
        with col2:
            st.page_link("pages/2_Score_Matcher.py", label="🎯 Score Matcher", use_container_width=True)
        with col3:
            st.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Guide", use_container_width=True)
        with col4:
            st.page_link("pages/4_AI_Guide.py", label="🤖 AI Guide", use_container_width=True)

    st.divider()
    st.markdown("**Quick reference:** [MOE](https://www.moe.gov.sg) · [SEAB](https://www.seab.gov.sg) · [ITE](https://www.ite.edu.sg) · [SkillsFuture](https://www.skillsfuture.gov.sg)")

    with st.sidebar:
        st.markdown("## 🎓 EduPath SG")
        st.caption("Singapore Education Journey Navigator")
        st.divider()
        st.markdown(f"**{user['full_name'].split()[0]}** ({user['role'].capitalize()})")
        st.divider()
        st.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner")
        st.page_link("pages/2_Score_Matcher.py", label="🎯 Score & School Matcher")
        st.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Guide")
        st.page_link("pages/4_AI_Guide.py", label="🤖 AI Education Guide")
        st.divider()
        st.page_link("pages/5_About_Us.py", label="ℹ️ About Us")
        st.page_link("pages/6_Methodology.py", label="📖 Methodology")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            clear_user()
            st.rerun()

else:
    # ── LOGIN / REGISTER ─────────────────────────────────────────────────────
    col_hero, col_form = st.columns([3, 2])

    with col_hero:
        st.markdown("# 🎓 EduPath SG")
        st.markdown("### Singapore Education Journey Navigator")
        st.markdown("""
Navigate every official education transition in Singapore — from birth through post-graduation.

**For Parents** — Plan your child's complete journey. Understand P1 registration, PSLE options,
IP vs non-IP schools, and what happens at every fork.

**For Students** — Enter your scores and instantly see which schools and programmes you qualify for.
Check fallback options and retake policies.

**For Teachers** — Full pathway data for student counselling. L1R5 calculator, school matcher,
and DAE university guide.
        """)
        st.info(f"ℹ️ {DISCLAIMER}")

        st.markdown("**Demo accounts (no sign-up needed):**")
        st.markdown("""
| Role | Email | Password |
|------|-------|----------|
| Parent | parent@edupathsg.sg | Parent123! |
| Student | student@edupathsg.sg | Student123! |
| Teacher | teacher@edupathsg.sg | Teacher123! |
        """)

    with col_form:
        st.markdown("### Sign In")
        tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])

        with tab_login:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

            if submitted:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    user_data, err = login_user(email, password)
                    if err:
                        st.error(err)
                    else:
                        set_user(user_data)
                        st.rerun()

        with tab_register:
            with st.form("register_form"):
                reg_name = st.text_input("Full Name")
                reg_email = st.text_input("Email", key="reg_email")
                reg_role = st.selectbox("Role", ["parent", "student", "teacher"])
                reg_pass = st.text_input("Password (min 8 chars)", type="password", key="reg_pass")
                reg_submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

            if reg_submitted:
                if not all([reg_name, reg_email, reg_pass]):
                    st.error("Please fill in all fields.")
                else:
                    user_data, err = register_user(reg_email, reg_pass, reg_role, reg_name)
                    if err:
                        st.error(err)
                    else:
                        set_user(user_data)
                        st.success("Account created! Welcome to EduPath SG.")
                        st.rerun()

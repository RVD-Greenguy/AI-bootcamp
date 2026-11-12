import streamlit as st

st.set_page_config(
    page_title="EduPath SG — Singapore Education Journey Navigator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner="Setting up EduPath SG…")
def _bootstrap():
    """Run once per process: initialise DB and build TF-IDF index."""
    from pathlib import Path
    from utils.config import DB_PATH
    import sqlite3, bcrypt

    # ── DB init ───────────────────────────────────────────────────────────────
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('parent','student','teacher')),
            full_name TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            question TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            chunks_json TEXT DEFAULT '[]',
            created_at TEXT
        );
    """)
    for email, pw, role, name in [
        ("parent@edupathsg.sg",  "Parent123!",  "parent",  "Demo Parent"),
        ("student@edupathsg.sg", "Student123!", "student", "Demo Student"),
        ("teacher@edupathsg.sg", "Teacher123!", "teacher", "Demo Teacher"),
    ]:
        if not conn.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
            pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
            conn.execute(
                "INSERT INTO users (email,password_hash,role,full_name) VALUES (?,?,?,?)",
                (email, pw_hash, role, name)
            )
    conn.commit()
    conn.close()

    # ── RAG index ─────────────────────────────────────────────────────────────
    from services.rag_service import build_index, index_status
    if not index_status()["indexed"]:
        build_index()

    # ── Geocode schools missing coordinates ───────────────────────────────────
    try:
        from services.geocode_bootstrap import geocode_all
        geocode_all()
    except Exception:
        pass

    return True


_bootstrap()

from utils.session_manager import get_user, set_user, clear_user, get_career_goal, set_career_goal
from utils.config import DISCLAIMER
from services.auth_service import login_user, register_user
from components.role_context import get_role_labels

user = get_user()

if user:
    st.title("🎓 EduPath SG")
    st.caption("Singapore Education Journey Navigator")
    st.info(f"⚠️ {DISCLAIMER}")
    st.divider()

    role = user["role"]
    name = user["full_name"].split()[0]
    labels = get_role_labels(role)

    st.markdown(f"### Welcome back, {name}! {labels['home_icon']}")
    st.markdown(f"{labels['welcome_action']}.")

    # ── Career aspiration section (all roles) ─────────────────────────────
    st.subheader(labels["career_question"])
    try:
        from services.career_service import get_career_list, trace_career_pathway
        import pandas as pd

        careers = get_career_list()
        career_options = ["Still exploring..."] + [f"{c['icon']} {c['career']}" for c in careers]
        current_goal = get_career_goal()
        idx = 0
        if current_goal:
            for i, opt in enumerate(career_options):
                if current_goal in opt:
                    idx = i
                    break
        selected = st.selectbox(
            labels["career_question"],
            career_options, index=idx,
            key="home_career",
            label_visibility="collapsed",
        )
        if selected and selected != "Still exploring...":
            career_name = selected.split(" ", 1)[1] if " " in selected else selected
            set_career_goal(career_name)
            pathway = trace_career_pathway(career_name)
            if pathway:
                st.divider()
                st.markdown(f"### {pathway['icon']} Path to becoming a {pathway['career']}")
                st.caption(f"**Professional requirements:** {pathway['professional_requirements']}")

                if pathway.get("university_targets"):
                    uni_df = pd.DataFrame([{
                        "University": t["uni"],
                        "Faculty": t["faculty"],
                        "Min RP (A-levels)": t["min_rp"],
                        "Min GPA (Poly DAE)": t["min_gpa"],
                        "Duration": t["duration"],
                    } for t in pathway["university_targets"]])
                    st.dataframe(uni_df, use_container_width=True, hide_index=True)

                for p in pathway.get("total_paths", []):
                    st.info(f"**{p['name']}** {p.get('tag','')} — ~{p['years']} years from Sec 1 · {len(p.get('steps',[]))} steps")

                st.page_link("pages/1_Pathway_Planner.py", label="🗺️ See full pathway details →", use_container_width=True)
        else:
            set_career_goal(None)
    except Exception:
        pass

    st.divider()

    # ── Quick links (role-specific) ───────────────────────────────────────
    if role == "parent":
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner", use_container_width=True)
        col2.page_link("pages/2_Score_Matcher.py", label="🎯 Score Matcher", use_container_width=True)
        col3.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Guide", use_container_width=True)
        col4.page_link("pages/4_AI_Guide.py", label="🤖 AI Guide", use_container_width=True)
        col5.page_link("pages/7_Support_Hub.py", label="🤝 Support Hub", use_container_width=True)
    elif role == "student":
        col1, col2, col3, col4 = st.columns(4)
        col1.page_link("pages/2_Score_Matcher.py", label="🎯 Check My Scores", use_container_width=True)
        col2.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Options", use_container_width=True)
        col3.page_link("pages/4_AI_Guide.py", label="🤖 Ask the Guide", use_container_width=True)
        col4.page_link("pages/7_Support_Hub.py", label="🤝 Support Hub", use_container_width=True)
    elif role == "teacher":
        st.caption("👩‍🏫 Full counselling data available on all pages.")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.page_link("pages/1_Pathway_Planner.py", label="🗺️ Pathway Planner", use_container_width=True)
        col2.page_link("pages/2_Score_Matcher.py", label="🎯 Score Matcher", use_container_width=True)
        col3.page_link("pages/3_Fallback_Guide.py", label="🔄 Fallback Guide", use_container_width=True)
        col4.page_link("pages/4_AI_Guide.py", label="🤖 AI Guide", use_container_width=True)
        col5.page_link("pages/8_Primary_Hub.py", label="🏫 Primary Hub", use_container_width=True)

    st.divider()
    st.markdown("**Quick reference:** [MOE](https://www.moe.gov.sg) · [SEAB](https://www.seab.gov.sg) · [ITE](https://www.ite.edu.sg) · [SkillsFuture](https://www.skillsfuture.gov.sg)")

    from components.sidebar import render_sidebar
    render_sidebar()

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

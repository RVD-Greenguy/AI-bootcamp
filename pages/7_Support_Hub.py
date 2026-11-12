"""
EduPath SG — Student Support Hub
Counselling, career guidance, talks/events, scholarships, earn-and-learn programmes.
"""
import streamlit as st
from services.pathway_service import get_support_resources
from utils.session_manager import require_login
from components.sidebar import render_sidebar
from components.chat_panel import render_chat_panel
from components.stage_theme import apply_stage_theme

require_login()
user = st.session_state.user
role = user.get("role", "student")

render_sidebar()
render_chat_panel()
apply_stage_theme()

st.title("🤝 Student Support Hub")
st.markdown("Singapore's official support network — counselling, scholarships, career guidance and work-study programmes.")

resources = get_support_resources()


def _stage_badge(stages: list) -> str:
    if not stages or "all" in stages:
        return ""
    labels = {
        "primary": "Pri", "secondary": "Sec", "jc": "JC",
        "poly": "Poly", "ite": "ITE", "university": "Uni",
        "postgrad": "Post-Grad", "normal_academic": "N(A)", "normal_technical": "N(T)"
    }
    return "  ".join(f"`{labels.get(s, s)}`" for s in stages)


def _url_button(url: str, label: str = "Official site →"):
    if url:
        st.markdown(f"[{label}]({url})", unsafe_allow_html=False)


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧠 Counselling",
    "🧭 Career Guidance",
    "🎤 Talks & Events",
    "🏆 Scholarships & Bursaries",
    "💼 Earn & Learn",
])


# ── TAB 1: Counselling ───────────────────────────────────────────────────────
with tab1:
    st.subheader("Counselling & Mental Health Support")
    st.info(
        "Every MOE school has at least one trained school counsellor. "
        "If you need to talk to someone, your school counsellor is always your first point of contact — "
        "it's free and confidential."
    )
    for item in resources.get("counselling", []):
        with st.expander(f"**{item['name']}** — {item.get('type','')}  {_stage_badge(item.get('stage',[]))}"):
            st.markdown(item.get("description", ""))
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Who can use it:** {item.get('eligibility','')}")
            with col2:
                st.markdown(f"**How to access:** {item.get('how_to_access','')}")
            _url_button(item.get("official_url",""))

    st.divider()
    st.markdown("### Emergency & Crisis Lines")
    crisis = {
        "Samaritans of Singapore (SOS)": "1-767 (24 hrs)",
        "IMH Mental Health Helpline": "6389 2222 (24 hrs)",
        "SAMH Helpline": "1800-283-7019 (Mon–Fri 9am–6pm)",
        "CHAT (Youth 16–30)": "chat.mentalhealth.sg or walk in to Orchard",
        "Child Helpline (HEART@FAM)": "1800-423-4646",
    }
    for name, contact in crisis.items():
        st.markdown(f"- **{name}**: {contact}")


# ── TAB 2: Career Guidance ────────────────────────────────────────────────────
with tab2:
    st.subheader("Career & Education Guidance")
    st.info(
        "Singapore's ECG (Education and Career Guidance) programme is embedded in every secondary school, JC, poly and ITE. "
        "ECG counsellors are trained professionals — not teachers — and sessions are free."
    )

    if role == "teacher":
        st.success(
            "**For teachers:** MOE provides ECG professional development training and resources via "
            "the ECG Professional Learning Network. Contact your school's ECG coordinator for details."
        )

    for item in resources.get("career_guidance", []):
        with st.expander(f"**{item['name']}** — {item.get('type','')}  {_stage_badge(item.get('stage',[]))}"):
            st.markdown(item.get("description", ""))
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Eligibility:** {item.get('eligibility','')}")
            with col2:
                st.markdown(f"**How to access:** {item.get('how_to_access','')}")
            _url_button(item.get("official_url",""))

    st.divider()
    st.markdown("### MySkillsFuture Career Interest Profiler")
    st.markdown(
        "Take the free **Career Interest Profiler** on MySkillsFuture to discover your Holland Code "
        "and explore aligned education pathways and jobs."
    )
    st.markdown("[Open MySkillsFuture →](https://www.myskillsfuture.gov.sg/content/student/en/secondary.html)")


# ── TAB 3: Talks & Events ────────────────────────────────────────────────────
with tab3:
    st.subheader("Talks, Open Houses & Career Events")
    st.markdown(
        "Open houses are the best way to feel the culture of a school before committing. "
        "Most are free and welcome parents and students together."
    )

    # Calendar summary
    st.markdown("### Typical Annual Calendar")
    calendar_data = {
        "January – February": ["JAE application window", "JC posting results", "Poly/ITE posting results"],
        "March – April": ["University open days (NUS, NTU, SMU)", "DAE application window for poly grads"],
        "May – June": ["School holiday career talks", "Industry attachment preview events"],
        "July – August": ["University offer letters", "Pre-enrolment orientation days"],
        "September – October": ["Secondary school open houses (for P6 students)", "University information sessions"],
        "October – November": ["Polytechnic open houses", "ITE open house", "PSLE results released"],
        "November – December": ["PSLE S1 posting (secondary school applications)", "O-level results (early Nov)"],
    }
    for period, events in calendar_data.items():
        with st.expander(f"**{period}**"):
            for e in events:
                st.markdown(f"- {e}")

    st.divider()
    for item in resources.get("talks_events", []):
        with st.expander(f"**{item['name']}** — {item.get('type','')}  {_stage_badge(item.get('stage',[]))}"):
            st.markdown(item.get("description", ""))
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Eligibility:** {item.get('eligibility','')}")
                if item.get("typical_timing"):
                    st.markdown(f"**Typical timing:** {item.get('typical_timing')}")
            with col2:
                if item.get("institutions"):
                    st.markdown(f"**Institutions:** {', '.join(item['institutions'])}")
            _url_button(item.get("official_url",""))


# ── TAB 4: Scholarships & Bursaries ─────────────────────────────────────────
with tab4:
    st.subheader("Scholarships, Bursaries & Financial Aid")

    sub_tab_gov, sub_tab_uni, sub_tab_bursary = st.tabs([
        "🏛️ Government Scholarships",
        "🎓 University Scholarships",
        "💰 Bursaries & FAS",
    ])

    gov_types = {"Government", "Government Research"}
    uni_types = {"University"}
    bursary_types = {"Bursary / Financial Aid", "Community Bursary", "Upskilling Credit"}

    with sub_tab_gov:
        st.markdown(
            "Government scholarships are highly competitive and come with a service bond. "
            "They are awarded to exceptional students with strong academics **and** leadership."
        )
        for item in resources.get("scholarships", []):
            if item.get("type") in gov_types:
                with st.expander(f"**{item['name']}**  {_stage_badge(item.get('stage',[]))}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(item.get("description", ""))
                        st.markdown(f"**Eligibility:** {item.get('eligibility','')}")
                        if item.get("bond"):
                            st.markdown(f"**Bond:** {item.get('bond')}")
                    with col2:
                        if item.get("value"):
                            st.metric("Award Value", item.get("value",""))
                        if item.get("application_period"):
                            st.markdown(f"**Apply:** {item.get('application_period')}")
                    _url_button(item.get("official_url",""))

    with sub_tab_uni:
        st.markdown("Each autonomous university offers merit and need-based awards for enrolled students.")
        for item in resources.get("scholarships", []):
            if item.get("type") in uni_types:
                with st.expander(f"**{item['name']}**  {_stage_badge(item.get('stage',[]))}"):
                    st.markdown(item.get("description", ""))
                    st.markdown(f"**Eligibility:** {item.get('eligibility','')}")
                    if item.get("value"):
                        st.markdown(f"**Value:** {item.get('value')}")
                    _url_button(item.get("official_url",""))

    with sub_tab_bursary:
        st.markdown(
            "Bursaries and the MOE Financial Assistance Scheme (FAS) support lower-income families. "
            "These are **non-competitive** — apply through your school or community organisation."
        )
        for item in resources.get("scholarships", []):
            if item.get("type") in bursary_types:
                with st.expander(f"**{item['name']}** ({item.get('type','')})`{item.get('award_level','')}` {_stage_badge(item.get('stage',[]))}"):
                    st.markdown(item.get("description", ""))
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Eligibility:** {item.get('eligibility','')}")
                    with col2:
                        if item.get("value"):
                            st.markdown(f"**Award:** {item.get('value')}")
                        if item.get("how_to_apply"):
                            st.markdown(f"**Apply:** {item.get('how_to_apply')}")
                    _url_button(item.get("official_url",""))

        st.divider()
        st.markdown("### Community Self-Help Groups (SHGs)")
        shg_data = [
            ("Mendaki", "Malay/Muslim students", "mendaki.org.sg"),
            ("CDAC", "Chinese students", "cdac.org.sg"),
            ("SINDA", "Indian students", "sinda.org.sg"),
            ("EA (Eurasian Association)", "Eurasian students", "eurasian.org.sg"),
        ]
        cols = st.columns(4)
        for col, (name, community, url) in zip(cols, shg_data):
            with col:
                st.markdown(f"**{name}**")
                st.caption(community)
                st.markdown(f"[Visit →](https://www.{url})")


# ── TAB 5: Earn & Learn ───────────────────────────────────────────────────────
with tab5:
    st.subheader("Earn & Learn Programmes")
    st.info(
        "Work-study and apprenticeship programmes let you earn a salary while completing a qualification. "
        "They are structured, employer-sponsored, and lead to the same certification as full-time study."
    )

    # Stage filter
    stage_filter = st.selectbox(
        "Filter by education level",
        ["All", "ITE", "Polytechnic", "University / Post-grad"],
        key="earn_learn_filter"
    )
    stage_map = {
        "ITE": ["ite"],
        "Polytechnic": ["poly"],
        "University / Post-grad": ["university", "postgrad"],
    }

    for item in resources.get("earn_and_learn", []):
        item_stages = item.get("stage", [])
        if stage_filter != "All":
            filter_stages = stage_map[stage_filter]
            if not any(s in item_stages for s in filter_stages):
                continue

        with st.expander(f"**{item['name']}** — {item.get('type','')}  {_stage_badge(item_stages)}"):
            st.markdown(item.get("description", ""))
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Eligibility:** {item.get('eligibility','')}")
                if item.get("sectors"):
                    st.markdown(f"**Sectors:** {', '.join(item.get('sectors',[]))}")
            with col2:
                if item.get("allowance"):
                    st.markdown(f"**Allowance/Salary:** {item.get('allowance')}")
                if item.get("stipend"):
                    st.markdown(f"**Stipend:** {item.get('stipend')}")
                if item.get("salary_support"):
                    st.markdown(f"**Salary support:** {item.get('salary_support')}")
            _url_button(item.get("official_url",""))

    st.divider()
    st.markdown("### Why choose Earn & Learn?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Zero debt**\nCompany pays your salary during training — you graduate with earnings, not loans.")
    with col2:
        st.markdown("**Same qualification**\nYou receive the identical diploma, degree or cert as full-time graduates.")
    with col3:
        st.markdown("**Job-ready**\nStructured OJT means employers know your skills before you graduate.")


# ── Sidebar quick links ──────────────────────────────────────────────────────
with st.sidebar:
    st.divider()
    st.markdown("### Quick links")
    st.markdown("- [MySkillsFuture](https://www.myskillsfuture.gov.sg)")
    st.markdown("- [MOE ECG](https://www.moe.gov.sg/education-in-sg/our-programmes/education-and-career-guidance)")
    st.markdown("- [PSC Scholarships](https://www.psc.gov.sg/scholarships)")
    st.markdown("- [SkillsFuture Earn & Learn](https://www.skillsfuture.gov.sg/initiatives/mid-career/earningandlearning)")
    st.markdown("- [SOS Crisis Line: 1-767](https://www.sos.org.sg)")
    st.markdown("- [CHAT Youth Mental Health](https://www.chat.mentalhealth.sg)")

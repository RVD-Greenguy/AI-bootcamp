import streamlit as st
st.set_page_config(page_title="About Us — EduPath SG", page_icon="ℹ️", layout="wide")

from utils.session_manager import require_login
from components.sidebar import render_sidebar
from components.chat_panel import render_chat_panel
from components.stage_theme import apply_stage_theme

user = require_login()
render_sidebar()
apply_stage_theme()
_main = render_chat_panel()

with _main:
    st.title("ℹ️ About EduPath SG")
    st.markdown("*Singapore Education Journey Navigator*")

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("## Project Overview")
        st.markdown("""
    **EduPath SG** is a citizen-facing web application that helps parents, students and teachers
    navigate Singapore's education system — from early childhood through post-graduation.

    The application consolidates publicly available information from multiple official government
    sources into a single, interactive platform that personalises guidance based on user inputs
    such as PSLE AL scores, O-level grades, A-level results and polytechnic GPA.

    EduPath SG covers **all citizenship categories** — Singapore Citizens, Permanent Residents,
    and International Students — with distinct pathways, fee structures, admission exercises
    (AEIS/S-AEIS), visa requirements, and National Service timelines where applicable.
        """)

        st.markdown("## Objectives")
        st.markdown("""
    1. **Consolidate** pathway data from MOE, SEAB, ITE, polytechnics, universities, and international schools into one place
    2. **Personalise** guidance based on the user's current education stage, scores, citizenship, and interests
    3. **Explain** every government process interactively — from P1 registration ballot to JAE, DAE, AEIS, and SNUFA
    4. **Present** information across multiple formats: visual timelines, comparison tables, score calculators and AI-powered Q&A
    5. **Differentiate** pathways for Singapore Citizens, PRs, and International Students — including fees, eligibility, and NS obligations
        """)

        st.markdown("## Key Features")
        data = {
            "Feature": [
                "🗺️ Pathway Planner",
                "🎯 Score & School Matcher",
                "🔄 Fallback Guide",
                "🤖 AI Education Guide",
                "📚 RAG Knowledge Base",
                "🌏 PR & International Pathways",
                "🏫 International Schools",
            ],
            "Description": [
                "Interactive visual timeline of the full Singapore education journey with citizenship-specific notes",
                "Enter PSLE AL / L1R5 / rank points / poly GPA and get matched schools & programmes with eligibility indicators",
                "Official policies on retakes, private candidates, certificate implications, and alternative pathways",
                "Ask any question about Singapore education policy — answered using retrieved official references",
                "TF-IDF retrieval over 250+ chunks sourced from MOE, SEAB, ITE, polytechnic, university, and international school data",
                "AEIS/S-AEIS admission, fee tiers by citizenship, Student Pass requirements, NS timelines, Tuition Grant & bond info",
                "18 international schools with curricula (IB, IGCSE, AP), fee ranges, and university pathway conversion guides",
            ],
            "Users": ["All roles", "Student / Parent", "All roles", "All roles", "All roles", "PR / International", "International"],
        }
        import pandas as pd
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    with col2:
        st.markdown("## Target Users")
        st.info("👨‍👩‍👧 **Parents**\nPlanning a child's education journey, understanding registration processes, comparing school options")
        st.success("🎒 **Students**\nChecking score eligibility, understanding options at each transition, planning fallback routes")
        st.warning("👩‍🏫 **Teachers / Counsellors**\nAdvising students on pathways, understanding all branching options, explaining policies")

        st.markdown("## Domain")
        st.markdown("""
    **Primary Government Agency:** Ministry of Education Singapore (MOE)

    **Supporting Agencies:**
    - Singapore Examinations and Assessment Board (SEAB)
    - ITE Education Services
    - SkillsFuture Singapore
    - Immigration & Checkpoints Authority (ICA)
    - Autonomous Universities (NUS, NTU, SMU, SUTD, SIT, SUSS)

    **Coverage:**
    - Singapore Citizens, PRs, and International Students
    - Government schools, autonomous/independent schools, and international schools
    - Full Subject-Based Banding (FSBB) from 2024 cohort onwards
        """)

    st.divider()
    st.markdown("## Data Sources")
    sources = {
        "Source": [
            "MOE — Primary Education",
            "MOE — Secondary Education",
            "MOE — Post-Secondary",
            "MOE — P1 Registration",
            "MOE — International Students (AEIS)",
            "MOE — School Fees",
            "SEAB — Examinations",
            "SEAB — Private Candidates",
            "ITE Education Services",
            "Singapore Polytechnic",
            "Temasek Polytechnic",
            "Nanyang Polytechnic",
            "Ngee Ann Polytechnic",
            "Republic Polytechnic",
            "NUS Admissions",
            "NTU Admissions",
            "SMU Admissions",
            "SUTD Admissions",
            "SIT Admissions",
            "SUSS Admissions",
            "SkillsFuture Singapore",
            "ICA — Student Pass",
            "International Schools (18 schools)",
        ],
        "URL": [
            "https://www.moe.gov.sg/primary",
            "https://www.moe.gov.sg/secondary",
            "https://www.moe.gov.sg/post-secondary",
            "https://www.moe.gov.sg/primary/p1-registration",
            "https://www.moe.gov.sg/international-students/aeis",
            "https://www.moe.gov.sg/financial-matters/fees",
            "https://www.seab.gov.sg/home/examinations",
            "https://www.seab.gov.sg/home/examinations/private-candidates",
            "https://www.ite.edu.sg",
            "https://www.sp.edu.sg/sp/admission",
            "https://www.tp.edu.sg/admissions",
            "https://www.nyp.edu.sg/admissions",
            "https://www.np.edu.sg/admissions",
            "https://www.rp.edu.sg/admissions",
            "https://www.nus.edu.sg/oam",
            "https://www.ntu.edu.sg/admissions",
            "https://admissions.smu.edu.sg",
            "https://www.sutd.edu.sg/Admissions",
            "https://www.singaporetech.edu.sg/admissions",
            "https://www.suss.edu.sg/admissions",
            "https://www.skillsfuture.gov.sg",
            "https://www.ica.gov.sg/reside/STP",
            "Individual school websites",
        ],
        "Data Used": [
            "PSLE AL scoring, curriculum, gifted education",
            "School types, IP programme, FSBB, O-levels",
            "JAE process, JC/poly/ITE admission criteria",
            "Phase 1–3 ballot, citizenship priority, PR/international rules",
            "AEIS/S-AEIS test details, age requirements, placement process",
            "Fee tiers by citizenship (SC/PR/ASEAN/non-ASEAN), Tuition Grant",
            "O/N/A-level syllabi, grading, results schedule",
            "Private candidate registration, retake policies",
            "NITEC/Higher NITEC courses, college info",
            "Diploma courses, ELR2B2 cutoffs",
            "Diploma courses, ELR2B2 cutoffs",
            "Diploma courses, ELR2B2 cutoffs",
            "Diploma courses, ELR2B2 cutoffs",
            "Diploma courses, ELR2B2 cutoffs",
            "Undergraduate admission, rank points, DAE",
            "Undergraduate admission, rank points, DAE",
            "Undergraduate admission, rank points",
            "Undergraduate admission, rank points",
            "Undergraduate admission, GPA, DAE",
            "Undergraduate admission, DAE",
            "SkillsFuture Credit, CPP, courses",
            "Student Pass application, renewal, work restrictions",
            "IB/IGCSE/AP curricula, fee ranges, IB-to-uni conversion",
        ],
    }
    st.dataframe(pd.DataFrame(sources), use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("## Technology Stack")
    tech = {
        "Component": ["Web Framework", "RAG / Vector Search", "AI Chat (optional)", "Data Storage", "Visualisation", "Authentication"],
        "Technology": ["Streamlit 1.41", "TF-IDF (scikit-learn) + ChromaDB (optional)", "OpenAI GPT-4o (optional — local RAG mode when no API key)", "SQLite 3", "Plotly 5", "bcrypt + SQLite"],
        "Notes": [
            "Multi-page app with role-based routing and SGDS gov.sg styling",
            "254+ chunks from 14 seed files; upgrades to semantic search when OpenAI key provided",
            "Fully functional without API key; local mode returns structured RAG + web results",
            "Lightweight, file-based, no server required",
            "Interactive charts, timelines, comparison tables",
            "AI Champion accounts for quick access + self-registration",
        ],
    }
    st.dataframe(pd.DataFrame(tech), use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("## AI Champion Bootcamp")
    st.markdown("""
    EduPath SG is a capstone project developed as part of the **AI Champion Bootcamp**.
    It demonstrates the practical application of AI, RAG (Retrieval-Augmented Generation),
    and web technologies to solve a real civic problem — helping families navigate
    Singapore's complex education system.

    **AI Champion accounts** (parent@edupathsg.sg / student@edupathsg.sg) are provided
    for quick evaluation without requiring sign-up.
    """)

    st.markdown("""
    <div class="gov-footer">
    <a href="https://www.moe.gov.sg">MOE</a> ·
    <a href="https://www.seab.gov.sg">SEAB</a> ·
    <a href="https://www.ite.edu.sg">ITE</a> ·
    <a href="https://www.skillsfuture.gov.sg">SkillsFuture</a><br>
    <small>EduPath SG is an AI Champion Bootcamp capstone project. Not affiliated with the Singapore Government.</small>
    </div>
    """, unsafe_allow_html=True)

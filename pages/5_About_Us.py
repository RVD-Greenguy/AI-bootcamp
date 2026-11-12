import streamlit as st
st.set_page_config(page_title="About Us — EduPath SG", page_icon="ℹ️", layout="wide")

from utils.session_manager import require_login
from components.sidebar import render_sidebar

user = require_login()
render_sidebar()

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
    """)

    st.markdown("## Objectives")
    st.markdown("""
1. **Consolidate** pathway data from MOE, SEAB, ITE, polytechnics and universities into one place
2. **Personalise** guidance based on the user's current education stage, scores and interests
3. **Explain** every government process interactively — from P1 registration ballot to JAE, DAE and SNUFA
4. **Present** information across multiple formats: visual timelines, comparison tables, score calculators and AI-powered Q&A
    """)

    st.markdown("## Key Features")
    data = {
        "Feature": [
            "🗺️ Pathway Planner",
            "🎯 Score & School Matcher",
            "🔄 Fallback Guide",
            "🤖 AI Education Guide",
            "📚 RAG Knowledge Base",
        ],
        "Description": [
            "Interactive visual timeline of the full Singapore education journey from any starting stage",
            "Enter PSLE AL / L1R5 / rank points / poly GPA and get matched schools & programmes with eligibility indicators",
            "Official policies on retakes, private candidates, certificate implications, and alternative pathways",
            "Ask any question about Singapore education policy — answered using retrieved official references",
            "TF-IDF retrieval over 200+ chunks sourced from MOE, SEAB, ITE, polytechnic and university websites",
        ],
        "Users": ["All roles", "Student / Parent", "All roles", "All roles", "All roles"],
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
- Autonomous Universities (NUS, NTU, SMU, SUTD, SIT, SUSS)
    """)

st.divider()
st.markdown("## Data Sources")
sources = {
    "Source": [
        "MOE — Primary Education",
        "MOE — Secondary Education",
        "MOE — Post-Secondary",
        "MOE — P1 Registration",
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
    ],
    "URL": [
        "https://www.moe.gov.sg/primary",
        "https://www.moe.gov.sg/secondary",
        "https://www.moe.gov.sg/post-secondary",
        "https://www.moe.gov.sg/primary/p1-registration",
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
    ],
    "Data Used": [
        "PSLE AL scoring, curriculum, gifted education",
        "School types, IP programme, streaming, O-levels",
        "JAE process, JC/poly/ITE admission criteria",
        "Phase 1–3 ballot, citizenship priority",
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
    ],
}
st.dataframe(pd.DataFrame(sources), use_container_width=True, hide_index=True)

st.divider()
st.markdown("## Technology Stack")
tech = {
    "Component": ["Web Framework", "RAG / Vector Search", "AI Chat (optional)", "Data Storage", "Visualisation", "Authentication"],
    "Technology": ["Streamlit 1.41", "TF-IDF (scikit-learn) + ChromaDB (optional)", "OpenAI GPT-4o (optional — demo uses stub)", "SQLite 3", "Plotly 5", "bcrypt + SQLite"],
    "Notes": [
        "Multi-page app with role-based routing",
        "156+ chunks; upgrades to semantic search when OpenAI key provided",
        "Fully functional without API key; stub returns retrieved chunks",
        "Lightweight, file-based, no server required",
        "Interactive charts, timelines, comparison tables",
        "Hardcoded demo accounts + self-registration",
    ],
}
st.dataframe(pd.DataFrame(tech), use_container_width=True, hide_index=True)

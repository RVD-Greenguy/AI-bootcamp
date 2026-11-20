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
    6. **Cover part-time options** — work-study diplomas, SUSS/SIT/private part-time degrees, and SkillsFuture funding for career changers and working adults
        """)

        st.markdown("## Key Features")
        import pandas as pd
        data = {
            "Feature": [
                "🗺️ Pathway Planner",
                "🎯 Score & School Matcher",
                "🔄 Fallback Guide",
                "🎓 Part-Time Diplomas & Degrees",
                "🤖 AI Education Guide",
                "📚 RAG Knowledge Base",
                "🌏 PR & International Pathways",
                "🏫 International Schools",
            ],
            "Description": [
                "Interactive visual timeline with citizenship-specific notes, fees, and admission rules",
                "Enter PSLE AL / L1R5 / rank points / poly GPA — matched schools with fee comparison by citizenship",
                "Official policies on retakes, private candidates, certificate implications, and alternatives",
                "Poly/ITE work-study, SUSS/SIT/private part-time degrees, SkillsFuture funding, fee comparison",
                "Ask any question about SG education — answered using retrieved official references",
                "TF-IDF retrieval over 254+ chunks from MOE, SEAB, ITE, polytechnic, university, and intl school data",
                "AEIS/S-AEIS admission, fee tiers, Student Pass, NS timelines, Tuition Grant & bond info",
                "18 international schools with curricula (IB, IGCSE, AP), fee ranges, and uni pathway conversion",
            ],
            "SC": ["✅", "✅", "✅", "✅", "✅", "✅", "—", "—"],
            "PR": ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
            "International": ["✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"],
            "Login Roles": [
                "All roles",
                "Student / Parent",
                "All roles",
                "All roles",
                "All roles",
                "All roles",
                "All roles",
                "All roles",
            ],
        }
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

        st.markdown("## Fee Comparison by Citizenship")
        st.markdown("*Monthly fees for MOE government schools (2024). All amounts in SGD.*")
        fee_data = {
            "Education Level": [
                "Primary (P1–P6)",
                "Secondary (S1–S4/S5)",
                "Pre-University (JC / MI)",
                "Polytechnic (per year)",
                "ITE (per year)",
                "University (per year, before grants)",
            ],
            "🇸🇬 Singapore Citizen": [
                "$6.50/mth",
                "$5/mth",
                "$6/mth",
                "~$2,900/yr",
                "~$500/yr",
                "$8,000–$12,000/yr",
            ],
            "🟢 Permanent Resident": [
                "$230/mth",
                "$380/mth",
                "$380/mth",
                "~$5,100/yr",
                "~$3,600/yr",
                "$11,000–$16,500/yr",
            ],
            "🌏 International (ASEAN)": [
                "$490/mth",
                "$780/mth",
                "$940/mth",
                "~$10,200/yr",
                "~$7,700/yr",
                "With Tuition Grant + 3-yr bond",
            ],
            "🌐 International (non-ASEAN)": [
                "$825/mth",
                "$1,450/mth",
                "$1,750/mth",
                "~$10,200/yr",
                "~$7,700/yr",
                "Full fees: $30,000–$55,000/yr",
            ],
        }
        st.dataframe(pd.DataFrame(fee_data), use_container_width=True, hide_index=True)

        st.markdown("### Additional Financial Considerations")
        fin_data = {
            "Item": [
                "Edusave Account",
                "SkillsFuture Credit",
                "MOE Tuition Grant (University)",
                "Student Pass (ICA)",
                "International School Fees",
                "National Service (NS)",
            ],
            "SC": [
                "$290/yr (P1–S4) auto-deposited",
                "$500 credit at age 25",
                "No bond required",
                "Not applicable",
                "Not applicable",
                "2 yrs after sec/JC/poly",
            ],
            "PR": [
                "$290/yr (P1–S4) auto-deposited",
                "$500 credit at age 25",
                "No bond required",
                "Not applicable",
                "Can enrol (fees apply)",
                "2 yrs (male 2nd-gen PR)",
            ],
            "International": [
                "Not eligible",
                "Not eligible",
                "3-year work bond in SG",
                "SGD ~$450 application fee",
                "$20,000–$55,000/yr",
                "Not applicable",
            ],
        }
        st.dataframe(pd.DataFrame(fin_data), use_container_width=True, hide_index=True)

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
    - Part-time diplomas (poly/ITE work-study) and degrees (SUSS, SIT, private institutions)
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
            "SkillsFuture — Work-Study Programmes",
            "Private Institutions (SIM, Kaplan, PSB, MDIS)",
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
            "https://www.skillsfuture.gov.sg/initiatives/mid-career/workstudy",
            "Individual institution websites + CPE registry",
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
            "Poly/ITE work-study diplomas, SkillsFuture subsidies, programme details",
            "Part-time degree programmes, fees, entry requirements, partner universities",
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

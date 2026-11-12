import streamlit as st
st.set_page_config(page_title="Methodology — EduPath SG", page_icon="📖", layout="wide")

from utils.session_manager import require_login
from components.sidebar import render_sidebar
import plotly.graph_objects as go

user = require_login()
render_sidebar()

st.title("📖 Methodology")
st.markdown("*Data flows, implementation details, and process flowcharts for each use case.*")

tab_uc1, tab_uc2, tab_rag, tab_data = st.tabs([
    "🗺️ Use Case 1: Pathway Planner",
    "🎯 Use Case 2: Score Matcher",
    "🔍 RAG Pipeline",
    "🗄️ Data Architecture",
])

# ── USE CASE 1 ────────────────────────────────────────────────────────────────
with tab_uc1:
    st.markdown("## Use Case 1: Education Pathway Planner")
    st.markdown("""
The Pathway Planner takes a user's current education stage, citizenship status and interests,
then renders a personalised visual journey through every remaining stage of Singapore's education system.
At each fork (PSLE, JAE, post-secondary), it explains the government process and eligibility criteria.
    """)

    st.markdown("### Process Flowchart")

    # Build a Plotly flowchart using scatter + annotations
    steps = [
        (0.5, 9, "User inputs:\nCurrent stage\nCitizenship\nInterests", "#1565C0"),
        (0.5, 7.5, "pathway_service\n.get_pathway_for_profile()", "#1976D2"),
        (0.5, 6, "Load education_stages.json\nFilter from current stage", "#1976D2"),
        (0.5, 4.5, "Identify decision forks\n(PSLE, O-levels, A-levels)", "#0288D1"),
        (0.5, 3, "Render Plotly timeline\n(colour-coded nodes)", "#0097A7"),
        (0.5, 1.5, "Expandable stage cards\n(entry criteria, gov process, URL)", "#00796B"),
        (0.5, 0, "Display citizenship notes\n+ links to Score Matcher", "#2E7D32"),
    ]

    x = [s[0] for s in steps]
    y = [s[1] for s in steps]
    labels = [s[2] for s in steps]
    colours = [s[3] for s in steps]

    fig1 = go.Figure()
    # Connecting lines
    fig1.add_trace(go.Scatter(
        x=x, y=y, mode="lines",
        line=dict(color="#90A4AE", width=2),
        showlegend=False,
    ))
    # Nodes
    fig1.add_trace(go.Scatter(
        x=x, y=y, mode="markers+text",
        marker=dict(size=40, color=colours, symbol="square"),
        text=labels,
        textposition="middle center",
        textfont=dict(color="white", size=10),
        showlegend=False,
    ))
    fig1.update_layout(
        height=600,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### Key Decision Points in the Pathway")
    st.markdown("""
| Fork | Exam | Timing | Key Metric | Outcome |
|------|------|--------|-----------|---------|
| Primary → Secondary | PSLE | Nov (Sec 1 posting Dec) | Total AL (4–32) | Express / NA / NT / IP |
| Secondary → Post-Sec | O-levels or IP internal | Nov (JAE Jan) | L1R5 / ELR2B2 | JC / Poly / ITE |
| Post-Sec → University | A-levels or Poly GPA | Nov/Mar (SNUFA/DAE) | Rank pts / GPA | Local / Overseas / Work |
| University → Post-Grad | Degree results | Varies | CGPA / research | Masters / PhD / SkillsFuture |
    """)

# ── USE CASE 2 ────────────────────────────────────────────────────────────────
with tab_uc2:
    st.markdown("## Use Case 2: Score & School Matcher")
    st.markdown("""
The Score Matcher takes a student's actual or projected exam results and returns a ranked list
of schools and programmes they qualify for, with eligibility indicators and comparison visualisations.
Covers four transition stages: PSLE → Sec, O-levels → JAE, A-levels → University, Poly GPA → DAE.
    """)

    st.markdown("### Process Flowchart")

    stages_uc2 = [
        (0.2, 6, "Student enters\nexam scores", "#1565C0"),
        (0.2, 4.5, "Select transition:\nPSLE / O-lvl / A-lvl / Poly", "#1976D2"),
        (0.8, 6, "Score calculator\n(L1R5 / ELR2B2 / Rank pts)", "#0288D1"),
        (0.8, 4.5, "Bonus points\n(CCA / affiliation)", "#0288D1"),
        (0.5, 3, "score_service\nmatch function", "#0097A7"),
        (0.5, 1.5, "Filter schools/courses\nfrom seed data JSON", "#00796B"),
        (0.5, 0, "Plotly bar chart +\ncomparison table + fit label", "#2E7D32"),
    ]

    x2 = [s[0] for s in stages_uc2]
    y2 = [s[1] for s in stages_uc2]
    labels2 = [s[2] for s in stages_uc2]
    colours2 = [s[3] for s in stages_uc2]

    fig2 = go.Figure()
    # Connect input boxes to calculator
    fig2.add_trace(go.Scatter(
        x=[0.2, 0.2, 0.5, 0.8, 0.8, 0.5],
        y=[6, 4.5, 3, 4.5, 6, 3],
        mode="lines",
        line=dict(color="#90A4AE", width=2),
        showlegend=False,
    ))
    fig2.add_trace(go.Scatter(
        x=[0.5, 0.5],
        y=[3, 0],
        mode="lines",
        line=dict(color="#90A4AE", width=2),
        showlegend=False,
    ))
    fig2.add_trace(go.Scatter(
        x=x2, y=y2, mode="markers+text",
        marker=dict(size=38, color=colours2, symbol="square"),
        text=labels2,
        textposition="middle center",
        textfont=dict(color="white", size=9),
        showlegend=False,
    ))
    fig2.update_layout(
        height=500,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Score Calculation Formulas")
    st.markdown("""
**PSLE (since 2021):**
> Total AL = AL(English) + AL(Mother Tongue) + AL(Mathematics) + AL(Science or Humanities)
> Scale: AL1 (best) → AL8 (weakest) per subject. Total range: 4 (best) → 32 (weakest)

**L1R5 for JC (JAE):**
> Raw L1R5 = English grade + best 5 relevant subjects (must include ≥1 humanities + ≥1 math/science)
> Net L1R5 = Raw L1R5 − CCA bonus (0–2) − Affiliation bonus (0–2). Minimum net = 2.
> Grade points: A1=1, A2=2, B3=3, B4=4, C5=5, C6=6, D7=7, E8=8, F9=9

**A-level University Admission Score (UAS):**
> UAS = H1 GP + H2 subject 1 + H2 subject 2 + H2 subject 3 + H1 MTL (capped at 10)
> H2 grade points: A=20, B=17.5, C=15, D=12.5, E=10, S/U=0
> H1 grade points: A=10, B=8.75, C=7.5, D=6.25, E=5, S/U=0. Maximum UAS = 90.
    """)

# ── RAG PIPELINE ─────────────────────────────────────────────────────────────
with tab_rag:
    st.markdown("## RAG Pipeline")
    st.markdown("""
EduPath SG uses a **two-tier Retrieval-Augmented Generation** pipeline:

**Tier 1 (always active — no API key needed):**
TF-IDF vectorisation using scikit-learn over 200+ curriculum chunks sourced from official
Singapore government websites. Retrieval uses cosine similarity. Works fully offline.

**Tier 2 (optional — requires OpenAI API key):**
ChromaDB vector store with OpenAI `text-embedding-3-small` embeddings for richer semantic retrieval.
Automatically activated when `USE_AI=true` and `OPENAI_API_KEY` is set in `.env`.
    """)

    st.markdown("### RAG Data Flow")
    st.code("""
User question
     │
     ▼
retrieve_chunks(query, n_results=4)
     │
     ├─── [USE_AI=false] TF-IDF cosine similarity over tfidf_store.pkl
     │         → returns top-k chunks with score, source, URL
     │
     └─── [USE_AI=true]  OpenAI text-embedding-3-small
                → ChromaDB cosine similarity search
                → returns top-k chunks with metadata

Retrieved chunks
     │
     ├─── Displayed in "📚 Sources Retrieved" expander (always shown)
     │
     └─── Passed to ask_guide(question, chunks, history)
               │
               ├─ [USE_AI=false] Returns stub with chunk summaries
               └─ [USE_AI=true]  GPT-4o with system prompt + context
    """, language="text")

    st.markdown("### Knowledge Base Coverage")
    kb_data = {
        "Source Type": ["Education stages", "Secondary schools", "JC data", "Poly courses", "ITE courses", "University faculties", "Fallback policies", "Static knowledge chunks"],
        "Chunks": ["8", "28", "12", "50", "12", "30", "10", "14"],
        "Source": ["MOE", "MOE school-info", "MOE JAE", "5 polytechnics", "ITE Education Services", "6 AUs", "MOE / SEAB", "Curated from official sources"],
    }
    import pandas as pd
    st.dataframe(pd.DataFrame(kb_data), use_container_width=True, hide_index=True)

# ── DATA ARCHITECTURE ────────────────────────────────────────────────────────
with tab_data:
    st.markdown("## Data Architecture")
    st.markdown("""
EduPath SG uses two data stores:

**1. SQLite (edupathsg.sqlite)**
- `users` table: bcrypt-hashed credentials, role
- `chat_sessions` table: persistent Q&A history

**2. JSON Seed Files (data/seed/)**
- Loaded at startup by pathway_service.py and score_service.py
- Cached in memory using `functools.lru_cache`
- No database writes needed for education data

**3. TF-IDF Store (storage/tfidf_store.pkl)**
- Pre-built by `scripts/build_vector_index.py`
- Loaded once per process and held in memory
- Rebuilt automatically on first query if missing
    """)

    st.markdown("### File Structure")
    st.code("""
edupathsg/
├── app.py                      # Login + role router
├── pages/
│   ├── 1_Pathway_Planner.py    # Use Case 1
│   ├── 2_Score_Matcher.py      # Use Case 2
│   ├── 3_Fallback_Guide.py     # Retake policies
│   ├── 4_AI_Guide.py           # RAG-powered chat
│   ├── 5_About_Us.py           # This project
│   └── 6_Methodology.py        # This page
├── services/
│   ├── db.py                   # SQLite helpers
│   ├── auth_service.py         # Login / register
│   ├── pathway_service.py      # Stage + fork data
│   ├── score_service.py        # L1R5 / rank pts calculators
│   ├── rag_service.py          # TF-IDF + ChromaDB RAG
│   └── llm_service.py          # OpenAI stub / live
├── data/seed/
│   ├── education_stages.json
│   ├── secondary_schools.json
│   ├── jc_data.json
│   ├── poly_courses.json
│   ├── ite_data.json
│   ├── university_data.json
│   └── fallback_policies.json
├── storage/
│   ├── edupathsg.sqlite
│   └── tfidf_store.pkl
└── scripts/
    ├── init_db.py
    └── build_vector_index.py
    """, language="text")

import streamlit as st

st.set_page_config(page_title="Methodology — EduPath SG", page_icon="📖", layout="wide")

from utils.session_manager import require_login
from components.sidebar import render_sidebar
from components.chat_panel import render_chat_panel

user = require_login()
render_sidebar()
render_chat_panel()

st.title("📖 Methodology")
st.markdown("*Data flows, implementation details, and process flowcharts for each use case.*")

tab_uc1, tab_uc2, tab_rag, tab_data = st.tabs([
    "🗺️ Use Case 1: Pathway Navigator",
    "🎯 Use Case 2: Score Matcher",
    "🔍 RAG Pipeline",
    "🗄️ Data Architecture",
])

# ── USE CASE 1 ────────────────────────────────────────────────────────────────
with tab_uc1:
    st.markdown("## Use Case 1: Education Pathway Navigator")
    st.markdown("""
The Pathway Navigator takes a user's current education stage, citizenship status and interests,
then renders a personalised visual roadmap through every remaining stage of Singapore's education system.
At each fork (PSLE, JAE, post-secondary), it explains the government process and eligibility criteria.
    """)

    st.markdown("### Process Flowchart")

    uc1_html = """
<style>
  .fc-wrap {
    background: #0f172a;
    padding: 32px 24px;
    border-radius: 12px;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 700px;
  }
  .fc-node {
    border-radius: 8px;
    padding: 12px 20px;
    width: 320px;
    text-align: center;
  }
  .fc-title { font-size: 13px; font-weight: 600; color: #e2e8f0; margin: 0 0 4px 0; }
  .fc-sub   { font-size: 11px; margin: 0; }
  .fc-arrow { color: #334155; font-size: 22px; line-height: 1; margin: 6px 0; }
  .fc-step  { font-size: 10px; font-weight: 700; text-transform: uppercase;
              letter-spacing: 1.5px; margin-bottom: 4px; }
</style>

<div class="fc-wrap">

  <!-- Step 1: User Input -->
  <div class="fc-node" style="background:#172554;border:2px solid #3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,0.2);">
    <p class="fc-step" style="color:#93c5fd;">Step 1</p>
    <p class="fc-title">👤 User Inputs</p>
    <p class="fc-sub" style="color:#93c5fd;">Current stage · Citizenship · Age · Interests</p>
  </div>

  <div class="fc-arrow">↓</div>

  <!-- Step 2: Service call -->
  <div class="fc-node" style="background:#1e1b4b;border:1.5px solid #6366f1;">
    <p class="fc-step" style="color:#a5b4fc;">Step 2</p>
    <p class="fc-title">⚙️ pathway_service</p>
    <p class="fc-sub" style="color:#a5b4fc;">get_pathway_for_profile(stage, interests, citizenship)</p>
  </div>

  <div class="fc-arrow">↓</div>

  <!-- Step 3: Data load -->
  <div class="fc-node" style="background:#1e1b4b;border:1.5px solid #6366f1;">
    <p class="fc-step" style="color:#a5b4fc;">Step 3</p>
    <p class="fc-title">📂 Load education_stages.json</p>
    <p class="fc-sub" style="color:#a5b4fc;">Filter stages from current position · lru_cache</p>
  </div>

  <div class="fc-arrow">↓</div>

  <!-- Step 4: Fork detection -->
  <div class="fc-node" style="background:#083344;border:1.5px solid #06b6d4;">
    <p class="fc-step" style="color:#67e8f9;">Step 4</p>
    <p class="fc-title">🔀 Identify Decision Forks</p>
    <p class="fc-sub" style="color:#67e8f9;">PSLE · O-levels / JAE · A-levels / DAE</p>
  </div>

  <div class="fc-arrow">↓</div>

  <!-- Step 5: Render roadmap -->
  <div class="fc-node" style="background:#022c22;border:1.5px solid #10b981;">
    <p class="fc-step" style="color:#6ee7b7;">Step 5</p>
    <p class="fc-title">🗺️ Render Roadmap HTML</p>
    <p class="fc-sub" style="color:#6ee7b7;">roadmap.sh-style nodes · track color-coding · current stage glow</p>
  </div>

  <div class="fc-arrow">↓</div>

  <!-- Step 6: Stage cards -->
  <div class="fc-node" style="background:#022c22;border:1.5px solid #10b981;">
    <p class="fc-step" style="color:#6ee7b7;">Step 6</p>
    <p class="fc-title">📋 Expandable Stage Cards</p>
    <p class="fc-sub" style="color:#6ee7b7;">Entry criteria · Governing body · Official URL · Key facts</p>
  </div>

  <div class="fc-arrow">↓</div>

  <!-- Step 7: Output -->
  <div class="fc-node" style="background:#052e16;border:1.5px solid #22c55e;">
    <p class="fc-step" style="color:#86efac;">Step 7</p>
    <p class="fc-title">✅ Citizenship Notes + Next Steps</p>
    <p class="fc-sub" style="color:#86efac;">Registration priority · Subsidies · Link to Score Matcher</p>
  </div>

</div>
"""
    st.html(uc1_html)

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

    uc2_html = """
<style>
  .fc2-wrap {
    background: #0f172a;
    padding: 32px 24px;
    border-radius: 12px;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 750px;
  }
  .fc2-node {
    border-radius: 8px;
    padding: 11px 16px;
    text-align: center;
  }
  .fc2-title { font-size: 13px; font-weight: 600; color: #e2e8f0; margin: 0 0 3px 0; }
  .fc2-sub   { font-size: 11px; margin: 0; }
  .fc2-arrow { color: #334155; font-size: 20px; line-height: 1; margin: 5px 0; }
  .fc2-step  { font-size: 10px; font-weight: 700; text-transform: uppercase;
               letter-spacing: 1.5px; margin-bottom: 3px; }
  .fc2-split { display: flex; gap: 16px; width: 100%; max-width: 640px; justify-content: center; }
  .fc2-col   { flex: 1; display: flex; flex-direction: column; align-items: center; min-width: 200px; }
  .fc2-col .fc2-node { width: 100%; }
  .fc2-hline { width: 100%; max-width: 640px; height: 1px; background: #334155; }
  .fc2-single { width: 320px; }
</style>

<div class="fc2-wrap">

  <!-- Top split -->
  <div class="fc2-hline"></div>
  <div class="fc2-split">

    <div class="fc2-col">
      <div class="fc2-arrow">↓</div>
      <div class="fc2-node" style="background:#172554;border:2px solid #3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,0.2);">
        <p class="fc2-step" style="color:#93c5fd;">Input A</p>
        <p class="fc2-title">👤 Student Enters Scores</p>
        <p class="fc2-sub" style="color:#93c5fd;">Raw subject grades · PSLE AL values</p>
      </div>
      <div class="fc2-arrow">↓</div>
      <div class="fc2-node" style="background:#172554;border:1.5px solid #3b82f6;">
        <p class="fc2-step" style="color:#93c5fd;">Input B</p>
        <p class="fc2-title">🔀 Select Transition</p>
        <p class="fc2-sub" style="color:#93c5fd;">PSLE → Sec · O-lvl → JC/Poly · A-lvl → Uni · Poly → DAE</p>
      </div>
    </div>

    <div class="fc2-col">
      <div class="fc2-arrow">↓</div>
      <div class="fc2-node" style="background:#083344;border:2px solid #06b6d4;">
        <p class="fc2-step" style="color:#67e8f9;">Process A</p>
        <p class="fc2-title">🧮 Score Calculator</p>
        <p class="fc2-sub" style="color:#67e8f9;">L1R5 · ELR2B2 · A-lvl Rank Points · Poly GPA</p>
      </div>
      <div class="fc2-arrow">↓</div>
      <div class="fc2-node" style="background:#083344;border:1.5px solid #06b6d4;">
        <p class="fc2-step" style="color:#67e8f9;">Process B</p>
        <p class="fc2-title">➕ Bonus Points</p>
        <p class="fc2-sub" style="color:#67e8f9;">CCA bonus (0–2) · Affiliation bonus (0–2)</p>
      </div>
    </div>

  </div>
  <div class="fc2-hline"></div>

  <div class="fc2-arrow">↓</div>

  <!-- Converge -->
  <div class="fc2-single">
    <div class="fc2-node" style="background:#1e1b4b;border:2px solid #8b5cf6;box-shadow:0 0 0 3px rgba(139,92,246,0.2);">
      <p class="fc2-step" style="color:#c4b5fd;">Core</p>
      <p class="fc2-title">⚙️ score_service match function</p>
      <p class="fc2-sub" style="color:#c4b5fd;">match_secondary_schools · match_jcs · match_poly_courses · match_universities</p>
    </div>
  </div>

  <div class="fc2-arrow">↓</div>

  <div class="fc2-single">
    <div class="fc2-node" style="background:#022c22;border:1.5px solid #10b981;">
      <p class="fc2-step" style="color:#6ee7b7;">Data</p>
      <p class="fc2-title">📂 Filter from Seed JSON</p>
      <p class="fc2-sub" style="color:#6ee7b7;">secondary_schools · jc_data · poly_courses · university_data</p>
    </div>
  </div>

  <div class="fc2-arrow">↓</div>

  <div class="fc2-single">
    <div class="fc2-node" style="background:#052e16;border:1.5px solid #22c55e;">
      <p class="fc2-step" style="color:#86efac;">Output</p>
      <p class="fc2-title">📊 Ranked Results</p>
      <p class="fc2-sub" style="color:#86efac;">Plotly bar chart · Comparison table · Fit labels (Eligible / Borderline)</p>
    </div>
  </div>

</div>
"""
    st.html(uc2_html)

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
TF-IDF vectorisation using scikit-learn over 147 chunks sourced from official
Singapore government websites. Retrieval uses cosine similarity. Works fully offline.

**Tier 2 (optional — requires OpenAI API key):**
ChromaDB vector store with OpenAI `text-embedding-3-small` embeddings for richer semantic retrieval.
Automatically activated when `USE_AI=true` and `OPENAI_API_KEY` is set in Streamlit Secrets.
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
    import pandas as pd
    kb_data = {
        "Source Type": [
            "Education stages", "Secondary schools", "JC data", "Poly courses",
            "ITE courses", "University faculties", "Fallback policies",
            "Support resources", "Static knowledge chunks"
        ],
        "Chunks": ["8", "28", "12", "50", "12", "30", "10", "35", "14"],
        "Source": [
            "MOE", "MOE school-info", "MOE JAE", "5 polytechnics",
            "ITE Education Services", "6 AUs", "MOE / SEAB",
            "MOE / PSC / SkillsFuture / WSG", "Curated from official sources"
        ],
    }
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
├── app.py                      # Login + role router + auto-bootstrap
├── pages/
│   ├── 1_Pathway_Planner.py    # Use Case 1 — roadmap.sh-style visualisation
│   ├── 2_Score_Matcher.py      # Use Case 2 — score calculators + school matching
│   ├── 3_Fallback_Guide.py     # Retake policies + private candidate guide
│   ├── 4_AI_Guide.py           # RAG-powered Q&A (GPT-4o + TF-IDF)
│   ├── 5_About_Us.py           # Project scope + 19 official data sources
│   ├── 6_Methodology.py        # This page
│   └── 7_Support_Hub.py        # Counselling, scholarships, Earn & Learn
├── services/
│   ├── db.py                   # SQLite helpers
│   ├── auth_service.py         # Login / register (bcrypt)
│   ├── pathway_service.py      # Stage + fork + support resource data
│   ├── score_service.py        # L1R5 / ELR2B2 / rank pts calculators
│   ├── rag_service.py          # TF-IDF + ChromaDB RAG
│   └── llm_service.py          # OpenAI GPT-4o stub / live
├── data/seed/
│   ├── education_stages.json
│   ├── secondary_schools.json
│   ├── jc_data.json
│   ├── poly_courses.json
│   ├── ite_data.json
│   ├── university_data.json
│   ├── fallback_policies.json
│   └── support_resources.json
├── storage/
│   ├── edupathsg.sqlite
│   └── tfidf_store.pkl
└── scripts/
    ├── init_db.py
    └── build_vector_index.py
    """, language="text")

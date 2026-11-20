import streamlit as st

st.set_page_config(page_title="Methodology — EduPath SG", page_icon="📖", layout="wide")

from utils.session_manager import require_login
from components.sidebar import render_sidebar
from components.chat_panel import render_chat_panel
from components.stage_theme import apply_stage_theme

user = require_login()
render_sidebar()
apply_stage_theme()
_main = render_chat_panel()

with _main:
    st.title("📖 Methodology")
    st.markdown("*Data flows, implementation details, and process flowcharts for each use case.*")

    tab_uc1, tab_uc2, tab_rag, tab_data = st.tabs([
        "🗺️ UC1: Pathway Navigator",
        "🎯 UC2: AI Q&A Guide",
        "🔍 RAG + Web Search Pipeline",
        "🗄️ Data Architecture",
    ])

    # ── USE CASE 1: PATHWAY NAVIGATOR + CAREER GOAL FLOW ────────────────────────
    with tab_uc1:
        st.markdown("## Use Case 1: Education Pathway Navigator + Career Goal Flow")
        st.markdown("""
    The Pathway Navigator takes a user's **role** (parent/student), **education stage**,
    **citizenship**, and optionally a **career aspiration** — then renders a personalised
    visual roadmap through Singapore's education system. When a career goal is set, the
    **reverse pathway engine** traces backward from the target university programme to show
    the required scores at every stage.

    Citizenship-specific guidance covers:
    - **Singapore Citizens:** P1 priority, subsidised fees, SkillsFuture, Edusave
    - **Permanent Residents:** Phase 2C registration, PR fee tier, NS obligations, Tuition Grant without bond
    - **International Students:** AEIS/S-AEIS entry, Student Pass requirements, international school alternatives, fee tiers, Tuition Grant with 3-year bond
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
        gap: 2px;
      }
      .fc-node {
        border-radius: 8px;
        padding: 12px 20px;
        width: 380px;
        text-align: center;
      }
      .fc-title { font-size: 13px; font-weight: 600; color: #e2e8f0; margin: 0 0 4px 0; }
      .fc-sub   { font-size: 11px; margin: 0; }
      .fc-arrow { color: #475569; font-size: 20px; line-height: 1; margin: 4px 0; }
      .fc-step  { font-size: 10px; font-weight: 700; text-transform: uppercase;
                  letter-spacing: 1.5px; margin-bottom: 4px; }
      .fc-split { display: flex; gap: 16px; width: 100%; max-width: 780px; justify-content: center; }
      .fc-col   { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 2px; }
      .fc-col .fc-node { width: 100%; }
    </style>

    <div class="fc-wrap">

      <div class="fc-node" style="background:#172554;border:2px solid #3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,0.2);">
        <p class="fc-step" style="color:#93c5fd;">Step 1 — Inputs</p>
        <p class="fc-title">👤 User Profile + Career Goal</p>
        <p class="fc-sub" style="color:#93c5fd;">Role (parent/student) · Education stage · Citizenship (SC/PR/International) · Career aspiration (optional)</p>
      </div>

      <div class="fc-arrow">↓</div>

      <div class="fc-node" style="background:#1e1b4b;border:1.5px solid #6366f1;">
        <p class="fc-step" style="color:#a5b4fc;">Step 2 — Role & Citizenship Context</p>
        <p class="fc-title">🎭 role_context + citizenship_notes</p>
        <p class="fc-sub" style="color:#a5b4fc;">Personalise language + load citizenship-specific fees, admission rules, NS info</p>
      </div>

      <div class="fc-arrow">↓</div>

      <!-- Split: pathway vs career -->
      <div class="fc-split">

        <div class="fc-col">
          <div class="fc-node" style="background:#1e1b4b;border:1.5px solid #6366f1;">
            <p class="fc-step" style="color:#a5b4fc;">Step 3A — Pathway</p>
            <p class="fc-title">📂 pathway_service</p>
            <p class="fc-sub" style="color:#a5b4fc;">Load education_stages.json + pr_international_pathways.json<br>Filter from current stage · Identify forks · FSBB info</p>
          </div>
          <div class="fc-arrow">↓</div>
          <div class="fc-node" style="background:#022c22;border:1.5px solid #10b981;">
            <p class="fc-step" style="color:#6ee7b7;">Step 4A — Roadmap</p>
            <p class="fc-title">🗺️ Render HTML Roadmap</p>
            <p class="fc-sub" style="color:#6ee7b7;">4 PSLE streams · 3 post-sec paths · Current stage glow<br>Citizenship-specific notes (fees, AEIS, NS, Student Pass)</p>
          </div>
        </div>

        <div class="fc-col">
          <div class="fc-node" style="background:#3b0764;border:1.5px solid #a855f7;">
            <p class="fc-step" style="color:#d8b4fe;">Step 3B — Career (if set)</p>
            <p class="fc-title">⚖️ career_service.trace_career_pathway()</p>
            <p class="fc-sub" style="color:#d8b4fe;">Reverse-lookup: career → university targets<br>→ JC/Poly/ITE routes with scores at each step</p>
          </div>
          <div class="fc-arrow">↓</div>
          <div class="fc-node" style="background:#1c1917;border:1.5px solid #f59e0b;">
            <p class="fc-step" style="color:#fcd34d;">Step 4B — 3-Column Viz</p>
            <p class="fc-title">📊 Career Pathway Visualization</p>
            <p class="fc-sub" style="color:#fcd34d;">JC Route (★ shortest) | Poly Route | ITE Route<br>Score targets at every transition</p>
          </div>
        </div>

      </div>

      <div class="fc-arrow">↓</div>

      <div class="fc-node" style="background:#052e16;border:2px solid #22c55e;box-shadow:0 0 0 3px rgba(34,197,94,0.2);">
        <p class="fc-step" style="color:#86efac;">Step 5 — Output</p>
        <p class="fc-title">✅ Personalised Pathway + Citizenship Notes</p>
        <p class="fc-sub" style="color:#86efac;">Entry criteria · Fees by citizenship · AEIS/NS/Student Pass info<br>Primary school guide (if stage = primary) · Score Matcher link</p>
      </div>

    </div>
    """
        st.html(uc1_html)

        st.markdown("### Key Decision Points")
        st.markdown("""
    | Fork | Exam | Timing | Key Metric | Outcome |
    |------|------|--------|-----------|---------|
    | Primary → Secondary | PSLE | Nov (posting Dec) | Total AL (4–32) | Express / NA / NT / IP (FSBB: Posting Groups 1–3 from 2024) |
    | Secondary → Post-Sec | O-levels | Nov (JAE Jan) | L1R5 / ELR2B2 | JC / Poly / ITE |
    | Post-Sec → University | A-levels or Poly GPA | Nov/Mar | UAS / GPA | Local uni / Overseas / Work |
    | International Entry | AEIS / S-AEIS | Sep / Feb | English + Maths test | Government school placement (P2–P5, S1–S3) |
        """)

        st.markdown("### Career Reverse Tracing Data Flow")
        st.code("""
    User selects career (e.g. "Lawyer")
         │
         ▼
    career_service.lookup_career("Lawyer")
         │  → Loads career_pathways.json (15 careers)
         │  → Matches by name or alias
         ▼
    career_service.trace_career_pathway("Lawyer")
         │
         ├─ Cross-reference university_data.json
         │    → NUS Law: min RP 84, min GPA 3.9
         │    → SMU Law: min RP 83, min GPA 3.9
         │
         ├─ Cross-reference poly_courses.json
         │    → NP Diploma in Law & Management: ELR2B2 ~13
         │
         ├─ Cross-reference ite_data.json
         │    → No direct ITE-to-law pathway
         │
         └─ Build total_paths[]
              ├─ JC Route: PSLE→Express→O-levels(L1R5≤7)→JC→A-levels(UAS 84+)→Uni  ~10yr
              ├─ Poly Route: PSLE→Express→O-levels(ELR2B2≤13)→Poly(GPA 3.9+)→DAE  ~11yr
              └─ ITE Route: N-levels→ITE→Poly→DAE  ~14yr
        """, language="text")


    # ── USE CASE 2: AI Q&A GUIDE ────────────────────────────────────────────────
    with tab_uc2:
        st.markdown("## Use Case 2: AI Education Q&A Guide")
        st.markdown("""
    The AI Guide answers questions about Singapore's education system using a
    **three-source pipeline**: local RAG knowledge base (TF-IDF), live web search
    from trusted `.gov.sg` / `.edu.sg` sites (DuckDuckGo), and GPT-4o-mini for
    natural language synthesis. Includes security guardrails for input validation
    and domain restriction.

    The knowledge base covers **all citizenship categories** — SC, PR, and International
    Students — including AEIS/S-AEIS admission, fee structures, Student Pass requirements,
    National Service timelines, 18 international schools, and IB-to-university score conversion.
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
        gap: 2px;
      }
      .fc2-node {
        border-radius: 8px;
        padding: 11px 16px;
        text-align: center;
      }
      .fc2-title { font-size: 13px; font-weight: 600; color: #e2e8f0; margin: 0 0 3px 0; }
      .fc2-sub   { font-size: 11px; margin: 0; }
      .fc2-arrow { color: #475569; font-size: 20px; line-height: 1; margin: 4px 0; }
      .fc2-step  { font-size: 10px; font-weight: 700; text-transform: uppercase;
                   letter-spacing: 1.5px; margin-bottom: 3px; }
      .fc2-split { display: flex; gap: 16px; width: 100%; max-width: 820px; justify-content: center; }
      .fc2-col   { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 2px; }
      .fc2-col .fc2-node { width: 100%; }
      .fc2-single { width: 400px; }
      .fc2-guard { background: #7f1d1d; border: 2px solid #ef4444; }
    </style>

    <div class="fc2-wrap">

      <!-- Input -->
      <div class="fc2-single">
        <div class="fc2-node" style="background:#172554;border:2px solid #3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,0.2);">
          <p class="fc2-step" style="color:#93c5fd;">Step 1 — User Input</p>
          <p class="fc2-title">💬 User Question (right-side chat panel)</p>
          <p class="fc2-sub" style="color:#93c5fd;">Persistent across all pages · Session history stored in SQLite</p>
        </div>
      </div>

      <div class="fc2-arrow">↓</div>

      <!-- Security guardrail -->
      <div class="fc2-single">
        <div class="fc2-node fc2-guard">
          <p class="fc2-step" style="color:#fca5a5;">Step 2 — Security Guardrails</p>
          <p class="fc2-title">🛡️ validate_question()</p>
          <p class="fc2-sub" style="color:#fca5a5;">Block: SQL injection · XSS · prompt injection · inappropriate content<br>Verify: education-related keywords present · length limits (3–500 chars)</p>
        </div>
      </div>

      <div class="fc2-arrow">↓</div>

      <!-- Split: RAG + Web -->
      <div class="fc2-split">

        <div class="fc2-col">
          <div class="fc2-node" style="background:#083344;border:1.5px solid #06b6d4;">
            <p class="fc2-step" style="color:#67e8f9;">Step 3A — Local RAG</p>
            <p class="fc2-title">📂 rag_service.retrieve_chunks()</p>
            <p class="fc2-sub" style="color:#67e8f9;">TF-IDF cosine similarity over 261 chunks<br>14 seed JSON files from MOE/SEAB/ITE/Polys/Unis/Intl Schools</p>
          </div>
        </div>

        <div class="fc2-col">
          <div class="fc2-node" style="background:#1c1917;border:1.5px solid #f59e0b;">
            <p class="fc2-step" style="color:#fcd34d;">Step 3B — Web Search</p>
            <p class="fc2-title">🌐 web_search_service.search_web()</p>
            <p class="fc2-sub" style="color:#fcd34d;">DuckDuckGo → domain allowlist filter<br>Only .gov.sg + .edu.sg results pass through</p>
          </div>
        </div>

      </div>

      <div class="fc2-arrow">↓</div>

      <!-- Context injection -->
      <div class="fc2-single">
        <div class="fc2-node" style="background:#1e1b4b;border:1.5px solid #8b5cf6;">
          <p class="fc2-step" style="color:#c4b5fd;">Step 4 — Context Assembly</p>
          <p class="fc2-title">📋 Build LLM Messages</p>
          <p class="fc2-sub" style="color:#c4b5fd;">System prompt + Role context (parent/student) + Stage context<br>+ Career context (if set) + RAG chunks + Web results + Chat history (last 8)</p>
        </div>
      </div>

      <div class="fc2-arrow">↓</div>

      <!-- LLM -->
      <div class="fc2-single">
        <div class="fc2-node" style="background:#3b0764;border:2px solid #a855f7;box-shadow:0 0 0 3px rgba(168,85,247,0.2);">
          <p class="fc2-step" style="color:#d8b4fe;">Step 5 — LLM</p>
          <p class="fc2-title">🤖 GPT-4o-mini (or Local RAG Mode)</p>
          <p class="fc2-sub" style="color:#d8b4fe;">Temperature 0.3 · max_tokens 1000 · Cites official URLs<br>Local mode: returns structured RAG context + web links without LLM</p>
        </div>
      </div>

      <div class="fc2-arrow">↓</div>

      <!-- Output -->
      <div class="fc2-single">
        <div class="fc2-node" style="background:#052e16;border:2px solid #22c55e;box-shadow:0 0 0 3px rgba(34,197,94,0.2);">
          <p class="fc2-step" style="color:#86efac;">Step 6 — Output</p>
          <p class="fc2-title">✅ Answer with Source Citations</p>
          <p class="fc2-sub" style="color:#86efac;">Styled response in right panel · Official URLs cited<br>Saved to chat_sessions (SQLite) · Persists across pages</p>
        </div>
      </div>

    </div>
    """
        st.html(uc2_html)

        st.markdown("### Security Guardrails")
        st.markdown("""
    | Layer | Protection | Implementation |
    |-------|-----------|----------------|
    | **Input validation** | Block SQL injection, XSS, prompt injection | Regex patterns in `validate_question()` |
    | **Topic enforcement** | Only education-related queries proceed to web search | Education keyword allowlist (60+ terms) |
    | **Domain allowlist** | Web results restricted to trusted sites | `.gov.sg` + `.edu.sg` suffixes + 22 specific domains |
    | **LLM system prompt** | Refuse off-topic, block system prompt reveal | Hardened `SYSTEM_PROMPT` in `llm_service.py` |
    | **Content moderation** | Block harmful/inappropriate content | `moderate_content()` with blocked-term patterns |
    | **Length limits** | Prevent abuse | 3–500 character input, max 1000 token response |
        """)

        st.markdown("### Score Calculation Formulas")
        st.markdown("""
    **PSLE (since 2021):**
    > Total AL = AL(English) + AL(Mother Tongue) + AL(Mathematics) + AL(Science)
    > Scale: AL1 (best, 90–100%) → AL8 (weakest, <45%). Total range: 4–32 (lower = better)

    **L1R5 for JC (JAE):**
    > Raw L1R5 = English grade + best 5 relevant subjects (≥1 humanities + ≥1 math/science)
    > Net L1R5 = Raw − CCA bonus (0–2) − Affiliation bonus (0–2). Minimum net = 2.

    **A-level University Admission Score (UAS):**
    > UAS = H1 GP + H1 PW + best 3 elective subjects + H1 MTL (capped at 10) + H3 bonus
    > H2: A=20, B=17.5, C=15, D=12.5, E=10. H1: A=10, B=8.75, C=7.5, D=6.25, E=5.
    > H3 bonus: Distinction=2.5, Merit=1.25 per subject (max 2). **Maximum UAS = 90 (+H3)**

    **Poly GPA for DAE:**
    > GPA 0.0–4.0 scale. Most competitive faculties require GPA ≥ 3.5. Medicine/Law require ≥ 3.9.
        """)


    # ── RAG + WEB SEARCH PIPELINE ───────────────────────────────────────────────
    with tab_rag:
        st.markdown("## RAG + Web Search Pipeline")
        st.markdown("""
    EduPath SG uses a **three-source retrieval** strategy:

    **Source 1 — Local TF-IDF RAG (always active, no API key needed):**
    scikit-learn TF-IDF vectorisation over 261 chunks from 14 official seed files.
    Covers government schools, international schools, PR/international pathways, fees,
    NS, Student Pass, FSBB, and IB-to-university conversion. Works fully offline.

    **Source 2 — DuckDuckGo Web Search (always active, no API key needed):**
    Live search restricted to `.gov.sg` and `.edu.sg` domains via site: filter
    and post-retrieval domain allowlist. Falls back to 17 curated official URLs
    if DuckDuckGo is unavailable.

    **Source 3 — OpenAI GPT-4o-mini (optional, requires API key):**
    Synthesises RAG chunks + web results into a natural language answer.
    When disabled, the app returns structured RAG context + web links directly (local RAG mode).
        """)

        st.markdown("### Combined Retrieval Flow")
        st.code("""
    User question: "What L1R5 do I need for Raffles JC?"
         │
         ├──── validate_question() ── PASS (contains "l1r5", "jc")
         │
         ├──── Source 1: rag_service.retrieve_chunks(query, top_k=6)
         │        │
         │        ├── TF-IDF vectorize query
         │        ├── Cosine similarity vs 254 indexed chunks
         │        └── Return: "Raffles JC L1R5 cutoff ~3-4" (score: 0.42)
         │                    "JAE application window Jan..." (score: 0.31)
         │
         ├──── Source 2: web_search_service.search_web(query, max_results=3)
         │        │
         │        ├── DuckDuckGo: "Singapore education L1R5 Raffles JC site:moe.gov.sg"
         │        ├── Filter results through domain allowlist
         │        └── Return: [{title: "MOE JAE", url: "moe.gov.sg/...", snippet: "..."}]
         │
         └──── Source 3: llm_service.ask_guide(question, rag_chunks, web_results)
                  │
                  ├── Build messages: system_prompt + role_context + stage_context
                  │     + career_context + rag_chunks + web_results + history
                  │
                  ├── [USE_AI=true]  → GPT-4o-mini generates answer citing sources
                  └── [USE_AI=false] → Return structured RAG context + web links
        """, language="text")

        st.markdown("### Knowledge Base Coverage")
        import pandas as pd
        kb_data = {
            "Source Type": [
                "Education stages", "Secondary schools", "Primary schools",
                "JC data", "Poly courses", "ITE courses", "University faculties",
                "Career pathways", "Fallback policies", "Support resources",
                "Success stories", "Institution locations",
                "International schools", "PR & International pathways",
                "Part-time diplomas & degrees",
                "Static knowledge (NS, fees, visa, FSBB, part-time, etc.)",
            ],
            "Items": [12, 88, 72, 12, "~50", "~12", 29, 15, 10, "~35", 10, 14, 18, "~25", 7, 28],
            "Source": [
                "MOE", "MOE school directory", "MOE P1 registration",
                "MOE JAE", "5 polytechnics", "ITE Education Services",
                "6 autonomous universities", "Cross-referenced from uni/poly/ITE data",
                "MOE / SEAB", "MOE / PSC / SkillsFuture / WSG",
                "Public records / biographies", "OneMap geocoding",
                "18 international schools (IB/IGCSE/AP)", "MOE AEIS, ICA, MINDEF, MOE fees",
                "SkillsFuture, SUSS, SIT, Kaplan, PSB, MDIS, SIM, ITE work-study (RAG static chunks)",
                "NS, Edusave, Student Pass, Tuition Grant, fee comparison, FSBB, IB conversion, part-time pathways",
            ],
        }
        st.dataframe(pd.DataFrame(kb_data), use_container_width=True, hide_index=True)

        st.markdown("### Web Search Domain Allowlist")
        st.markdown("""
    Only results from these domains pass through the security filter:

    | Category | Domains |
    |----------|---------|
    | **Government** | moe.gov.sg, seab.gov.sg, skillsfuture.gov.sg, cpf.gov.sg, psc.gov.sg, ssg.gov.sg, ica.gov.sg |
    | **Universities** | nus.edu.sg, ntu.edu.sg, smu.edu.sg, sutd.edu.sg, sit.edu.sg, suss.edu.sg |
    | **Polytechnics** | sp.edu.sg, tp.edu.sg, nyp.edu.sg, np.edu.sg, rp.edu.sg |
    | **Other .edu.sg** | ite.edu.sg, nie.edu.sg, any *.edu.sg subdomain |
    | **Other .gov.sg** | Any *.gov.sg subdomain (MINDEF, ICA, etc.) |
        """)


    # ── DATA ARCHITECTURE ────────────────────────────────────────────────────────
    with tab_data:
        st.markdown("## Data Architecture")
        st.markdown("""
    **1. SQLite** (`storage/edupathsg.sqlite`) — user credentials (bcrypt-hashed) + chat history

    **2. JSON Seed Files** (`data/seed/`) — 14 files loaded at startup via `@lru_cache`

    **3. TF-IDF Store** (`storage/tfidf_store.pkl`) — pre-built index (261 chunks), auto-rebuilt if missing

    **4. Geocode Cache** (`storage/geocode_cache.json`) — OneMap results for school coordinates
        """)

        st.markdown("### Application Structure")
        st.code("""
    edupathsg/
    ├── app.py                          # Login + home page + auto-bootstrap
    ├── pages/
    │   ├── 1_Pathway_Planner.py        # UC1: Roadmap + career pathway viz
    │   ├── 2_Score_Matcher.py          # UC1: PSLE/O-lvl/A-lvl/DAE calculators + nearby map
    │   ├── 3_Fallback_Support.py       # Fallback policies + part-time diplomas/degrees + success stories
    │   ├── 4_About_Us.py               # Project scope, objectives, data sources
    │   └── 5_Methodology.py            # This page — flowcharts + data architecture
    ├── components/
    │   ├── sidebar.py                  # Navigation + stage/career selectors
    │   ├── chat_panel.py               # Right-side AI assistant (persistent)
    │   ├── stage_theme.py              # Per-stage CSS theming
    │   └── role_context.py             # Role-aware language labels
    ├── services/
    │   ├── db.py                       # SQLite connection helpers
    │   ├── auth_service.py             # Login / register (bcrypt)
    │   ├── pathway_service.py          # Education stage + fork data loaders
    │   ├── score_service.py            # L1R5 / ELR2B2 / UAS / GPA calculators
    │   ├── career_service.py           # Reverse career → pathway tracer
    │   ├── rag_service.py              # TF-IDF RAG (261 chunks)
    │   ├── llm_service.py              # OpenAI GPT-4o-mini + local RAG mode
    │   ├── web_search_service.py       # DuckDuckGo + domain allowlist + guardrails
    │   ├── location_service.py         # OneMap geocoding + travel time
    │   └── geocode_bootstrap.py        # Auto-geocode schools on cold start
    ├── data/seed/                      # 14 JSON files (education data)
    │   ├── education_stages.json       # 12 stages (early childhood → postgrad)
    │   ├── secondary_schools.json      # 88 schools with PSLE cutoffs
    │   ├── primary_schools.json        # 72 schools with P1 registration data
    │   ├── jc_data.json                # 12 JCs with L1R5 cutoffs
    │   ├── poly_courses.json           # ~50 courses across 5 polytechnics
    │   ├── ite_data.json               # ~12 courses across 3 ITE colleges
    │   ├── university_data.json        # 6 universities, 29 faculties
    │   ├── career_pathways.json        # 15 careers with reverse pathway data
    │   ├── fallback_policies.json      # 10 exam failure / retake scenarios
    │   ├── support_resources.json      # Counselling, scholarships, career guidance
    │   ├── success_stories.json        # 10 Singapore success stories
    │   ├── institution_locations.json  # 14 poly/ITE/uni locations (lat/lng)
    │   ├── international_schools.json  # 18 international schools (IB/IGCSE/AP)
    │   └── pr_international_pathways.json  # AEIS, fees, NS, Student Pass, FSBB
    ├── utils/
    │   ├── config.py                   # Secrets loader (_secret helper)
    │   ├── session_manager.py          # Session state helpers (user, stage, career)
    │   └── stage_config.py             # 5 education stages with color themes
    ├── storage/                        # Auto-generated at runtime
    │   ├── edupathsg.sqlite            # User DB + chat history
    │   ├── tfidf_store.pkl             # TF-IDF index (261 chunks)
    │   └── geocode_cache.json          # OneMap coordinate cache
    └── requirements.txt                # 10 dependencies
        """, language="text")

        st.markdown("### Data Flow Summary")
        st.code("""
                             ┌─────────────────────┐
                             │    Streamlit App     │
                             │  (5 pages + sidebar) │
                             └──────────┬──────────┘
                                        │
                  ┌─────────────────────┼─────────────────────┐
                  │                     │                     │
        ┌─────────▼──────────┐ ┌───────▼────────┐ ┌─────────▼──────────┐
        │   pathway_service  │ │ score_service  │ │  career_service    │
        │   14 seed JSONs + static KB    │ │ 4 calculators  │ │  15 career paths   │
        │   @lru_cache       │ │ 4 matchers     │ │  reverse tracing   │
        └────────────────────┘ └────────────────┘ └────────────────────┘
                  │                     │                     │
                  └─────────────────────┼─────────────────────┘
                                        │
                  ┌─────────────────────┼─────────────────────┐
                  │                     │                     │
        ┌─────────▼──────────┐ ┌───────▼────────┐ ┌─────────▼──────────┐
        │   rag_service      │ │ web_search     │ │  llm_service       │
        │   TF-IDF / 261     │ │ DuckDuckGo     │ │  GPT-4o-mini       │
        │   chunks           │ │ .gov.sg only   │ │  or local RAG mode │
        └────────────────────┘ └────────────────┘ └────────────────────┘
                  │                     │                     │
                  └─────────────────────┼─────────────────────┘
                                        │
                             ┌──────────▼──────────┐
                             │      SQLite DB      │
                             │  users · chat_sessions │
                             └─────────────────────┘
        """, language="text")

    st.markdown("""
    <div class="gov-footer">
    <a href="https://www.moe.gov.sg">MOE</a> ·
    <a href="https://www.seab.gov.sg">SEAB</a> ·
    <a href="https://www.ite.edu.sg">ITE</a> ·
    <a href="https://www.skillsfuture.gov.sg">SkillsFuture</a><br>
    <small>EduPath SG is an AI Champion Bootcamp capstone project. Not affiliated with the Singapore Government.</small>
    </div>
    """, unsafe_allow_html=True)

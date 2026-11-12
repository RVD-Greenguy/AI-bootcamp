import streamlit as st

st.set_page_config(page_title="Pathway Planner — EduPath SG", page_icon="🗺️", layout="wide")

from utils.session_manager import require_login
from utils.config import DISCLAIMER
from components.sidebar import render_sidebar
from components.chat_panel import render_chat_panel
from components.stage_theme import apply_stage_theme
from services.pathway_service import get_stages, get_pathway_for_profile

user = require_login()
render_sidebar()
render_chat_panel()
apply_stage_theme()

st.title("🗺️ Singapore Education Pathway Planner")
st.caption("Visualise your complete education journey from any stage to graduation and beyond.")
st.warning(f"⚠️ {DISCLAIMER}", icon="⚠️")

STAGE_ID_MAP = {
    "Early Childhood (0–6)": "early_childhood",
    "Primary School": "primary",
    "Secondary School": "secondary_express",
    "Post-Secondary (JC/Poly/ITE)": "junior_college",
    "University": "university",
    "Post-Graduate": "postgrad",
}

# ── INPUT FORM ──────────────────────────────────────────────────────────────
with st.form("pathway_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        stage_label = st.selectbox("Current stage:", list(STAGE_ID_MAP.keys()))
    with col2:
        citizenship = st.selectbox("Citizenship:", ["Singapore Citizen", "Permanent Resident", "International Student"])
    with col3:
        age = st.number_input("Child's current age:", min_value=0, max_value=25, value=7)

    interests = st.multiselect(
        "Areas of interest (optional):",
        ["STEM / Engineering", "Business / Finance", "Arts / Design / Media",
         "Healthcare / Medicine", "Law", "Education / Social Work", "IT / Computing", "Vocational / Technical"],
    )
    submitted = st.form_submit_button("🗺️ Show My Pathway", type="primary", use_container_width=True)

if submitted or st.session_state.get("pathway_shown"):
    st.session_state["pathway_shown"] = True
    stage_id = STAGE_ID_MAP[stage_label]
    pathway = get_pathway_for_profile(stage_id, interests, citizenship)

    # ── ROADMAP HTML ─────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📍 Singapore Education Roadmap")

    # Determine which nodes are highlighted
    hl = stage_id  # current highlight key

    def node_style(track: str, active: bool = False, past: bool = False) -> str:
        track_styles = {
            "early":    ("border: 2px solid #3b82f6", "#0f2550", "#93c5fd"),
            "primary":  ("border: 2px solid #3b82f6", "#0f2550", "#93c5fd"),
            "ip":       ("border: 1.5px solid #22c55e", "#052e16", "#86efac"),
            "express":  ("border: 1.5px solid #3b82f6", "#172554", "#93c5fd"),
            "na":       ("border: 1.5px solid #f59e0b", "#422006", "#fcd34d"),
            "nt":       ("border: 1.5px solid #6b7280", "#111827", "#9ca3af"),
            "jc":       ("border: 1.5px solid #8b5cf6", "#2e1065", "#c4b5fd"),
            "poly":     ("border: 1.5px solid #06b6d4", "#083344", "#67e8f9"),
            "ite":      ("border: 1.5px solid #f97316", "#431407", "#fdba74"),
            "uni":      ("border: 1.5px solid #10b981", "#022c22", "#6ee7b7"),
            "postgrad": ("border: 1.5px solid #10b981", "#022c22", "#6ee7b7"),
        }
        border, bg, sub = track_styles.get(track, ("border: 1.5px solid #334155", "#1e293b", "#94a3b8"))
        if active:
            return f"background:{bg};{border};border-width:2px;box-shadow:0 0 0 4px rgba(59,130,246,0.25);border-radius:8px;padding:12px 14px;"
        if past:
            return "background:#0a0f1a;border:1.5px solid #1e293b;border-radius:8px;padding:12px 14px;opacity:0.5;"
        return f"background:{bg};{border};border-radius:8px;padding:12px 14px;"

    def sub_color(track: str) -> str:
        colors = {
            "ip": "#86efac", "express": "#93c5fd", "na": "#fcd34d",
            "nt": "#9ca3af", "jc": "#c4b5fd", "poly": "#67e8f9",
            "ite": "#fdba74", "uni": "#6ee7b7", "postgrad": "#6ee7b7",
            "early": "#93c5fd", "primary": "#93c5fd",
        }
        return colors.get(track, "#94a3b8")

    # Determine active nodes based on stage
    active_early    = hl == "early_childhood"
    active_primary  = hl == "primary"
    active_sec      = hl == "secondary_express"
    active_postsec  = hl == "junior_college"
    active_uni      = hl == "university"
    active_postgrad = hl == "postgrad"

    past_early   = hl in ("primary", "secondary_express", "junior_college", "university", "postgrad")
    past_primary = hl in ("secondary_express", "junior_college", "university", "postgrad")
    past_sec     = hl in ("junior_college", "university", "postgrad")
    past_postsec = hl in ("university", "postgrad")
    past_uni     = hl == "postgrad"

    ec_style  = node_style("early",    active=active_early,    past=past_early)
    pri_style = node_style("primary",  active=active_primary,  past=past_primary)

    ip_style  = node_style("ip",   active=active_sec, past=past_sec)
    ex_style  = node_style("express", active=active_sec, past=past_sec)
    na_style  = node_style("na",   active=active_sec, past=past_sec)
    nt_style  = node_style("nt",   active=active_sec, past=past_sec)

    jc_style   = node_style("jc",   active=active_postsec, past=past_postsec)
    poly_style = node_style("poly", active=active_postsec, past=past_postsec)
    ite_style  = node_style("ite",  active=active_postsec, past=past_postsec)

    uni_style  = node_style("uni",      active=active_uni,      past=past_uni)
    pg_style   = node_style("postgrad", active=active_postgrad, past=False)

    you_here = "▼ You are here"

    html = f"""
<style>
  .rm-wrap {{
    background: #0f172a;
    padding: 32px 24px;
    border-radius: 12px;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: #e2e8f0;
    min-height: 1200px;
  }}
  .rm-node-title {{ font-size: 14px; font-weight: 600; color: #e2e8f0; margin:0 0 4px 0; }}
  .rm-node-sub   {{ font-size: 11px; margin: 0; }}
  .rm-you-here   {{ font-size: 10px; color: #60a5fa; font-weight:600; margin-top:6px; letter-spacing:0.5px; }}
  .rm-center {{ display:flex; flex-direction:column; align-items:center; }}
  .rm-arrow  {{ color:#334155; font-size:20px; line-height:1; margin:4px 0; }}
  .rm-fork-label {{
    display:inline-block;
    background:rgba(245,158,11,0.15);
    color:#f59e0b;
    font-size:11px;
    font-weight:700;
    letter-spacing:1.5px;
    text-transform:uppercase;
    padding:4px 14px;
    border-radius:20px;
    margin:8px 0;
    border:1px solid rgba(245,158,11,0.3);
  }}
  .rm-section-label {{
    color:#64748b;
    font-size:11px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:2px;
    margin-bottom:8px;
  }}
  .rm-fork-row {{
    display:flex;
    gap:10px;
    width:100%;
    max-width:800px;
    justify-content:center;
  }}
  .rm-fork-col {{
    flex:1;
    min-width:140px;
    max-width:195px;
    display:flex;
    flex-direction:column;
    align-items:center;
  }}
  .rm-fork-col .rm-node {{
    width:100%;
  }}
  .rm-node {{
    width:220px;
  }}
  .rm-hline {{
    width:100%;
    max-width:800px;
    height:1px;
    background:#334155;
    margin:0;
  }}
  .rm-converge {{
    display:flex;
    gap:10px;
    width:100%;
    max-width:800px;
    justify-content:center;
    align-items:flex-start;
  }}
  .rm-conv-col {{
    flex:1;
    min-width:140px;
    max-width:195px;
    display:flex;
    flex-direction:column;
    align-items:center;
  }}
  .rm-conv-col .rm-node {{
    width:100%;
  }}
</style>

<div class="rm-wrap">
  <div class="rm-center">

    <!-- EARLY CHILDHOOD -->
    <div class="rm-section-label">Foundation</div>
    <div class="rm-node" style="{ec_style}">
      <p class="rm-node-title">🏠 Early Childhood</p>
      <p class="rm-node-sub" style="color:{sub_color('early')}">Age 0–6 · Preschool / Kindergarten</p>
      {'<p class="rm-you-here">' + you_here + '</p>' if active_early else ''}
    </div>

    <div class="rm-arrow">↓</div>

    <!-- PRIMARY SCHOOL -->
    <div class="rm-node" style="{pri_style}">
      <p class="rm-node-title">📚 Primary School (P1–P6)</p>
      <p class="rm-node-sub" style="color:{sub_color('primary')}">Age 7–12 · 6 years · MOE curriculum</p>
      {'<p class="rm-you-here">' + you_here + '</p>' if active_primary else ''}
    </div>

    <div class="rm-arrow">↓</div>
    <span class="rm-fork-label">PSLE — Age 12</span>
    <div class="rm-arrow">↓</div>

    <!-- PSLE FORK ROW -->
    <div class="rm-hline"></div>
    <div class="rm-fork-row">

      <div class="rm-fork-col">
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{ip_style}">
          <p class="rm-node-title">🌟 IP Track</p>
          <p class="rm-node-sub" style="color:{sub_color('ip')}">AL 4–8 · Top schools</p>
          {'<p class="rm-you-here">' + you_here + '</p>' if active_sec else ''}
        </div>
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{ip_style}">
          <p class="rm-node-title">6-Year Programme</p>
          <p class="rm-node-sub" style="color:{sub_color('ip')}">RI · HCI · ACSI · SCGS · NJC…</p>
          <p class="rm-node-sub" style="color:{sub_color('ip')}">Leads to A-levels or IB</p>
        </div>
      </div>

      <div class="rm-fork-col">
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{ex_style}">
          <p class="rm-node-title">🔵 Express Stream</p>
          <p class="rm-node-sub" style="color:{sub_color('express')}">AL ≤ 20 · Sec 1–4</p>
          {'<p class="rm-you-here">' + you_here + '</p>' if active_sec else ''}
        </div>
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{ex_style}">
          <p class="rm-node-title">O-Levels (Sec 4)</p>
          <p class="rm-node-sub" style="color:{sub_color('express')}">GCE O-Level examination</p>
          <p class="rm-node-sub" style="color:{sub_color('express')}">JAE in January</p>
        </div>
      </div>

      <div class="rm-fork-col">
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{na_style}">
          <p class="rm-node-title">🟡 Normal Academic</p>
          <p class="rm-node-sub" style="color:{sub_color('na')}">AL 21–22 · Sec 1–5</p>
          {'<p class="rm-you-here">' + you_here + '</p>' if active_sec else ''}
        </div>
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{na_style}">
          <p class="rm-node-title">N(A)-Levels → O-Levels</p>
          <p class="rm-node-sub" style="color:{sub_color('na')}">Sec 4 N(A) → Sec 5 O-lvl</p>
          <p class="rm-node-sub" style="color:{sub_color('na')}">Or PFP direct to Poly</p>
        </div>
      </div>

      <div class="rm-fork-col">
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{nt_style}">
          <p class="rm-node-title">⬜ Normal Technical</p>
          <p class="rm-node-sub" style="color:{sub_color('nt')}">AL 23–32 · Sec 1–4</p>
          {'<p class="rm-you-here">' + you_here + '</p>' if active_sec else ''}
        </div>
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{nt_style}">
          <p class="rm-node-title">N(T)-Levels → ITE</p>
          <p class="rm-node-sub" style="color:{sub_color('nt')}">Direct ITE pathway</p>
          <p class="rm-node-sub" style="color:{sub_color('nt')}">NITEC programmes</p>
        </div>
      </div>

    </div>
    <div class="rm-hline"></div>

    <div class="rm-arrow">↓</div>
    <span class="rm-fork-label">JAE — Joint Admissions Exercise</span>
    <div class="rm-arrow">↓</div>

    <!-- POST-SECONDARY FORK ROW -->
    <div class="rm-hline"></div>
    <div class="rm-fork-row">

      <div class="rm-fork-col">
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{jc_style}">
          <p class="rm-node-title">🟣 Junior College</p>
          <p class="rm-node-sub" style="color:{sub_color('jc')}">Net L1R5 ≤ 20 · 2 years</p>
          {'<p class="rm-you-here">' + you_here + '</p>' if active_postsec else ''}
        </div>
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{jc_style}">
          <p class="rm-node-title">A-Levels / H1 / H2</p>
          <p class="rm-node-sub" style="color:{sub_color('jc')}">12 JCs incl. RJC, HCJC, NJC</p>
          <p class="rm-node-sub" style="color:{sub_color('jc')}">Rank pts 0–90</p>
        </div>
      </div>

      <div class="rm-fork-col">
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{poly_style}">
          <p class="rm-node-title">🩵 Polytechnic</p>
          <p class="rm-node-sub" style="color:{sub_color('poly')}">ELR2B2 aggregate · 3 years</p>
          {'<p class="rm-you-here">' + you_here + '</p>' if active_postsec else ''}
        </div>
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{poly_style}">
          <p class="rm-node-title">Diploma (100+ courses)</p>
          <p class="rm-node-sub" style="color:{sub_color('poly')}">SP · TP · NYP · NP · RP</p>
          <p class="rm-node-sub" style="color:{sub_color('poly')}">Work-Study (WSDip) option</p>
        </div>
      </div>

      <div class="rm-fork-col">
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{ite_style}">
          <p class="rm-node-title">🟠 ITE</p>
          <p class="rm-node-sub" style="color:{sub_color('ite')}">O/N-level passes · 2 years</p>
          {'<p class="rm-you-here">' + you_here + '</p>' if active_postsec else ''}
        </div>
        <div class="rm-arrow">↓</div>
        <div class="rm-node" style="{ite_style}">
          <p class="rm-node-title">NITEC / Higher NITEC</p>
          <p class="rm-node-sub" style="color:{sub_color('ite')}">ITE College East/Central/West</p>
          <p class="rm-node-sub" style="color:{sub_color('ite')}">Work-Study Programme (WSP)</p>
        </div>
      </div>

    </div>
    <div class="rm-hline"></div>

    <div class="rm-arrow">↓</div>
    <span class="rm-fork-label">University Admissions (SNUFA / DAE)</span>
    <div class="rm-arrow">↓</div>

    <!-- UNIVERSITY -->
    <div class="rm-node" style="{uni_style}">
      <p class="rm-node-title">🎓 Autonomous Universities</p>
      <p class="rm-node-sub" style="color:{sub_color('uni')}">NUS · NTU · SMU · SUTD · SIT · SUSS</p>
      <p class="rm-node-sub" style="color:{sub_color('uni')}">A-lvl rank pts (SNUFA) or Poly GPA (DAE)</p>
      {'<p class="rm-you-here">' + you_here + '</p>' if active_uni else ''}
    </div>

    <div class="rm-arrow">↓</div>

    <!-- POST-GRAD -->
    <div class="rm-node" style="{pg_style}">
      <p class="rm-node-title">🏆 Post-Graduate / SkillsFuture</p>
      <p class="rm-node-sub" style="color:{sub_color('postgrad')}">Masters · PhD · Professional Conversion</p>
      <p class="rm-node-sub" style="color:{sub_color('postgrad')}">SkillsFuture Credit · Earn &amp; Learn</p>
      {'<p class="rm-you-here">' + you_here + '</p>' if active_postgrad else ''}
    </div>

  </div>

  <!-- LEGEND -->
  <div style="margin-top:28px;padding-top:20px;border-top:1px solid #1e293b;display:flex;flex-wrap:wrap;gap:16px;justify-content:center;">
    <span style="font-size:12px;color:#9ca3af;">🟢 IP Track</span>
    <span style="font-size:12px;color:#9ca3af;">🔵 Express</span>
    <span style="font-size:12px;color:#9ca3af;">🟡 Normal Academic</span>
    <span style="font-size:12px;color:#9ca3af;">⬜ Normal Technical</span>
    <span style="font-size:12px;color:#9ca3af;">🟣 JC</span>
    <span style="font-size:12px;color:#9ca3af;">🩵 Polytechnic</span>
    <span style="font-size:12px;color:#9ca3af;">🟠 ITE</span>
    <span style="font-size:12px;color:#9ca3af;">🟩 University</span>
    <span style="font-size:12px;color:#60a5fa;font-weight:600;">▼ You are here</span>
  </div>
</div>
"""

    st.html(html)

    # ── CITIZENSHIP NOTES ───────────────────────────────────────────────────
    if pathway.get("citizenship_notes"):
        st.divider()
        st.subheader(f"🌐 Notes for {citizenship}")
        for note in pathway["citizenship_notes"]:
            st.info(note)

    # ── STAGE DETAILS ───────────────────────────────────────────────────────
    st.divider()
    st.subheader("📋 Stage-by-Stage Details")

    for stage in pathway.get("stages", []):
        age_range = stage.get("age_range", "")
        with st.expander(f"**{stage.get('name', '')}** — Age {age_range}", expanded=False):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Description:** {stage.get('description', '')}")
                st.markdown(f"**Entry criteria:** {stage.get('entry_criteria', '')}")
            with col_b:
                st.markdown(f"**Exit process:** {stage.get('exit_process', '')}")
                st.markdown(f"**Governing body:** {stage.get('governing_body', '')}")
            if stage.get("official_url"):
                st.markdown(f"🔗 [Official information]({stage['official_url']})")
            if stage.get("key_facts"):
                st.markdown("**Key facts:**")
                for fact in stage["key_facts"]:
                    st.markdown(f"- {fact}")

    # ── FORKS ───────────────────────────────────────────────────────────────
    if pathway.get("forks"):
        st.divider()
        st.subheader("🔀 Key Decision Points")
        for fork in pathway["forks"]:
            st.markdown(f"### Fork at: **{fork['at']}**")
            for i, opt in enumerate(fork["options"]):
                colour_fn = st.success if i == 0 else (st.info if i == 1 else st.warning)
                colour_fn(f"**{opt['name']}** — _{opt['criteria']}_ → {opt['leads_to']}")
            st.divider()

    # ── QUICK LINK ──────────────────────────────────────────────────────────
    st.divider()
    st.markdown("**🎯 Want to check specific school eligibility based on scores?**")
    st.page_link("pages/2_Score_Matcher.py", label="→ Go to Score & School Matcher", icon="🎯")

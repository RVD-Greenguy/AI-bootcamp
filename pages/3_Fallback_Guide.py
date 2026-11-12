import streamlit as st

st.set_page_config(page_title="Fallback Guide — EduPath SG", page_icon="🔄", layout="wide")

import pandas as pd
import plotly.graph_objects as go

from utils.session_manager import require_login
from utils.config import DISCLAIMER
from components.sidebar import render_sidebar
from services.pathway_service import get_fallback_policies

user = require_login()
render_sidebar()

st.title("🔄 Fallback & Recovery Guide")
st.caption("What to do when results don't go as planned — retake policies, alternative pathways, and certificate implications.")
st.warning(f"⚠️ {DISCLAIMER}", icon="⚠️")
st.info("This guide covers official MOE and SEAB policies. Always verify current policies at **moe.gov.sg** and **seab.gov.sg** before making decisions.")

SCENARIO_MAP = {
    "Failed English Language at O-levels": "failed_english_olevels",
    "Didn't meet JC L1R5 cutoff": "failed_to_meet_jc_cutoff",
    "Failed one or more O-level subjects": "failed_olevels_subjects",
    "Failed A-level subject(s)": "failed_alevels",
    "Failed H1 General Paper (A-levels)": "failed_english_alevels",
    "IP student struggling / may exit programme": "ip_exit",
    "Normal Academic student at Sec 4 N-level results": "n_level_pathway",
    "Polytechnic GPA too low for desired university": "poly_low_gpa",
    "Want to understand private candidate rules": "private_candidate_rules",
    "Understanding certificate implications of retakes": "cert_endorsement",
}

# ── SCENARIO SELECTOR ────────────────────────────────────────────────────────
st.subheader("🔍 Select Your Scenario")
selected_scenario = st.selectbox("What situation are you facing?", list(SCENARIO_MAP.keys()))
scenario_id = SCENARIO_MAP[selected_scenario]

policies = get_fallback_policies()
policy = next((p for p in policies if p.get("id") == scenario_id), None)

if policy:
    st.divider()
    st.subheader(f"📋 {selected_scenario}")

    # Trigger + official policy
    st.warning(f"**Situation:** {policy.get('trigger_condition', '')}")
    st.info(f"**Official Policy:** {policy.get('official_policy', '')}")

    # Options
    options = policy.get("options", [])
    if options:
        st.markdown("### 🛤️ Your Options")
        for opt in options:
            with st.expander(f"**{opt.get('option_name', 'Option')}**", expanded=False):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"**Description:** {opt.get('description', '')}")
                    st.markdown(f"**Timeline:** {opt.get('timeline', '')}")
                    st.markdown(f"**Eligibility:** {opt.get('eligibility', '')}")
                with col_b:
                    st.success(f"✅ **Pros:** {opt.get('pros', '')}")
                    st.error(f"⚠️ **Cons:** {opt.get('cons', '')}")

    # Important notes
    notes = policy.get("important_notes", [])
    if notes:
        st.markdown("### ⚠️ Important Notes")
        for note in notes:
            st.warning(f"• {note}")

    # Official URL
    if policy.get("official_url"):
        st.markdown(f"🔗 [Official MOE / SEAB Information]({policy['official_url']})")

else:
    # Fallback if JSON not yet seeded — show hardcoded content for key scenarios
    st.divider()
    hardcoded = {
        "Failed English Language at O-levels": {
            "policy": "English Language is a mandatory requirement for JC admission and most polytechnic courses. Failing English (grade below C6 at O-levels) significantly limits post-secondary options.",
            "options": [
                ("Retake English as private candidate", "Register with SEAB (March–April) to sit English in October/November. Results in January next year. This is the most common path.", "Any student who sat O-levels", "Proven route; allows access to JC/poly if passed", "Delays post-secondary by one year"),
                ("Apply to ITE", "Some ITE NITEC courses accept D7 English or N-level English. Check specific course requirements.", "O-level D7 or N-level grade 1–3 in English", "No delay; begin vocational training immediately", "Limited to ITE courses; restricted progression"),
                ("Conditional poly offer", "Some polytechnic courses may offer conditional acceptance pending English retake. Check with individual polys.", "Varies by poly and course", "May secure poly place while retaking", "Not guaranteed; poly-dependent"),
            ],
            "notes": ["First-attempt results remain on SEAB certificate permanently", "Most NUS/NTU/SMU courses require O-level English pass for DAE pathway"],
        },
        "Didn't meet JC L1R5 cutoff": {
            "policy": "JC cutoffs are determined by competition each year. If net L1R5 is above 20, JC is not an option. If within 20 but above your desired JC's cutoff, options include appeal or alternative JC.",
            "options": [
                ("Accept JAE posting to available JC", "JAE system posts you to the highest-ranked JC your score qualifies for. All JCs offer the same A-level syllabus.", "Net L1R5 ≤ 20", "Guaranteed JC place; no delay", "May not be preferred JC or location"),
                ("Appeal in January", "During JAE, you can appeal to your desired JC if places remain after the posting exercise.", "Borderline scores; appeals accepted at JC's discretion", "Possibility of getting into desired JC", "Not guaranteed; competitive"),
                ("Polytechnic via JAE", "If JC is not possible, choose polytechnic instead. Diploma route still leads to university via DAE.", "ELR2B2 meets course requirements", "Practical skills; university pathway still open", "3 years vs 2 years for JC; different university admission route"),
                ("Millennia Institute (3-year A-levels)", "For Normal Academic students or those who want more preparation time before A-levels.", "O-level passes (Sec 5 or N-level route)", "More time to prepare for A-levels", "3 years; less well-known than JCs"),
            ],
            "notes": ["Apply online during JAE window (usually Jan 4–6)", "Decisions must be made quickly — JAE window is only 3 days"],
        },
    }
    if selected_scenario in hardcoded:
        d = hardcoded[selected_scenario]
        st.info(f"**Official Policy:** {d['policy']}")
        st.markdown("### 🛤️ Your Options")
        for opt_name, desc, elig, pros, cons in d["options"]:
            with st.expander(f"**{opt_name}**"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Description:** {desc}")
                    st.markdown(f"**Eligibility:** {elig}")
                with c2:
                    st.success(f"✅ **Pros:** {pros}")
                    st.error(f"⚠️ **Cons:** {cons}")
        for note in d.get("notes", []):
            st.warning(f"• {note}")
    else:
        st.info("Detailed policy information will be loaded from the knowledge base. Use the AI Guide for specific questions about this scenario.")

# ── PRIVATE CANDIDATE CALENDAR ───────────────────────────────────────────────
st.divider()
st.subheader("📅 Private Candidate Key Dates")

calendar_data = [
    ("January", "O-level / A-level / N-level results released", "SEAB"),
    ("January (days 1–3 of release)", "JAE application window opens — apply to JC / Poly / ITE", "MOE JAE"),
    ("Late January", "JAE posting results released", "MOE"),
    ("March–April", "SEAB private candidate registration opens for October/November sittings", "SEAB"),
    ("May–June", "Some JCs / polys supplementary / appeal registration", "Individual schools"),
    ("October–November", "Private candidate exam sitting (O/N/A-levels)", "SEAB"),
    ("January (following year)", "Private candidate results released", "SEAB"),
]

cal_df = pd.DataFrame(calendar_data, columns=["Month / Period", "Event", "Authority"])

fig_cal = go.Figure(data=[
    go.Table(
        header=dict(
            values=["📅 Month / Period", "📋 Event", "🏛️ Authority"],
            fill_color="#1565C0",
            font=dict(color="white", size=13),
            align="left",
        ),
        cells=dict(
            values=[cal_df[c] for c in cal_df.columns],
            fill_color=[["#E8EEF7", "#F5F7FA"] * 10],
            align="left",
            font=dict(size=12),
            height=30,
        )
    )
])
fig_cal.update_layout(height=300, margin=dict(t=10, b=10))
st.plotly_chart(fig_cal, use_container_width=True)

# ── CERTIFICATE IMPLICATIONS ─────────────────────────────────────────────────
st.divider()
st.subheader("📜 Certificate & Transcript Implications")

col_cert1, col_cert2 = st.columns(2)
with col_cert1:
    st.markdown("""
    **What appears on your SEAB certificate:**
    - ✅ All exam sittings are recorded
    - ✅ Original first-attempt grade is **permanently visible**
    - ✅ Improved grades shown alongside the original
    - ✅ Private candidate results are legitimate and identical in format
    - ✅ No indication that a grade was achieved as private candidate
    """)
with col_cert2:
    st.markdown("""
    **How universities view retake results:**
    - 🏥 **NUS Medicine / Dentistry / Law** — may review all attempts; first attempt matters
    - 🏛️ **NTU / SMU competitive faculties** — similar consideration for high-demand courses
    - 🎓 **Most university faculties** — accept best attempt for rank point calculation
    - 🏫 **Polytechnics** — typically accept best attempt for ELR2B2
    - 🛠️ **ITE** — accept any pass; first or retake does not matter
    """)

st.info("""
💡 **Practical advice:**
- Retake as early as possible so improved grades are available before the next JAE window
- If targeting competitive courses (Medicine, Law), be aware first-attempt grades are considered
- For most pathways, an improved retake grade is treated the same as an original result
- Use SkillsFuture or private school routes as alternatives if public university admission is challenging
""")

st.divider()
st.markdown("### 🔗 Official Resources")
links = {
    "MOE Post-Secondary Admissions": "https://www.moe.gov.sg/post-secondary/admissions",
    "SEAB Private Candidates": "https://www.seab.gov.sg/home/examinations/private-candidates",
    "JAE Information": "https://www.moe.gov.sg/post-secondary/admissions/jae",
    "PFP (Poly Foundation Programme)": "https://www.moe.gov.sg/post-secondary/admissions/pfp",
    "ITE Courses": "https://www.ite.edu.sg/courses",
    "SkillsFuture": "https://www.skillsfuture.gov.sg",
}
cols = st.columns(3)
for i, (name, url) in enumerate(links.items()):
    cols[i % 3].markdown(f"🔗 [{name}]({url})")

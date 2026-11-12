import streamlit as st

st.set_page_config(page_title="Fallback Guide — EduPath SG", page_icon="🔄", layout="wide")

import pandas as pd
import plotly.graph_objects as go

from utils.session_manager import require_login
from utils.config import DISCLAIMER
from components.sidebar import render_sidebar
from components.chat_panel import render_chat_panel
from services.pathway_service import get_fallback_policies

user = require_login()
render_sidebar()
render_chat_panel()

st.title("🔄 Fallback & Recovery Guide")
st.caption("What to do when results don't go as planned — retake policies, alternative pathways, and success stories.")
st.warning(f"⚠️ {DISCLAIMER}", icon="⚠️")
st.info("This guide covers official MOE and SEAB policies. Always verify current policies at **moe.gov.sg** and **seab.gov.sg** before making decisions.")

tab_primary, tab_secondary, tab_postsec, tab_stories = st.tabs([
    "🏫 Primary School",
    "📚 Secondary School",
    "🎓 Post-Secondary",
    "🌟 Success Stories",
])

# ── TAB 1: PRIMARY SCHOOL ────────────────────────────────────────────────────
with tab_primary:
    st.subheader("🏫 Primary School — When Things Don't Go as Planned")
    st.markdown("Primary school challenges are more common than parents think. Here are the official options at each scenario.")

    with st.expander("😟 Child struggling academically in primary school", expanded=True):
        st.markdown("""
**Step 1 — Talk to the school first**
Every MOE school has a Learning Support Coordinator (LSC) and a School Counsellor.
Request a meeting with the form teacher and ask for a learning support assessment.

**Learning Support Programme (LSP) — P1 & P2:**
- Free, small-group support classes for English literacy and Numeracy
- Identified by school in January; opt-in by parents
- Proven to close learning gaps before P3

**Subject-Based Banding (SBB) — from P5:**
- Students can take different subjects at Standard vs Foundation level
- E.g., Standard English + Standard Maths + Foundation Science
- Reduces pressure while still allowing secondary school placement
- Note: Foundation subjects are capped at AL C in PSLE aggregate

**School-based Dyslexia Remediation (SDR):**
- Targeted support for students with dyslexia-related reading difficulties (P3–P4)
- Conducted within school hours by trained teachers

**If learning differences are suspected:**
- Request referral to the school's Allied Educator (Learning & Behavioural Support)
- Child Guidance Clinic (CGC) assessments are available through restructured hospitals
- SPED schools (Pathlight, MINDS, DAS) provide specialist education for more significant needs

🔗 [MOE Learning Support](https://www.moe.gov.sg/primary/curriculum/learning-support)
        """)

    with st.expander("📊 Poor PSLE results — high AL total (23–32)", expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
**What AL 23–32 means:**
- Placed in Normal Technical (N(T)) stream at secondary school
- N(T) leads to N(T)-level exams, then ITE NITEC courses

**The ITE pathway is real and valid:**
1. N(T) stream → Sec 3–4 → N(T)-level exams
2. ITE NITEC (2–3 years) — vocational skills training
3. ITE Higher NITEC (1–2 years)
4. Polytechnic diploma via direct entry
5. University via DAE (Direct Admissions Exercise)

This is a proven, full pathway to university.
            """)
        with col_b:
            st.success("""
✅ **Key facts:**
- ITE graduates can and do get polytechnic diplomas
- Poly graduates can and do get university places
- Singapore's ITE graduates win WorldSkills medals globally
- Many employers value trade skills over paper qualifications

**Appeal process:**
Within 3 days of PSLE posting release, parents can appeal for reconsideration of secondary school placement. Contact MOE directly.
            """)

        st.markdown("""
**Private school option:**
If public school placement is unsatisfactory, private secondary schools (e.g., Spectra Secondary School, private institutions) offer alternative pathways. These typically lead to private or overseas qualifications.

🔗 [MOE Secondary School Posting](https://www.moe.gov.sg/primary/assessment/psle/secondary-school-posting)
        """)

    with st.expander("🏠 Requesting a school transfer (Primary)", expanded=False):
        st.markdown("""
**Within P1–P2 (most flexible):**
- Parents who have moved home can request transfer to a school closer to the new address
- MOE facilitates these transfers subject to vacancy
- Contact the **receiving school** directly first, then MOE

**After P2 (case-by-case basis):**
Transfers are considered for:
- Family relocation (new HDB purchase, job relocation)
- Medical or psychological grounds with documentation from a healthcare professional
- Exceptional family circumstances

**Important:**
- Transfers during **P6 (PSLE year) are generally not approved**
- The transfer does not change the child's PSLE registration
- Contact MOE Customer Service: **1800-2255-942**

🔗 [MOE Primary School Transfers](https://www.moe.gov.sg/primary/transfers)
        """)

    with st.expander("📝 PSLE retake as private candidate", expanded=False):
        st.markdown("""
**Is it possible?** Yes. Students can sit PSLE as a private candidate to attempt to improve their results.

**How it works:**
- Register with SEAB in **March–April** for the October/November sitting
- All four subjects must be retaken (partial retake is not available for PSLE)
- Results released the following January

**Is it common?** No. Most students proceed to secondary school regardless of PSLE results.
The N(T) → ITE → Poly pathway means that even a high AL score does not close the door to university.

**When retaking makes sense:**
- Student is significantly below their true ability (e.g., due to illness during exams)
- Family prefers a specific secondary school that requires a certain AL score
- Strong improvement expected from additional preparation

**When retaking may not make sense:**
- The delay costs one year of secondary school
- N(T) stream is not a "failure" — it leads to full career pathways via ITE

🔗 [SEAB Private Candidates — PSLE](https://www.seab.gov.sg/home/examinations/private-candidates)
        """)


# ── TAB 2: SECONDARY SCHOOL ──────────────────────────────────────────────────
with tab_secondary:
    st.subheader("📚 Secondary School — Scenario Navigator")

    SCENARIO_MAP = {
        "Failed English Language at O-levels": "failed_english_olevels",
        "Didn't meet JC L1R5 cutoff": "failed_to_meet_jc_cutoff",
        "Failed one or more O-level subjects": "failed_olevels_subjects",
        "IP student struggling / may exit programme": "ip_exit",
        "Normal Academic student at Sec 4 N-level results": "n_level_pathway",
        "Polytechnic GPA too low for desired university": "poly_low_gpa",
        "Want to understand private candidate rules": "private_candidate_rules",
        "Understanding certificate implications of retakes": "cert_endorsement",
    }

    selected_scenario = st.selectbox("What situation are you facing?", list(SCENARIO_MAP.keys()))
    scenario_id = SCENARIO_MAP[selected_scenario]

    policies = get_fallback_policies()
    policy = next((p for p in policies if p.get("id") == scenario_id), None)

    if policy:
        st.divider()
        st.subheader(f"📋 {selected_scenario}")
        st.warning(f"**Situation:** {policy.get('trigger_condition', '')}")
        st.info(f"**Official Policy:** {policy.get('official_policy', '')}")

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

        notes = policy.get("important_notes", [])
        if notes:
            st.markdown("### ⚠️ Important Notes")
            for note in notes:
                st.warning(f"• {note}")

        if policy.get("official_url"):
            st.markdown(f"🔗 [Official MOE / SEAB Information]({policy['official_url']})")

    else:
        st.divider()
        hardcoded = {
            "Failed English Language at O-levels": {
                "policy": "English Language is a mandatory requirement for JC admission and most polytechnic courses. Failing English (grade below C6 at O-levels) significantly limits post-secondary options.",
                "options": [
                    ("Retake English as private candidate", "Register with SEAB (March–April) to sit English in October/November. Results in January next year.", "Any student who sat O-levels", "Proven route; allows access to JC/poly if passed", "Delays post-secondary by one year"),
                    ("Apply to ITE", "Some ITE NITEC courses accept D7 English or N-level English. Check specific course requirements.", "O-level D7 or N-level grade 1–3 in English", "No delay; begin vocational training immediately", "Limited to ITE courses; restricted progression"),
                ],
                "notes": ["First-attempt results remain on SEAB certificate permanently", "Most NUS/NTU/SMU courses require O-level English pass for DAE pathway"],
            },
            "Didn't meet JC L1R5 cutoff": {
                "policy": "If net L1R5 is above 20, JC is not an option via JAE. If within 20 but above your desired JC's cutoff, options include appeal or alternative JC.",
                "options": [
                    ("Accept JAE posting to available JC", "JAE system posts you to the highest-ranked JC your score qualifies for.", "Net L1R5 ≤ 20", "Guaranteed JC place; no delay", "May not be preferred JC or location"),
                    ("Appeal in January", "During JAE, appeal to your desired JC if places remain after the posting exercise.", "Borderline scores", "Possibility of getting into desired JC", "Not guaranteed; competitive"),
                    ("Polytechnic via JAE", "If JC is not possible, choose polytechnic. Diploma route still leads to university via DAE.", "ELR2B2 meets course requirements", "Practical skills; university pathway still open", "3 years vs 2 years for JC"),
                ],
                "notes": ["Apply online during JAE window (usually Jan 4–6)", "JAE window is only 3 days"],
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
            st.info("Use the AI Guide for specific questions about this scenario.")


# ── TAB 3: POST-SECONDARY ───────────────────────────────────────────────────
with tab_postsec:
    st.subheader("🎓 Post-Secondary — A-levels, Polytechnic & Beyond")

    with st.expander("Failed A-level subject(s)", expanded=False):
        st.markdown("""
**Options after poor A-level results:**
- **Retake as private candidate** — Register with SEAB March–April, sit October–November. Most common for borderline cases.
- **Apply with current results** — Many universities use the best 3 H2 + 1 H1 for rank points. A single poor grade may be dropped.
- **Poly route (DAE)** — Apply to polytechnic based on O-level results (not A-levels). Then apply to university via Direct Admissions Exercise.
- **Private universities** — SIM Global Education, PSB Academy, Kaplan Singapore. Some offer progression to overseas partner university degrees.
- **Overseas university** — UK/Australian universities consider A-level results directly; requirements vary by course.

🔗 [SEAB A-level Private Candidates](https://www.seab.gov.sg/home/examinations/private-candidates)
        """)

    with st.expander("Poly diploma — GPA too low for desired university course", expanded=False):
        st.markdown("""
**GPA benchmarks (approximate 2023 AY):**
- NUS/NTU competitive faculties (Law, Medicine, CS, Biz): GPA 3.5–4.0 typically needed
- Mid-range NUS/NTU courses: GPA 3.0–3.5
- SIT, SUSS, SUSS: typically accessible from GPA 2.5+

**Options if GPA is below target:**
- **Apply anyway** — Some courses use a holistic review; portfolio and interview can compensate
- **Upgrade GPA** — Take additional modules to raise GPA before the application window
- **Alternative universities** — SIT, SUSS, UniSIM offer many poly-route-friendly programmes
- **Private universities** — SIM (affiliation with Uni of London / others), Kaplan, PSB
- **Work experience route** — Some programmes (especially SIT) value work experience; spend 1–2 years building relevant experience
- **Overseas** — Australian/UK universities accept poly diplomas; some offer advanced standing (entering Year 2)

🔗 [MOE DAE Information](https://www.moe.gov.sg/post-secondary/admissions/dae)
        """)

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


# ── TAB 4: SUCCESS STORIES ──────────────────────────────────────────────────
with tab_stories:
    st.subheader("🌟 Success Stories — Different Roads, Same Destination")

    st.success("""
**Singapore's education system offers multiple pathways. A setback at one stage is never the
end of the journey — it is often the beginning of a different, equally valid, path to success.**

The stories below are of real Singaporeans who faced academic struggles or took unconventional
paths, and went on to achieve remarkable things. They are shared not to diminish academic
achievement, but to remind students and parents that there is more than one road to a fulfilling life.
    """)

    try:
        from services.pathway_service import get_success_stories
        stories = get_success_stories()
    except Exception:
        stories = []

    STAGE_LABEL = {
        "primary": "Primary School",
        "psle": "PSLE",
        "o_levels": "O-levels",
        "n_levels": "N-levels",
        "ite": "ITE",
        "poly": "Polytechnic",
        "dropped_out": "Left school early",
    }
    STAGE_COLOR = {
        "primary": "#dbeafe",
        "psle": "#ede9fe",
        "o_levels": "#fce7f3",
        "n_levels": "#ffedd5",
        "ite": "#d1fae5",
        "poly": "#fef3c7",
        "dropped_out": "#fee2e2",
    }

    if not stories:
        st.info("Success stories data not available.")
    else:
        for story in stories:
            stage = story.get("stage", "")
            stage_label = STAGE_LABEL.get(stage, stage.replace("_", " ").title())
            stage_bg = STAGE_COLOR.get(stage, "#f1f5f9")

            with st.container(border=True):
                col_head, col_badge = st.columns([4, 1])
                with col_head:
                    st.markdown(f"### {story['name']}")
                    st.caption(story.get("known_as", ""))
                with col_badge:
                    st.markdown(
                        f"<div style='background:{stage_bg};padding:6px 12px;border-radius:16px;"
                        f"text-align:center;font-size:12px;font-weight:600;margin-top:12px'>"
                        f"Turning point: {stage_label}</div>",
                        unsafe_allow_html=True,
                    )

                st.warning(f"**The struggle:** {story.get('struggle', '')}")
                st.info(f"**Turning point:** {story.get('turning_point', '')}")
                st.success(f"**Achievement:** {story.get('achievement', '')}")

                col_lesson, col_source = st.columns([3, 1])
                with col_lesson:
                    st.markdown(f"💡 **Lesson:** *{story.get('lesson', '')}*")
                with col_source:
                    st.caption(f"Source: {story.get('source_note', '')}")

                st.markdown("")  # spacer

    st.divider()
    st.markdown("""
### 📌 Remember
Every person on this list took a road that looked wrong at the time. What made the difference
was not the stream they were placed in — it was the **decision to keep going**.

If you or your child is at a crossroads, the EduPath AI Guide can help you understand all
the options available from wherever you are right now.
    """)

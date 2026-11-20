import streamlit as st

st.set_page_config(page_title="Fallback Guide — EduPath SG", page_icon="🔄", layout="wide")

import pandas as pd
import plotly.graph_objects as go

from utils.session_manager import require_login
from utils.config import DISCLAIMER
from components.sidebar import render_sidebar
from components.chat_panel import render_chat_panel
from components.stage_theme import apply_stage_theme
from components.role_context import get_role_labels
from services.pathway_service import get_fallback_policies

user = require_login()
labels = get_role_labels(user["role"])
render_sidebar()
apply_stage_theme()
_main = render_chat_panel()

with _main:
    from utils.session_manager import get_education_stage
    from utils.stage_config import get_stage_config
    _stage = get_education_stage()
    _stage_cfg = get_stage_config(_stage)
    _fb_hints = {
        "early_childhood": ("🏫 Primary School", "P1 registration, school transfers, learning support, PSLE fallbacks.", "🏫"),
        "primary":         ("🏫 Primary School", "PSLE didn't go as planned? Transfers, retakes, and alternative pathways.", "📝"),
        "secondary":       ("📚 Secondary School", "O-level/N-level retakes, stream changes, private candidate rules.", "📚"),
        "post_secondary":  ("🎓 Post-Secondary", "A-level retakes, poly GPA recovery, ITE progression, certificate implications.", "🎓"),
        "university_plus": ("🎓 Part-Time Diplomas & Degrees", "Part-time diplomas, degrees, and work-study options for career changers and working adults.", "🏛️"),
    }
    if _stage in _fb_hints:
        _hint_tab, _hint_text, _hint_icon = _fb_hints[_stage]
        st.markdown(f"""
    <div style="background:linear-gradient(135deg, {_stage_cfg['bg']}, {_stage_cfg['bg']}90);
        border:2px solid {_stage_cfg['color']}; border-radius:10px; padding:14px 20px;
        margin-bottom:12px; display:flex; align-items:center; gap:12px;
        animation: ep-fade-slide-in 0.4s ease-out;">
        <div style="font-size:1.8em;">{_hint_icon}</div>
        <div>
            <div style="font-weight:700;color:{_stage_cfg['dark']};font-size:0.95em;">
                {_stage_cfg['label']} → Go to "{_hint_tab}" tab
            </div>
            <div style="color:{_stage_cfg['dark']}cc;font-size:0.82em;">{_hint_text}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.title("🔄 Fallback & Recovery Guide")
    st.caption(f"{labels['fallback_prefix']} didn't go as planned — retake policies, alternative pathways, and success stories.")

    from utils.session_manager import get_career_goal
    _career = get_career_goal()
    if _career:
        st.info(f"💡 Even with setbacks, the path to becoming a **{_career}** remains open through alternative routes. Check the **Pathway Planner** for details.")
    st.warning(f"⚠️ {DISCLAIMER}", icon="⚠️")
    st.info("This guide covers official MOE and SEAB policies. Always verify current policies at **moe.gov.sg** and **seab.gov.sg** before making decisions.")

    tab_primary, tab_secondary, tab_postsec, tab_parttime, tab_stories, tab_support = st.tabs([
        "🏫 Primary School",
        "📚 Secondary School",
        "🎓 Post-Secondary",
        "🎓 Part-Time Diplomas & Degrees",
        "🌟 Success Stories",
        "🤝 Support & Resources",
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


    # ── TAB 4: PART-TIME DIPLOMAS & DEGREES ────────────────────────────────────
    with tab_parttime:
        st.subheader("🎓 Part-Time Diplomas & Degrees")
        st.markdown("""
    Whether you're a working adult looking to upskill, a career changer, or someone who didn't qualify
    for full-time programmes — **part-time study is a legitimate, well-supported pathway** in Singapore.
    Many programmes are subsidised by SkillsFuture and can be completed alongside full-time work.
        """)

        st.markdown("## 📜 Part-Time Diplomas")

        with st.expander("🏛️ Polytechnic Work-Study Diplomas", expanded=True):
            st.markdown("""
    All 5 polytechnics offer **Work-Study Diplomas** for ITE graduates and working adults.
    You work full-time with a sponsoring employer while earning a polytechnic diploma.

    | Polytechnic | Example Programmes | Duration | Entry |
    |---|---|---|---|
    | **SP** | Engineering, Business, ICT | 2–3 years | NITEC/Higher NITEC or relevant work experience |
    | **TP** | Applied Sciences, Business, Design | 2–3 years | NITEC/Higher NITEC or relevant work experience |
    | **NYP** | Engineering, Health Sciences, IT | 2–3 years | NITEC/Higher NITEC or relevant work experience |
    | **NP** | Engineering, Business, ICT | 2–3 years | NITEC/Higher NITEC or relevant work experience |
    | **RP** | Engineering, Technology, Business | 2–3 years | NITEC/Higher NITEC or relevant work experience |

    **Key benefits:**
    - Earn a salary while studying (employer-sponsored)
    - SkillsFuture subsidy covers up to 70–90% of course fees
    - Same diploma qualification as full-time poly graduates
    - Direct pathway to university via DAE after graduation

    🔗 [SkillsFuture Work-Study Programmes](https://www.skillsfuture.gov.sg/initiatives/mid-career/workstudy)
            """)

        with st.expander("🔧 ITE Work-Study Programme"):
            st.markdown("""
    ITE offers **Work-Study programmes** that allow you to earn a Higher NITEC or Technical Diploma
    while working full-time with a participating employer.

    **How it works:**
    - Study 1–2 days per week at ITE, work the remaining days
    - Employer pays a monthly training allowance (~$1,200–$1,800/mth)
    - Programme duration: 1.5–2.5 years
    - SkillsFuture subsidised: SC pay minimal out-of-pocket fees

    **Entry requirements:**
    - NITEC or Higher NITEC holders
    - Or O-level / N-level holders with relevant work experience (min 2 years)

    **Progression:**
    - Higher NITEC → Poly Work-Study Diploma → University (DAE)

    🔗 [ITE Work-Study Programmes](https://www.ite.edu.sg/admissions/work-study-programmes)
            """)

        with st.expander("🏢 Private Institution Diplomas"):
            st.markdown("""
    Several private institutions offer part-time diplomas with **evening and weekend classes**,
    suitable for working adults who cannot attend daytime classes.

    | Institution | Programmes | Duration | Fees (approx) | Schedule |
    |---|---|---|---|---|
    | **Kaplan Singapore** | Business, IT, Hospitality, Accounting | 8–16 months | $8,000–$15,000 | Evenings / weekends |
    | **PSB Academy** | Engineering, Business, Life Sciences | 8–16 months | $8,000–$14,000 | Evenings / weekends |
    | **MDIS** | Business, Tourism, Engineering, IT | 8–14 months | $7,000–$13,000 | Evenings / weekends |
    | **SIM Global Education** | Business, IT, Social Sciences | 12–18 months | $8,000–$16,000 | Evenings / weekends |

    **Note:** These are **private qualifications** or qualifications from overseas partner universities.
    Check that the institution is registered with CPE (Committee for Private Education) at
    [ssg.gov.sg](https://www.ssg.gov.sg).

    **SkillsFuture Credit** ($500) can be used for eligible private diploma courses.
            """)

        st.divider()
        st.markdown("## 🎓 Part-Time Degrees")

        with st.expander("🏛️ SUSS — Singapore University of Social Sciences", expanded=True):
            st.markdown("""
    SUSS is Singapore's **primary university for part-time degrees**, with ~30 undergraduate programmes
    designed for working adults. Classes are held on **weekday evenings and Saturdays**.

    **Popular programmes:**
    - Bachelor of Business Administration (BBA)
    - Bachelor of Science in Finance / Marketing / HR
    - Bachelor of Laws (LLB) — part-time only
    - Bachelor of Social Work
    - Bachelor of Science in IT / Data Analytics

    **Duration:** 4–6 years (part-time)

    **Entry requirements:**
    - Polytechnic diploma (GPA 2.5+ for most), or
    - A-level results, or
    - Mature applicants (age 30+) with 8+ years work experience — no diploma needed

    **Fees (subsidised for SC):**
    - SC: ~$3,000–$4,500 per year (after MOE subsidy)
    - PR: ~$5,000–$7,000 per year
    - International: ~$10,000–$14,000 per year
    - Total over 4–6 years: ~$18,000–$27,000 (SC)

    **MOE Tuition Grant:** Available for SC and PR (no bond for SC/PR)

    🔗 [SUSS Part-Time Undergraduate](https://www.suss.edu.sg/programmes)
            """)

        with st.expander("🏗️ SIT — Singapore Institute of Technology"):
            st.markdown("""
    SIT offers **applied degree programmes** with an integrated work-study model.
    While most SIT programmes are full-time, some are structured for working adults.

    **Work-Study Degree options:**
    - Typically 3–4 year programmes with industry placements built in
    - Employer-sponsored options available under SkillsFuture Work-Study Degree
    - Focus areas: Engineering, Health Sciences, ICT, Design, Hospitality

    **Entry:** Poly diploma (GPA 3.0+) or relevant industry experience

    **Fees (SC):** ~$3,000–$5,000/yr (after MOE subsidy) — comparable to SUSS

    🔗 [SIT Admissions](https://www.singaporetech.edu.sg/admissions)
            """)

        with st.expander("🏛️ NUS / NTU / SMU — Part-Time Options"):
            st.markdown("""
    The top 3 autonomous universities have **limited part-time undergraduate** options
    but offer more part-time postgraduate programmes.

    **Part-time undergraduate:**
    - **NUS** — Bachelor of Technology (BTech) in selected engineering fields, part-time over 4–5 years
    - **NTU** — Very limited part-time undergrad; mainly postgraduate and continuing education
    - **SMU** — No part-time undergrad; strong executive and postgraduate part-time offerings

    **Part-time postgraduate (all 3 universities):**
    - MBA (part-time): $50,000–$80,000 total, 2–3 years
    - Masters programmes in Business, IT, Engineering, Public Policy: $20,000–$50,000
    - Evening/weekend classes, typically 1.5–3 years

    **For working adults without a degree:**
    SUSS or private universities are usually the better part-time undergrad route.
            """)

        with st.expander("🏢 Private Universities — Overseas Partner Degrees"):
            st.markdown("""
    Private education institutions in Singapore partner with overseas universities to offer
    **part-time bachelor's degrees** with evening and weekend classes.

    | Institution | Partner University | Programmes | Duration | Fees (total) |
    |---|---|---|---|---|
    | **SIM Global Education** | University of London (UOL) | Business, IT, Accounting, Economics | 2–4 years | $15,000–$28,000 |
    | **SIM Global Education** | University of Birmingham | Business, Engineering | 2–3 years | $20,000–$35,000 |
    | **Kaplan Singapore** | Murdoch University | Business, IT, Psychology, Communications | 2–3 years | $22,000–$35,000 |
    | **Kaplan Singapore** | Northumbria University | Business, Engineering, Computing | 2–3 years | $20,000–$32,000 |
    | **PSB Academy** | La Trobe University | Business, IT, Engineering | 2–3 years | $22,000–$38,000 |
    | **PSB Academy** | Edinburgh Napier University | Business, Engineering, Hospitality | 2–3 years | $20,000–$30,000 |
    | **MDIS** | University of Sunderland | Business, Tourism, Engineering | 2–3 years | $18,000–$30,000 |

    **Important considerations:**
    - Ensure the programme is registered with CPE (Committee for Private Education)
    - Check if the degree is recognised by your target employers
    - SIM-UOL degrees are widely recognised in Singapore's job market
    - Some employers may treat private degrees differently from local university degrees
    - SkillsFuture Credit can be used for eligible programmes

    🔗 [CPE — List of Registered Institutions](https://www.ssg.gov.sg/cpe/pei.html)
            """)

        st.divider()
        st.markdown("## 💰 Funding & Financial Support")
        st.info("""
    **Singapore offers substantial subsidies for part-time education:**

    - **SkillsFuture Credit** — Every SC aged 25+ receives $500 (one-time top-ups periodically). Usable for approved courses at any provider.
    - **SkillsFuture Mid-Career Enhanced Subsidy** — SC aged 40+: up to **90% subsidy** on course fees for SSG-supported programmes.
    - **PSEA (Post-Secondary Education Account)** — SC students: government-deposited funds usable for approved part-time diplomas and degrees.
    - **CPF Education Scheme** — Use your CPF Ordinary Account to pay for approved part-time degree programmes.
    - **MOE Tuition Grant** — Available for SUSS, SIT part-time degrees (SC/PR: no bond; International: 3-year bond).
    - **Employer Sponsorship** — Many Work-Study programmes are employer-sponsored (employer pays fees + training allowance).
    - **NTUC Union Training Assistance Programme (UTAP)** — NTUC members: up to $500/yr for approved courses.
        """)

        st.divider()
        st.markdown("## 📊 Part-Time Study Comparison")
        _pt_compare = pd.DataFrame({
            "Provider": [
                "Poly Work-Study Diploma",
                "ITE Work-Study",
                "SUSS (Part-Time Degree)",
                "SIT (Work-Study Degree)",
                "SIM-UOL (Private Degree)",
                "Kaplan / PSB / MDIS",
            ],
            "Qualification": [
                "Polytechnic Diploma",
                "Higher NITEC / Tech Diploma",
                "Bachelor's Degree",
                "Bachelor's Degree (Applied)",
                "Bachelor's Degree (Overseas Uni)",
                "Bachelor's Degree (Overseas Uni)",
            ],
            "Duration": [
                "2–3 years", "1.5–2.5 years", "4–6 years",
                "3–4 years", "2–4 years", "2–3 years",
            ],
            "Schedule": [
                "Work + study days", "1–2 days/wk at ITE", "Evenings + Sat",
                "Work-integrated", "Evenings + weekends", "Evenings + weekends",
            ],
            "Fees (SC, approx)": [
                "$1,000–$3,000 total",
                "$500–$2,000 total",
                "$18,000–$27,000 total",
                "$15,000–$25,000 total",
                "$15,000–$28,000 total",
                "$20,000–$38,000 total",
            ],
            "Entry Requirement": [
                "NITEC / Higher NITEC",
                "NITEC or O/N-level + work exp",
                "Poly diploma (GPA 2.5+) or age 30+",
                "Poly diploma (GPA 3.0+)",
                "Poly diploma or A-levels",
                "Poly diploma or A-levels",
            ],
        })
        st.dataframe(_pt_compare, use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("## 🧭 Which Path is Right for Me?")
        st.markdown("""
    | Your Current Qualification | Recommended Part-Time Path | Next Step |
    |---|---|---|
    | **N-level / NITEC** | ITE Work-Study → Higher NITEC → Poly Work-Study Diploma | Check ITE work-study listings |
    | **O-level** | Poly Work-Study Diploma or private diploma (Kaplan/PSB/MDIS) | Apply to poly work-study or private institution |
    | **Higher NITEC** | Poly Work-Study Diploma → SUSS / SIT / private degree | Apply via SkillsFuture Work-Study |
    | **Poly Diploma** | SUSS part-time degree, SIT work-study, or SIM-UOL | Apply to SUSS (most flexible entry) |
    | **Working Adult (no diploma, age 30+)** | SUSS mature entry (8+ years work exp, no diploma needed) | Apply directly to SUSS |
    | **Career Changer (any qualification)** | SkillsFuture Career Transition Programme → industry cert → degree | Visit MySkillsFuture portal |
        """)

        st.success("""
    **Remember:** Part-time study takes longer, but it means you earn while you learn. Many employers
    in Singapore value the combination of a degree + work experience. A SUSS part-time BBA graduate
    with 6 years of work experience is highly employable — often more so than a fresh full-time graduate.
        """)

        st.markdown("### 🔗 Official Resources")
        pt_links = {
            "SkillsFuture Work-Study Programmes": "https://www.skillsfuture.gov.sg/initiatives/mid-career/workstudy",
            "SUSS Part-Time Programmes": "https://www.suss.edu.sg/programmes",
            "SIT Admissions": "https://www.singaporetech.edu.sg/admissions",
            "MySkillsFuture Portal": "https://www.myskillsfuture.gov.sg",
            "CPE Registered Institutions": "https://www.ssg.gov.sg/cpe/pei.html",
            "ITE Work-Study": "https://www.ite.edu.sg/admissions/work-study-programmes",
        }
        pt_cols = st.columns(3)
        for i, (name, url) in enumerate(pt_links.items()):
            pt_cols[i % 3].markdown(f"🔗 [{name}]({url})")


    # ── TAB 5: SUCCESS STORIES ──────────────────────────────────────────────────
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

    # ── TAB 5: SUPPORT & RESOURCES ─────────────────────────────────────────────
    with tab_support:
        st.subheader("🤝 Support & Resources")
        st.markdown("Singapore's official support network — counselling, scholarships, career guidance and work-study programmes.")

        try:
            from services.pathway_service import get_support_resources
            resources = get_support_resources()
        except Exception:
            resources = {}

        with st.expander("🧠 Counselling & Mental Health", expanded=True):
            st.info("Every MOE school has a trained counsellor. Sessions are free and confidential.")
            for item in resources.get("counselling", [])[:4]:
                st.markdown(f"- **{item['name']}** — {item.get('description','')[:120]}... [{item.get('how_to_access','See website')}]({item.get('official_url','')})")
            st.markdown("**Crisis lines:** SOS 1-767 (24h) · IMH 6389-2222 (24h) · CHAT youth: chat.mentalhealth.sg")

        with st.expander("🧭 Career & Education Guidance"):
            st.info("ECG counsellors are in every secondary school, JC, poly and ITE — free sessions.")
            for item in resources.get("career_guidance", [])[:4]:
                st.markdown(f"- **{item['name']}** — {item.get('description','')[:120]}...")
            st.markdown("[MySkillsFuture Career Profiler →](https://www.myskillsfuture.gov.sg/content/student/en/secondary.html)")

        with st.expander("🏆 Scholarships & Bursaries"):
            role = user.get("role", "student")
            if role == "parent":
                st.caption("💡 You can apply for most scholarships on behalf of your child.")
            for item in resources.get("scholarships", [])[:6]:
                value = f" · **{item.get('value','')}**" if item.get("value") else ""
                st.markdown(f"- **{item['name']}** ({item.get('type','')}) — {item.get('eligibility','')[:100]}{value}")
            st.markdown("**Community SHGs:** [Mendaki](https://www.mendaki.org.sg) · [CDAC](https://www.cdac.org.sg) · [SINDA](https://www.sinda.org.sg)")

        with st.expander("💼 Earn & Learn Programmes"):
            st.info("Work-study programmes: earn a salary while completing a qualification.")
            for item in resources.get("earn_and_learn", [])[:4]:
                st.markdown(f"- **{item['name']}** — {item.get('description','')[:120]}...")
            st.markdown("[SkillsFuture Earn & Learn →](https://www.skillsfuture.gov.sg/initiatives/mid-career/earningandlearning)")

    st.markdown("""
    <div class="gov-footer">
    <a href="https://www.moe.gov.sg">MOE</a> ·
    <a href="https://www.seab.gov.sg">SEAB</a> ·
    <a href="https://www.ite.edu.sg">ITE</a> ·
    <a href="https://www.skillsfuture.gov.sg">SkillsFuture</a><br>
    <small>EduPath SG is an AI Champion Bootcamp capstone project. Not affiliated with the Singapore Government.</small>
    </div>
    """, unsafe_allow_html=True)

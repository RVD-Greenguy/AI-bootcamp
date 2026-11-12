import streamlit as st

st.set_page_config(page_title="Primary School Hub — EduPath SG", page_icon="🏫", layout="wide")

import pandas as pd
from utils.session_manager import require_login
from utils.config import DISCLAIMER
from components.sidebar import render_sidebar
from components.chat_panel import render_chat_panel
from components.stage_theme import apply_stage_theme

user = require_login()
render_sidebar()
render_chat_panel()
apply_stage_theme()

st.title("🏫 Primary School Hub")
st.caption("P1 registration, school options, transfer policies, and PSLE guidance.")
st.warning(f"⚠️ {DISCLAIMER}", icon="⚠️")

tab_p1, tab_schools, tab_transfer, tab_psle = st.tabs([
    "📋 P1 Registration",
    "🏫 Primary Schools",
    "🔄 Transfer & Support",
    "📊 PSLE Guide",
])

# ── TAB 1: P1 REGISTRATION ───────────────────────────────────────────────────
with tab_p1:
    st.subheader("📋 P1 Registration Phases")
    st.markdown(
        "Singapore primary school P1 registration is conducted in phases. "
        "Earlier phases have higher priority. If a school is oversubscribed in any phase, "
        "a **ballot** is held — with Singapore Citizens given priority over PRs."
    )

    phases_html = """
    <style>
    .phase-table { width:100%; border-collapse:collapse; font-family:sans-serif; font-size:14px; }
    .phase-table th { background:#1565C0; color:white; padding:10px 12px; text-align:left; }
    .phase-table td { padding:9px 12px; border-bottom:1px solid #e2e8f0; vertical-align:top; }
    .phase-table tr:nth-child(even) td { background:#f0f4fb; }
    .badge { display:inline-block; padding:2px 8px; border-radius:12px; font-size:12px; font-weight:600; }
    .p1 { background:#dbeafe; color:#1e40af; }
    .p2a1 { background:#ede9fe; color:#5b21b6; }
    .p2a2 { background:#fce7f3; color:#9d174d; }
    .p2b { background:#d1fae5; color:#065f46; }
    .p2c { background:#fef3c7; color:#92400e; }
    .p2cs { background:#ffedd5; color:#9a3412; }
    .p3 { background:#fee2e2; color:#991b1b; }
    </style>
    <table class="phase-table">
      <tr>
        <th>Phase</th><th>Who qualifies</th><th>Distance priority?</th><th>Ballot?</th>
      </tr>
      <tr>
        <td><span class="badge p1">Phase 1</span></td>
        <td>Child has a sibling currently studying in the school</td>
        <td>Not applicable</td>
        <td>No ballot</td>
      </tr>
      <tr>
        <td><span class="badge p2a1">Phase 2A(1)</span></td>
        <td>Parent is a former student (alumni) of the school <strong>or</strong> parent is currently serving as a staff member</td>
        <td>Not applicable</td>
        <td>Ballot if oversubscribed (SC before PR)</td>
      </tr>
      <tr>
        <td><span class="badge p2a2">Phase 2A(2)</span></td>
        <td>Parent is an active community leader endorsed by an MP, RC Chairman, or grassroots organisation affiliated with the school</td>
        <td>Not applicable</td>
        <td>Ballot if oversubscribed (SC before PR)</td>
      </tr>
      <tr>
        <td><span class="badge p2b">Phase 2B</span></td>
        <td>Parent is an active community leader (non-school-affiliated) endorsed by school or church/temple connected to the school <strong>or</strong> child lives within 1 km of the school</td>
        <td>✅ Within 1 km = highest priority within this phase</td>
        <td>Ballot if oversubscribed (SC before PR, then distance)</td>
      </tr>
      <tr>
        <td><span class="badge p2c">Phase 2C</span></td>
        <td>All Singapore Citizens and Permanent Residents not yet registered</td>
        <td>✅ Within 1 km priority, then 1–2 km</td>
        <td>Ballot if oversubscribed (SC before PR, then distance)</td>
      </tr>
      <tr>
        <td><span class="badge p2cs">Phase 2C Supp.</span></td>
        <td>Singapore Citizens only who were not placed in Phase 2C</td>
        <td>Distance considered</td>
        <td>Ballot</td>
      </tr>
      <tr>
        <td><span class="badge p3">Phase 3</span></td>
        <td>International Students (non-Singapore Citizens / PRs)</td>
        <td>Not applicable</td>
        <td>Subject to vacancy; apply through school directly</td>
      </tr>
    </table>
    """
    st.html(phases_html)

    st.divider()
    st.markdown("### 📅 Approximate P1 Registration Timeline")
    timeline_data = [
        ("May–June", "MOE announces P1 registration exercise for following year", "MOE"),
        ("Mid July", "Phase 1 registration opens", "MOE / School"),
        ("Late July", "Phase 2A(1) registration", "MOE / School"),
        ("Early August", "Phase 2A(2) registration", "MOE / School"),
        ("Mid August", "Phase 2B registration", "MOE / School"),
        ("Late August", "Phase 2C registration (most families)", "MOE / School"),
        ("Early September", "Phase 2C Supplementary registration", "MOE"),
        ("October–November", "Phase 3 (International students)", "Individual schools"),
        ("January (following year)", "Child starts Primary 1", "School"),
    ]
    tl_df = pd.DataFrame(timeline_data, columns=["Period", "Event", "Authority"])
    st.dataframe(tl_df, use_container_width=True, hide_index=True)

    st.divider()
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.info("""
**Distance Priority Rules**
- **Within 1 km** of school: Highest priority in Phase 2B and 2C balloting
- **1–2 km** from school: Next priority tier in Phase 2C
- Beyond 2 km: No distance advantage; purely ballot order

Distance is measured from home address to school gate using straight-line distance.
        """)
    with col_n2:
        st.info("""
**Reserved Places per Phase**
- At least **40 places** are reserved for Singapore Citizens in each phase through 2C
- This means even popular schools must retain spaces for citizens at each phase
- Balloting sequence: **SC first → PR → distance tier → computerised random**

Always register as early in the process as your eligibility allows.
        """)

    st.markdown("🔗 [Official MOE P1 Registration Information](https://www.moe.gov.sg/primary/p1-registration)")


# ── TAB 2: PRIMARY SCHOOLS ───────────────────────────────────────────────────
with tab_schools:
    st.subheader("🏫 Singapore Primary Schools Directory")

    try:
        from services.pathway_service import get_primary_schools
        schools = get_primary_schools()
    except Exception:
        schools = []

    if not schools:
        st.warning("Primary schools data not available. Check data/seed/primary_schools.json.")
    else:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            type_filter = st.multiselect(
                "School type:",
                ["government", "government_aided", "sap"],
                default=["government", "government_aided", "sap"],
                format_func=lambda x: {"government": "Government", "government_aided": "Govt-Aided", "sap": "SAP (Chinese-medium)"}[x],
            )
        with col_f2:
            location_filter = st.multiselect(
                "Location:",
                ["North", "South", "East", "West", "Central", "Northeast", "Northwest"],
                default=["North", "South", "East", "West", "Central", "Northeast", "Northwest"],
            )
        with col_f3:
            gender_filter = st.selectbox("Gender:", ["All", "Mixed", "Boys only", "Girls only"])

        filtered = []
        for s in schools:
            t = s.get("type", "")
            is_sap = s.get("is_sap", False)
            effective_type = "sap" if is_sap else t
            if effective_type not in type_filter:
                continue
            if s.get("location", "") not in location_filter:
                continue
            g = s.get("gender", "mixed")
            if gender_filter == "Boys only" and g != "boys":
                continue
            if gender_filter == "Girls only" and g != "girls":
                continue
            if gender_filter == "Mixed" and g != "mixed":
                continue
            filtered.append(s)

        st.caption(f"Showing {len(filtered)} of {len(schools)} schools")

        if filtered:
            TYPE_LABEL = {"government": "Government", "government_aided": "Govt-Aided", "sap": "SAP"}
            GENDER_LABEL = {"mixed": "Mixed", "boys": "Boys", "girls": "Girls"}
            rows = []
            for s in filtered:
                t = "SAP" if s.get("is_sap") else TYPE_LABEL.get(s.get("type", ""), s.get("type", ""))
                rows.append({
                    "School": s["name"],
                    "Type": t,
                    "Gender": GENDER_LABEL.get(s.get("gender", "mixed"), "Mixed"),
                    "Location": s.get("location", ""),
                    "Notable": s.get("notable", ""),
                    "URL": s.get("official_url", ""),
                })
            df = pd.DataFrame(rows)
            st.dataframe(
                df[["School", "Type", "Gender", "Location", "Notable"]],
                use_container_width=True,
                hide_index=True,
            )

            st.divider()
            st.markdown("### School Details")
            for s in filtered[:20]:
                with st.expander(f"**{s['name']}** — {s.get('location','')} · {s.get('gender','mixed').title()}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**Type:** {'SAP' if s.get('is_sap') else s.get('type','').replace('_',' ').title()}")
                        st.markdown(f"**Gender:** {s.get('gender','mixed').title()}")
                        st.markdown(f"**Location:** {s.get('location','')}")
                    with c2:
                        st.markdown(f"**Notable:** {s.get('notable','')}")
                        if s.get("official_url"):
                            st.markdown(f"[Official website →]({s['official_url']})")
        else:
            st.info("No schools match the current filters.")


# ── TAB 3: TRANSFER & SUPPORT ────────────────────────────────────────────────
with tab_transfer:
    st.subheader("🔄 Transfer Requests & Learning Support")

    with st.expander("📦 School Transfers — When and How", expanded=True):
        st.markdown("""
**Within P1–P2 (easiest):**
Families who have recently moved home can request a transfer to a school closer to the new address.
MOE facilitates these transfers subject to vacancy at the receiving school.

**After P2 (more restricted):**
Transfers are considered on a case-by-case basis. Accepted reasons include:
- Family relocation (new HDB/condo purchase)
- Medical or psychological grounds with documentation
- Parents' work transfer requiring family relocation

**Important rules:**
- Transfers during **P6 (PSLE year)** are generally **not approved**
- Transfers do not reset P1 priority; the original registration phase still applies
- Contact **MOE Customer Service (1800-2255-942)** or the receiving school directly

🔗 [MOE School Transfer Information](https://www.moe.gov.sg/primary/transfers)
        """)

    with st.expander("📚 Learning Support Programme (LSP)", expanded=False):
        st.markdown("""
**What it is:** The Learning Support Programme identifies P1 and P2 students who need extra help
with English literacy and Mathematics. Schools administer a screening in January of P1.

**How it works:**
- Identified students join small-group support classes (usually 8–10 per group)
- Conducted by trained Learning Support Coordinators (LSCs)
- **Completely free** — no additional cost to parents
- Opt-in: parents can discuss with the school whether participation suits their child

**Who it helps:**
- Students with early reading or numeracy difficulties
- Students adjusting to English as a second language
- Students who benefit from more structured, small-group instruction

**After LSP:** Most students transition back to mainstream classes by P3. Some continue with
additional support through the School-based Dyslexia Remediation (SDR) programme if needed.

🔗 [MOE Learning Support](https://www.moe.gov.sg/primary/curriculum/learning-support)
        """)

    with st.expander("📐 Subject-Based Banding (SBB) at Primary Level", expanded=False):
        st.markdown("""
**What it is:** From **P5 onwards**, students can take different subjects at different difficulty levels
(Standard or Foundation) based on their strengths.

**How it works:**
- P4 results determine initial SBB placement in P5
- Students can take, for example, Standard English + Standard Maths + Foundation Science
- Each subject is assessed independently — no "streaming" into a fixed band
- Foundation subjects are graded differently: highest grade is AL C (not AL A)

**Key point:** Foundation subjects are capped at AL C in PSLE aggregate calculation.
Taking Foundation MT (Mother Tongue Language) can lower the total AL significantly,
which affects secondary school stream placement.

**Appeal process:** Parents can discuss subject levels with the form teacher at P4 year-end.

🔗 [MOE Subject-Based Banding](https://www.moe.gov.sg/primary/curriculum/subject-based-banding)
        """)

    with st.expander("🏥 If Your Child is Struggling — Support Options", expanded=False):
        st.markdown("""
**Within school:**
- Request a meeting with the **form teacher** or **Subject Head**
- Ask about the **Learning Support Programme (LSP)** or **School-based Dyslexia Remediation (SDR)**
- Referral to the **School Counsellor** (every MOE school has one)
- **FAS (Financial Assistance Scheme)** covers tuition fees, school meals, and uniforms for qualifying families

**External support:**
- MOE-subsidised student care centres (before/after school programmes)
- Community-based tuition via **ComCare** and **Student Care Centres**
- **SHINE Children and Youth Services** — tuition and mentoring for lower-income students
- **SG Cares Volunteer Centres** — community tuition matching

**If learning differences are suspected:**
- Speak to school's Allied Educator (Learning & Behavioural Support)
- Early referral to the **Child Guidance Clinic (CGC)** for assessment (dyslexia, ADHD, autism)
- **SPED Schools** for children with more significant learning needs:
  - Pathlight School (autism spectrum)
  - MINDS schools (intellectual disability)
  - Dyslexia Association of Singapore (DAS) centres
  - Movement for the Intellectually Disabled of Singapore (MINDS)

🔗 [MOE Special Education](https://www.moe.gov.sg/special-education)
        """)


# ── TAB 4: PSLE GUIDE ───────────────────────────────────────────────────────
with tab_psle:
    st.subheader("📊 PSLE — Primary School Leaving Examination Guide")
    st.markdown(
        "PSLE is taken at the end of Primary 6. Since 2021, results use **Achievement Levels (AL)** "
        "instead of T-scores. Lower total AL = better result."
    )

    # Subjects
    st.markdown("### 📚 PSLE Subjects")
    subj_col1, subj_col2 = st.columns(2)
    with subj_col1:
        st.markdown("""
**Four subjects:**
1. **English Language** (EL) — compulsory, Standard level only
2. **Mother Tongue Language** (MTL) — compulsory; Standard or Foundation
3. **Mathematics** — Standard or Foundation
4. **Science** — Standard or Foundation
        """)
    with subj_col2:
        st.markdown("""
**Special cases:**
- **Higher Mother Tongue (HMT):** Optional add-on for strong MTL students; contributes bonus AL points
- **MTL Exemption:** Students with significant difficulties may apply for exemption
- **Foreign Language:** Approved foreign languages (French, German, Japanese, etc.) can replace MTL
        """)

    st.divider()

    # AL scoring table
    st.markdown("### 🎯 Achievement Level (AL) Scoring")
    al_data = [
        ("AL 1", "90 – 100", "Distinction", "#166534", "#dcfce7"),
        ("AL 2", "85 – 89", "Distinction", "#166534", "#dcfce7"),
        ("AL 3", "80 – 84", "Merit", "#1e40af", "#dbeafe"),
        ("AL 4", "75 – 79", "Merit", "#1e40af", "#dbeafe"),
        ("AL 5", "65 – 74", "Pass", "#854d0e", "#fef3c7"),
        ("AL 6", "45 – 64", "Pass", "#854d0e", "#fef3c7"),
        ("AL 7", "20 – 44", "Pass", "#9a3412", "#ffedd5"),
        ("AL 8", "Below 20", "Needs improvement", "#991b1b", "#fee2e2"),
    ]

    al_html = """
    <style>
    .al-table { width:100%; border-collapse:collapse; font-family:sans-serif; font-size:14px; }
    .al-table th { background:#1565C0; color:white; padding:8px 12px; text-align:left; }
    .al-table td { padding:8px 12px; border-bottom:1px solid #e2e8f0; }
    </style>
    <table class="al-table">
      <tr><th>AL</th><th>Score Range (%)</th><th>Grade Label</th></tr>
    """
    for al, score, label, color, bg in al_data:
        al_html += f'<tr><td><span style="font-weight:700;color:{color};background:{bg};padding:2px 8px;border-radius:8px">{al}</span></td><td>{score}</td><td>{label}</td></tr>'
    al_html += "</table>"
    st.html(al_html)

    st.markdown("""
> **Foundation subjects** are scored on a compressed scale:
> AL A = AL 1–4 equivalent, AL B = AL 5–6, AL C = AL 7–8.
> The highest possible Foundation grade converts to **AL C** in PSLE aggregate — it cannot achieve AL 1–6.
    """)

    st.divider()

    # Total score and stream placement
    st.markdown("### 🏫 Total AL Score & Secondary School Stream Placement")
    stream_data = {
        "Total AL Score": ["4 – 20", "21 – 22", "23 – 32"],
        "Secondary Stream": ["Express", "Normal Academic (N(A))", "Normal Technical (N(T))"],
        "Leads to": ["O-levels (Sec 4) / IP (6-year)", "N(A)-levels (Sec 4), then Sec 5 O-levels or PFP", "N(T)-levels → ITE NITEC"],
        "University pathway": ["JC → A-levels → Uni / Poly → DAE", "PFP → Poly → University", "ITE → Higher NITEC → Poly → Uni"],
    }
    st.dataframe(pd.DataFrame(stream_data), use_container_width=True, hide_index=True)

    st.info("""
💡 **Key tips:**
- **IP schools** (Integrated Programme) take students with AL 4–8 typically; they skip O-levels entirely
- If Foundation MTL is taken, the PSLE aggregate uses a converted score — plan carefully with the school
- Appeals for secondary school placement can be made within **3 days** of PSLE posting release
- An AL score of 20 or below qualifies for Express stream, but very popular IP schools may require AL 8 or below
    """)

    st.divider()
    st.markdown("### 🔗 Official Resources")
    for label, url in [
        ("SEAB PSLE Information", "https://www.seab.gov.sg/home/examinations/psle"),
        ("MOE PSLE Scoring System", "https://www.moe.gov.sg/primary/assessment/psle/scoring"),
        ("MOE Secondary School Posting", "https://www.moe.gov.sg/primary/assessment/psle/secondary-school-posting"),
        ("DSA-Sec (Direct School Admission)", "https://www.moe.gov.sg/secondary/dsa"),
    ]:
        st.markdown(f"🔗 [{label}]({url})")

import streamlit as st

st.set_page_config(page_title="Score & School Matcher — EduPath SG", page_icon="🎯", layout="wide")

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from utils.session_manager import require_login
from utils.config import DISCLAIMER
from components.sidebar import render_sidebar
from services.score_service import (
    psle_al_to_stream, match_secondary_schools,
    calculate_l1r5, calculate_elr2b2, match_jcs, match_poly_courses,
    calculate_rank_points, match_universities, match_universities_dae,
)

user = require_login()
render_sidebar()

st.title("🎯 Score & School Matcher")
st.caption("Enter your exam scores to see which schools and programmes you qualify for.")
st.warning(f"⚠️ {DISCLAIMER}", icon="⚠️")
st.info("All cutoff figures are **approximate** based on recent years. Actual cutoffs vary annually — always verify at the school's official website or MOE.")

GRADE_OPTIONS = ["A1", "A2", "B3", "B4", "C5", "C6", "D7", "E8", "F9"]
GRADE_POINTS = {"A1": 1, "A2": 2, "B3": 3, "B4": 4, "C5": 5, "C6": 6, "D7": 7, "E8": 8, "F9": 9}

tab_psle, tab_olevels, tab_alevels, tab_dae = st.tabs([
    "📊 PSLE → Secondary School",
    "🏫 O-levels → JC / Poly / ITE (JAE)",
    "🎓 A-levels → University",
    "📜 Poly Diploma → University (DAE)",
])

# ── TAB 1: PSLE ──────────────────────────────────────────────────────────────
with tab_psle:
    st.subheader("📊 PSLE Achievement Level → Secondary School")

    with st.expander("ℹ️ How PSLE AL scoring works", expanded=False):
        st.markdown("""
        Since 2021, PSLE uses Achievement Levels (AL) instead of T-scores:
        - Each of the **4 subjects** is graded **AL1 (best) to AL8 (weakest)**
        - Your **total AL = sum of all 4 subject ALs** (range: **4–32**, lower = better)
        - The total determines your secondary school stream
        """)
        al_table = pd.DataFrame({
            "Total AL Score": ["4–20", "21–22", "23–32"],
            "Stream": ["Express", "Normal Academic (N(A))", "Normal Technical (N(T))"],
            "Notes": [
                "Top scorers (AL 4–8) may qualify for IP schools. All express students sit O-levels at Sec 4 (unless in IP).",
                "Sit N(A)-levels at Sec 4. Can proceed to Sec 5 O-levels or apply for PFP (Polytechnic Foundation Programme).",
                "Sit N(T)-levels. Direct progression to ITE.",
            ]
        })
        st.dataframe(al_table, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        al_score = st.slider("Your PSLE total AL score:", min_value=4, max_value=32, value=12, step=1)
    with col2:
        gender_pref = st.selectbox("Gender preference:", ["Any", "Boys", "Girls"])
    with col3:
        prefer_ip = st.checkbox("Show IP schools only")

    stream_result = psle_al_to_stream(al_score)
    if al_score <= 20:
        st.success(f"**Stream: {stream_result['stream']}** — {stream_result['note']}")
    elif al_score <= 22:
        st.info(f"**Stream: {stream_result['stream']}** — {stream_result['note']}")
    else:
        st.warning(f"**Stream: {stream_result['stream']}** — {stream_result['note']}")

    schools = match_secondary_schools(al_score, gender_pref, prefer_ip)

    if schools:
        st.markdown(f"**{len(schools)} schools matched for AL {al_score}:**")

        # Bar chart
        df_s = pd.DataFrame(schools)
        df_s["cutoff_mid"] = df_s.apply(
            lambda r: (r.get("psle_al_cutoff_min", 0) + r.get("psle_al_cutoff_max", 0)) / 2, axis=1
        )
        df_s["ip_label"] = df_s["is_ip"].apply(lambda x: "IP School" if x else "Non-IP")
        fig = px.bar(
            df_s.head(15), x="name", y="cutoff_mid", color="ip_label",
            color_discrete_map={"IP School": "#1565C0", "Non-IP": "#42A5F5"},
            labels={"name": "School", "cutoff_mid": "AL Cutoff (midpoint)", "ip_label": "Type"},
            title="Matching Secondary Schools by AL Cutoff",
        )
        fig.add_hline(y=al_score, line_dash="dash", line_color="red",
                      annotation_text=f"Your score: {al_score}")
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=400, margin=dict(b=120))
        st.plotly_chart(fig, use_container_width=True)

        # Table
        display_cols = ["name", "type", "is_ip", "ip_end_qual", "location", "gender", "fit"]
        display_df = df_s[[c for c in display_cols if c in df_s.columns]].copy()
        display_df.columns = [c.replace("_", " ").title() for c in display_df.columns]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No schools matched. Try adjusting your score or removing filters.")

    st.caption("Note: Cutoffs vary each year based on cohort performance. IP schools may also use interviews, aptitude tests or other criteria.")

# ── TAB 2: O-LEVELS → JAE ────────────────────────────────────────────────────
with tab_olevels:
    st.subheader("🏫 O-level Results → JAE (JC / Poly / ITE)")

    jc_col, poly_col = st.columns(2)

    # ── L1R5 for JC ──
    with jc_col:
        st.markdown("### 📐 L1R5 Calculator (for JC)")
        with st.expander("ℹ️ How L1R5 works"):
            st.markdown("""
            **L1** = English Language grade
            **R5** = Best 5 relevant subjects (must include ≥1 humanities AND ≥1 maths/science)
            Grade points: A1=1, A2=2, B3=3 ... F9=9 *(lower = better)*
            **Net L1R5** = Raw − CCA bonus (up to −2) − Affiliation bonus (−2)
            Minimum net L1R5 = **2**. Eligible for JC if net ≤ 20.
            """)

        g_eng   = st.selectbox("English Language:", GRADE_OPTIONS, index=2, key="l_eng")
        g_hum   = st.selectbox("Best Humanities subject:", GRADE_OPTIONS, index=2, key="l_hum")
        g_ms    = st.selectbox("Best Maths/Science subject:", GRADE_OPTIONS, index=1, key="l_ms")
        g_s4    = st.selectbox("Subject 4:", GRADE_OPTIONS, index=2, key="l_s4")
        g_s5    = st.selectbox("Subject 5:", GRADE_OPTIONS, index=3, key="l_s5")
        g_s6    = st.selectbox("Subject 6:", GRADE_OPTIONS, index=4, key="l_s6")
        cca_b   = st.selectbox("CCA bonus points:", [0, 1, 2], key="l_cca")
        aff_b   = st.selectbox("Affiliation bonus points:", [0, 2], key="l_aff")

        l1r5 = calculate_l1r5(
            GRADE_POINTS[g_eng], GRADE_POINTS[g_hum], GRADE_POINTS[g_ms],
            GRADE_POINTS[g_s4], GRADE_POINTS[g_s5], GRADE_POINTS[g_s6],
            cca_b, aff_b,
        )

        m1, m2 = st.columns(2)
        m1.metric("Raw L1R5", l1r5["raw_l1r5"])
        m2.metric("Net L1R5 (after bonus)", l1r5["net_l1r5"])

        if l1r5["eligible_for_jc"]:
            st.success(l1r5["note"])
        else:
            st.warning(l1r5["note"])
            st.info("Consider polytechnic (ELR2B2) or ITE as alternatives.")

        jcs = match_jcs(l1r5["net_l1r5"])
        if jcs:
            st.markdown(f"**{len(jcs)} JCs matched:**")
            jc_df = pd.DataFrame([{
                "JC": j.get("name", j.get("short_name", "")),
                "Cutoff (net L1R5)": j.get("l1r5_cutoff_2023", ""),
                "Fit": j.get("fit", ""),
                "Affiliated Schools": ", ".join(j.get("affiliation_schools", [])[:2]),
            } for j in jcs])

            colours_jc = ["#2ecc71" if "Comfort" in r else ("#f39c12" if "Within" in r else "#e74c3c")
                          for r in jc_df["Fit"]]
            fig_jc = go.Figure(go.Bar(
                x=jc_df["JC"], y=[j.get("l1r5_cutoff_2023", 0) if isinstance(j.get("l1r5_cutoff_2023"), (int, float)) else 0 for j in jcs],
                marker_color=colours_jc,
                text=jc_df["Fit"], textposition="outside",
            ))
            fig_jc.add_hline(y=l1r5["net_l1r5"], line_dash="dash", line_color="blue",
                             annotation_text=f"Your net: {l1r5['net_l1r5']}")
            fig_jc.update_layout(title="JC Eligibility", xaxis_tickangle=45,
                                 yaxis_title="L1R5 Cutoff", height=350, margin=dict(b=100))
            st.plotly_chart(fig_jc, use_container_width=True)
            st.dataframe(jc_df, use_container_width=True, hide_index=True)

    # ── ELR2B2 for Poly ──
    with poly_col:
        st.markdown("### 📐 ELR2B2 Calculator (for Poly)")
        with st.expander("ℹ️ How ELR2B2 works"):
            st.markdown("""
            **E** = English | **L** = 2nd Language or relevant subject
            **R2** = 2 relevant subjects | **B2** = 2 best other subjects
            Lower aggregate = more competitive. English must be ≥ C6 for most courses.
            """)

        p_eng  = st.selectbox("English Language:", GRADE_OPTIONS, index=2, key="p_eng")
        p_l2   = st.selectbox("2nd Language / Relevant subject:", GRADE_OPTIONS, index=2, key="p_l2")
        p_r1   = st.selectbox("Relevant subject 1:", GRADE_OPTIONS, index=1, key="p_r1")
        p_r2   = st.selectbox("Relevant subject 2:", GRADE_OPTIONS, index=2, key="p_r2")
        p_b1   = st.selectbox("Best other subject 1:", GRADE_OPTIONS, index=2, key="p_b1")
        p_b2   = st.selectbox("Best other subject 2:", GRADE_OPTIONS, index=3, key="p_b2")
        p_int  = st.text_input("Interest area (optional filter):", key="p_interest")

        elr2b2_r = calculate_elr2b2(
            GRADE_POINTS[p_eng], GRADE_POINTS[p_l2],
            GRADE_POINTS[p_r1], GRADE_POINTS[p_r2],
            GRADE_POINTS[p_b1], GRADE_POINTS[p_b2],
        )

        st.metric("ELR2B2 Aggregate", elr2b2_r["elr2b2"])
        if elr2b2_r["english_pass"]:
            st.success(elr2b2_r["note"])
        else:
            st.warning(elr2b2_r["note"])

        poly_matches = match_poly_courses(elr2b2_r["elr2b2"], p_int)
        if poly_matches:
            st.markdown(f"**{len(poly_matches)} poly courses matched:**")
            poly_df = pd.DataFrame([{
                "Polytechnic": c.get("poly_name", ""),
                "Course": c.get("course_name", ""),
                "ELR2B2 Cutoff": c.get("elr2b2_cutoff_approximate", ""),
                "Fit": c.get("fit", ""),
            } for c in poly_matches])
            st.dataframe(poly_df, use_container_width=True, hide_index=True)

    st.divider()
    st.info("**ITE pathway:** If L1R5 > 20 and ELR2B2 is high, consider ITE (NITEC or Higher NITEC). Entry requires N-level or O-level passes. ITE graduates can progress to polytechnic.")

# ── TAB 3: A-LEVELS → UNIVERSITY ─────────────────────────────────────────────
with tab_alevels:
    st.subheader("🎓 A-level Rank Points → University")

    with st.expander("ℹ️ How University Admission Score (UAS) works"):
        pts_df = pd.DataFrame({
            "Grade": ["A", "B", "C", "D", "E", "S/U"],
            "H2 Points": [20, 17.5, 15, 12.5, 10, 0],
            "H1 Points": [10, 8.75, 7.5, 6.25, 5, 0],
        })
        st.markdown("**Formula:** H1 GP + best 3 H2 subjects + H1 MTL (capped at 10) = max **90 points**")
        st.dataframe(pts_df, use_container_width=True, hide_index=True)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        ALEVEL_GRADES = ["A", "B", "C", "D", "E", "S", "U"]
        h1_gp  = st.selectbox("H1 General Paper (GP):", ALEVEL_GRADES, key="gp")
        h2_1   = st.selectbox("H2 Subject 1:", ALEVEL_GRADES, key="h2_1")
        h2_2   = st.selectbox("H2 Subject 2:", ALEVEL_GRADES, index=1, key="h2_2")
        h2_3   = st.selectbox("H2 Subject 3:", ALEVEL_GRADES, index=2, key="h2_3")
        h1_mtl = st.selectbox("H1 Mother Tongue Language:", ALEVEL_GRADES, key="mtl")
        uni_int = st.text_input("Interest / faculty area:", placeholder="e.g. Computer Science, Medicine")

    rp = calculate_rank_points(h1_gp, h2_1, h2_2, h2_3, h1_mtl)

    with col_b:
        st.metric("Your UAS", f"{rp['rank_points']} / 90")
        for k, v in rp["breakdown"].items():
            st.caption(f"{k}: {v}")

    st.markdown(f"*{rp['note']}*")

    uni_matches = match_universities(rp["rank_points"], uni_int)
    if uni_matches:
        st.markdown(f"**{len(uni_matches)} programmes matched:**")
        uni_df = pd.DataFrame([{
            "University": m["university"],
            "Faculty / Course": m["faculty"],
            "Min Rank Points": m["min_rank_points"],
            "Duration": m.get("course_duration", ""),
            "Fit": m["fit"],
        } for m in uni_matches])

        fig_uni = px.scatter(
            uni_df, x="Min Rank Points", y="University",
            color="Fit", size_max=14,
            color_discrete_map={"Eligible": "#2ecc71", "Borderline / competitive": "#f39c12"},
            hover_data=["Faculty / Course", "Duration"],
            title="University Programmes by Rank Points Requirement",
        )
        fig_uni.add_vline(x=rp["rank_points"], line_dash="dash", line_color="blue",
                          annotation_text=f"Your UAS: {rp['rank_points']}")
        fig_uni.update_layout(height=400)
        st.plotly_chart(fig_uni, use_container_width=True)
        st.dataframe(uni_df, use_container_width=True, hide_index=True)
    else:
        st.info("No matches found. Try adjusting your grades or removing the interest filter.")

# ── TAB 4: POLY → DAE ────────────────────────────────────────────────────────
with tab_dae:
    st.subheader("📜 Polytechnic Diploma → University (DAE)")

    st.markdown("""
    **Direct Admissions Exercise (DAE)** allows polytechnic graduates to apply directly to university
    based on their **GPA** (Grade Point Average, 0–4.0 scale), portfolio, and sometimes an interview.

    - Applications open **March–April** each year
    - Results typically released **May–June**
    - Competitive courses (Medicine, Law, Dentistry) rarely offered via DAE
    """)

    dcol1, dcol2 = st.columns(2)
    with dcol1:
        gpa = st.slider("Your Poly GPA:", min_value=0.0, max_value=4.0, value=3.2, step=0.05)
        poly_name = st.selectbox("Your Polytechnic:", ["SP", "TP", "NYP", "NP", "RP"])
    with dcol2:
        diploma = st.text_input("Your Diploma course:", placeholder="e.g. Business Studies")
        dae_int = st.text_input("Interest area:", placeholder="e.g. Business, Engineering, IT")

    gpa_colour = "green" if gpa >= 3.5 else ("orange" if gpa >= 3.0 else "red")
    st.markdown(
        f"<h3 style='color:{gpa_colour};'>GPA: {gpa:.2f} / 4.00</h3>",
        unsafe_allow_html=True,
    )
    if gpa >= 3.5:
        st.success("Strong GPA — eligible for most DAE programmes including competitive options.")
    elif gpa >= 3.0:
        st.info("Good GPA — eligible for most programmes. Competitive courses may require portfolio/interview.")
    else:
        st.warning("GPA below 3.0 — consider SIT or SUSS which have broader intake, or SkillsFuture courses.")

    dae_matches = match_universities_dae(gpa, dae_int)
    if dae_matches:
        st.markdown(f"**{len(dae_matches)} university programmes matched:**")
        dae_df = pd.DataFrame([{
            "University": m["university"],
            "Faculty / Course": m["faculty"],
            "Min GPA": m["min_gpa"],
            "Duration": m.get("course_duration", ""),
            "Fit": m["fit"],
        } for m in dae_matches])
        st.dataframe(dae_df, use_container_width=True, hide_index=True)

        st.caption("💡 SIT and SUSS have the broadest DAE intake. NUS/NTU/SMU are more competitive and may require interviews.")
    else:
        st.info("No matches found. Adjust your GPA or interest area.")

    st.divider()
    with st.expander("📋 DAE vs SNUFA — What's the difference?"):
        st.markdown("""
        | | **DAE (Poly graduates)** | **SNUFA (A-level / IB)** |
        |---|---|---|
        | **Applicants** | Polytechnic diploma holders | A-level / IB / other pre-university |
        | **Main criteria** | GPA + portfolio + interview | Rank points (UAS) |
        | **Timing** | March–April application | April–May application |
        | **Result** | May–June | June–July |
        | **Advance standing** | May get credit exemptions | Standard Year 1 entry |
        """)

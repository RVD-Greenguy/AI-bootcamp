"""
Score calculation and school/course matching engine.
Handles: PSLE AL, L1R5 (O-levels → JC), ELR2B2 (O-levels → Poly),
         A-level rank points → University, Poly GPA → DAE.
"""
from services.pathway_service import (
    get_secondary_schools, get_jc_data,
    get_poly_courses, get_university_data, get_ite_data
)


# ── PSLE ─────────────────────────────────────────────────────────────────────

def psle_al_to_stream(al_score: int) -> dict:
    """Map total AL (4-32) to secondary school stream."""
    if al_score <= 20:
        stream = "Express"
        note = "Eligible for Express stream. Top scorers (AL ≤ 8–10) may qualify for IP schools."
    elif al_score <= 22:
        stream = "Normal Academic"
        note = "Eligible for Normal Academic stream. Leads to N(A)-levels and potentially Sec 5 O-levels or PFP."
    else:
        stream = "Normal Technical"
        note = "Eligible for Normal Technical stream. Leads to N(T)-levels and ITE pathways."
    return {"stream": stream, "note": note, "al_score": al_score}


def match_secondary_schools(al_score: int, gender: str = "Any", prefer_ip: bool = False) -> list[dict]:
    """Return schools the student is likely eligible for based on AL score."""
    schools = get_secondary_schools()
    matches = []
    for s in schools:
        cutoff_min = s.get("psle_al_cutoff_min")
        cutoff_max = s.get("psle_al_cutoff_max")
        if cutoff_min is None or cutoff_max is None:
            continue
        if cutoff_min <= al_score <= cutoff_max + 2:
            if gender != "Any":
                school_gender = s.get("gender", "mixed")
                if school_gender != "mixed" and school_gender != gender.lower():
                    continue
            if prefer_ip and not s.get("is_ip"):
                continue
            match = dict(s)
            match["fit"] = "Good fit" if al_score <= cutoff_max else "Borderline"
            matches.append(match)
    matches.sort(key=lambda x: x.get("psle_al_cutoff_min", 99))
    return matches[:15]


# ── O-LEVELS → JAE ───────────────────────────────────────────────────────────

def calculate_l1r5(
    english: int,
    humanities: int,
    math_or_science: int,
    subject4: int,
    subject5: int,
    subject6: int,
    cca_bonus: int = 0,
    affiliation_bonus: int = 0,
) -> dict:
    """
    Calculate L1R5 net aggregate for JC admission.
    All grades are O-level points: A1=1, A2=2, B3=3, B4=4, C5=5, C6=6, D7=7, E8=8, F9=9.
    Returns raw, net (after bonus), and eligibility note.
    """
    l1 = english
    r5 = sorted([humanities, math_or_science, subject4, subject5, subject6])[:5]
    raw = l1 + sum(r5)
    net = max(2, raw - cca_bonus - affiliation_bonus)
    eligible_jc = net <= 20
    return {
        "raw_l1r5": raw,
        "net_l1r5": net,
        "cca_bonus": cca_bonus,
        "affiliation_bonus": affiliation_bonus,
        "eligible_for_jc": eligible_jc,
        "note": "Eligible for JC via JAE." if eligible_jc else "Net L1R5 > 20: not eligible for JC. Consider polytechnic or ITE.",
    }


def calculate_elr2b2(
    english: int,
    second_lang_or_relevant: int,
    relevant1: int,
    relevant2: int,
    best_other1: int,
    best_other2: int,
) -> dict:
    """
    Calculate ELR2B2 aggregate for polytechnic admission.
    E = English, L = second lang or best relevant, R2 = 2 relevant subjects, B2 = 2 best other.
    Lower = better for poly, subject to English min C6.
    """
    aggregate = english + second_lang_or_relevant + relevant1 + relevant2 + best_other1 + best_other2
    english_pass = english <= 6  # C6 or better
    return {
        "elr2b2": aggregate,
        "english_pass": english_pass,
        "note": (
            f"ELR2B2 aggregate: {aggregate}. "
            + ("English pass: eligible for most poly courses." if english_pass
               else "English grade below C6 — many poly courses require at least C6 English.")
        ),
    }


def match_jcs(net_l1r5: int) -> list[dict]:
    """Return JCs the student is eligible for based on net L1R5."""
    jcs = get_jc_data()
    matches = []
    for jc in jcs:
        cutoff = jc.get("l1r5_cutoff_2023")
        if cutoff is None:
            continue
        if isinstance(cutoff, dict):
            lo, hi = cutoff.get("min"), cutoff.get("max")
            if lo is None or hi is None:
                continue
        elif isinstance(cutoff, (int, float)):
            lo, hi = cutoff - 1, cutoff + 2
        else:
            continue
        if net_l1r5 <= hi + 2:
            match = dict(jc)
            if net_l1r5 <= lo:
                match["fit"] = "Comfortably eligible"
            elif net_l1r5 <= hi:
                match["fit"] = "Within range"
            else:
                match["fit"] = "Borderline / appeal"
            matches.append(match)
    matches.sort(key=lambda x: x.get("l1r5_cutoff_2023") if isinstance(x.get("l1r5_cutoff_2023"), (int, float)) else 99)
    return matches


def match_poly_courses(elr2b2: int, interest: str = "") -> list[dict]:
    """Return poly courses within range of the student's ELR2B2."""
    courses = get_poly_courses()
    matches = []
    for c in courses:
        cutoff = c.get("elr2b2_cutoff_approximate")
        if cutoff is None:
            continue
        if elr2b2 <= cutoff + 4:
            match = dict(c)
            match["fit"] = "Eligible" if elr2b2 <= cutoff else "Borderline"
            if interest and interest.lower() in (c.get("course_name", "") + c.get("school_within_poly", "")).lower():
                match["interest_match"] = True
            matches.append(match)
    matches.sort(key=lambda x: x.get("elr2b2_cutoff_approximate", 99))
    return matches[:20]


# ── A-LEVELS → UNIVERSITY ────────────────────────────────────────────────────

def calculate_rank_points(h1_gp: str, h2_1: str, h2_2: str, h2_3: str, h1_mtl: str = "S") -> dict:
    """
    Calculate A-level University Admission Score (rank points).
    H2 = 20 (A), 17.5 (B), 15 (C), 12.5 (D), 10 (E), 0 (S/U)
    H1 = 10 (A), 8.75 (B), 7.5 (C), 6.25 (D), 5 (E), 0 (S/U)
    H1 GP + best 3 H2 + H1 MTL (capped at 10) = max 90.
    """
    h2_map = {"A": 20, "B": 17.5, "C": 15, "D": 12.5, "E": 10, "S": 0, "U": 0}
    h1_map = {"A": 10, "B": 8.75, "C": 7.5, "D": 6.25, "E": 5, "S": 0, "U": 0}

    gp_pts = h1_map.get(h1_gp.upper(), 0)
    h2_pts = sorted([h2_map.get(h2_1.upper(), 0), h2_map.get(h2_2.upper(), 0), h2_map.get(h2_3.upper(), 0)], reverse=True)[:3]
    mtl_pts = min(h1_map.get(h1_mtl.upper(), 0), 10)
    total = gp_pts + sum(h2_pts) + mtl_pts

    return {
        "rank_points": round(total, 2),
        "breakdown": {
            "H1 GP": gp_pts,
            "H2 subjects": sum(h2_pts),
            "H1 MTL (capped 10)": mtl_pts,
        },
        "note": f"University Admission Score (UAS): {round(total, 2)} / 90",
    }


def match_universities(rank_points: float, interest: str = "") -> list[dict]:
    """Return university faculties within range of rank points."""
    unis = get_university_data()
    matches = []
    for uni in unis:
        for faculty in uni.get("popular_faculties", []):
            min_rp = faculty.get("min_rank_points_alevel")
            if min_rp is None:
                continue
            if rank_points >= min_rp - 5:
                entry = {
                    "university": uni["short_name"],
                    "faculty": faculty["faculty_name"],
                    "min_rank_points": min_rp,
                    "course_duration": faculty.get("course_duration"),
                    "fit": "Eligible" if rank_points >= min_rp else "Borderline / competitive",
                    "interest_match": interest.lower() in faculty["faculty_name"].lower() if interest else False,
                }
                matches.append(entry)
    matches.sort(key=lambda x: x["min_rank_points"], reverse=True)
    return matches[:20]


# ── POLY GPA → DAE ───────────────────────────────────────────────────────────

def match_universities_dae(gpa: float, interest: str = "") -> list[dict]:
    """Match universities for polytechnic DAE applicants."""
    unis = get_university_data()
    matches = []
    for uni in unis:
        for faculty in uni.get("popular_faculties", []):
            min_gpa = faculty.get("min_gpa_poly")
            if min_gpa is None:
                continue
            if gpa >= min_gpa - 0.3:
                entry = {
                    "university": uni["short_name"],
                    "faculty": faculty["faculty_name"],
                    "min_gpa": min_gpa,
                    "course_duration": faculty.get("course_duration"),
                    "fit": "Eligible" if gpa >= min_gpa else "Borderline",
                    "interest_match": interest.lower() in faculty["faculty_name"].lower() if interest else False,
                }
                matches.append(entry)
    matches.sort(key=lambda x: x["min_gpa"], reverse=True)
    return matches[:20]

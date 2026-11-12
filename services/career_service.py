"""
Career pathway reverse-lookup service.
Maps career aspirations → university targets → required scores → education pathways.
"""
import json
from pathlib import Path
from functools import lru_cache

DATA_DIR = Path(__file__).parent.parent / "data" / "seed"


@lru_cache(maxsize=1)
def get_career_pathways() -> list[dict]:
    """Load all career pathway entries."""
    path = DATA_DIR / "career_pathways.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


def get_career_list() -> list[dict]:
    """Return simplified list for UI picker: [{career, icon, category}]."""
    return [
        {"career": c["career"], "icon": c["icon"], "category": c["category"]}
        for c in get_career_pathways()
    ]


def get_career_categories() -> list[str]:
    """Return unique categories for grouping."""
    seen = []
    for c in get_career_pathways():
        if c["category"] not in seen:
            seen.append(c["category"])
    return seen


def lookup_career(career_name: str):
    """Find career by exact name or alias (case-insensitive)."""
    name_lower = career_name.lower().strip()
    for c in get_career_pathways():
        if c["career"].lower() == name_lower:
            return c
        if name_lower in [a.lower() for a in c.get("aliases", [])]:
            return c
    # Fuzzy: substring match
    for c in get_career_pathways():
        if name_lower in c["career"].lower():
            return c
    return None


def trace_career_pathway(career_name: str):
    """
    Main reverse-lookup. Returns enriched pathway dict with:
    - career info (name, icon, category, professional_requirements)
    - university_targets (enriched with live data from university_data.json)
    - jc_route, poly_route, ite_route (from career data)
    - total_paths: [{name, years, tag, steps[{label, detail, score}]}] for display
    """
    career = lookup_career(career_name)
    if not career:
        return None

    from services.pathway_service import get_university_data, get_poly_courses, get_ite_data

    # Enrich university targets with live data
    unis = get_university_data()
    enriched_targets = []
    for target in career.get("university_targets", []):
        matched = False
        for uni in unis:
            if uni["short_name"] == target["uni"]:
                for fac in uni.get("popular_faculties", []):
                    if fac["faculty_name"] == target["faculty"]:
                        enriched_targets.append({
                            **target,
                            "official_url": fac.get("official_url", uni.get("official_url", "")),
                            "notable_courses": fac.get("notable_courses", []),
                            "full_notes": fac.get("notes", target.get("notes", "")),
                        })
                        matched = True
                        break
                if not matched:
                    enriched_targets.append(target)
                break
        else:
            enriched_targets.append(target)

    # Enrich poly route with live diploma data
    poly_route = dict(career.get("poly_route", {}))
    poly_courses = get_poly_courses()
    matched_diplomas = []
    for dip_name in poly_route.get("relevant_diplomas", []):
        for pc in poly_courses:
            if pc.get("course_name", "") == dip_name:
                matched_diplomas.append({
                    "name": dip_name,
                    "poly": pc.get("poly_name", pc.get("poly_short", "")),
                    "elr2b2": pc.get("elr2b2_cutoff_approximate", ""),
                })
                break
    poly_route["matched_diplomas"] = matched_diplomas

    # Enrich ITE route
    ite_route = dict(career.get("ite_route", {}))
    ite_data = get_ite_data()
    matched_ite = []
    for course_name in ite_route.get("relevant_courses", []):
        for ic in ite_data:
            if ic.get("course_name", "") == course_name:
                matched_ite.append({
                    "name": course_name,
                    "college": ic.get("college", ""),
                })
                break
    ite_route["matched_courses"] = matched_ite

    jc_route = career.get("jc_route", {})

    # Build total_paths summary for display
    total_paths = []

    # JC Route
    jc_steps = [
        {"label": "PSLE", "detail": career.get("psle_target", {}).get("competitive_schools", "AL ≤ 12"), "score": ""},
        {"label": "Express Stream", "detail": "Secondary school (4 years)", "score": ""},
        {"label": "O-levels", "detail": f"Target L1R5 ≤ {jc_route.get('recommended_jc_l1r5', 7)}", "score": f"L1R5 ≤ {jc_route.get('recommended_jc_l1r5', 7)}"},
        {"label": "Junior College", "detail": f"2 years · H2: {', '.join(jc_route.get('recommended_h2', [])[:3])}", "score": ""},
        {"label": "A-levels", "detail": f"Target UAS {jc_route.get('target_rp', 80)}+", "score": f"UAS ≥ {jc_route.get('target_rp', 80)}"},
        {"label": "University", "detail": f"{enriched_targets[0]['uni']} {enriched_targets[0]['faculty']}" if enriched_targets else "University degree", "score": f"{enriched_targets[0].get('duration', '4 years')}" if enriched_targets else ""},
    ]
    total_paths.append({
        "name": "JC Route",
        "tag": "★ Shortest",
        "years": jc_route.get("estimated_years_from_sec1", 10),
        "color": "#10b981",
        "steps": jc_steps,
    })

    # Poly Route
    elr2b2 = poly_route.get("elr2b2_needed", "varies")
    poly_steps = [
        {"label": "PSLE", "detail": career.get("psle_target", {}).get("express_stream", "AL ≤ 20"), "score": ""},
        {"label": "Express / NA Stream", "detail": "Secondary school (4–5 years)", "score": ""},
        {"label": "O-levels", "detail": f"Target ELR2B2 ≤ {elr2b2}", "score": f"ELR2B2 ≤ {elr2b2}"},
        {"label": "Polytechnic Diploma", "detail": f"3 years · {poly_route.get('relevant_diplomas', ['Relevant diploma'])[0]}", "score": f"GPA ≥ {poly_route.get('target_gpa', 3.5)}"},
        {"label": "University (DAE)", "detail": f"Direct Admission · {enriched_targets[0].get('duration', '4 years')}" if enriched_targets else "University degree", "score": ""},
    ]
    total_paths.append({
        "name": "Poly Route",
        "tag": "Alternative",
        "years": poly_route.get("estimated_years_from_sec1", 11),
        "color": "#8b5cf6",
        "steps": poly_steps,
    })

    # ITE Route
    ite_years = ite_route.get("estimated_years_from_sec1", 14)
    ite_steps = [
        {"label": "PSLE / N-levels", "detail": "Normal stream → N-levels", "score": ""},
        {"label": "ITE NITEC", "detail": f"2 years · {ite_route.get('relevant_courses', ['General course'])[0] if ite_route.get('relevant_courses') else 'Related course'}", "score": ""},
        {"label": "Higher NITEC / Poly", "detail": "1–3 years progression", "score": ""},
        {"label": "Polytechnic Diploma", "detail": "3 years (if not yet completed)", "score": f"GPA ≥ {poly_route.get('target_gpa', 3.5)}"},
        {"label": "University (DAE)", "detail": "Direct Admission", "score": ""},
    ]
    ite_notes = ite_route.get("notes", "")
    total_paths.append({
        "name": "ITE Route",
        "tag": "Longest but valid" if not ite_notes or "No direct" not in ite_notes else "Via Poly",
        "years": ite_years,
        "color": "#f59e0b",
        "steps": ite_steps,
    })

    return {
        "career": career["career"],
        "icon": career["icon"],
        "category": career["category"],
        "professional_requirements": career.get("professional_requirements", ""),
        "university_targets": enriched_targets,
        "jc_route": jc_route,
        "poly_route": poly_route,
        "ite_route": ite_route,
        "psle_target": career.get("psle_target", {}),
        "total_paths": total_paths,
    }

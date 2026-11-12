"""
Loads and queries education pathway data from seed JSON + SQLite.
"""
import json
from pathlib import Path
from functools import lru_cache
from services.db import fetchall, fetchone

DATA_DIR = Path(__file__).parent.parent / "data" / "seed"


@lru_cache(maxsize=1)
def get_stages() -> list[dict]:
    path = DATA_DIR / "education_stages.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@lru_cache(maxsize=1)
def get_secondary_schools() -> list[dict]:
    path = DATA_DIR / "secondary_schools.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@lru_cache(maxsize=1)
def get_jc_data() -> list[dict]:
    path = DATA_DIR / "jc_data.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@lru_cache(maxsize=1)
def get_poly_courses() -> list[dict]:
    path = DATA_DIR / "poly_courses.json"
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    # Support both flat list and nested {poly_name, courses:[...]} structure
    flat = []
    for item in raw:
        if "courses" in item:
            for course in item["courses"]:
                c = dict(course)
                c.setdefault("poly_name", item.get("poly_name", ""))
                c.setdefault("poly_short", item.get("poly_short", ""))
                c.setdefault("poly_id", item.get("poly_id", ""))
                flat.append(c)
        else:
            flat.append(item)
    return flat


@lru_cache(maxsize=1)
def get_ite_data() -> list[dict]:
    path = DATA_DIR / "ite_data.json"
    if not path.exists():
        return []
    raw = json.loads(path.read_text())
    flat = []
    for item in raw:
        if "courses" in item:
            for course in item["courses"]:
                c = dict(course)
                c.setdefault("college", item.get("college", ""))
                c.setdefault("college_id", item.get("college_id", ""))
                flat.append(c)
        else:
            flat.append(item)
    return flat


@lru_cache(maxsize=1)
def get_university_data() -> list[dict]:
    path = DATA_DIR / "university_data.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@lru_cache(maxsize=1)
def get_fallback_policies() -> list[dict]:
    path = DATA_DIR / "fallback_policies.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@lru_cache(maxsize=1)
def get_institution_locations() -> list[dict]:
    path = DATA_DIR / "institution_locations.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@lru_cache(maxsize=1)
def get_support_resources() -> dict:
    path = DATA_DIR / "support_resources.json"
    if path.exists():
        return json.loads(path.read_text())
    return {"counselling": [], "career_guidance": [], "talks_events": [], "scholarships": [], "earn_and_learn": []}


@lru_cache(maxsize=1)
def get_primary_schools() -> list[dict]:
    path = DATA_DIR / "primary_schools.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


@lru_cache(maxsize=1)
def get_success_stories() -> list[dict]:
    path = DATA_DIR / "success_stories.json"
    if path.exists():
        return json.loads(path.read_text())
    return []


def get_stage_by_id(stage_id: str) -> dict | None:
    for s in get_stages():
        if s.get("id") == stage_id:
            return s
    return None


def get_pathway_for_profile(current_stage: str, interests: list[str], citizenship: str) -> dict:
    """
    Returns a structured pathway dict for the visual planner.
    current_stage: one of the stage ids
    """
    stages = get_stages()
    stage_ids = [s["id"] for s in stages]

    try:
        current_idx = stage_ids.index(current_stage)
    except ValueError:
        current_idx = 0

    upcoming = stages[current_idx:]
    pathway = {
        "current_stage": current_stage,
        "stages": upcoming,
        "forks": _get_forks(current_stage, interests),
        "citizenship_notes": _citizenship_notes(citizenship),
    }
    return pathway


def _get_forks(current_stage: str, interests: list[str]) -> list[dict]:
    forks = []
    if current_stage in ("primary", "early_childhood"):
        forks.append({
            "at": "End of P6 — PSLE",
            "options": [
                {"name": "IP Schools (top scorers)", "criteria": "AL 4–8 typically", "leads_to": "A-levels / IB in 6 years"},
                {"name": "Express Stream", "criteria": "AL ≤ 20", "leads_to": "O-levels at Sec 4"},
                {"name": "Normal Academic", "criteria": "AL 21–22", "leads_to": "N(A)-levels → Sec 5 O-levels or PFP"},
                {"name": "Normal Technical", "criteria": "AL 23–32", "leads_to": "N(T)-levels → ITE"},
            ]
        })
        forks.append({
            "at": "After O-levels — JAE",
            "options": [
                {"name": "Junior College", "criteria": "L1R5 net ≤ 20 (most JCs ≤ 14)", "leads_to": "A-levels in 2 years"},
                {"name": "Polytechnic", "criteria": "ELR2B2 aggregate (varies by course)", "leads_to": "Diploma in 3 years"},
                {"name": "ITE", "criteria": "N-level grades or O-level passes", "leads_to": "NITEC / Higher NITEC"},
            ]
        })
    if current_stage in ("primary", "early_childhood", "secondary_express", "secondary_normal_academic", "ip_programme"):
        forks.append({
            "at": "Post-Secondary → University",
            "options": [
                {"name": "A-levels → SNUFA", "criteria": "Rank points (varies by course)", "leads_to": "NUS / NTU / SMU / SUTD / SIT / SUSS"},
                {"name": "Poly Diploma → DAE", "criteria": "GPA typically 3.0+ for most courses", "leads_to": "Direct entry to Year 1 / advanced standing"},
                {"name": "IB → University", "criteria": "IB points (varies)", "leads_to": "Local or overseas university"},
            ]
        })
    return forks


def _citizenship_notes(citizenship: str) -> list[str]:
    notes = []
    if citizenship == "Singapore Citizen":
        notes.append("Priority in P1 registration Phase 1–2B.")
        notes.append("Eligible for MOE subsidies and bursaries.")
        notes.append("SkillsFuture Credit ($500 + top-ups) from age 25.")
    elif citizenship == "Permanent Resident":
        notes.append("P1 registration starts from Phase 2C.")
        notes.append("Higher school fees than citizens but same curriculum.")
        notes.append("May apply for MOE bursary schemes; check eligibility.")
    else:
        notes.append("International students apply through school directly.")
        notes.append("Must sit AEIS/SAEIS admissions test for P2–Sec 3 entry.")
        notes.append("Full fees apply; limited places available.")
    return notes

"""Education stage definitions with color themes."""

STAGES = {
    "early_childhood": {
        "label": "🌱 Early Childhood",
        "subtitle": "Birth – 6 years (before P1)",
        "color": "#f59e0b",
        "bg": "#fef3c7",
        "dark": "#92400e",
        "tab_hint": None,
        "relevant_pages": ["Pathway Planner", "Primary Hub", "Fallback Guide"],
        "ai_context": "The user is focused on early childhood education in Singapore (ages 0-6, before Primary 1). Topics include KidSTART, Anchor/Partner Operator PCF preschools, MK kindergartens, developmental milestones, P1 registration preparation.",
    },
    "primary": {
        "label": "🏫 Primary School",
        "subtitle": "P1 – P6 · Age 7–12",
        "color": "#10b981",
        "bg": "#d1fae5",
        "dark": "#065f46",
        "tab_hint": "psle",
        "relevant_pages": ["Primary Hub", "Score Matcher (PSLE)", "Fallback Guide", "Support Hub"],
        "ai_context": "The user is focused on primary school in Singapore (P1-P6, ages 7-12). Topics include P1 registration phases, school transfers, Learning Support Programme, Subject-Based Banding, PSLE AL scoring, Foundation vs Standard subjects, PSLE preparation strategies.",
    },
    "secondary": {
        "label": "📚 Secondary School",
        "subtitle": "Sec 1–5 · Age 13–17",
        "color": "#3b82f6",
        "bg": "#dbeafe",
        "dark": "#1e3a5f",
        "tab_hint": "olevels",
        "relevant_pages": ["Score Matcher", "Pathway Planner", "Fallback Guide", "Support Hub"],
        "ai_context": "The user is focused on secondary school in Singapore (Sec 1-5, ages 13-17). Topics include O-levels, N-levels, Express/Normal Academic/Normal Technical streams, IP programmes, SAP schools, CCA, O-level subject combinations, JAE preparation.",
    },
    "post_secondary": {
        "label": "🎓 Post-Secondary",
        "subtitle": "JC / Poly / ITE · Age 17–21",
        "color": "#8b5cf6",
        "bg": "#ede9fe",
        "dark": "#4c1d95",
        "tab_hint": "alevels",
        "relevant_pages": ["Score Matcher", "Support Hub", "AI Guide", "Fallback Guide"],
        "ai_context": "The user is focused on post-secondary education in Singapore (JC/Poly/ITE, ages 17-21). Topics include A-levels, H1/H2/H3 subjects, JAE, polytechnic diplomas, ITE NITEC/Higher NITEC, PFP, DAE pathways, scholarships, bursaries.",
    },
    "university_plus": {
        "label": "🏛️ University & Beyond",
        "subtitle": "University / Working Adult",
        "color": "#0891b2",
        "bg": "#cffafe",
        "dark": "#164e63",
        "tab_hint": "dae",
        "relevant_pages": ["Score Matcher (DAE)", "Support Hub", "AI Guide"],
        "ai_context": "The user is focused on university admission or lifelong learning in Singapore. Topics include SNUFA rank points, DAE (Diploma to University), university courses, NUS/NTU/SMU/SUTD/SIT/SUSS, graduate programmes, SkillsFuture, Earn and Learn.",
    },
}

STAGE_ORDER = ["early_childhood", "primary", "secondary", "post_secondary", "university_plus"]
DEFAULT_STAGE = "secondary"


def get_stage_config(stage_key: str) -> dict:
    return STAGES.get(stage_key, STAGES[DEFAULT_STAGE])

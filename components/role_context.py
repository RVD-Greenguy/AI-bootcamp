"""Role-aware language helper for EduPath SG."""


def get_role_labels(role: str) -> dict:
    """Return role-specific language labels."""
    LABELS = {
        "parent": {
            "possessive": "your child's",
            "subject": "your child",
            "subject_cap": "Your child",
            "score_prompt": "Enter your child's scores",
            "journey_label": "your child's journey",
            "fallback_prefix": "What to do if your child",
            "career_question": "What does your child want to be?",
            "home_icon": "👨‍👩‍👧",
            "welcome_action": "Plan your child's education journey",
            "ai_role_context": (
                "You are speaking to a parent planning their child's education in Singapore. "
                "Use language like 'your child' and 'your son/daughter'. Focus on what the parent "
                "can do to support their child — school selection, registration, enrichment, "
                "emotional support. Be reassuring but factual."
            ),
        },
        "student": {
            "possessive": "your",
            "subject": "you",
            "subject_cap": "You",
            "score_prompt": "Enter your scores",
            "journey_label": "your journey",
            "fallback_prefix": "What can I do if I",
            "career_question": "What do you want to be?",
            "home_icon": "🎒",
            "welcome_action": "Explore your education options",
            "ai_role_context": (
                "You are speaking directly to a student in Singapore's education system. "
                "Use 'you' and 'your'. Focus on actionable steps the student can take. "
                "Be encouraging and straightforward. Avoid condescending language."
            ),
        },
        "teacher": {
            "possessive": "the student's",
            "subject": "the student",
            "subject_cap": "The student",
            "score_prompt": "Enter student scores",
            "journey_label": "the student's journey",
            "fallback_prefix": "Advising a student who",
            "career_question": "Student's career aspiration:",
            "home_icon": "👩‍🏫",
            "welcome_action": "Access full pathway data for counselling",
            "ai_role_context": (
                "You are speaking to a teacher or school counsellor in Singapore. "
                "Use professional language. Reference official MOE/SEAB policies where relevant. "
                "Include specific policy details, cutoff numbers, and counselling talking points. "
                "Provide information suitable for advising students and briefing parents."
            ),
        },
    }
    return LABELS.get(role, LABELS["student"])

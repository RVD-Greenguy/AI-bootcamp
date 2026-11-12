import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

def _secret(key: str, default: str = "") -> str:
    """Read from st.secrets first (Streamlit Cloud), then env, then default."""
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

DB_PATH = str(BASE_DIR / _secret("DB_PATH", "storage/edupathsg.sqlite"))
OPENAI_API_KEY = _secret("OPENAI_API_KEY", "")
USE_AI = _secret("USE_AI", "false").lower() == "true"
APP_SECRET_KEY = _secret("APP_SECRET_KEY", "edupathsg-dev-secret")

DISCLAIMER = (
    "EduPath SG provides general guidance based on publicly available MOE and government information. "
    "Policies and cutoffs change each year — always verify at moe.gov.sg or the relevant institution's official website "
    "before making decisions."
)

ROLES = ["parent", "student", "teacher"]

EDUCATION_STAGES = [
    "Early Childhood (0–6)",
    "Primary School (7–12)",
    "Secondary School (13–16/17)",
    "Post-Secondary (JC / Poly / ITE)",
    "University",
    "Post-Graduate / SkillsFuture",
]

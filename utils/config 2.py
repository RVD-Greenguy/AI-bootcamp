import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

DB_PATH = str(BASE_DIR / os.getenv("DB_PATH", "storage/edupathsg.sqlite"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
USE_AI = os.getenv("USE_AI", "false").lower() == "true"
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "edupathsg-dev-secret")

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

import bcrypt
from services.db import fetchone, execute


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False


def login_user(email: str, password: str):
    user = fetchone("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
    if not user:
        return None, "Invalid email or password."
    if not verify_password(password, user["password_hash"]):
        return None, "Invalid email or password."
    return dict(user), None


def register_user(email: str, password: str, role: str, full_name: str):
    email = email.lower().strip()
    if fetchone("SELECT id FROM users WHERE email = ?", (email,)):
        return None, "An account with this email already exists."
    if len(password) < 8:
        return None, "Password must be at least 8 characters."
    if role not in ("parent", "student", "teacher"):
        return None, "Invalid role."
    pw_hash = hash_password(password)
    uid = execute(
        "INSERT INTO users (email, password_hash, role, full_name) VALUES (?,?,?,?)",
        (email, pw_hash, role, full_name),
    )
    return fetchone("SELECT * FROM users WHERE id = ?", (uid,)), None


def get_user_by_id(user_id: int):
    return fetchone("SELECT * FROM users WHERE id = ?", (user_id,))

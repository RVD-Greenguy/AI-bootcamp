import streamlit as st


def get_user():
    return st.session_state.get("user")


def set_user(user: dict):
    st.session_state["user"] = user


def clear_user():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def require_login():
    user = get_user()
    if not user:
        st.error("Please log in to access this page.")
        st.stop()
    return user


def require_role(*roles):
    user = require_login()
    if user["role"] not in roles:
        st.error(f"This page is not available for your role ({user['role']}).")
        st.stop()
    return user


def append_chat(role: str, content: str, key: str = "chat"):
    history = st.session_state.setdefault(f"chat_{key}", [])
    history.append({"role": role, "content": content})


def get_chat_history(key: str = "chat") -> list:
    return st.session_state.get(f"chat_{key}", [])


def clear_chat(key: str = "chat"):
    st.session_state[f"chat_{key}"] = []
    st.session_state.pop(f"rag_{key}_chunks", None)

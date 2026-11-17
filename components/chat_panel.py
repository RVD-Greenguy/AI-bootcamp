"""
Sidebar AI assistant panel — VS Code-style persistent chat.
Renders in the sidebar below navigation. Session history persists
across page navigations (session_state) and across logins (SQLite).
"""
import streamlit as st
from utils.session_manager import get_user

_HISTORY_KEY = "guide_chat_history"
_LOADED_KEY = "guide_chat_loaded"
_MAX_PERSIST = 20
_MAX_DISPLAY = 8


def _load_history_from_db(user_id: int) -> list[dict]:
    try:
        from services.db import fetchall
        rows = fetchall(
            "SELECT question, ai_response FROM chat_sessions "
            "WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
            (user_id, _MAX_PERSIST // 2),
        )
        history = []
        for r in reversed(rows):
            history.append({"role": "user", "content": r["question"]})
            history.append({"role": "assistant", "content": r["ai_response"]})
        return history
    except Exception:
        return []


def _save_turn_to_db(user_id: int, question: str, answer: str, chunks: list):
    try:
        import json
        from services.db import execute
        execute(
            "INSERT INTO chat_sessions (user_id, question, ai_response, chunks_json, created_at) "
            "VALUES (?, ?, ?, ?, datetime('now'))",
            (user_id, question, answer, json.dumps([c.get("text", "")[:200] for c in chunks[:3]])),
        )
    except Exception:
        pass


def render_chat_panel():
    """Render AI assistant in the sidebar. Call once per page, after render_sidebar()."""
    user = get_user()
    if not user:
        return

    user_id = user["id"]

    if not st.session_state.get(_LOADED_KEY):
        st.session_state[_HISTORY_KEY] = _load_history_from_db(user_id)
        st.session_state[_LOADED_KEY] = True

    history: list[dict] = st.session_state.get(_HISTORY_KEY, [])

    with st.sidebar:
        st.markdown("---")
        msg_count = len(history) // 2
        st.markdown(f"### 🤖 AI Assistant {'· ' + str(msg_count) + ' msgs' if msg_count else ''}")

        # Scrollable chat area via container with fixed height
        chat_container = st.container(height=320)
        with chat_container:
            display = history[-_MAX_DISPLAY * 2:]
            if display:
                for msg in display:
                    if msg["role"] == "user":
                        st.markdown(f"""<div style="background:#1e3a5f;color:#e2e8f0;padding:8px 12px;
                            border-radius:12px 12px 4px 12px;margin:4px 0;font-size:0.85em;">
                            💬 {msg['content']}</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""<div style="background:#f0fdf4;color:#1a1a2e;padding:8px 12px;
                            border-radius:12px 12px 12px 4px;margin:4px 0;font-size:0.85em;
                            border-left:3px solid #10b981;">
                            {msg['content']}</div>""", unsafe_allow_html=True)
            else:
                st.caption("Ask me anything about Singapore's education system.")

        # Input
        question = st.text_input(
            "Ask EduPath AI:",
            key="sidebar_chat_input",
            placeholder="e.g. PSLE cutoffs for Express?",
            label_visibility="collapsed",
        )
        col_send, col_clear = st.columns([3, 1])
        with col_send:
            send = st.button("💬 Send", type="primary", use_container_width=True, key="sidebar_chat_send")
        with col_clear:
            clear = st.button("🗑️", use_container_width=True, key="sidebar_chat_clear")

        if clear:
            st.session_state[_HISTORY_KEY] = []
            st.rerun()

        if send and question and question.strip():
            q = question.strip()

            with st.spinner("Thinking…"):
                try:
                    from services.rag_service import search
                    chunks = search(q, top_k=4)
                except Exception:
                    chunks = []

                try:
                    from services.llm_service import ask_guide
                    from utils.session_manager import get_education_stage, get_career_goal
                    from utils.stage_config import get_stage_config
                    from components.role_context import get_role_labels

                    stage_cfg = get_stage_config(get_education_stage())
                    stage_context = [{"role": "system", "content": stage_cfg["ai_context"]}]

                    role_labels = get_role_labels(user["role"])
                    role_context = [{"role": "system", "content": role_labels["ai_role_context"]}]

                    career = get_career_goal()
                    career_context = []
                    if career:
                        career_context = [{"role": "system", "content": f"The user's career aspiration is: {career}. Tailor your advice toward achieving this goal where relevant."}]

                    answer = ask_guide(q, chunks, role_context + career_context + stage_context + history[-10:])
                except Exception as e:
                    answer = f"Sorry, I couldn't process that: {e}"

            history.append({"role": "user", "content": q})
            history.append({"role": "assistant", "content": answer})
            st.session_state[_HISTORY_KEY] = history

            _save_turn_to_db(user_id, q, answer, chunks)
            st.rerun()

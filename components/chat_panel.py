"""
Persistent top-of-page AI chat panel.
Renders a collapsible expander on every page.
Conversation history lives in st.session_state and is persisted to SQLite.
"""
import streamlit as st
from utils.session_manager import get_user

_HISTORY_KEY = "guide_chat_history"
_LOADED_KEY = "guide_chat_loaded"
_MAX_PERSIST = 20   # turns saved to DB per user
_MAX_DISPLAY = 6    # messages shown in panel before scroll


def _load_history_from_db(user_id: int) -> list[dict]:
    """Load last N turns from chat_sessions for this user."""
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
    """Render the top-of-page AI chat panel. Call once per page, after render_sidebar()."""
    user = get_user()
    if not user:
        return

    user_id = user["id"]

    # Load history from DB once per session per user
    if not st.session_state.get(_LOADED_KEY):
        st.session_state[_HISTORY_KEY] = _load_history_from_db(user_id)
        st.session_state[_LOADED_KEY] = True

    history: list[dict] = st.session_state.get(_HISTORY_KEY, [])

    # Determine expander label
    unread = len(history)
    label = (
        f"💬 Ask EduPath AI — {unread // 2} message{'s' if unread // 2 != 1 else ''} in history"
        if unread
        else "💬 Ask EduPath AI Guide"
    )

    with st.expander(label, expanded=st.session_state.get("chat_panel_open", False)):
        # Chat display
        display = history[-_MAX_DISPLAY * 2:] if len(history) > _MAX_DISPLAY * 2 else history
        if display:
            for msg in display:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        else:
            st.caption("Ask me anything about Singapore's education system — PSLE, O-levels, JC, Poly, ITE, University, scholarships and more.")

        st.divider()

        # Input row
        col_input, col_btn, col_clear = st.columns([6, 1, 1])
        with col_input:
            question = st.text_input(
                "Your question:",
                key="chat_panel_input",
                placeholder="e.g. What are the PSLE AL cutoffs for Express stream?",
                label_visibility="collapsed",
            )
        with col_btn:
            send = st.button("Send", type="primary", use_container_width=True)
        with col_clear:
            clear = st.button("Clear", use_container_width=True)

        if clear:
            st.session_state[_HISTORY_KEY] = []
            st.rerun()

        if send and question and question.strip():
            q = question.strip()
            with st.spinner("Searching knowledge base…"):
                try:
                    from services.rag_service import search
                    chunks = search(q, top_k=4)
                except Exception:
                    chunks = []

            with st.spinner("Generating answer…"):
                try:
                    from services.llm_service import ask_guide
                    from utils.session_manager import get_education_stage
                    from utils.stage_config import get_stage_config
                    stage_cfg = get_stage_config(get_education_stage())
                    stage_context = [{"role": "system", "content": stage_cfg["ai_context"]}]
                    answer = ask_guide(q, chunks, stage_context + history[-10:])
                except Exception as e:
                    answer = f"Sorry, I couldn't process that: {e}"

            # Update session history
            history.append({"role": "user", "content": q})
            history.append({"role": "assistant", "content": answer})
            st.session_state[_HISTORY_KEY] = history

            # Persist to DB
            _save_turn_to_db(user_id, q, answer, chunks)

            # Keep panel open after send
            st.session_state["chat_panel_open"] = True
            st.rerun()

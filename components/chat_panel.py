"""
Right-side AI assistant using Streamlit native two-column layout.
Each page wraps its content in the left column; the chat occupies the right.
Session history persists across pages (session_state) and logins (SQLite).
"""
import streamlit as st
from utils.session_manager import get_user

_HISTORY_KEY = "guide_chat_history"
_LOADED_KEY = "guide_chat_loaded"
_MAX_PERSIST = 20
_MAX_DISPLAY = 10


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
    """
    Render AI assistant in a right-side column.
    Returns a column context manager for the main content.

    Usage in pages:
        main_col = render_chat_panel()
        with main_col:
            st.title("Page Title")
            # ... rest of page content

    If user is not logged in, returns a dummy that works as a no-op context.
    """
    user = get_user()
    if not user:
        return st.container()

    user_id = user["id"]

    if not st.session_state.get(_LOADED_KEY):
        st.session_state[_HISTORY_KEY] = _load_history_from_db(user_id)
        st.session_state[_LOADED_KEY] = True

    history: list[dict] = st.session_state.get(_HISTORY_KEY, [])
    is_open = st.session_state.get("chat_panel_open", True)

    if not is_open:
        # Closed: full-width main content + small toggle in corner
        main_col, toggle_col = st.columns([50, 1])
        with toggle_col:
            if st.button("🤖", key="chat_open_btn", help="Open AI Assistant"):
                st.session_state["chat_panel_open"] = True
                st.rerun()
        return main_col

    # Open: main content (left ~75%) + chat panel (right ~25%)
    main_col, chat_col = st.columns([3, 1], gap="medium")

    with chat_col:
        # Header
        hdr_left, hdr_right = st.columns([4, 1])
        with hdr_left:
            msg_count = len(history) // 2
            st.markdown(f"**🤖 AI Assistant** {'· ' + str(msg_count) if msg_count else ''}")
        with hdr_right:
            if st.button("✕", key="chat_close_btn", help="Close AI Assistant"):
                st.session_state["chat_panel_open"] = False
                st.rerun()

        # Chat messages in a scrollable container
        chat_box = st.container(height=420)
        with chat_box:
            display = history[-_MAX_DISPLAY * 2:]
            if display:
                for msg in display:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
            else:
                st.caption("Ask me anything about Singapore's education system — PSLE, O-levels, JC, Poly, ITE, University, scholarships and more.")

        # Input
        question = st.text_input(
            "Ask EduPath AI:",
            key="chat_input",
            placeholder="e.g. PSLE cutoffs for Express?",
            label_visibility="collapsed",
        )
        btn_left, btn_right = st.columns([3, 1])
        with btn_left:
            send = st.button("💬 Send", type="primary", use_container_width=True, key="chat_send")
        with btn_right:
            clear = st.button("🗑️", use_container_width=True, key="chat_clear")

        if clear:
            st.session_state[_HISTORY_KEY] = []
            st.rerun()

        if send and question and question.strip():
            q = question.strip()

            # Input validation
            try:
                from services.web_search_service import validate_question
                is_valid, reason = validate_question(q)
                if not is_valid:
                    history.append({"role": "user", "content": q})
                    history.append({"role": "assistant", "content": f"I can't process that: {reason}\n\nPlease ask about Singapore's education system."})
                    st.session_state[_HISTORY_KEY] = history
                    st.rerun()
            except Exception:
                pass

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

    return main_col

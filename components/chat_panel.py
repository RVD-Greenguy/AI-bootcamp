"""
Right-side AI assistant panel using Streamlit columns.
Each page calls render_chat_panel() BEFORE its content to get
a main-content column. All page content must go inside `with main:`.
"""
import streamlit as st
from utils.session_manager import get_user

_HISTORY_KEY = "guide_chat_history"
_PENDING_KEY = "_chat_pending_q"
_MAX_DISPLAY = 8

_SUGGESTED = [
    "What PSLE score for Express?",
    "How does L1R5 work?",
    "JC cutoff points?",
    "DAE with poly diploma?",
]


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


def _process_question(q: str, user: dict, history: list[dict], user_id: int):
    try:
        from services.web_search_service import validate_question
        is_valid, reason = validate_question(q)
        if not is_valid:
            history.append({"role": "user", "content": q})
            history.append({"role": "assistant", "content": f"I can't process that: {reason}\n\nPlease ask about Singapore's education system."})
            st.session_state[_HISTORY_KEY] = history
            return
    except Exception:
        pass

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
        chunks = []

    history.append({"role": "user", "content": q})
    history.append({"role": "assistant", "content": answer})
    st.session_state[_HISTORY_KEY] = history
    _save_turn_to_db(user_id, q, answer, chunks)


def _render_chat_ui(user: dict, history: list[dict]):
    """Render the full chat interface."""
    msg_count = len(history) // 2

    st.markdown("""
<div style="background:linear-gradient(135deg,#0269D0,#0151A0);
    color:white;padding:10px 14px;border-radius:8px;
    font-weight:600;font-size:0.85em;margin-bottom:8px;
    display:flex;align-items:center;gap:8px;">
    🤖 AI Assistant
    <span style="margin-left:auto;opacity:0.7;font-size:0.72em;">RAG + GPT-4o</span>
</div>
""", unsafe_allow_html=True)

    chat_box = st.container(height=320)
    with chat_box:
        if not history:
            st.markdown("""
<div style="text-align:center;padding:12px 4px;color:#6B6B6B;">
    <div style="font-size:1.5em;margin-bottom:6px;">🎓</div>
    <div style="font-size:0.8em;font-weight:600;color:#3B3B3B;">Ask about SG education</div>
    <div style="font-size:0.72em;color:#6B6B6B;margin-top:3px;">PSLE · O-levels · JC · Poly · ITE · Uni</div>
</div>
""", unsafe_allow_html=True)
            for i, sq in enumerate(_SUGGESTED):
                if st.button(f"→ {sq}", key=f"sq_{i}", use_container_width=True):
                    st.session_state[_PENDING_KEY] = sq
                    st.rerun()
        else:
            for msg in history[-_MAX_DISPLAY * 2:]:
                if msg["role"] == "user":
                    st.markdown(f"""
<div style="background:#ECF5FE;border:1px solid #C8E2FB;
    padding:6px 10px;border-radius:8px 8px 2px 8px;
    margin:3px 0;font-size:0.78em;color:#0E0E0E;">
    💬 {msg['content']}
</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
<div style="background:#fff;border:1px solid #DFDFDF;border-left:3px solid #0269D0;
    padding:6px 10px;border-radius:2px 8px 8px 8px;
    margin:3px 0;font-size:0.78em;color:#3B3B3B;">
    {msg['content'].replace(chr(10), '<br>')}
</div>""", unsafe_allow_html=True)

    if msg_count:
        st.caption(f"📋 {msg_count} exchanges")

    def _on_send():
        q = st.session_state.get("chat_input", "").strip()
        if q:
            st.session_state[_PENDING_KEY] = q
            st.session_state["chat_input"] = ""

    def _on_clear():
        st.session_state[_HISTORY_KEY] = []
        st.session_state["chat_input"] = ""

    st.text_input("Ask:", key="chat_input", placeholder="Ask about pathways…", label_visibility="collapsed", on_change=_on_send)
    c1, c2 = st.columns([4, 1])
    with c1:
        st.button("Send", type="primary", use_container_width=True, key="chat_send", on_click=_on_send)
    with c2:
        st.button("🗑️", use_container_width=True, key="chat_clear", on_click=_on_clear)

    st.markdown("""
<div style="font-size:0.62em;color:#6B6B6B;text-align:center;margin-top:3px;">
    <a href="https://www.moe.gov.sg" style="color:#0269D0;">MOE</a> ·
    <a href="https://www.seab.gov.sg" style="color:#0269D0;">SEAB</a> ·
    <a href="https://www.ite.edu.sg" style="color:#0269D0;">ITE</a> · For guidance only.
</div>
""", unsafe_allow_html=True)


def render_chat_panel():
    """
    Creates a two-column layout with chat on the right.
    Returns the main content column for the page to use with `with main:`.
    If user not logged in, returns a full-width container.
    """
    user = get_user()
    if not user:
        return st.container()

    if _HISTORY_KEY not in st.session_state:
        st.session_state[_HISTORY_KEY] = []

    history: list[dict] = st.session_state.get(_HISTORY_KEY, [])
    pending = st.session_state.pop(_PENDING_KEY, None)

    is_open = st.session_state.get("chat_panel_open", True)

    if is_open:
        main_col, chat_col = st.columns([3, 1], gap="medium")
        with chat_col:
            if st.button("✕ Hide Chat", key="chat_hide_btn", use_container_width=True):
                st.session_state["chat_panel_open"] = False
                st.rerun()
            if pending:
                with st.status("🔍 Searching knowledge base…", expanded=True) as status:
                    st.write("Retrieving relevant information…")
                    _process_question(pending, user, history, user["id"])
                    status.update(label="✅ Done!", state="complete")
                st.rerun()
            _render_chat_ui(user, history)
        return main_col
    else:
        if pending:
            st.session_state[_PENDING_KEY] = pending
            st.session_state["chat_panel_open"] = True
            st.rerun()
        main_col, btn_col = st.columns([14, 1])
        with btn_col:
            if st.button("🤖", key="chat_show_btn", help="Open AI Assistant"):
                st.session_state["chat_panel_open"] = True
                st.rerun()
        return main_col

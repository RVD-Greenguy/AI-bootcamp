"""
Right-side AI assistant panel — fixed position, persistent across pages.
Uses CSS fixed positioning to create a VS Code-style right panel.
Session history persists across navigations (session_state) and logins (SQLite).
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


def _build_chat_html(history: list[dict]) -> str:
    """Build the chat messages HTML."""
    if not history:
        return '<p style="color:#94a3b8;font-size:0.85em;text-align:center;padding:20px 0;">Ask me anything about Singapore\'s education system — PSLE, O-levels, JC, Poly, ITE, University and more.</p>'

    display = history[-_MAX_DISPLAY * 2:]
    msgs_html = ""
    for msg in display:
        if msg["role"] == "user":
            msgs_html += f"""
<div style="background:#1e3a5f;color:#e2e8f0;padding:8px 12px;
    border-radius:12px 12px 4px 12px;margin:6px 0 6px 20%;font-size:0.82em;">
    {msg['content']}</div>"""
        else:
            content = msg["content"].replace("\n", "<br>")
            msgs_html += f"""
<div style="background:#f0fdf4;color:#1a1a2e;padding:8px 12px;
    border-radius:12px 12px 12px 4px;margin:6px 20% 6px 0;font-size:0.82em;
    border-left:3px solid #10b981;">
    {content}</div>"""
    return msgs_html


def render_chat_panel():
    """Render AI assistant as a fixed right-side panel. Call once per page."""
    user = get_user()
    if not user:
        return

    user_id = user["id"]

    if not st.session_state.get(_LOADED_KEY):
        st.session_state[_HISTORY_KEY] = _load_history_from_db(user_id)
        st.session_state[_LOADED_KEY] = True

    history: list[dict] = st.session_state.get(_HISTORY_KEY, [])
    msg_count = len(history) // 2

    is_open = st.session_state.get("chat_panel_open", False)

    # Toggle button (floating, always visible)
    toggle_css = """
<style>
.chat-toggle {
    position: fixed;
    right: 20px;
    bottom: 20px;
    z-index: 99998;
    background: #1565C0;
    color: white;
    border: none;
    border-radius: 50%;
    width: 56px;
    height: 56px;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
}
.chat-toggle:hover { background: #0d47a1; }
.chat-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: #ef4444;
    color: white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    font-size: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
"""
    st.markdown(toggle_css, unsafe_allow_html=True)

    # Right panel CSS
    panel_width = "340px"
    st.markdown(f"""
<style>
.right-chat-panel {{
    position: fixed;
    top: 0;
    right: 0;
    width: {panel_width};
    height: 100vh;
    background: #ffffff;
    border-left: 2px solid #e2e8f0;
    box-shadow: -4px 0 20px rgba(0,0,0,0.08);
    z-index: 99999;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}
.right-chat-header {{
    background: linear-gradient(135deg, #1565C0, #0d47a1);
    color: white;
    padding: 14px 16px;
    font-weight: 700;
    font-size: 0.95em;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}}
.right-chat-messages {{
    flex: 1;
    overflow-y: auto;
    padding: 12px;
    background: #fafbfc;
}}
.right-chat-input {{
    border-top: 1px solid #e2e8f0;
    padding: 10px 12px;
    background: white;
    flex-shrink: 0;
}}
/* Shrink main content when panel is open */
.right-panel-active section.main > div {{
    margin-right: {panel_width} !important;
}}
</style>
""", unsafe_allow_html=True)

    # Open/close via Streamlit button
    col_spacer, col_toggle = st.columns([20, 1])
    with col_toggle:
        if st.button("🤖" if not is_open else "✕", key="chat_toggle_btn", help="Toggle AI Assistant"):
            st.session_state["chat_panel_open"] = not is_open
            st.rerun()

    if not is_open:
        return

    # Add class to body for margin adjustment
    st.markdown('<div class="right-panel-active"></div>', unsafe_allow_html=True)

    # Build the panel HTML
    msgs_html = _build_chat_html(history)

    panel_html = f"""
<div class="right-chat-panel">
    <div class="right-chat-header">
        🤖 EduPath AI Assistant
        <span style="margin-left:auto;font-size:0.8em;opacity:0.8;">{msg_count} messages</span>
    </div>
    <div class="right-chat-messages" id="chat-messages">
        {msgs_html}
    </div>
    <div class="right-chat-input">
        <small style="color:#64748b;">Type below and press Send ↓</small>
    </div>
</div>
<script>
    // Auto-scroll to bottom
    var el = document.getElementById('chat-messages');
    if (el) el.scrollTop = el.scrollHeight;
</script>
"""
    st.markdown(panel_html, unsafe_allow_html=True)

    # Streamlit input widgets (rendered in main area but logically for the panel)
    st.markdown("---")
    st.markdown("#### 🤖 AI Assistant")
    question = st.text_input(
        "Ask EduPath AI:",
        key="right_chat_input",
        placeholder="Ask about PSLE, O-levels, pathways...",
        label_visibility="collapsed",
    )
    col_send, col_clear = st.columns([3, 1])
    with col_send:
        send = st.button("💬 Send", type="primary", use_container_width=True, key="right_chat_send")
    with col_clear:
        clear = st.button("🗑️ Clear", use_container_width=True, key="right_chat_clear")

    if clear:
        st.session_state[_HISTORY_KEY] = []
        st.rerun()

    if send and question and question.strip():
        q = question.strip()

        # Input validation
        from services.web_search_service import validate_question
        is_valid, reason = validate_question(q)
        if not is_valid:
            history.append({"role": "user", "content": q})
            history.append({"role": "assistant", "content": f"I can't process that: {reason}\n\nPlease ask about Singapore's education system."})
            st.session_state[_HISTORY_KEY] = history
            st.rerun()

        with st.spinner("Searching knowledge base + official sources…"):
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

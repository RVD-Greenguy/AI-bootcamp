"""
Right-side AI assistant — SGDS gov.sg styled.
Shows as a floating tab on the right edge when minimised.
Opens the full chat UI in the sidebar when expanded.
Session-only history (clears on logout).
"""
import streamlit as st
from utils.session_manager import get_user

_HISTORY_KEY = "guide_chat_history"
_PENDING_KEY = "_chat_pending_q"
_MAX_PERSIST = 20
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
    """Process a question through validation, RAG, web search, LLM."""
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


def _inject_floating_tab(msg_count: int):
    """Inject a floating blue tab on the right edge using st.components.v1.html for JS support."""
    import streamlit.components.v1 as components

    badge_html = f'<span class="ep-badge">{msg_count}</span>' if msg_count else ""

    components.html(f"""
<script>
(function() {{
    // Remove any previous floating tab from parent
    var old = window.parent.document.getElementById('ep-chat-tab');
    if (old) old.remove();

    // Create floating tab in parent document
    var tab = window.parent.document.createElement('div');
    tab.id = 'ep-chat-tab';
    tab.innerHTML = '🤖 AI Assistant {badge_html}';
    tab.style.cssText = `
        position: fixed;
        right: 0;
        bottom: 100px;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #0269D0, #0151A0);
        color: white;
        padding: 16px 12px;
        border-radius: 12px 0 0 12px;
        cursor: pointer;
        box-shadow: -2px 2px 16px rgba(0,0,0,0.18);
        writing-mode: vertical-rl;
        font-size: 0.85em;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.25s ease;
        user-select: none;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    `;

    tab.addEventListener('mouseenter', function() {{
        tab.style.paddingRight = '18px';
        tab.style.boxShadow = '-4px 2px 24px rgba(2,105,208,0.35)';
    }});
    tab.addEventListener('mouseleave', function() {{
        tab.style.paddingRight = '12px';
        tab.style.boxShadow = '-2px 2px 16px rgba(0,0,0,0.18)';
    }});

    tab.addEventListener('click', function() {{
        // Find the sidebar button with "AI Assistant" text and click it
        var buttons = window.parent.document.querySelectorAll('button');
        for (var i = 0; i < buttons.length; i++) {{
            if (buttons[i].textContent.indexOf('AI Assistant') !== -1) {{
                buttons[i].click();
                return;
            }}
        }}
    }});

    window.parent.document.body.appendChild(tab);

    // Add badge style if not present
    if (!window.parent.document.getElementById('ep-badge-style')) {{
        var style = window.parent.document.createElement('style');
        style.id = 'ep-badge-style';
        style.textContent = `
            .ep-badge {{
                background: #ef4444;
                color: white;
                font-size: 10px;
                font-weight: 700;
                min-width: 20px;
                height: 20px;
                border-radius: 10px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                writing-mode: horizontal-tb;
            }}
        `;
        window.parent.document.head.appendChild(style);
    }}
}})();
</script>
""", height=0)


def _remove_floating_tab():
    """Remove the floating tab from parent document when chat is open."""
    import streamlit.components.v1 as components
    components.html("""
<script>
(function() {
    var tab = window.parent.document.getElementById('ep-chat-tab');
    if (tab) tab.remove();
})();
</script>
""", height=0)


def render_chat_panel():
    """
    Render AI assistant as a right-side floating tab + sidebar chat panel.
    When minimised: floating tab visible on right edge, chat hidden.
    When opened: full chat UI in sidebar, floating tab hidden.
    Returns st.container() for page content.
    """
    user = get_user()
    if not user:
        return st.container()

    user_id = user["id"]

    if _HISTORY_KEY not in st.session_state:
        st.session_state[_HISTORY_KEY] = []
    if "chat_panel_open" not in st.session_state:
        st.session_state["chat_panel_open"] = False

    history: list[dict] = st.session_state.get(_HISTORY_KEY, [])

    pending = st.session_state.pop(_PENDING_KEY, None)
    if pending:
        with st.spinner("Searching knowledge base + official sources…"):
            _process_question(pending, user, history, user_id)
        st.rerun()

    is_open = st.session_state.get("chat_panel_open", False)
    msg_count = len(history) // 2

    if not is_open:
        _inject_floating_tab(msg_count)
        with st.sidebar:
            st.divider()
            if st.button(f"🤖 AI Assistant", key="chat_open_btn", type="primary", use_container_width=True):
                st.session_state["chat_panel_open"] = True
                st.rerun()
    else:
        _remove_floating_tab()
        with st.sidebar:
            st.divider()

            st.markdown("""
<style>
@keyframes ep-fade-in {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
<div style="background:linear-gradient(135deg,#0269D0,#0151A0);
    color:white;padding:12px 16px;border-radius:8px;
    font-weight:600;font-size:0.9em;margin-bottom:10px;
    display:flex;align-items:center;gap:8px;
    animation: ep-fade-in 0.3s ease-out;">
    🤖 AI Assistant
    <span style="margin-left:auto;opacity:0.7;font-size:0.78em;">RAG + GPT-4o</span>
</div>
""", unsafe_allow_html=True)

            if st.button("▾ Minimize", key="chat_close_btn", use_container_width=True):
                st.session_state["chat_panel_open"] = False
                st.rerun()

            chat_box = st.container(height=300)
            with chat_box:
                if not history:
                    st.markdown("""
<div style="text-align:center;padding:16px 4px;color:#6B6B6B;">
    <div style="font-size:1.8em;margin-bottom:8px;">🎓</div>
    <div style="font-size:0.85em;font-weight:600;color:#3B3B3B;">
        Ask about SG education
    </div>
    <div style="font-size:0.78em;color:#6B6B6B;margin-top:4px;">
        PSLE, O-levels, JC, Poly, ITE, University...
    </div>
</div>
""", unsafe_allow_html=True)
                    for i, sq in enumerate(_SUGGESTED):
                        if st.button(f"→ {sq}", key=f"sq_{i}", use_container_width=True):
                            st.session_state[_PENDING_KEY] = sq
                            st.rerun()
                else:
                    display = history[-_MAX_DISPLAY * 2:]
                    for msg in display:
                        if msg["role"] == "user":
                            st.markdown(f"""
<div style="background:#ECF5FE;border:1px solid #C8E2FB;
    padding:8px 12px;border-radius:8px 8px 2px 8px;
    margin:6px 0;font-size:0.82em;color:#0E0E0E;
    animation:ep-fade-in 0.3s ease-out;">
    💬 {msg['content']}
</div>""", unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
<div style="background:#fff;border:1px solid #DFDFDF;border-left:3px solid #0269D0;
    padding:8px 12px;border-radius:2px 8px 8px 8px;
    margin:6px 0;font-size:0.82em;color:#3B3B3B;
    animation:ep-fade-in 0.3s ease-out;">
    {msg['content'].replace(chr(10), '<br>')}
</div>""", unsafe_allow_html=True)

            if msg_count:
                st.caption(f"📋 {msg_count} exchanges · KB + gov.sg")

            question = st.text_input(
                "Ask:",
                key="chat_input",
                placeholder="Ask about pathways…",
                label_visibility="collapsed",
            )
            c1, c2 = st.columns([4, 1])
            with c1:
                send = st.button("Send", type="primary", use_container_width=True, key="chat_send")
            with c2:
                clear = st.button("🗑️", use_container_width=True, key="chat_clear")

            if clear:
                st.session_state[_HISTORY_KEY] = []
                st.rerun()

            if send and question and question.strip():
                st.session_state[_PENDING_KEY] = question.strip()
                st.rerun()

            st.markdown("""
<div style="font-size:0.68em;color:#6B6B6B;text-align:center;margin-top:6px;">
    <a href="https://www.moe.gov.sg" style="color:#0269D0;">MOE</a> ·
    <a href="https://www.seab.gov.sg" style="color:#0269D0;">SEAB</a> ·
    <a href="https://www.ite.edu.sg" style="color:#0269D0;">ITE</a><br>
    For guidance only. Verify with official sources.
</div>
""", unsafe_allow_html=True)

    return st.container()

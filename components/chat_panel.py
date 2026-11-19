"""
Right-side AI assistant — SGDS gov.sg styled.
Streamlit-native two-column layout. Session-only history.
"""
import streamlit as st
from utils.session_manager import get_user

_HISTORY_KEY = "guide_chat_history"
_MAX_PERSIST = 20
_MAX_DISPLAY = 10

_SUGGESTED = [
    "What PSLE score do I need for Express stream?",
    "How does the L1R5 calculation work?",
    "What are the JC cutoff points?",
    "How to apply via DAE with a poly diploma?",
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


def render_chat_panel():
    """
    Render SGDS-styled AI assistant in right column.
    Returns main_col for page content.
    """
    user = get_user()
    if not user:
        return st.container()

    user_id = user["id"]

    if _HISTORY_KEY not in st.session_state:
        st.session_state[_HISTORY_KEY] = []

    history: list[dict] = st.session_state.get(_HISTORY_KEY, [])
    is_open = st.session_state.get("chat_panel_open", True)

    if not is_open:
        main_col, toggle_col = st.columns([50, 1])
        with toggle_col:
            if st.button("💬", key="chat_open_btn", help="Open AI Assistant"):
                st.session_state["chat_panel_open"] = True
                st.rerun()
        return main_col

    main_col, chat_col = st.columns([3, 1], gap="medium")

    with chat_col:
        # ── Header (gov.sg blue) ──────────────────────────────
        st.markdown("""
<div style="background:linear-gradient(135deg,#0269D0,#0151A0);
    color:white;padding:12px 16px;border-radius:8px 8px 0 0;
    margin:-1rem -1rem 0 -1rem;font-weight:600;font-size:0.9em;
    display:flex;align-items:center;gap:8px;">
    🤖 EduPath AI Assistant
    <span style="margin-left:auto;opacity:0.8;font-size:0.85em;">
        Powered by RAG + GPT-4o
    </span>
</div>
""", unsafe_allow_html=True)

        # Close button
        if st.button("✕ Close", key="chat_close_btn", use_container_width=True):
            st.session_state["chat_panel_open"] = False
            st.rerun()

        # ── Chat messages ─────────────────────────────────────
        chat_box = st.container(height=380)
        with chat_box:
            if not history:
                # Welcome state with suggestions
                st.markdown("""
<div style="text-align:center;padding:16px 8px;color:#6B6B6B;">
    <div style="font-size:2em;margin-bottom:8px;">🎓</div>
    <div style="font-size:0.9em;font-weight:600;color:#3B3B3B;">
        Ask me about Singapore's education system
    </div>
    <div style="font-size:0.8em;margin-top:4px;">
        PSLE · O-levels · A-levels · JC · Poly · ITE · University
    </div>
</div>
""", unsafe_allow_html=True)
                st.markdown("**Try asking:**")
                for sq in _SUGGESTED:
                    if st.button(f"→ {sq}", key=f"sq_{hash(sq)}", use_container_width=True):
                        st.session_state["_prefill_q"] = sq
                        st.rerun()
            else:
                display = history[-_MAX_DISPLAY * 2:]
                for msg in display:
                    if msg["role"] == "user":
                        st.markdown(f"""
<div style="background:#ECF5FE;border:1px solid #C8E2FB;
    padding:8px 12px;border-radius:8px 8px 2px 8px;
    margin:6px 0 6px 15%;font-size:0.85em;color:#0E0E0E;">
    {msg['content']}
</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
<div style="background:#FFFFFF;border:1px solid #DFDFDF;
    border-left:3px solid #0269D0;
    padding:8px 12px;border-radius:2px 8px 8px 8px;
    margin:6px 15% 6px 0;font-size:0.85em;color:#3B3B3B;">
    {msg['content'].replace(chr(10), '<br>')}
</div>""", unsafe_allow_html=True)

        # ── Source indicator ──────────────────────────────────
        msg_count = len(history) // 2
        if msg_count:
            st.caption(f"📋 {msg_count} exchange{'s' if msg_count != 1 else ''} · Sources: Local KB + gov.sg/edu.sg")

        # ── Input ─────────────────────────────────────────────
        prefill = st.session_state.pop("_prefill_q", "")
        question = st.text_input(
            "Your question:",
            value=prefill,
            key="chat_input",
            placeholder="Ask about education pathways...",
            label_visibility="collapsed",
        )

        c1, c2 = st.columns([4, 1])
        with c1:
            send = st.button("Send", type="primary", use_container_width=True, key="chat_send")
        with c2:
            clear = st.button("🗑️", use_container_width=True, key="chat_clear", help="Clear chat history")

        if clear:
            st.session_state[_HISTORY_KEY] = []
            st.rerun()

        if send and question and question.strip():
            q = question.strip()

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

        # ── Footer note ───────────────────────────────────────
        st.markdown("""
<div style="background:#F3F3F3;border-radius:0 0 8px 8px;padding:8px 12px;
    margin:8px -1rem -1rem -1rem;font-size:0.72em;color:#6B6B6B;text-align:center;">
    Data from <a href="https://www.moe.gov.sg" style="color:#0269D0;">MOE</a> ·
    <a href="https://www.seab.gov.sg" style="color:#0269D0;">SEAB</a> ·
    <a href="https://www.ite.edu.sg" style="color:#0269D0;">ITE</a><br>
    AI responses are for guidance only. Verify with official sources.
</div>
""", unsafe_allow_html=True)

    return main_col

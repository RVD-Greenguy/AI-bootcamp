import streamlit as st

st.set_page_config(page_title="AI Education Guide — EduPath SG", page_icon="🤖", layout="wide")

from utils.session_manager import require_login, append_chat, get_chat_history, clear_chat, get_career_goal
from utils.config import DISCLAIMER
from components.sidebar import render_sidebar
from components.chat_panel import render_chat_panel
from components.stage_theme import apply_stage_theme
from components.role_context import get_role_labels
from components.rag_sources import render_rag_sources
from services.rag_service import retrieve_chunks
from services.llm_service import ask_guide, moderate_content

user = require_login()
render_sidebar()
render_chat_panel()
apply_stage_theme()

st.title("🤖 AI Education Guide")
st.caption("Ask anything about Singapore's education system — policies, scores, pathways, fallbacks.")
st.warning(f"⚠️ {DISCLAIMER}", icon="⚠️")

SUGGESTED = {
    "parent": [
        "How does P1 registration work?",
        "What's the difference between IP and non-IP schools?",
        "My child got AL 15 — what are the options?",
        "How do I compare polytechnic vs JC?",
    ],
    "student": [
        "How do I calculate my L1R5?",
        "What JCs can I get into with net L1R5 of 10?",
        "I failed English at O-levels — what can I do?",
        "What's the DAE process for poly students?",
    ],
    "teacher": [
        "Explain the JAE process step by step",
        "What fallback options exist for Normal Academic students?",
        "How does A-level rank points calculation work?",
        "What is the PFP pathway?",
    ],
}

GREETINGS = {
    "parent": "Welcome! Ask me anything about planning your child's education journey in Singapore. I cover everything from P1 registration to university admission.",
    "student": "Hi! Ask me about your score, your options, or what happens if things don't go as planned. I know the full Singapore education pathway.",
    "teacher": "Hello! Use this guide for student counselling — full pathway coverage from PSLE to post-grad, including fallback policies.",
}

col_chat, col_ref = st.columns([3, 1])

with col_chat:
    role = user.get("role", "student")
    st.info(GREETINGS.get(role, GREETINGS["student"]))

    # Suggested questions as quick buttons
    st.markdown("**Quick questions:**")
    suggested = SUGGESTED.get(role, SUGGESTED["student"])
    btn_cols = st.columns(2)
    for i, q in enumerate(suggested):
        if btn_cols[i % 2].button(q, key=f"sq_{i}", use_container_width=True):
            st.session_state["pending_question"] = q

    st.divider()

    # Main question input
    user_input = st.text_area(
        "Your question:",
        value=st.session_state.pop("pending_question", ""),
        height=100,
        placeholder="e.g. What happens if my child doesn't get into any JC? What are the alternatives?",
        key="guide_input",
    )

    col_send, col_clear = st.columns([3, 1])
    with col_send:
        send = st.button("🤖 Ask Guide", type="primary", use_container_width=True)
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            clear_chat("guide")
            st.session_state.pop("guide_last_chunks", None)
            st.rerun()

    if send:
        q = user_input.strip()
        if not q:
            st.warning("Please enter a question.")
        elif not moderate_content(q):
            st.error("Your question contains inappropriate content. Please revise.")
        else:
            with st.spinner("Retrieving references and generating answer..."):
                chunks = retrieve_chunks(q, n_results=4)
                history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in get_chat_history("guide")
                ]
                role_labels = get_role_labels(role)
                role_ctx = [{"role": "system", "content": role_labels["ai_role_context"]}]
                career = get_career_goal()
                career_ctx = [{"role": "system", "content": f"The user's career aspiration is: {career}. Tailor advice toward this goal."}] if career else []
                append_chat("user", q, "guide")
                response = ask_guide(q, chunks, role_ctx + career_ctx + history)
                append_chat("assistant", response, "guide")
                st.session_state["guide_last_chunks"] = chunks

    # Show RAG sources for last response
    if st.session_state.get("guide_last_chunks"):
        render_rag_sources(st.session_state["guide_last_chunks"], key="guide_rag")

    # Chat history
    history = get_chat_history("guide")
    if history:
        st.divider()
        st.markdown("**Conversation:**")
        for msg in reversed(history):
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").markdown(msg["content"])

with col_ref:
    st.markdown("### 📊 Key Thresholds")
    thresholds = {
        "PSLE": [
            ("AL 4–8", "Top IP schools"),
            ("AL 4–20", "Express stream"),
            ("AL 21–22", "Normal Academic"),
            ("AL 23–32", "Normal Technical"),
        ],
        "O-levels → JC": [
            ("Net ≤ 4", "RJC / HCJC"),
            ("Net ≤ 7", "NJC / ACJC / VJC"),
            ("Net ≤ 10", "TJC / CJC"),
            ("Net ≤ 20", "Any JC eligible"),
        ],
        "A-levels → Uni": [
            ("85–90 pts", "Medicine / Dentistry"),
            ("80–88 pts", "Law"),
            ("75–85 pts", "CS / Data Science"),
            ("70–82 pts", "Engineering"),
            ("65–78 pts", "Arts / Social Sci"),
        ],
        "Poly GPA → DAE": [
            ("3.8+", "Competitive courses"),
            ("3.4+", "Engineering"),
            ("3.2+", "Business"),
            ("3.0+", "Most programmes"),
            ("2.5+", "SIT / SUSS"),
        ],
    }
    for section, rows in thresholds.items():
        st.markdown(f"**{section}**")
        for score, label in rows:
            st.caption(f"`{score}` → {label}")
        st.markdown("")

    st.divider()
    st.markdown("### 🔗 Official Links")
    official_links = [
        ("MOE", "https://www.moe.gov.sg"),
        ("SEAB", "https://www.seab.gov.sg"),
        ("ITE", "https://www.ite.edu.sg"),
        ("JAE Info", "https://www.moe.gov.sg/post-secondary/admissions/jae"),
        ("SP", "https://www.sp.edu.sg"),
        ("TP", "https://www.tp.edu.sg"),
        ("NYP", "https://www.nyp.edu.sg"),
        ("NP", "https://www.np.edu.sg"),
        ("RP", "https://www.rp.edu.sg"),
        ("NUS", "https://www.nus.edu.sg/admissions"),
        ("NTU", "https://www.ntu.edu.sg/admissions"),
        ("SMU", "https://admissions.smu.edu.sg"),
        ("SUTD", "https://www.sutd.edu.sg/admissions"),
        ("SIT", "https://www.singaporetech.edu.sg/admissions"),
        ("SUSS", "https://www.suss.edu.sg/admissions"),
        ("SkillsFuture", "https://www.skillsfuture.gov.sg"),
    ]
    for name, url in official_links:
        st.markdown(f"[{name}]({url})")

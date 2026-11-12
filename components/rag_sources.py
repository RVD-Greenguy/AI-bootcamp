import streamlit as st


def render_rag_sources(chunks: list[dict], key: str = "rag") -> None:
    if not chunks:
        return
    with st.expander(f"📚 Sources Retrieved ({len(chunks)} references)", expanded=False):
        st.caption("These official references were retrieved from the knowledge base to inform this response.")
        for i, c in enumerate(chunks, 1):
            score = c.get("score", 0)
            relevance = "🟢 High" if score >= 0.25 else ("🟡 Medium" if score >= 0.1 else "🔴 Low")
            st.markdown(f"**{i}. {c.get('topic', 'Reference')}** — *{c.get('source', 'Knowledge Base')}* | {relevance} relevance")
            st.markdown(f"> {c['text'][:250]}{'...' if len(c['text']) > 250 else ''}")
            if c.get("url"):
                st.markdown(f"🔗 [Official Source]({c['url']})")
            if i < len(chunks):
                st.divider()

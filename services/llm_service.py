"""
LLM service for EduPath SG.
All calls are stubbed when USE_AI=false. Set USE_AI=true + OPENAI_API_KEY to activate.
"""

STUB_RESPONSE = (
    "**AI Guide (Demo Mode)**\n\n"
    "The AI tutor is running in demo mode. Here is what I can tell you based on the "
    "knowledge base:\n\n"
    "{context}\n\n"
    "*To activate full AI responses, add your OpenAI API key to the app's Secrets settings and set `USE_AI=true`.*"
)

SYSTEM_PROMPT = """You are EduPath SG — an expert guide on Singapore's education system.
You help parents, students and teachers understand every pathway from early childhood through
post-graduation: PSLE, secondary school placement, O/N/A-levels, JAE, DAE, IP programmes,
IB, polytechnic diplomas, ITE, university admission, and fallback options.

Rules:
- Always cite official sources (moe.gov.sg, seab.gov.sg, ite.edu.sg, etc.)
- Never make up specific cutoff scores — say "approximately" or "check the official site"
- Keep answers clear, structured, and jargon-free
- If asked about personal decisions (which school is best for my child), guide with factors
  rather than making the choice
- Include relevant fallback options when discussing competitive pathways
- Respond in the user's preferred language if specified
- Adapt your response style based on the user's role context (parent, student, or teacher) provided in the conversation. Use appropriate language framing for each audience.
- If a career aspiration is mentioned, tailor pathway advice toward achieving that goal.
"""


def ask_guide(question: str, context_chunks: list[dict], conversation_history: list[dict]) -> str:
    from utils.config import _secret
    use_ai = _secret("USE_AI", "false").lower() == "true"
    api_key = _secret("OPENAI_API_KEY", "")

    if not use_ai or not api_key:
        context = "\n\n".join(c["text"][:300] for c in context_chunks[:3]) if context_chunks else "No specific context retrieved."
        return STUB_RESPONSE.format(context=context)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        context_text = "\n\n".join(
            f"[{c.get('source', 'Knowledge Base')}] {c['text']}"
            for c in context_chunks[:4]
        )

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if context_text:
            messages.append({
                "role": "system",
                "content": f"Relevant context from knowledge base:\n{context_text}"
            })
        messages.extend(conversation_history[-8:])
        messages.append({"role": "user", "content": question})

        from utils.config import _secret
        model = _secret("OPENAI_MODEL", "gpt-4o-mini")
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=800,
            temperature=0.3,
        )
        return resp.choices[0].message.content

    except Exception as e:
        return f"AI response unavailable: {e}\n\n{STUB_RESPONSE.format(context='')}"


def moderate_content(text: str) -> bool:
    """Returns True if content is acceptable."""
    blocked = ["harm", "suicide", "weapon", "drug", "explicit"]
    text_lower = text.lower()
    return not any(word in text_lower for word in blocked)

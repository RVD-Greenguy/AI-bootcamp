"""
Secure web search for Singapore education content.

Only fetches from allowlisted government and education domains.
Includes input sanitisation and content guardrails.
"""
from __future__ import annotations
import re
import requests
import streamlit as st

# ── Domain allowlist ─────────────────────────────────────────────────────────
ALLOWED_DOMAINS = [
    "moe.gov.sg",
    "seab.gov.sg",
    "ite.edu.sg",
    "skillsfuture.gov.sg",
    "myskillsfuture.gov.sg",
    "ecg.moe.edu.sg",
    "nus.edu.sg",
    "ntu.edu.sg",
    "smu.edu.sg",
    "sutd.edu.sg",
    "sit.edu.sg",
    "suss.edu.sg",
    "sp.edu.sg",
    "tp.edu.sg",
    "nyp.edu.sg",
    "np.edu.sg",
    "rp.edu.sg",
    "nie.edu.sg",
    "cpf.gov.sg",
    "mom.gov.sg",
    "ssg.gov.sg",
    "psc.gov.sg",
]

ALLOWED_SUFFIXES = (".gov.sg", ".edu.sg")

# ── Security: blocked terms ──────────────────────────────────────────────────
BLOCKED_INPUT_PATTERNS = [
    r"(?i)(hack|exploit|bypass|inject|<script|javascript:|data:text|eval\()",
    r"(?i)(password|credential|token|api.key|secret)",
    r"(?i)(drop\s+table|select\s+\*|union\s+select|insert\s+into)",
    r"(?i)(porn|xxx|gambling|casino|bet\s+online)",
    r"(?i)(weapon|bomb|explosive|how\s+to\s+kill)",
]

# ── Topic guardrail ──────────────────────────────────────────────────────────
EDUCATION_KEYWORDS = [
    "school", "psle", "o-level", "a-level", "n-level", "ite", "jc",
    "polytechnic", "poly", "university", "uni", "education", "student",
    "admission", "cutoff", "score", "grade", "exam", "tuition", "moe",
    "seab", "scholarship", "bursary", "diploma", "degree", "course",
    "curriculum", "teacher", "parent", "primary", "secondary", "tertiary",
    "skillsfuture", "pathway", "stream", "express", "normal", "ip",
    "dae", "jae", "career", "counselling", "study", "registration",
    "enrollment", "subject", "h1", "h2", "h3", "gpa", "al score",
    "l1r5", "elr2b2", "rank point", "uas", "faculty", "nitec",
]


def _is_domain_allowed(url: str) -> bool:
    """Check if URL belongs to an allowlisted domain."""
    try:
        from urllib.parse import urlparse
        hostname = urlparse(url).hostname or ""
        hostname = hostname.lower()
        if any(hostname == d or hostname.endswith("." + d) for d in ALLOWED_DOMAINS):
            return True
        if any(hostname.endswith(suffix) for suffix in ALLOWED_SUFFIXES):
            return True
        return False
    except Exception:
        return False


def _sanitise_query(query: str) -> str | None:
    """
    Sanitise and validate a search query.
    Returns cleaned query or None if blocked.
    """
    query = query.strip()
    if not query or len(query) < 3 or len(query) > 300:
        return None

    for pattern in BLOCKED_INPUT_PATTERNS:
        if re.search(pattern, query):
            return None

    # Must contain at least one education-related keyword
    query_lower = query.lower()
    if not any(kw in query_lower for kw in EDUCATION_KEYWORDS):
        return None

    # Strip any HTML/script tags
    query = re.sub(r"<[^>]+>", "", query)
    query = re.sub(r"[^\w\s\-.,?!'\"/()]+", " ", query)
    return query.strip()


def _build_search_url(query: str) -> str:
    """Build a Google Custom Search-compatible URL restricted to allowed sites."""
    site_restrict = " OR ".join(f"site:{d}" for d in ALLOWED_DOMAINS[:8])
    full_query = f"Singapore education {query} ({site_restrict})"
    return full_query


@st.cache_data(ttl=3600, show_spinner=False)
def search_web(query: str, max_results: int = 3) -> list[dict]:
    """
    Search for Singapore education content from trusted .gov.sg / .edu.sg sites.

    Uses DuckDuckGo (no API key needed) with domain filtering.
    Falls back to curated static URL list if DDG fails.

    Returns list of {"title", "url", "snippet"} dicts.
    """
    clean_query = _sanitise_query(query)
    if not clean_query:
        return []

    # Try DuckDuckGo first
    results = _search_duckduckgo(clean_query, max_results)
    if results:
        return results

    # Fallback: curated URL matching based on keywords
    return _search_curated(clean_query, max_results)


def _search_duckduckgo(query: str, max_results: int) -> list[dict]:
    """Search DuckDuckGo and filter to allowed .gov.sg / .edu.sg domains."""
    try:
        from duckduckgo_search import DDGS

        site_filter = "site:moe.gov.sg OR site:seab.gov.sg OR site:edu.sg OR site:gov.sg"
        full_query = f"Singapore education {query} {site_filter}"

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(full_query, max_results=max_results * 3):
                url = r.get("href", "")
                if _is_domain_allowed(url):
                    results.append({
                        "title": r.get("title", ""),
                        "url": url,
                        "snippet": r.get("body", ""),
                    })
                if len(results) >= max_results:
                    break

        return results
    except ImportError:
        return _search_duckduckgo_lite(query, max_results)
    except Exception:
        return []


def _search_duckduckgo_lite(query: str, max_results: int) -> list[dict]:
    """Fallback: use DuckDuckGo HTML lite endpoint (no pip package needed)."""
    try:
        full_query = f"Singapore education {query} site:gov.sg OR site:edu.sg"
        resp = requests.get(
            "https://lite.duckduckgo.com/lite/",
            params={"q": full_query},
            headers={"User-Agent": "EduPathSG/1.0 (Education Navigator)"},
            timeout=8,
        )
        resp.raise_for_status()
        text = resp.text

        import re
        results = []
        # Parse result links from the lite HTML
        links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="result-link"[^>]*>([^<]+)</a>', text)
        if not links:
            links = re.findall(r'<a[^>]+rel="nofollow"[^>]+href="(https?://[^"]+)"[^>]*>([^<]+)</a>', text)

        for url, title in links:
            if _is_domain_allowed(url):
                results.append({
                    "title": title.strip(),
                    "url": url,
                    "snippet": "",
                })
            if len(results) >= max_results:
                break

        return results
    except Exception:
        return []


# ── Curated knowledge URLs ───────────────────────────────────────────────────
_CURATED_SOURCES = [
    {"keywords": ["psle", "primary", "p1", "al score", "achievement level"],
     "title": "MOE — PSLE Scoring & Secondary School Posting",
     "url": "https://www.moe.gov.sg/primary/psle",
     "snippet": "Information on PSLE Achievement Level scoring, secondary school posting, and what to expect after P6."},

    {"keywords": ["p1", "registration", "primary 1", "phase 2"],
     "title": "MOE — P1 Registration",
     "url": "https://www.moe.gov.sg/primary/p1-registration",
     "snippet": "Official P1 registration exercise phases, eligibility, and key dates."},

    {"keywords": ["secondary", "school", "express", "normal", "stream"],
     "title": "MOE — Secondary School Education",
     "url": "https://www.moe.gov.sg/secondary",
     "snippet": "Singapore secondary school system: streams, IP, subject-based banding, and school types."},

    {"keywords": ["o-level", "o level", "olevel", "jae", "jc", "junior college"],
     "title": "MOE — JAE (Joint Admissions Exercise)",
     "url": "https://www.moe.gov.sg/post-secondary/admissions/jae",
     "snippet": "Apply to JC, Polytechnic or ITE after O-level results. Application window, cutoff points, and posting."},

    {"keywords": ["a-level", "a level", "alevel", "rank point", "uas", "university"],
     "title": "MOE — University Admissions",
     "url": "https://www.moe.gov.sg/post-secondary/admissions/university",
     "snippet": "University admission pathways: A-level rank points, polytechnic GPA (DAE), IB, and international qualifications."},

    {"keywords": ["polytechnic", "poly", "diploma", "elr2b2"],
     "title": "MOE — Polytechnic Education",
     "url": "https://www.moe.gov.sg/post-secondary/admissions/polytechnics",
     "snippet": "Polytechnic admissions, course information, ELR2B2 aggregate scoring, and career pathways."},

    {"keywords": ["ite", "nitec", "higher nitec", "technical"],
     "title": "ITE — Courses & Admissions",
     "url": "https://www.ite.edu.sg/courses",
     "snippet": "ITE NITEC and Higher NITEC courses, entry requirements, and progression to polytechnic."},

    {"keywords": ["scholarship", "bursary", "financial", "assistance"],
     "title": "MOE — Financial Assistance Scheme",
     "url": "https://www.moe.gov.sg/financial-matters/financial-assistance",
     "snippet": "MOE Financial Assistance Scheme (FAS), bursaries, and fee subsidies for Singapore students."},

    {"keywords": ["skillsfuture", "credit", "lifelong", "adult"],
     "title": "SkillsFuture Singapore",
     "url": "https://www.skillsfuture.gov.sg",
     "snippet": "SkillsFuture Credit, courses, Earn and Learn programmes, and mid-career support for Singaporeans."},

    {"keywords": ["ip", "integrated programme", "through-train"],
     "title": "MOE — Integrated Programme (IP)",
     "url": "https://www.moe.gov.sg/secondary/courses/integrated-programme",
     "snippet": "IP schools allow students to skip O-levels, proceeding directly to A-levels or IB after 6 years."},

    {"keywords": ["dae", "direct admission", "poly to uni", "gpa"],
     "title": "MOE — Direct Admissions Exercise",
     "url": "https://www.moe.gov.sg/post-secondary/admissions/university",
     "snippet": "Polytechnic diploma holders apply directly to university via DAE. GPA requirements and portfolio."},

    {"keywords": ["private candidate", "retake", "resit", "seab"],
     "title": "SEAB — Private Candidates",
     "url": "https://www.seab.gov.sg/home/examinations/private-candidates",
     "snippet": "Registration for retaking O-level, N-level, or A-level exams as a private candidate with SEAB."},

    {"keywords": ["special education", "sped", "learning support", "dyslexia"],
     "title": "MOE — Special Educational Needs",
     "url": "https://www.moe.gov.sg/special-educational-needs",
     "snippet": "Support for students with special educational needs: SPED schools, mainstream integration, Allied Educators."},

    {"keywords": ["pfp", "foundation programme", "normal academic"],
     "title": "MOE — Polytechnic Foundation Programme (PFP)",
     "url": "https://www.moe.gov.sg/post-secondary/admissions/pfp",
     "snippet": "N(A) students with good results can enter polytechnic directly via PFP, saving one year."},

    {"keywords": ["law", "lawyer", "llb", "bar exam"],
     "title": "NUS Faculty of Law",
     "url": "https://law.nus.edu.sg",
     "snippet": "NUS Law LLB programme: admission requirements, A-level rank points ~84, interview process."},

    {"keywords": ["medicine", "doctor", "mbbs", "medical"],
     "title": "NUS Yong Loo Lin School of Medicine",
     "url": "https://medicine.nus.edu.sg",
     "snippet": "NUS Medicine MBBS: 5-year programme, rank points ~87, interview and aptitude test required."},

    {"keywords": ["computing", "computer science", "software", "engineering", "data science"],
     "title": "NUS School of Computing",
     "url": "https://www.comp.nus.edu.sg",
     "snippet": "NUS Computing: CS, Information Systems, Data Science. Rank points ~80. High demand."},
]


def _search_curated(query: str, max_results: int) -> list[dict]:
    """Match query against curated education URLs."""
    query_lower = query.lower()
    scored = []
    for entry in _CURATED_SOURCES:
        score = sum(1 for kw in entry["keywords"] if kw in query_lower)
        if score > 0:
            scored.append((score, entry))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {"title": e["title"], "url": e["url"], "snippet": e["snippet"]}
        for _, e in scored[:max_results]
    ]


def validate_question(question: str) -> tuple[bool, str]:
    """
    Validate a user question before processing.
    Returns (is_valid, reason).
    """
    if not question or len(question.strip()) < 3:
        return False, "Question is too short."
    if len(question) > 500:
        return False, "Question is too long (max 500 characters)."

    for pattern in BLOCKED_INPUT_PATTERNS:
        if re.search(pattern, question):
            return False, "Your question contains blocked content. Please rephrase."

    q_lower = question.lower()
    if any(kw in q_lower for kw in EDUCATION_KEYWORDS):
        return True, ""

    # Allow general questions that don't match keywords (the LLM will handle them)
    return True, ""

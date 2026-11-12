"""
TF-IDF RAG over Singapore education policy data.
Works with zero API keys. Upgrades to OpenAI embeddings when USE_AI=true.
"""
from __future__ import annotations
import pickle
import json
from pathlib import Path
from threading import Lock

import numpy as np

_STORE_PATH = Path(__file__).parent.parent / "storage" / "tfidf_store.pkl"
_lock = Lock()
_vectorizer = None
_matrix = None
_docs: list[dict] = []

DATA_DIR = Path(__file__).parent.parent / "data" / "seed"


def build_index() -> int:
    global _vectorizer, _matrix, _docs
    from sklearn.feature_extraction.text import TfidfVectorizer

    chunks: list[dict] = []

    def _load(filename):
        p = DATA_DIR / filename
        return json.loads(p.read_text()) if p.exists() else []

    # Education stages
    for s in _load("education_stages.json"):
        text = f"{s.get('name','')}. {s.get('description','')} Entry: {s.get('entry_criteria','')} Exit: {s.get('exit_process','')}"
        chunks.append({"text": text, "source": "MOE Education Stages", "topic": s.get("name",""), "url": s.get("official_url","")})

    # Secondary schools
    for s in _load("secondary_schools.json"):
        text = (f"{s.get('name','')} — {s.get('type','')} school. "
                f"{'IP school. ' if s.get('is_ip') else ''}"
                f"PSLE AL cutoff approximately {s.get('psle_al_cutoff_min')}–{s.get('psle_al_cutoff_max')}. "
                f"End qualification: {s.get('ip_end_qual') or 'O-levels'}. "
                f"Location: {s.get('location','')}. Gender: {s.get('gender','')}.")
        chunks.append({"text": text, "source": "MOE Secondary Schools", "topic": s.get("name",""), "url": s.get("official_url","")})

    # JC data
    for j in _load("jc_data.json"):
        cutoff = j.get("l1r5_cutoff_2023","")
        text = (f"{j.get('name','')} Junior College. "
                f"L1R5 cutoff approximately {cutoff}. "
                f"Affiliated secondary schools: {', '.join(j.get('affiliation_schools',[]))}.")
        chunks.append({"text": text, "source": "MOE JC Admissions", "topic": j.get("name",""), "url": j.get("official_url","")})

    # Poly courses
    for c in _load("poly_courses.json"):
        text = (f"{c.get('poly_name','')} — {c.get('course_name','')}. "
                f"ELR2B2 cutoff approximately {c.get('elr2b2_cutoff_approximate','')}. "
                f"Career paths: {', '.join(c.get('career_paths',[]))}.")
        chunks.append({"text": text, "source": "Polytechnic Admissions", "topic": c.get("course_name",""), "url": c.get("official_url","")})

    # ITE data
    for c in _load("ite_data.json"):
        text = (f"ITE {c.get('college','')} — {c.get('course_name','')} ({c.get('qualification','')}). "
                f"Entry: {c.get('entry_requirement','')}. "
                f"Sector: {c.get('industry_sector','')}. "
                f"Progression to poly: {'Yes' if c.get('progression_to_poly') else 'Possible with Higher NITEC'}.")
        chunks.append({"text": text, "source": "ITE Education Services", "topic": c.get("course_name",""), "url": c.get("official_url","")})

    # University data
    for u in _load("university_data.json"):
        for f in u.get("popular_faculties", []):
            text = (f"{u.get('name','')} — {f.get('faculty_name','')}. "
                    f"A-level rank points: approximately {f.get('min_rank_points_alevel','')}+. "
                    f"Poly GPA (DAE): {f.get('min_gpa_poly','')}+. "
                    f"Duration: {f.get('course_duration','')}.")
            chunks.append({"text": text, "source": f"{u.get('short_name','')} Admissions", "topic": f.get("faculty_name",""), "url": ""})

    # Fallback policies
    for fp in _load("fallback_policies.json"):
        text = (f"Fallback: {fp.get('scenario','')}. "
                f"Trigger: {fp.get('trigger_condition','')}. "
                f"Policy: {fp.get('official_policy','')}. "
                f"Options: {'; '.join(o.get('option_name','') + ': ' + o.get('description','') for o in fp.get('options',[])[:3])}.")
        chunks.append({"text": text, "source": "MOE / SEAB Policies", "topic": fp.get("scenario",""), "url": fp.get("official_url","")})

    # Support resources
    support = _load("support_resources.json")
    if isinstance(support, dict):
        for item in support.get("counselling", []):
            text = (f"Counselling: {item.get('name','')}. {item.get('description','')} "
                    f"How to access: {item.get('how_to_access','')} Eligibility: {item.get('eligibility','')}")
            chunks.append({"text": text, "source": "MOE / Mental Health Support", "topic": item.get("name",""), "url": item.get("official_url","")})
        for item in support.get("career_guidance", []):
            text = (f"Career guidance: {item.get('name','')}. {item.get('description','')} "
                    f"How to access: {item.get('how_to_access','')} Eligibility: {item.get('eligibility','')}")
            chunks.append({"text": text, "source": "MOE / WSG Career Guidance", "topic": item.get("name",""), "url": item.get("official_url","")})
        for item in support.get("talks_events", []):
            text = (f"Event/Talk: {item.get('name','')}. {item.get('description','')} "
                    f"Timing: {item.get('typical_timing','')} Eligibility: {item.get('eligibility','')}")
            chunks.append({"text": text, "source": "Open Houses & Career Events", "topic": item.get("name",""), "url": item.get("official_url","")})
        for item in support.get("scholarships", []):
            text = (f"Scholarship/Bursary: {item.get('name','')} ({item.get('type','')}). {item.get('description','')} "
                    f"Eligibility: {item.get('eligibility','')} Value: {item.get('value','')} Bond: {item.get('bond','N/A')}")
            chunks.append({"text": text, "source": "Scholarships & Financial Aid", "topic": item.get("name",""), "url": item.get("official_url","")})
        for item in support.get("earn_and_learn", []):
            text = (f"Earn & Learn: {item.get('name','')} ({item.get('type','')}). {item.get('description','')} "
                    f"Eligibility: {item.get('eligibility','')} Sectors: {', '.join(item.get('sectors', []))}")
            chunks.append({"text": text, "source": "SkillsFuture / WSG Programmes", "topic": item.get("name",""), "url": item.get("official_url","")})

    # Static knowledge chunks (key facts not in JSON)
    static_chunks = [
        {"text": "PSLE Achievement Level (AL) scoring: each subject graded AL1-AL8. Total AL = sum of 4 subjects (4 = best, 32 = weakest). Introduced in 2021 replacing T-score.", "source": "MOE PSLE", "topic": "PSLE Scoring", "url": "https://www.moe.gov.sg/primary/psle"},
        {"text": "JAE (Joint Admissions Exercise) is held in January after O-level results. Students apply to JC, Polytechnic or ITE. Applications open for about 3 days. Results in late January.", "source": "MOE JAE", "topic": "JAE Process", "url": "https://www.moe.gov.sg/post-secondary/admissions/jae"},
        {"text": "DAE (Direct Admissions Exercise) allows polytechnic diploma holders to apply directly to university based on GPA and portfolio. Applications in March-April. Universities consider GPA, interview, portfolio.", "source": "MOE DAE", "topic": "DAE Process", "url": "https://www.moe.gov.sg/post-secondary/admissions/university"},
        {"text": "L1R5 for JC: L1 = English Language grade. R5 = best 5 relevant subjects including at least one humanities and one math/science. Grade points: A1=1, A2=2, B3=3, B4=4, C5=5, C6=6, D7=7, E8=8, F9=9. Net aggregate = raw L1R5 minus bonus points (CCA up to -2, affiliation -2). Minimum net aggregate is 2.", "source": "MOE JAE", "topic": "L1R5 Calculation", "url": "https://www.moe.gov.sg/post-secondary/admissions/jae"},
        {"text": "IP (Integrated Programme) schools allow high-achieving students to bypass O-levels and proceed directly to A-levels or IB after 6 years. Schools include RI, RGS, HCI, ACSI (IB), SCGS, Victoria School, NJC, Dunman High, River Valley High, Cedar Girls, CHIJ St Nicholas, Nanyang Girls, SJI (IB), NUS High (special programme).", "source": "MOE", "topic": "IP Programme", "url": "https://www.moe.gov.sg/secondary/schools"},
        {"text": "O-level private candidates: Students who fail to meet progression criteria, or wish to improve grades, can register with SEAB as private candidates. Registration period: March-April. Exam sitting: October/November. All results appear on official SEAB certificate. First-attempt results are visible to universities.", "source": "SEAB", "topic": "Private Candidate O-levels", "url": "https://www.seab.gov.sg/home/examinations/private-candidates"},
        {"text": "A-level private candidates: Can retake individual H1 or H2 subjects. Must re-sit as full H2 subject if retaking. Results from all sittings appear on cert. Some faculties (Medicine, Law) may consider all attempts.", "source": "SEAB", "topic": "Private Candidate A-levels", "url": "https://www.seab.gov.sg"},
        {"text": "English Language is mandatory for most post-secondary pathways. Failing English O-levels (grade below C6) means: no JC admission, most poly courses require at least C6 English. Can retake English as private candidate. Some ITE courses accept D7.", "source": "MOE", "topic": "English Requirement", "url": "https://www.moe.gov.sg"},
        {"text": "Polytechnic Foundation Programme (PFP): Normal Academic students who pass N(A)-levels with a good aggregate can apply directly to polytechnic via PFP. Saves one year compared to Sec 5 → O-levels route.", "source": "MOE", "topic": "PFP", "url": "https://www.moe.gov.sg/post-secondary/admissions/pfp"},
        {"text": "SkillsFuture Credit: All Singapore Citizens aged 25 and above receive $500 credit (topped up with additional $500 for mid-career support). Can be used for approved courses at polytechnics, ITE, universities and private providers.", "source": "SkillsFuture Singapore", "topic": "SkillsFuture", "url": "https://www.skillsfuture.gov.sg"},
        {"text": "IB (International Baccalaureate) offered at ACS(I), St Joseph's Institution and some international schools. Maximum 45 points. University admission: NUS/NTU/SMU accept IB. Points conversion differs by faculty.", "source": "IBDP Schools", "topic": "IB Programme", "url": "https://www.ibo.org"},
        {"text": "P1 Registration Phases: Phase 1 (siblings in school), Phase 2A1 (child of staff/former student), Phase 2A2 (member/former student of school), Phase 2B (community/CCA affiliation), Phase 2C (all citizens), Phase 2C Supplementary, Phase 3 (PRs and others). Priority given to Singapore Citizens over PRs in oversubscribed phases.", "source": "MOE P1 Registration", "topic": "P1 Registration", "url": "https://www.moe.gov.sg/primary/p1-registration"},
        {"text": "NITEC and Higher NITEC at ITE: NITEC is 2-year programme. Higher NITEC is 2-year programme for NITEC graduates or O-level holders. Higher NITEC graduates can apply to polytechnic Year 1 or Year 2 (with exemptions). ITE offers 3 colleges: College East, Central, West.", "source": "ITE Education Services", "topic": "ITE NITEC", "url": "https://www.ite.edu.sg"},
        {"text": "Millennia Institute (MI): 3-year A-level programme for Normal Academic students who perform well at O-levels. Alternative to 2-year JC. Offers same A-level subjects. Good option for students who need more preparation time.", "source": "MOE", "topic": "Millennia Institute", "url": "https://www.millenniainstitute.moe.edu.sg"},
    ]
    chunks.extend(static_chunks)

    if not chunks:
        return 0

    texts = [c["text"] for c in chunks]
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=25000)
    mat = vec.fit_transform(texts)

    with _lock:
        _vectorizer = vec
        _matrix = mat
        _docs = chunks

    _STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_STORE_PATH, "wb") as f:
        pickle.dump({"vectorizer": vec, "matrix": mat, "docs": chunks}, f)

    return len(chunks)


def _load_index() -> bool:
    global _vectorizer, _matrix, _docs
    if _vectorizer is not None:
        return True
    if not _STORE_PATH.exists():
        return False
    try:
        with open(_STORE_PATH, "rb") as f:
            store = pickle.load(f)
        with _lock:
            _vectorizer = store["vectorizer"]
            _matrix = store["matrix"]
            _docs = store["docs"]
        return True
    except Exception:
        return False


def retrieve_chunks(query: str, n_results: int = 4) -> list[dict]:
    from utils.config import USE_AI, OPENAI_API_KEY
    if USE_AI and OPENAI_API_KEY:
        result = _retrieve_openai(query, n_results)
        if result:
            return result
    return _retrieve_tfidf(query, n_results)


def _retrieve_tfidf(query: str, n_results: int) -> list[dict]:
    from sklearn.metrics.pairwise import cosine_similarity
    if not _load_index():
        count = build_index()
        if count == 0:
            return []
    try:
        q_vec = _vectorizer.transform([query])
        scores = cosine_similarity(q_vec, _matrix)[0]
        top_indices = np.argsort(scores)[::-1][:n_results]
        results = []
        for idx in top_indices:
            if scores[idx] > 0.01:
                doc = _docs[idx].copy()
                doc["score"] = round(float(scores[idx]), 3)
                results.append(doc)
        return results
    except Exception:
        return []


def _retrieve_openai(query: str, n_results: int) -> list[dict]:
    try:
        import chromadb
        from openai import OpenAI
        from utils.config import OPENAI_API_KEY
        db_path = str(Path(__file__).parent.parent / "storage" / "chroma_db")
        client = chromadb.PersistentClient(path=db_path)
        col = client.get_or_create_collection("edupathsg", metadata={"hnsw:space": "cosine"})
        if col.count() == 0:
            return []
        oai = OpenAI(api_key=OPENAI_API_KEY)
        emb = oai.embeddings.create(input=query, model="text-embedding-3-small").data[0].embedding
        res = col.query(query_embeddings=[emb], n_results=n_results)
        return [{"text": doc, **meta, "score": round(1 - dist, 3)}
                for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])]
    except Exception:
        return []


def index_status() -> dict:
    _load_index()
    return {"indexed": _vectorizer is not None, "num_chunks": len(_docs) if _docs else 0}

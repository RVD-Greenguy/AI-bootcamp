"""
Build TF-IDF RAG index from Singapore education data.
Run: python scripts/build_vector_index.py
No API key needed.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))


def main():
    print("Building EduPath SG RAG index...")
    from services.rag_service import build_index, retrieve_chunks, index_status

    count = build_index()
    print(f"Indexed {count} chunks → {BASE_DIR / 'storage' / 'tfidf_store.pkl'}")

    print("\n── Smoke tests ──────────────────────────────────────")
    tests = [
        "how does P1 registration work in Singapore",
        "what is PSLE AL scoring system",
        "IP school vs non-IP secondary school",
        "L1R5 calculation for JC admission",
        "failed English O levels what can I do",
        "polytechnic GPA for university DAE",
        "A-level rank points NUS medicine",
        "SkillsFuture Credit how to use",
        "where can students get counselling or mental health support",
        "PSC scholarship eligibility and bond",
        "ITE work study earn and learn programme",
        "career guidance ECG counsellor how to book",
        "MOE financial assistance scheme FAS bursary",
        "polytechnic open house dates",
    ]
    for q in tests:
        results = retrieve_chunks(q, n_results=2)
        print(f"\nQ: '{q}'")
        for r in results:
            print(f"  [{r['score']}] {r['topic']} — {r['source']}")

    print("\nDone.")


if __name__ == "__main__":
    main()

import re
from collections import Counter

STOPWORDS = {
    "and", "or", "the", "is", "are", "was", "were", "to", "of", "in", "for",
    "with", "on", "at", "by", "an", "a", "as", "from", "that", "this", "it",
    "be", "have", "has", "had", "will", "would", "can", "could", "should"
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return [w for w in text.split() if w not in STOPWORDS and len(w) > 2]


def ats_analysis(resume_text: str, role: str):
    if not resume_text or not resume_text.strip():
        return {"score": 0, "matched": [], "missing": []}

    resume_words = Counter(clean_text(resume_text))
    role_words = clean_text(role)

    # -------- CASE 1: Role is empty or too vague --------
    if len(role_words) < 2:
        # Treat most frequent resume terms as ATS signals
        keywords = [w for w, _ in resume_words.most_common(10)]
        score = min(len(keywords) * 10, 100)

        return {
            "score": score,
            "matched": keywords,
            "missing": []
        }

    # -------- CASE 2: Normal role-based ATS --------
    matched = set(role_words) & set(resume_words.keys())
    missing = set(role_words) - matched

    score = int((len(matched) / len(set(role_words))) * 100)

    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing)
    }

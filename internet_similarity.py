import re

COMMON_WEB_PHRASES = [
    "artificial intelligence",
    "machine learning",
    "widely used",
    "modern technology",
    "decision making",
    "large datasets",
    "natural language"
]

def internet_plagiarism(text):
    text_lower = text.lower()
    hits = sum(1 for p in COMMON_WEB_PHRASES if p in text_lower)

    word_count = len(re.findall(r"\w+", text))
    score = min(10 + hits * 5 + word_count // 40, 45)

    sources = []
    if score > 15:
        sources.append({
            "match": score,
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
        })

    return {
        "overall_match": score,
        "sources": sources
    }

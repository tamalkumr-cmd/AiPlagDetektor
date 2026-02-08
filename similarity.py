import ast
import tokenize
import io
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- TEXT SIMILARITY ----------------

def cosine_text_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def ngram_similarity(text1, text2, n=3):
    def ngrams(text):
        words = text.split()
        return set(zip(*[words[i:] for i in range(n)]))

    n1 = ngrams(text1)
    n2 = ngrams(text2)

    if not n1 or not n2:
        return 0.0

    return round((len(n1 & n2) / len(n1 | n2)) * 100, 2)

def text_similarity_engine(text1, text2):
    cosine_score = cosine_text_similarity(text1, text2)
    ngram_score = ngram_similarity(text1, text2)

    overall = 0.7 * cosine_score + 0.3 * ngram_score

    return {
        "cosine_similarity": cosine_score,
        "ngram_similarity": ngram_score,
        "overall_similarity": round(overall, 2)
    }

# ---------------- FLASK ADAPTER ----------------

def compute_similarity(text1, text2):
    scores = text_similarity_engine(text1, text2)

    label = (
        "High Plagiarism" if scores["overall_similarity"] > 70
        else "Medium Plagiarism" if scores["overall_similarity"] > 40
        else "Low Plagiarism"
    )

    return {
        "similarity_percent": scores["overall_similarity"],
        "label": label,
        "details": scores
    }

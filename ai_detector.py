from collections import Counter
import math
import re

def tokenize(text):
    return re.findall(r"\w+", text.lower())

def perplexity(text):
    words = tokenize(text)
    total = len(words)
    if total < 50:
        return 100.0

    freq = Counter(words)
    entropy = -sum((c / total) * math.log2(c / total) for c in freq.values())
    return round(2 ** entropy, 2)

def repetition_score(text):
    words = tokenize(text)
    if len(words) < 50:
        return 0.1

    bigrams = list(zip(words, words[1:]))
    freq = Counter(bigrams)
    repeated = sum(1 for c in freq.values() if c > 2)
    return round(min(repeated / max(len(bigrams), 1), 1.0), 2)

def sentence_variance(text):
    sentences = [s for s in re.split(r"[.!?]", text) if len(s.split()) > 4]
    if len(sentences) < 3:
        return 20.0

    lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    return round(variance, 2)

def ai_likelihood(text):
    words = tokenize(text)
    length = len(words)

    if length < 50:
        return {
            "ai_probability": "Insufficient Text",
            "perplexity": 100.0,
            "repetition_score": 0.0,
            "sentence_variance": 0.0,
            "word_count": length,
            "heuristic_score": 0
        }

    perp = perplexity(text)
    rep = repetition_score(text)
    var = sentence_variance(text)

    score = 0
    if perp < 55: score += 30
    if rep > 0.15: score += 25
    if var < 10: score += 20
    if length > 100: score += 15

    label = "Low AI Probability"
    if score >= 60:
        label = "High AI Probability"
    elif score >= 40:
        label = "Medium AI Probability"

    return {
        "ai_probability": label,
        "perplexity": perp,
        "repetition_score": rep,
        "sentence_variance": var,
        "word_count": length,
        "heuristic_score": score
    }

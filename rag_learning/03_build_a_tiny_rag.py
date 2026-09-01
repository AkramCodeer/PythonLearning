"""A minimal, dependency-free RAG retrieval demonstration.

It uses keyword scoring rather than embeddings so you can see the mechanism.
Replace `keyword_score` with embedding/vector search in a real system.
"""

import re
from collections import Counter

DOCUMENTS = [
    ("refund-policy", "Refunds are available within 30 days of purchase when an order has not been used."),
    ("shipping", "Standard shipping takes three to five business days. Express shipping takes one to two days."),
    ("support", "Support is available Monday to Friday, 9:00 to 17:00 India time."),
]


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def keyword_score(question: str, passage: str) -> int:
    """Simple overlap score: useful for learning, not production semantic search."""
    query_terms = Counter(tokens(question))
    passage_terms = Counter(tokens(passage))
    return sum(min(count, passage_terms[word]) for word, count in query_terms.items())


def retrieve(question: str, top_k: int = 2):
    ranked = sorted(
        ((keyword_score(question, text), source, text) for source, text in DOCUMENTS),
        reverse=True,
    )
    return [(source, text) for score, source, text in ranked[:top_k] if score > 0]


def make_prompt(question: str, contexts: list[tuple[str, str]]) -> str:
    evidence = "\n".join(f"[{source}] {text}" for source, text in contexts)
    return (
        "Answer only from the context below. If it does not contain the answer, say so.\n\n"
        f"Context:\n{evidence}\n\nQuestion: {question}"
    )


if __name__ == "__main__":
    question = "How long does standard shipping take?"
    contexts = retrieve(question)
    print("Retrieved context:")
    for source, text in contexts:
        print(f"- [{source}] {text}")
    print("\nPrompt to send to an LLM:\n")
    print(make_prompt(question, contexts))

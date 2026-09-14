import re
from database import get_documents

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "can",
    "do",
    "from",
    "how",
    "i",
    "is",
    "my",
    "of",
    "the",
    "to",
    "what",
    "when",
    "where",
}


def extract_words(text: str) -> set[str]:
    words = set(re.findall(r"\w+", text.lower()))
    return words - STOP_WORDS

def retrieve_document(question: str):
    question_words = extract_words(question)
    best_document = None
    best_score = 0

    for document in get_documents():
        searchable_text = document['title'] + ' ' + document['content']
        document_words = extract_words(searchable_text)
        score = len(question_words.intersection(document_words))
        if score > best_score:
            best_score = score
            best_document = document

    return best_document
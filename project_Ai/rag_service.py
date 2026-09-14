from local_llm import generate_answer
from prompt_builder import build_prompt
from vector_search import search_similar_document
import logging

import httpx
import psycopg

logger = logging.getLogger(__name__)


class RAGServiceUnavailableError(RuntimeError):
    pass

FALLBACK_ANSWER = (
    "I could not find enough information to answer your question. " 
    "Please contact support for further assistance."
)
def answer_question(question: str) -> dict:
    try:
        document = search_similar_document(question)

        if document is None:
            return {
                "question": question,
                "answer": FALLBACK_ANSWER,
                "source": None,
                "similarity": None,
            }

        prompt = build_prompt(question, document)
        generated_answer = generate_answer(prompt)

        return {
            "question": question,
            "answer": generated_answer,
            "source": {
                "id": document["id"],
                "title": document["title"],
            },
            "similarity": round(
                float(document["similarity"]),
                3,
            ),
        }

    except (psycopg.Error, httpx.HTTPError, KeyError) as error:
        logger.exception("RAG pipeline dependency failed")

        raise RAGServiceUnavailableError(
            "The AI service is temporarily unavailable."
        ) from error
import psycopg

from pgvector import Vector
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row

from database import DATABASE_URL
from embeddings import create_embedding

MIN_SIMILARITY = 0.30


def find_best_document(question: str):
    question_embedding = Vector(create_embedding(question))

    with psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
    ) as connection:
        register_vector(connection)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    content,
                    1 - (embedding <=> %s) AS similarity
                FROM documents
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s
                LIMIT 1
                """,
                (question_embedding, question_embedding),
            )

            return cursor.fetchone()


def search_similar_document(question: str):
    document = find_best_document(question)

    if document is None:
        return None

    if document["similarity"] < MIN_SIMILARITY:
        return None

    return document

if __name__ == "__main__":
    questions = [
        "I forgot my login credentials.",
        "What is the weather today?",
    ]
    for question in questions:
        result = search_similar_document(question)

        print("\nQuestion:", question)

        if result is None:
            print("No relevant document found.")
        else:
            print("Title:", result["title"])
            print("Similarity:", round(result["similarity"], 3))

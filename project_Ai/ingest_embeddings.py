import psycopg

from pgvector import Vector
from pgvector.psycopg import register_vector

from database import DATABASE_URL
from embeddings import create_embedding


def ingest_embeddings():
    with psycopg.connect(DATABASE_URL) as connection:
        register_vector(connection)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, content
                FROM documents
                WHERE embedding IS NULL
                ORDER BY id
                """
            )

            documents = cursor.fetchall()

            for document_id, title, content in documents:
                text_to_embed = f"{title}. {content}"
                embedding = create_embedding(text_to_embed)

                cursor.execute(
                    """
                    UPDATE documents
                    SET embedding = %s
                    WHERE id = %s
                    """,
                    (Vector(embedding), document_id),
                )

                print(f"Created embedding for: {title}")


if __name__ == "__main__":
    ingest_embeddings()

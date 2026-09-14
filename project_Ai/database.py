import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")


def get_documents():
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, content FROM documents ORDER BY id"
            )
            return cursor.fetchall()


if __name__ == "__main__":
    documents = get_documents()

    for document in documents:
        print(document)

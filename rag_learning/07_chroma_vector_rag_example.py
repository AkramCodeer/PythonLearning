"""A minimal RAG retriever using Chroma and Sentence Transformers.

Install once:
    python -m pip install chromadb sentence-transformers

Run:
    python .\\07_chroma_vector_rag_example.py
"""

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


DOCUMENT = """
Refund policy: Customers may request a refund within 30 days of purchase.
The item must be unused and include the original order ID. Processing normally
takes five business days after the returned item is received. Standard shipping
takes three to five business days. Express shipping takes one to two days.
""".strip()


def chunk_words(text: str, size: int = 40, overlap: int = 10) -> list[str]:
    """Learning-only word chunker; use structure-aware chunking for real documents."""
    words = text.split()
    step = size - overlap
    return [" ".join(words[start : start + size]) for start in range(0, len(words), step)]


def main() -> None:
    chunks = chunk_words(DOCUMENT)
    metadata = [{"source": "refund_policy.txt", "chunk": index} for index in range(len(chunks))]

    # The same model embeds chunks during indexing and the question during retrieval.
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    document_vectors = model.encode(chunks, normalize_embeddings=True).tolist()

    data_path = Path(__file__).parent / "chroma_data"
    client = chromadb.PersistentClient(path=str(data_path))
    collection = client.get_or_create_collection(name="learning_rag")

    # upsert makes the script safe to run repeatedly with the same chunk IDs.
    collection.upsert(
        ids=[f"refund-{index}" for index in range(len(chunks))],
        documents=chunks,
        embeddings=document_vectors,
        metadatas=metadata,
    )

    question = "How long do I have to ask for a refund?"
    question_vector = model.encode([question], normalize_embeddings=True).tolist()
    results = collection.query(
        query_embeddings=question_vector,
        n_results=2,
        include=["documents", "metadatas", "distances"],
    )

    print(f"Question: {question}\n")
    print("Retrieved evidence:")
    for text, meta, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        print(f"- [{meta['source']} chunk {meta['chunk']}; distance={distance:.4f}]")
        print(f"  {text}\n")

    print("Next RAG step: send the question and these evidence chunks to an LLM prompt.")


if __name__ == "__main__":
    main()

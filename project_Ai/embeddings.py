from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embedding(text: str) -> list[float]:
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


if __name__ == "__main__":
    result = create_embedding("How can I change my login credentials?")

    print("Number of dimensions:", len(result))
    print("First five values:", result[:5])

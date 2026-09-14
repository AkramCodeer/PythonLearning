from pathlib import Path


def load_text_file(file_path: Path) -> str :
    return file_path.read_text(encoding="utf-8")


def chunk_text(
    text: str,
    chunk_size: int = 80,
    overlap: int = 15,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    words = text.split()
    chunks = []
    step_size = chunk_size - overlap

    for start_index in range(0, len(words), step_size):
        end_index = start_index + chunk_size
        chunk_words = words[start_index:end_index]

        if not chunk_words:
            break

        chunks.append(" ".join(chunk_words))

        if end_index >= len(words):
            break

    return chunks


if __name__ == "__main__":
    source_path = Path("data/support_guide.txt")
    source_text = load_text_file(source_path)
    chunks = chunk_text(source_text)

    print("Number of chunks:", len(chunks))

    for index, chunk in enumerate(chunks):
        print(f"\n--- Chunk {index} ---")
        print(chunk)
        print("Word count:", len(chunk.split()))
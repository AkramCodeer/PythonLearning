# 5. RAG project roadmap

## Beginner: FAQ assistant

Use 10–30 text files. Split by paragraph, retrieve with the demo approach, and print the prompt. Goal: understand the data flow.

## Intermediate: semantic document chat

Add an embedding model, a vector database (for example FAISS or Chroma), document metadata, and LLM-generated answers with citations. Evaluate against 20 real questions.

## Advanced: trustworthy knowledge assistant

Add document ingestion for PDF/HTML, hybrid retrieval, reranking, access control, answer abstention, feedback collection, tracing, and automated evaluation. Optimize quality before scaling the index.

## Practical build checklist

- Define one user group and one document collection.
- Write 20 representative questions before implementation.
- Choose chunk boundaries that preserve headings and meaning.
- Attach metadata to every chunk.
- Require citations in the answer format.
- Test failure cases: missing answer, conflicting sources, stale documents, and restricted documents.
- Measure retrieval and answer quality independently.

## Next step

When you are ready to connect this to an LLM, keep the `retrieve()` and `make_prompt()` separation from the demo. Swap in embeddings/vector search for `retrieve()`, then send the generated prompt to your chosen LLM provider.

# 1. RAG fundamentals

## What problem does RAG solve?

LLMs can write fluent answers, but they may not know your private files, recent updates, or the source behind a statement. RAG supplies selected source passages at question time. The model then answers from that supplied context.

## The two phases

### A. Indexing (done when documents change)

1. Collect documents: PDFs, web pages, manuals, databases, notes.
2. Clean and normalize text.
3. Split it into small, meaningful **chunks** (often 300–800 tokens, with overlap).
4. Turn chunks into embeddings: numerical vectors representing meaning.
5. Store vectors plus metadata (title, URL, page, access permissions) in a vector database.

### B. Querying (done for every question)

1. Receive a user question.
2. Turn it into an embedding.
3. Retrieve the most relevant chunks.
4. Optionally rerank/filter them.
5. Place them and the question in the LLM prompt.
6. Return an answer with citations.

## Vocabulary

| Term | Meaning |
| --- | --- |
| Chunk | A small piece of a document that can be retrieved. |
| Embedding | A vector whose position captures semantic similarity. |
| Vector store | Database optimized for nearest-neighbor vector search. |
| Retriever | Component that returns passages for a query. |
| Top-k | Number of initial results returned (for example, 5). |
| Reranker | Stronger model that reorders candidate results by relevance. |
| Grounding | Tying the answer to retrieved evidence. |

## A good answer prompt

```text
Answer only from the supplied context. If the answer is absent, say you do not know.
For every factual claim, cite the source label in square brackets.

Context:
{retrieved_chunks}

Question: {question}
```

This reduces unsupported answers, but retrieval quality still determines the ceiling of the system.

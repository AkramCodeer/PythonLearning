# RAG Vector Databases, Retrieval, Chunking, and Embeddings

This guide explains where a vector database is used in RAG, how retrieval works, how chunks are created, and how to implement a small RAG retriever in Python.

> New to RAG? Read [08_rag_vector_db_for_beginners.md](08_rag_vector_db_for_beginners.md) first. It explains the same flow without technical detail.

![RAG indexing and retrieval flow](rag_vector_db_retrieval_flow.png)

## The short answer

A vector database is used in two different phases:

| RAG phase | When it runs | What the vector database does |
| --- | --- | --- |
| **Indexing** | When a source document is added, changed, or deleted | Stores each chunk’s embedding, text (or pointer), and metadata in a searchable index. |
| **Querying / retrieval** | Every time a user asks a question | Finds the stored chunk vectors most similar to the question vector, then returns their text and metadata. |

The vector database does **not** generate the final answer. It supplies relevant evidence to the LLM.

```text
Documents → chunks → embeddings → vector DB
Question → query embedding → vector DB search → evidence → LLM → answer
```

## 1. What is stored in a vector database?

Each indexed chunk is a record such as:

```python
{
    "id": "handbook-p12-c03",
    "document": "Employees can claim travel expenses within 30 days...",
    "embedding": [0.012, -0.318, 0.771, ...],
    "metadata": {
        "source": "employee_handbook.pdf",
        "page": 12,
        "section": "Travel expenses",
        "updated_at": "2026-09-01",
        "department": "finance",
        "allowed_roles": ["employee", "finance"]
    }
}
```

The embedding is a long list of numbers. Similar meanings are placed near each other in vector space. Therefore, a question such as “When can I submit a travel claim?” can retrieve a passage that says “claim travel expenses within 30 days,” even when the words do not exactly match.

## 2. Common vector database choices

| Choice | Best starting use | Notes |
| --- | --- | --- |
| **Chroma** | Learning, prototypes, local RAG | Simple Python API; can persist data locally. |
| **FAISS** | Local, high-speed similarity index | Library, not a full database; you manage metadata/persistence. |
| **Qdrant** | Production self-hosted or managed RAG | Strong filtering and production features. |
| **Pinecone** | Managed production service | Fully managed; minimal infrastructure work. |
| **Weaviate** | Production systems with rich search | Supports vector and hybrid-search patterns. |
| **pgvector** | Data already lives in PostgreSQL | Adds vector search to your existing database. |
| **Elasticsearch / OpenSearch** | Keyword search already exists | Useful for hybrid keyword + vector retrieval. |

For this folder, use **Chroma** first. Later, the same RAG steps transfer to Qdrant, Pinecone, Weaviate, pgvector, or a managed cloud service.

## 3. Indexing time: how chunks are created

Do not create one vector for an entire 100-page PDF. A whole document is too broad to retrieve precisely and may exceed the LLM context window. Split it into chunks that each represent one focused idea.

### Simple chunking strategy

1. Extract text from a source file.
2. Preserve useful structure: title, heading, page number, source URL, permissions.
3. Split near natural boundaries—headings, paragraphs, sentences, or code blocks.
4. Target roughly **300–800 tokens** per chunk as a starting point.
5. Keep a small overlap, commonly **50–150 tokens**, so a sentence split across two chunks retains context.
6. Store the chunk text and its metadata together.

### Why overlap exists

```text
Chunk 1: ...refund requests must be submitted within 30 days of purchase.
Chunk 2: Within 30 days of purchase, include the order ID and reason for return...
```

The repeated boundary makes either chunk usable for questions about the deadline or the required return details.

### Chunking choices by content type

| Content | Recommended boundary |
| --- | --- |
| Policies / manuals | Heading → paragraph → sentence |
| PDFs | Page and heading, while retaining page metadata |
| Source code | Function, class, module, or AST-aware chunks |
| Tables | Keep a complete row group with its column headings |
| Conversations | Message turns, keeping speaker and timestamp metadata |

Bad chunking is one of the biggest reasons for poor RAG answers. A perfect model cannot retrieve an answer that was split incorrectly or indexed without its source context.

## 4. Embeddings: what happens?

An embedding model accepts text and outputs a fixed-length numeric vector.

```text
"Standard delivery takes three to five business days"
                    ↓ embedding model
[0.12, -0.31, 0.67, 0.04, ...]
```

At indexing time, embed every document chunk. At query time, embed the user’s question with the **same embedding model**. The vector database compares the query vector with stored vectors using a distance/similarity metric such as cosine similarity.

Important rules:

- Use the same model and vector dimension for indexed chunks and query embeddings.
- Reindex a collection if you change embedding models.
- Normalize vectors if your chosen similarity strategy/model expects it.
- Keep the original text; vectors alone are not readable evidence for an LLM.

## 5. How retrieval works, step by step

For the question “What is the refund deadline?” the pipeline is:

1. Convert the question to an embedding vector.
2. Search the vector index for nearest chunk vectors.
3. Retrieve more candidates than you plan to show the LLM (for example, top 20).
4. Apply metadata/permission filters, such as `department = finance` or a user access rule.
5. Optionally run a reranker to order the remaining candidates more accurately.
6. Select a small evidence set (for example, the best 3–5 chunks).
7. Put those chunks, their source labels, and the question into the LLM prompt.
8. Require citations and allow “I don’t know” when evidence is weak.

### Vector-only versus hybrid retrieval

- **Vector search** finds conceptual meaning: “cancel my purchase” can find “refund policy.”
- **Keyword/BM25 search** finds exact terms: SKU IDs, product codes, names, and error messages.
- **Hybrid retrieval** combines both result sets; this is usually stronger in production.

## 6. Python implementation with Chroma + Sentence Transformers

This companion script uses explicit embeddings so the important steps are visible:

```powershell
python -m pip install chromadb sentence-transformers
python .\07_chroma_vector_rag_example.py
```

The first run downloads the small local embedding model. The script creates a local `chroma_data/` index folder; it is intentionally ignored by Git.

### What the code does

1. Splits a sample document into overlapping word chunks.
2. Uses `sentence-transformers/all-MiniLM-L6-v2` to embed the chunks.
3. Saves vectors, chunk text, and metadata to a persistent Chroma collection.
4. Embeds a question with the same model.
5. Queries Chroma for the nearest chunks and prints the evidence.

Chroma can also create embeddings internally when you attach an embedding function, but explicit embeddings are better for learning and make it obvious that document and query vectors must use the same model.

## 7. Retrieval quality checklist

- Is the correct answer’s chunk present in the top-k results? Measure retrieval recall.
- Are the returned chunks mostly useful? Measure context precision.
- Is every answer claim supported by retrieved context? Measure faithfulness.
- Are source URL/page/section and permissions preserved in metadata?
- Are you filtering inaccessible content **before** it reaches the LLM?
- Does the system abstain if the best results are weak or unrelated?

## Official references

- [Chroma Python collection add/query reference](https://docs.trychroma.com/reference/python/collection)
- [Chroma query guide](https://docs.trychroma.com/docs/querying-collections/query-and-get)
- [Sentence Transformers usage guide](https://sbert.net/docs/sentence_transformer/usage/usage.html)

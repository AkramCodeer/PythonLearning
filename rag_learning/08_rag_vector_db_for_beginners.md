# RAG and Vector DB: A Very Simple Explanation

Start here. Do not worry about Python or big technical words yet.

## Imagine a library

You have 1,000 company documents. A user asks:

> “What is the refund deadline?”

The AI cannot read all 1,000 documents every time. That would be slow and expensive.

So we create a smart library search system. This is RAG.

```text
User asks a question
        ↓
Smart search finds the best document paragraphs
        ↓
AI reads only those paragraphs
        ↓
AI gives an answer
```

**RAG means:** first **Retrieve** useful information, then let the AI **Generate** an answer.

## What is a vector database?

A vector database is the smart search shelf in that library.

It stores small pieces of your documents and helps find pieces with a similar meaning to the user’s question.

For example, these two sentences mean almost the same thing:

```text
Question: “When can I get my money back?”
Document: “Customers may request a refund within 30 days.”
```

The exact words are different, but the meanings are similar. A vector database helps find that document sentence.

## Three important words

| Word | Simple meaning |
| --- | --- |
| **Chunk** | A small piece of a large document, like one paragraph. |
| **Embedding** | A list of numbers that represents the meaning of text. |
| **Vector DB** | A database that searches those number lists to find similar meanings. |

## Step 1: Prepare your documents (one-time work)

Suppose this is your document:

```text
Refund policy
Customers may request a refund within 30 days of purchase.
The product must be unused.
Standard delivery takes three to five days.
```

We split it into chunks:

```text
Chunk 1: Customers may request a refund within 30 days of purchase.
Chunk 2: The product must be unused.
Chunk 3: Standard delivery takes three to five days.
```

Then an embedding model changes each chunk into numbers:

```text
Chunk 1 → [0.12, -0.31, 0.67, ...]
Chunk 2 → [0.44,  0.18, -0.22, ...]
Chunk 3 → [-0.05, 0.91, 0.10, ...]
```

Finally, we save all chunks, numbers, and source details in the vector database.

```text
Document → split into chunks → make embeddings → save in vector DB
```

This work happens when documents are added or changed. It does **not** happen for every user question.

## Step 2: Answer a user question (happens every time)

The user asks:

> “What is the refund deadline?”

The same embedding model changes the question into numbers:

```text
Question → [0.10, -0.29, 0.70, ...]
```

The vector DB compares that question vector with all stored chunk vectors. It sees that the question is closest to Chunk 1.

```text
Question
   ↓
Vector DB finds Chunk 1
   ↓
"Customers may request a refund within 30 days..."
   ↓
AI receives the question + Chunk 1
   ↓
Answer: "You can request a refund within 30 days of purchase."
```

## Where does the LLM fit?

The vector DB **finds information**. The LLM **writes the answer**.

```text
Vector DB: “Here is the relevant paragraph.”
LLM: “I will explain that paragraph in a helpful answer.”
```

The LLM does not need to search your entire company database itself.

## What should you learn first?

Learn in this order:

1. Understand the flow in this file.
2. Read [03_build_a_tiny_rag.py](03_build_a_tiny_rag.py). It shows search without any external library.
3. Read the PNG: [rag_vector_db_retrieval_flow.png](rag_vector_db_retrieval_flow.png).
4. Then open [07_vector_databases_retrieval_and_embeddings.md](07_vector_databases_retrieval_and_embeddings.md) for the detailed explanation.
5. Run `07_chroma_vector_rag_example.py` only after you understand chunks and embeddings.

## One interview answer

> In RAG, we split company documents into small chunks. We convert every chunk into an embedding and save it in a vector database. When a user asks a question, we convert the question into an embedding and search for the most similar chunks. We give only those chunks to the LLM, so it can answer using relevant company information.

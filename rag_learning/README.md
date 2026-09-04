# RAG: Basics to Advanced

This folder is a practical path for learning **Retrieval-Augmented Generation (RAG)**: a system that finds relevant information first, then gives that information to an LLM so its answer is grounded in your data.

## Learning path

1. [01_rag_fundamentals.md](01_rag_fundamentals.md) — concepts and the end-to-end flow.
2. [02_visual_architecture.md](02_visual_architecture.md) — diagrams for basic and production RAG.
3. [03_build_a_tiny_rag.py](03_build_a_tiny_rag.py) — dependency-free lexical retrieval.
4. [04_advanced_rag.md](04_advanced_rag.md) — embeddings, hybrid search, reranking, evaluation, and safety.
5. [05_rag_project_roadmap.md](05_rag_project_roadmap.md) — how to turn the concepts into a project.
6. [06_generative_vs_agentic_ai_interview_guide.md](06_generative_vs_agentic_ai_interview_guide.md) — interview-ready explanations and examples from current-company work.
7. [07_vector_databases_retrieval_and_embeddings.md](07_vector_databases_retrieval_and_embeddings.md) — vector DB choices, chunking, embeddings, retrieval, and a Chroma Python example.
8. [08_rag_vector_db_for_beginners.md](08_rag_vector_db_for_beginners.md) — plain-English RAG and vector database explanation; start here before the detailed guide.

## Suggested order

Read files 1 and 2, run file 3, then use files 4 and 5 to choose an advanced project. The Python demo runs with any recent Python 3 installation:

```powershell
python .\03_build_a_tiny_rag.py
```

## Core idea

```text
Your documents -> split + index -> retrieve relevant passages -> LLM -> grounded answer
```

RAG is usually a better fit than fine-tuning when knowledge changes frequently, must be traceable to sources, or is private to a team.

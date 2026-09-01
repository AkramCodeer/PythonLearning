# 4. Advanced RAG

## Improve retrieval before changing the model

| Technique | When it helps | Trade-off |
| --- | --- | --- |
| Better chunking | Documents have sections, tables, or code | Requires format-aware parsing |
| Metadata filters | Users need only authorized/current content | Metadata must be accurate |
| Hybrid search | Exact terms and concepts both matter | More components to tune |
| Reranking | Top-k contains near misses | Added latency/cost |
| Query rewriting | Questions are vague or conversational | Can alter user intent |
| Parent-document retrieval | Small chunks lose surrounding meaning | More context tokens |

## Hybrid retrieval

Vector search recognizes meaning: “cancel my purchase” can find “refund policy.” Keyword/BM25 search recognizes exact words: product IDs, error codes, names. Hybrid search combines both result sets, then a reranker selects the best evidence.

## Evaluation loop

Measure these separately:

1. **Retrieval recall** — did the correct source appear in top-k?
2. **Context precision** — how much retrieved material was actually useful?
3. **Answer faithfulness** — are claims supported by the context?
4. **Answer relevance** — did the answer address the question?
5. **Latency and cost** — can the system meet its operating target?

Create a small “golden” set of real questions with expected source passages. Run it after each retrieval, chunking, or prompt change.

## Security and reliability

- Enforce document permissions during retrieval, not only in the prompt.
- Treat retrieved text as untrusted input: it may contain prompt-injection instructions.
- Preserve source, page/section, date, and document version in metadata.
- Cite displayed evidence and abstain when evidence is weak.
- Log retrieval IDs and scores; avoid logging sensitive full content unnecessarily.

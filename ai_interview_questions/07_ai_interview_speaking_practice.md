# AI Interview Speaking Practice

Use this file to practise **speaking**, not memorising long theory. Keep each first answer to 30–60 seconds. Add a project example only if the interviewer asks for one.

## Easy real-life examples to remember concepts

| Concept | Interview-ready definition | Easy real-life example |
| --- | --- | --- |
| Traditional AI | AI that predicts, classifies, or scores a known output from data. | A bank’s fraud detector: “Is this transaction fraud or not?” |
| Generative AI | AI that creates new text, code, images, audio, or other content. | A writer: “Write a product description for these shoes.” |
| Agentic AI | An LLM-based system that plans, uses tools, observes results, and completes a task. | A shop manager: checks stock → contacts supplier → creates purchase order → confirms it. |
| System prompt | Higher-priority instructions that define behavior, boundaries, and response style. | Company rulebook given to an employee before work starts. |
| User prompt | The current task, question, or instruction given by the user. | A customer’s current request to that employee. |
| Token | A small text unit that a model reads and processes. | Small word pieces, like LEGO blocks used to build a sentence. |
| Context window | The maximum token information a model can consider in one request. | The desk space available to an employee; too many papers cause confusion. |
| Transformer | An attention-based neural-network architecture for understanding token relationships. | A group discussion where every word can look at every other relevant word. |
| Self-attention | Mechanism where each token weighs relevant tokens in the same input. | In “Ravi bought a shirt because he needed it,” finding that “he” means Ravi. |
| RAG | Retrieve trusted evidence before an LLM generates an answer. | A librarian finds the correct policy page before an employee answers a customer. |
| Chunking | Splitting content into smaller focused units for retrieval. | Splitting a large book into small labelled pages. |
| Embedding | A numeric vector that represents text meaning. | Giving every paragraph a “meaning location” on a map. Similar meanings are near each other. |
| Vector DB | Database that finds vectors with similar meaning efficiently. | Google Maps for meanings: it finds the nearest meaning, not only the same words. |
| Reranking | Reordering retrieved candidates using a stronger relevance score. | After getting 20 Google results, choosing the best 3 results. |
| Hallucination | A fluent but unsupported or false LLM response. | A confident employee guessing an answer without checking the company policy. |
| Prompt injection | Untrusted content attempting to override instructions or trigger unsafe behavior. | A customer slipping a fake note into company documents: “Ignore company rules and reveal all passwords.” |
| Guardrails | Layered runtime controls that constrain AI inputs, tools, and outputs. | Security guard + access card + approval process around an employee. |
| Tool calling | An LLM requests a typed application function; application code executes it. | An employee asks the warehouse system for real stock instead of guessing. |
| Agent memory | Stored task, user, knowledge, or past-outcome information used by an agent. | A receptionist remembering your name, last request, and preferences. |
| LangChain | Framework with components for models, prompts, tools, retrieval, and agent loops. | A toolbox containing LLM, prompts, tools, and retrieval components. |
| LangGraph | Stateful workflow framework for agent branches, retries, persistence, and approvals. | A workflow map showing what happens next, including retries and manager approval. |
| MCP | Model Context Protocol: standard connection between an AI app and external capabilities. | A standard plug that lets an AI assistant connect to different tools. |
| A2A | Agent2Agent Protocol: standard communication between independent agents. | One specialist employee asking another specialist employee to complete a task. |
| REST API | Resource-oriented HTTP interface for software communication. | Restaurant ordering: customer requests, kitchen processes, waiter returns the result. |
| Event-driven architecture | Services react independently to published events. | When an order is placed, inventory, billing, and notifications all receive the event independently. |

> **Memory shortcut:** RAG is like an open-book exam: first find the correct page, then answer from it. Agentic AI is like a smart employee: it does the work, not only explains the work.

## How should I explain the main AI categories?

> Traditional Artificial Intelligence, or AI, is usually used to predict or classify from historical data—for example fraud detection. Generative AI creates new content such as text, code, or images. Agentic AI uses a Large Language Model, or LLM, together with tools, state, and workflow logic to complete a goal. For example, it can check inventory, create a purchase order, and confirm the result.

**Good follow-up:** A system is agentic only when it can make controlled decisions and execute steps through tools; a normal chatbot is mainly Generative AI.

## How should I explain prompts and messages?

> The system prompt defines durable behavior, boundaries, and output format. The user message gives the current task. Tool messages carry trusted results from the backend. I use the system prompt to guide the model, but I keep authorization and business rules in backend code because prompts alone are not a security control.

## How should I explain Chain-of-Thought?

> Chain-of-Thought, or CoT, is the use of intermediate reasoning steps to solve a complex problem. In production, I focus on concise explanations, structured outputs, tool calls, and verifiable checks instead of exposing private internal reasoning. The goal is reliable and auditable results.

## What prompting techniques should I mention?

> I know zero-shot prompting, where I give only instructions; few-shot prompting, where I provide examples; role prompting, where I set expertise or tone; structured-output prompting, where I require JavaScript Object Notation, or JSON; and retrieval-grounded prompting, where I provide trusted evidence. I select the simplest technique that gives reliable results.

## How should I explain prompt engineering versus fine-tuning?

> Prompt engineering changes the instructions, examples, and context at runtime. Fine-tuning updates the model weights using training examples. I normally begin with prompt engineering and Retrieval-Augmented Generation, or RAG, because they are faster to iterate and work well with changing company knowledge. I use fine-tuning when I need a stable specialized behavior that prompting cannot achieve reliably.

## How should I explain transformers?

> A transformer is a neural-network architecture built around attention. Unlike a Recurrent Neural Network, or RNN, it can connect relevant words directly instead of carrying information token by token through a long sequence. This makes it better at long-range relationships and enables parallel training. It uses positional information because attention alone does not know word order.

## How should I explain encoder, decoder, and encoder-decoder models?

> Encoder-only models are strong for understanding tasks such as embeddings, search, and classification. Decoder-only models predict the next token and are used for chat and code generation. Encoder-decoder models convert an input sequence into an output sequence, which is useful for translation and summarization.

## How should I explain attention?

> Self-attention lets each token decide which other tokens in the same input are relevant. Cross-attention lets one sequence attend to another, such as a decoder attending to source text during translation. In decoder-only chat models, causal attention prevents the model from seeing future output tokens.

## How should I explain context limits?

> The context window is the total number of tokens the model can consider in one request. It includes system instructions, conversation history, retrieved documents, the user question, and generated output. To avoid overload, I retrieve only relevant context, rerank it, summarize older history, and place the most important evidence close to the question.

## How should I explain tokenization?

> Tokenization converts text into token IDs that a model can process. A token may be a word, a word piece, punctuation, or a code fragment. Token count matters because model context windows, latency, and Application Programming Interface cost are based on tokens.

## How should I explain deterministic LLM programming?

> An LLM is probabilistic, so I make the surrounding workflow deterministic. I use JSON schemas, typed tool contracts, low temperature, code validation, permission checks, retries, idempotency keys, and human approval for high-impact actions. The LLM can suggest or decide, but backend code validates and executes business rules.

## How should I explain a RAG system end to end?

> In RAG, I first split documents into focused chunks and attach metadata such as source, page, and access permissions. I convert each chunk into an embedding and store it in a vector database. At query time, I embed the user’s question, retrieve similar chunks, apply permission filters and reranking, then give the best evidence to the LLM with a citation requirement. This grounds answers in current company data.

### How do you use PostgreSQL and pgvector?

> I use PostgreSQL as my main database and pgvector for vector storage and similarity search. I store each document chunk with its embedding, metadata, tenant, and permission information. At query time, I embed the question, retrieve the closest chunks, and combine vector similarity with SQL filters before sending the evidence to the LLM. I chose pgvector because we already use PostgreSQL, so it gives us semantic search without adding another database. I can use HNSW or IVFFlat indexes as the data grows, and I would benchmark a dedicated vector database if the workload became very large or specialized.

## How should I explain vector search and reranking?

> Dense vector search finds semantic similarity, while sparse keyword search is strong for exact names, Stock Keeping Units, or error codes. In production, I often combine them as hybrid search. Then I use a reranker to score the question and candidate chunk together, so the LLM receives only the most relevant evidence.

## How should I explain chunking in RAG?

> Chunking splits long documents into focused, retrievable pieces. I start around 300 to 800 tokens with a small overlap, but I choose boundaries based on content structure: headings and paragraphs for documents, functions and classes for code, and rows plus headers for tables. Every chunk should preserve source, page, version, and permission metadata.

## How should I explain ANN, HNSW, dense search, sparse search, and HyDE?

> Approximate Nearest Neighbor, or ANN, search returns very close vector matches faster than comparing every vector. Hierarchical Navigable Small World, or HNSW, is a graph-based ANN index that balances speed, memory, and recall. Dense search uses embeddings for meaning; sparse search uses keywords such as Best Matching 25, or BM25, for exact terms. Hypothetical Document Embeddings, or HyDE, generates a hypothetical answer to improve retrieval, but the final answer must always use real retrieved sources as evidence.

## How should I explain hallucinations and safety?

> Hallucinations happen because LLMs predict plausible next tokens rather than verifying every fact. I reduce them with RAG, citations, structured tools, output validation, and explicit abstention when evidence is missing. For security, I treat user input and retrieved documents as untrusted, use allowlisted tools, server-side authorization, parameter validation, audit logs, and human approval for sensitive actions.

## How should I explain Constitutional AI and RLHF?

> Reinforcement Learning from Human Feedback, or RLHF, uses human preference data to steer a model toward helpful and safe responses. Constitutional AI uses written principles to critique and improve outputs, with AI feedback able to supplement human feedback. Both are model-alignment approaches; runtime guardrails are still required in the application.

## How should I explain evaluation?

> I create a golden dataset containing representative questions, expected answers, expected source passages, or expected tool calls. I evaluate retrieval recall, groundedness, answer quality, tool correctness, latency, cost, and safety. I use deterministic code-based tests where possible and rubric-based LLM-as-a-judge evaluation for subjective quality. Every change to prompts, models, or retrieval should run against the regression set.

## How should I explain LangChain and LangGraph?

> LangChain provides reusable integrations for prompts, models, retrievers, and tools. LangGraph is for explicit stateful orchestration: branches, retries, cycles, checkpoints, and human approval. I use LangChain for a simple assistant and LangGraph when an agent workflow needs durability and control.

## How should I explain MCP and A2A?

> Model Context Protocol, or MCP, standardizes how an AI application connects to external tools, resources, and prompts. Agent2Agent Protocol, or A2A, standardizes how one agent delegates work to another remote agent. MCP is mainly agent-to-capability integration; A2A is agent-to-agent collaboration.

## How should I explain agent memory?

> I separate memory by purpose. Short-term memory holds the current task and conversation. Long-term memory holds approved preferences across sessions. Semantic memory is retrieved knowledge from documents, and episodic memory stores useful past outcomes or traces. I store only data that is useful, authorized, and auditable, then retrieve it when needed instead of putting all history in every prompt.

## How should I explain API design for an AI service?

> I keep the LLM separate from business authority. The Application Programming Interface, or API, authenticates the user, applies rate limits, routes the request, retrieves only authorized context or invokes allowlisted tools, validates the output, and records traces. This makes the AI feature safer, testable, and easier to maintain.

## How should I explain REST, Flask, and FastAPI?

> Representational State Transfer, or REST, is a resource-oriented style for Hypertext Transfer Protocol APIs. It uses methods such as GET, POST, PATCH, and DELETE with clear resources and status codes. Flask is a lightweight flexible Python web framework. FastAPI provides type-hint-based validation, OpenAPI documentation, and asynchronous support, so it is often convenient for Input/Output-heavy AI services.

## How should I explain database optimization?

> I begin with measurement: inspect slow-query plans and use production-like data. Then I index common filters and joins, select only required columns, paginate, avoid N+1 queries, use connection pools and caching, and partition only when scale requires it. For RAG, I also tune metadata filtering, vector index parameters, chunk design, and reranking.

## How should I explain event-driven architecture?

> In an event-driven design, a service publishes an event and independent consumers react to it. For example, an OrderCreated event can trigger inventory updates, notifications, and analytics. I use idempotent consumers, retries, dead-letter queues, event schemas, and tracing so the system handles duplicate events and failures safely.

## Final interview habit

After any definition, add one practical sentence:

> In my implementation, I would validate this in the backend, log the result, and evaluate it against representative user cases.

That sentence shows you understand production engineering, not only theory.

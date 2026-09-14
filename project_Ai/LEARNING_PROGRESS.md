# AI Support Knowledge Copilot — Learning Progress

Last updated: 13 September 2026

## 1. Project purpose

We are building an AI support knowledge copilot one small, understandable step at a time. The project is designed to teach backend development, PostgreSQL, pgvector, embeddings, retrieval-augmented generation (RAG), evaluation, and eventually agent workflows such as CrewAI.

The goal is not to assemble a large amount of framework code quickly. The goal is to understand why every component exists, how data moves through the system, how failures appear, and how the design changes when a prototype becomes a production application.

## 2. Industry problem

Organizations store useful knowledge across support articles, PDFs, policies, product documentation, tickets, and internal tools. A support employee often has to search several systems before answering a customer. This creates several problems:

- Slow response times
- Inconsistent answers between support agents
- Answers based on outdated policies
- Expensive employee onboarding
- Unsupported AI answers or hallucinations
- Poor visibility into which questions the knowledge base cannot answer

Our intended solution accepts a user question, finds the most relevant approved company information, and uses that information to create a grounded answer with a source.

The eventual request flow will be:

```text
User question
    ↓
FastAPI validation
    ↓
Question embedding
    ↓
pgvector similarity search
    ↓
Relevant document chunks
    ↓
Prompt containing question + retrieved context
    ↓
LLM API call
    ↓
Grounded answer + citations + confidence/fallback
```

## 3. Important terminology

### Ingestion

The process of taking source information, cleaning it, splitting it when necessary, generating embeddings, and storing the results. The current project has completed a very small ingestion pipeline for three database records.

This is called **ingestion**, not injection. Prompt injection is a separate security topic involving malicious instructions placed in user input or retrieved documents.

### Embedding

An embedding is a numeric representation of text. We use `sentence-transformers/all-MiniLM-L6-v2`, which maps each text into 384 floating-point values. Texts with related meanings should have vectors that are closer together.

### pgvector

pgvector is a PostgreSQL extension. It adds the `vector` data type, distance operators, and vector indexes. PostgreSQL remains responsible for durable storage, metadata, permissions, transactions, and ordinary SQL queries.

### RAG

RAG means Retrieval-Augmented Generation:

1. **Retrieval:** Find relevant source passages.
2. **Augmentation:** Put those passages into the model prompt as context.
3. **Generation:** Ask a language model to answer using that context.

At the current checkpoint, ingestion, semantic retrieval, prompt augmentation, and local LLM generation are connected through FastAPI. The project now has a complete minimal RAG path, although it still needs broader data, evaluation, automated tests, and production infrastructure.

## 4. Current architecture

The primary application path is now a complete minimal RAG flow.

### Current FastAPI RAG path

```text
POST /questions
    ↓
main.py
    ↓
rag_service.py
    ↓
embeddings.py
    ↓
vector_search.py → PostgreSQL + pgvector
    ↓
similarity threshold
    ↓
prompt_builder.py
    ↓
local_llm.py → Ollama → qwen3:4b-instruct
    ↓
answer + backend-controlled source + similarity
```

This path works end to end. Invalid request bodies are rejected by Pydantic, insufficient retrieval returns a fallback without calling the LLM, and dependency failures are mapped to HTTP `503`.

### Legacy learning path

```text
retrieval.py → keyword overlap → PostgreSQL
```

This earlier keyword retriever remains for comparison but is no longer used by the FastAPI endpoint.

### Ingestion path

```text
Rows with embedding IS NULL
    ↓
ingest_embeddings.py
    ↓
Title + content
    ↓
embeddings.py
    ↓
384-dimensional vector
    ↓
documents.embedding in PostgreSQL
```

## 5. Technology choices

| Technology | Current responsibility | Why it was chosen |
|---|---|---|
| Python | Application language | Strong AI ecosystem and readable backend code |
| FastAPI | HTTP API | Validation, type hints, JSON responses, and generated API docs |
| Uvicorn | Development web server | Runs the ASGI FastAPI application |
| Pydantic | Request models | Validates incoming JSON before business logic runs |
| PostgreSQL 16 | Durable knowledge storage | Mature relational database with transactions and rich querying |
| pgvector 0.8.6 | Vector storage and search | Keeps semantic vectors beside relational metadata |
| Psycopg 3 | Python/PostgreSQL adapter | Allows Python to execute SQL safely with parameters |
| python-dotenv | Local configuration | Loads development environment variables from `.env` |
| Sentence Transformers | Local embedding generation | No API key or per-request cost while learning |
| all-MiniLM-L6-v2 | Current embedding model | Small English semantic-search model with 384 dimensions |
| Docker | Local database runtime | Reproducible PostgreSQL + pgvector environment |

## 6. Current files and responsibilities

| File | Responsibility | Current status |
|---|---|---|
| `main.py` | FastAPI app, `/health`, and `/questions` | Works; `/questions` still calls keyword retrieval |
| `database.py` | Loads `DATABASE_URL` and reads documents | Works; opens a new synchronous connection per call |
| `knowledge_base.py` | Original in-memory sample records | Retained for learning comparison; no longer the main data source |
| `retrieval.py` | Stop-word filtering and keyword-overlap retrieval | Works against PostgreSQL |
| `embeddings.py` | Loads MiniLM and creates normalized 384-dimensional embeddings | Works locally |
| `ingest_embeddings.py` | Embeds database rows whose embedding is `NULL` | Works and is safely rerunnable for unchanged rows |
| `vector_search.py` | Cosine-similarity search with a `0.30` threshold | Works from CLI and through the RAG API |
| `.env` | Local database connection string | Exists; must remain private |
| `.gitignore` | Prevents local/generated files entering Git | Configured for secrets, virtual environments, caches, and bytecode |
| `schema.sql` | Defines source and chunk storage | Applied; creates `sources` and `document_chunks` |
| `evaluation_cases.py` | Labeled questions and expected retrieval sources | Contains eight baseline cases |
| `evaluate_retrieval.py` | Measures retrieval without calling the LLM | Baseline result: 8/8 cases passed |
| `data/support_guide.txt` | First realistic multi-topic source document | Created and ready for chunking |
| `chunking.py` | Loads and divides text into overlapping chunks | Current task; not created yet |

## 7. Database design at this checkpoint

The simplified table is conceptually:

```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    embedding vector(384)
);
```

Current records:

- Password Reset
- Refund Policy
- Support Hours

All three records currently have 384-dimensional embeddings.

This schema is appropriate for learning, but a real RAG system would usually separate source documents and searchable chunks:

```text
sources
├── source identity, URI, version, owner, timestamps
└── document_chunks
    ├── source_id
    ├── chunk position
    ├── chunk text
    ├── metadata
    └── embedding
```

That separation allows citations to point to an exact page or section and lets one large document produce many searchable passages.

## 8. Work completed

1. Created and activated a Python virtual environment.
2. Installed FastAPI and Uvicorn.
3. Created `GET /health` to prove the server can accept requests.
4. Created `POST /questions` with a Pydantic request body.
5. Built a small in-memory knowledge base.
6. Implemented keyword-overlap retrieval.
7. Removed common stop words to reduce false matches.
8. Returned an answer and source from the API.
9. Started PostgreSQL with pgvector in Docker.
10. Created the `documents` table and inserted three records.
11. Connected Python to PostgreSQL through Psycopg.
12. Moved the database URL into `.env`.
13. Replaced in-memory retrieval data with PostgreSQL data.
14. Enabled the pgvector extension.
15. Installed and tested a local embedding model.
16. Added a `vector(384)` database column.
17. Generated and stored embeddings for all three documents.
18. Performed cosine-distance semantic retrieval.
19. Observed a relevant score of `0.453` and an unrelated score of `0.116`.
20. Added an initial minimum similarity threshold of `0.30`.
21. Connected semantic retrieval, augmentation, and local Ollama generation to FastAPI.
22. Added strict Pydantic request and response schemas.
23. Added safe HTTP `503` handling for database and local-model failures.
24. Created an eight-question retrieval evaluation set and achieved an 8/8 baseline.
25. Created `sources` and `document_chunks` tables for real document ingestion.
26. Created the first realistic source file at `data/support_guide.txt`.

## 9. What we learned from real errors

### Python indentation controls lifetime and execution

The `if __name__ == "__main__"` block was initially placed inside a function after a `return`, so it was unreachable. Another indentation issue moved `fetchall()` outside the cursor context and produced `psycopg.InterfaceError: the cursor is closed`.

Lesson: indentation is program structure in Python, not just formatting.

### Context managers own resources

Code inside:

```python
with connection.cursor() as cursor:
```

may use the cursor. When indentation leaves that block, the cursor is closed. The same principle applies to files, HTTP clients, transactions, and database connections.

### Host ports can conflict

A native Windows `postgres.exe` already owned IPv4 port `5432`. Docker also attempted to expose PostgreSQL on that port, so Python reached the wrong server and reported password authentication failures.

We resolved this by mapping:

```text
Windows port 5433 → container port 5432
```

Lesson: an authentication error can be caused by reaching the wrong service, not only by typing the wrong password.

### Virtual environments must be used explicitly

Psycopg was initially installed under a different Python interpreter. Using:

```powershell
.\.venv\Scripts\python.exe -m pip install <package>
```

ensures installation into this project. Running scripts with the same interpreter removes ambiguity.

### Native ML libraries have operating-system dependencies

PyTorch was installed but could not load `shm.dll` until the Microsoft Visual C++ Redistributable was installed. Python packages can depend on native compiled libraries outside Python itself.

### Nearest does not mean relevant

The weather question still received a nearest vector result. Its similarity was only `0.116`, compared with `0.453` for the password-related query. A vector database always ranks available candidates; the application must decide whether the best candidate is good enough.

### Public model download warning

The Hugging Face warning about unauthenticated requests does not prevent this public model from working. A token may improve rate limits, but it is not required for the current lesson.

## 10. Commands for resuming the project

Move to the project directory:

```powershell
cd C:\Users\akram\OneDrive\Desktop\python\project_Ai
```

Use the project interpreter explicitly:

```powershell
.\.venv\Scripts\python.exe --version
```

Check the database container:

```powershell
docker ps --filter "name=ai-knowledge-db"
```

If it is stopped:

```powershell
docker start ai-knowledge-db
```

Run the database read test:

```powershell
.\.venv\Scripts\python.exe database.py
```

Run ingestion for documents missing embeddings:

```powershell
.\.venv\Scripts\python.exe ingest_embeddings.py
```

Run standalone semantic search:

```powershell
.\.venv\Scripts\python.exe vector_search.py
```

Run the current API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Useful URLs:

- Health: `http://127.0.0.1:8000/health`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

## 11. Current limitations

This prototype is intentionally incomplete:

- Generation uses a local Ollama model rather than a managed hosted LLM service.
- Only three short records exist.
- There is no document upload or parsing.
- Large documents are not divided into chunks.
- The `0.30` threshold is based on very few examples.
- Only one nearest document is returned.
- No vector index is needed yet and none has been created.
- Database connections are opened per operation instead of using a pool.
- The synchronous RAG work runs in a normal `def` route and still needs explicit concurrency/load testing.
- There are response models, but no committed automated test suite, authentication, authorization, rate limits, metrics, or tracing.
- There is no tenant isolation or permission filtering.
- The system prompt tells the model to treat context as data, but robust prompt-injection testing and document trust controls are not implemented.
- A new HTTP client and database connection are created per request; production traffic will require connection reuse/pooling.
- The embedding model is loaded inside the API process, increasing startup time and memory use for every worker.

## 12. Next session: exact resume point

The next lesson should begin with a small chunking task:

1. Create `chunking.py`.
2. Load `data/support_guide.txt` as UTF-8 text.
3. Split it into overlapping word windows.
4. Print every chunk and inspect topic boundaries before storing anything.

After that, the learning sequence should be:

1. Tune the similarity threshold using measured examples.
2. Retrieve multiple results with top-k search.
3. Add document chunking and source metadata.
4. Add automated tests for schemas, retrieval, fallback, and API errors.
5. Add document ingestion through a background job or admin workflow.
6. Add connection pooling, structured logging, and observability.
7. Add vector indexes only after the data volume justifies them.
8. Compare local and hosted LLM tradeoffs when hosted access is available.
9. Evaluate whether an agent workflow adds genuine value.

## 13. How the first real LLM API call will fit

The first LLM call should be built and tested separately before connecting it to the endpoint:

```text
System instruction:
Answer only from the supplied company context. If the context is insufficient,
say that the answer is not available.

Retrieved context:
<document chunks and source identifiers>

User question:
<validated question>
```

The backend—not the model—should control retrieval, source identifiers, authorization filters, timeouts, and the response structure. The model should not be trusted to invent citations or decide which private records a user may access.

## 14. Production best practices

### Code organization

As the code grows, separate responsibilities:

```text
app/
├── main.py              # application creation
├── api/                 # HTTP routes and request/response models
├── core/                # settings, logging, security
├── db/                  # connections, repositories, migrations
├── ingestion/           # loaders, cleaning, chunking, embedding jobs
├── retrieval/           # vector search, keyword search, reranking
├── generation/          # prompts and LLM client
└── tests/               # unit, integration, retrieval, and API tests
```

Routes should be thin. They validate HTTP input and call services. SQL belongs in a repository/data-access layer. Embedding and generation logic belong in separate services.

### Configuration and secrets

- Never commit `.env`.
- Add `.env`, `.venv/`, and `__pycache__/` to `.gitignore`.
- Commit an `.env.example` containing variable names but no real secrets.
- Use a managed secret store in production.
- Rotate credentials when exposure is suspected.
- Use separate credentials for development, testing, and production.

### Database reliability

- Use migrations instead of manually changing production schemas.
- Use a connection pool rather than opening unlimited connections.
- Set connection and statement timeouts.
- Keep transactions short.
- Add retry logic only for retryable failures.
- Do not catch every database error and pretend no data exists.
- Back up the database and test restores.
- Store source version and embedding-model version.

### Retrieval quality

- Split large documents into meaningful chunks with limited overlap.
- Preserve page, section, URL, owner, and access metadata.
- Retrieve several candidates rather than only one.
- Consider hybrid search: keyword ranking plus semantic similarity.
- Add a reranker when top-k results need better ordering.
- Evaluate thresholds by question category rather than guessing.
- Re-embed content when the embedding model or chunking logic changes.
- Never compare vectors produced by different embedding spaces as though they were compatible.

### LLM reliability and safety

- Instruct the model to use only supplied context.
- Provide citations from backend-controlled metadata.
- Refuse or escalate when retrieval is insufficient.
- Treat retrieved documents as untrusted data, not system instructions.
- Defend against prompt injection in user questions and documents.
- Redact sensitive data where appropriate.
- Set request timeouts and bounded retries.
- Track token use, latency, failures, and model version.
- Keep a deterministic non-LLM fallback when possible.

### API design

- Validate question length and reject blank input.
- Use explicit response models.
- Return stable error structures.
- Use appropriate status codes.
- Add authentication and authorization before private data is exposed.
- Rate-limit expensive embedding and generation calls.
- Add request IDs for tracing.
- Do not expose internal exceptions or secrets to clients.

### Testing and evaluation

Traditional backend tests and AI evaluations solve different problems:

- Unit tests verify small deterministic functions.
- Integration tests verify PostgreSQL and pgvector behavior.
- API tests verify request validation and response contracts.
- Retrieval evaluations measure whether relevant chunks appear in top-k.
- Generation evaluations measure groundedness, citation correctness, and usefulness.
- Regression datasets prevent a prompt or model change from silently reducing quality.

Useful retrieval metrics later include recall@k, precision@k, mean reciprocal rank, threshold false-positive rate, and threshold false-negative rate.

## 15. Scaling path

### Small prototype

- Exact pgvector scan
- A few hundred or thousand chunks
- One FastAPI process
- Local embedding model
- Simple synchronous ingestion

Exact search is appropriate now. An index would add complexity without helping three rows.

### Growing internal application

- Database connection pool
- Batched embedding generation
- Background ingestion queue
- Source and chunk tables
- Top-k retrieval and reranking
- HNSW vector index after measurement
- Structured logs, metrics, traces, and evaluation jobs
- Authentication and document-level permissions

### Larger production system

- Multiple API workers
- Separate ingestion workers
- Managed PostgreSQL with backups and replicas
- Carefully tuned HNSW indexes
- Caching for repeated questions and embeddings
- Tenant-aware filtering before ranking
- Dedicated model-serving or hosted embedding API
- Versioned prompts, models, chunks, and embeddings
- Gradual re-embedding without downtime
- Capacity planning based on QPS, vector count, dimensions, latency, and cost

An approximate vector index should be introduced only after measuring exact-search latency and recall. Scaling is not merely adding servers; it also requires correct permissions, failure handling, observability, and quality evaluation.

## 16. Where CrewAI or other agents may fit

CrewAI should not replace a simple, reliable RAG request. Agents become useful when a business task genuinely requires multiple steps, tools, roles, or review stages. Possible later workflows include:

- A triage agent classifies a support request.
- A retrieval agent searches approved knowledge.
- A drafting agent prepares an answer.
- A reviewer checks grounding and policy compliance.
- An escalation agent creates a human-support ticket when confidence is low.

Before adding agents, the single retrieval-and-generation pipeline must be tested. Otherwise, agents multiply latency, cost, and failure modes without solving a demonstrated problem.

## 17. Definition of the first useful MVP

The first useful MVP will be complete when it can:

- Accept a validated support question through an API.
- Retrieve authorized and relevant document chunks with pgvector.
- Reject weak retrieval results.
- Call an LLM with only the retrieved context.
- Produce a concise answer.
- Return trustworthy source metadata.
- Say “I do not know” when the knowledge base is insufficient.
- Record enough telemetry to diagnose latency and failures.
- Pass a small, repeatable evaluation set.

That MVP solves a real problem while remaining small enough to understand fully.

## 18. Current checkpoint summary

The project now has a complete minimal RAG API: validated questions are embedded, searched with pgvector, filtered by similarity, augmented with source context, and answered by a local Ollama model. The backend returns its own source metadata and avoids calling the LLM when retrieval is insufficient. The eight-case baseline retrieval evaluation passed, the source/chunk schema exists, and a realistic text source is ready. The exact next boundary is implementing and inspecting chunking before inserting chunks into PostgreSQL.

The most important principle so far is:

```text
A strong RAG answer begins with relevant, authorized, traceable retrieval.
An LLM cannot repair missing or incorrect source context reliably.
```

## 19. Live learning map

This section is updated as implementation progresses.

```text
[Backend fundamentals] COMPLETE
          |
          v
[PostgreSQL storage] COMPLETE
          |
          v
[Embeddings + pgvector] COMPLETE
          |
          v
[Semantic retrieval] COMPLETE
          |
          v
[Prompt augmentation] COMPLETE
          |
          v
[Local LLM generation] COMPLETE
          |
          v
[Minimal RAG API] COMPLETE
          |
          v
[Retrieval evaluation] BASELINE COMPLETE (8/8)
          |
          v
[Real source + chunk schema] COMPLETE
          |
          v
[Text chunking] CURRENT TASK
          |
          v
[Chunk ingestion] NEXT
          |
          v
[Top-k chunk retrieval]
          |
          v
[Grounded multi-chunk answer]
          |
          v
[Tests, security, observability, scale]
          |
          v
[CrewAI workflow, only where justified]
```

### Current learning focus

Chunking determines the unit that retrieval can find. Chunks that are too large mix unrelated topics and waste prompt space. Chunks that are too small lose context. Overlap reduces boundary loss but duplicates content and storage. The current word-window implementation is intentionally simple; after inspecting it, we will compare it with paragraph-aware and token-aware approaches.

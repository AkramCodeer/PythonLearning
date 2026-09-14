CREATE EXTENSION IF NOT EXISTS vector;


CREATE TABLE IF NOT EXISTS sources (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_path TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL
        REFERENCES sources(id)
        ON DELETE CASCADE,

    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(384),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (source_id, chunk_index)
);
# Architecture Decisions

Decisions made while building this project, and the reasoning behind each one.

---

## Stack overview

| layer | technology | why |
|-------|-----------|-----|
| Backend | FastAPI | async support, automatic docs via Swagger, minimal boilerplate |
| Database | PostgreSQL | relational data with foreign keys; runs locally via Docker |
| ORM | SQLAlchemy | industry standard for Python, works well with Alembic |
| Migrations | Alembic | autogenerates migrations from SQLAlchemy models |
| LLM (summarization + questions) | Gemini `2.5 Flash` | free tier sufficient for development sprints |
| Embeddings | OpenAI `text-embedding-3-small` | best quality/cost ratio for semantic search |
| Vector store | ChromaDB | local, no infrastructure needed, simple Python API |
| PDF extraction | PyMuPDF | fast, reliable, handles most academic PDFs |
| Logging | Loguru | simpler API than standard logging, file sink out of the box |
| Package manager | uv | faster than pip, handles virtual envs and Python versions |

---

## Backend structure

```
backend/
├── main.py              — app entrypoint, router registration, loguru file sink
├── database.py          — SQLAlchemy engine, SessionLocal, get_db dependency
├── models/              — SQLAlchemy models (DB schema)
├── schemas/             — Pydantic models (AI response validation)
├── repositories/        — all database operations (one file per entity)
├── routers/             — FastAPI endpoints (one file per resource)
└── services/            — external integrations: AI, PDF, chunking, vector store
```

**Why this structure:** routers handle HTTP, repositories handle the database, services handle external calls. Each layer has one responsibility and doesn't cross into another's territory. This makes it easy to change one layer without touching the others.

---

## Data model

```
users
 └── folders (user_id → users)
 └── papers (user_id → users, folder_id → folders)
      ├── paper_content (paper_id → papers)   — raw extracted text, stored separately
      ├── paper_authors (paper_id × author_id) — many-to-many junction table
      └── paper_questions (paper_id → papers)  — AI-generated Q&A pairs
authors
```

**Why separate `paper_content`:** the raw text of a paper can be hundreds of thousands of characters. Storing it in the `papers` table would load it on every list query. Separating it means `GET /papers` is fast — the raw text is only fetched when needed.

**Why `authors` as a separate table:** the same author can have multiple papers. Storing names as a list in the paper row would make author-based queries impossible. The `paper_authors` junction table enables many-to-many without duplication.

**Why `paper_questions` saved to DB:** questions are generated once and reused. Re-generating on every request would cost API calls and introduce inconsistency. If questions exist, they're returned from the database.

**Why `content_hash` on papers:** SHA256 hash of the PDF bytes enables duplicate detection before any AI call is made, regardless of filename.

---

## AI pipeline

### Upload flow
```
PDF bytes
  → extract text (PyMuPDF)
  → strip NUL characters
  → send to Gemini → structured analysis (name, authors, summary, methodology...)
  → save paper + content to PostgreSQL
  → save authors to PostgreSQL
  → split text into chunks (chunk_size=1000, overlap=200)
  → embed chunks (OpenAI text-embedding-3-small)
  → save chunks + embeddings to ChromaDB
  → single db.commit()
```

Everything after validation runs inside a `try/except`. If any step fails, `db.rollback()` undoes all PostgreSQL changes. ChromaDB is written last, after the DB commit succeeds.

### Search flow
```
query string
  → embed query (OpenAI)
  → search ChromaDB (filtered by user_id)
  → extract unique paper_ids from chunk metadata
  → fetch papers from PostgreSQL
  → return papers
```

### Question generation flow
```
paper_id
  → check if questions already exist in DB → return if yes
  → fetch raw text from paper_content
  → send to Gemini with peer-reviewer prompt
  → save each question+answer pair to paper_questions
  → return questions
```

---

## Chunking strategy

Papers are split into overlapping chunks of 1000 characters with 200-character overlap. The overlap ensures sentences at chunk boundaries aren't lost when searching.

A single embedding for an entire paper would average out all its content into one vector, making precise retrieval impossible. Chunking allows ChromaDB to return the specific part of the paper relevant to a query.

---

## Atomicity

All upload operations run in a single transaction. Repository functions use `db.flush()` (not `db.commit()`) so that auto-generated IDs (like `paper_id`) are available for subsequent operations, while keeping the transaction open. A single `db.commit()` happens at the end of the router function. On any exception, `db.rollback()` is called so no partial data is left in the database.

Validations (duplicate check, content type, empty text) run **before** the `try` block so they return HTTP 400 errors, not 500s.

---

## What's not here yet

- **Authentication** — `user_id` is hardcoded as `1`. All endpoints accept it as a query parameter so the migration to real auth will be a small change.
- **Frontend** — React app placeholder only. To be built when the backend is stable.
- **RAG chat** — Sprint 5. Will use ChromaDB chunks as context for a conversational interface over a specific paper.

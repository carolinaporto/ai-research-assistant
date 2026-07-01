# Learnings

Personal notes on concepts learned while building this project.

---

## Summary

| topic | section | sprint |
|-------|---------|--------|
| Conventional Commits | [Git](#git) | 0 |
| Loguru log levels | [Logging](#logging) | 1 |
| Alembic commands | [Database & Migrations](#database--migrations) | 1 |
| Foreign key deletion order | [Database & Migrations](#database--migrations) | 4 |
| NUL characters in PDFs | [Database & Migrations](#database--migrations) | 4 |
| flush() vs commit() | [Database & Migrations](#database--migrations) | 4 |
| Atomic transactions | [Database & Migrations](#database--migrations) | 4 |
| Embeddings | [AI & Embeddings](#ai--embeddings) | 4 |
| Chunking | [AI & Embeddings](#ai--embeddings) | 4 |
| ChromaDB | [AI & Embeddings](#ai--embeddings) | 4 |
| Semantic search flow | [AI & Embeddings](#ai--embeddings) | 4 |
| multipart/form-data | [HTTP & APIs](#http--apis) | 0 |
| UploadFile in FastAPI | [HTTP & APIs](#http--apis) | 0 |

---

## Git

### Conventional Commits
`Sprint 0`

Format: `type(scope): message` — scope is optional.

| type | when to use |
|------|-------------|
| `feat` | new feature |
| `fix` | bug fix |
| `docs` | documentation only |
| `chore` | setup, config, tooling |
| `refactor` | restructure without changing behavior |
| `style` | formatting, no logic change |

---

## Logging

### loguru — log levels and when to use each
`Sprint 1`

| level | when to use |
|-------|-------------|
| `logger.debug()` | Internal details — variable values, sizes, flow tracing. |
| `logger.info()` | Normal operations — request received, paper saved, API call made. |
| `logger.warning()` | Unexpected but recoverable — duplicate upload, empty PDF. |
| `logger.error()` | Something failed — API error, DB error, parse failure. |

**Rule:** log where something *happens*, not in every layer that calls it. Use `{}` placeholders instead of f-strings — loguru only formats the string if the log level is active.

---

## Database & Migrations

### Alembic — common commands
`Sprint 1`

| command | what it does |
|---------|-------------|
| `alembic init alembic` | Set up Alembic in the project (only once) |
| `alembic revision --autogenerate -m "message"` | Compare models vs DB and generate a migration file |
| `alembic upgrade head` | Apply all pending migrations to the DB |
| `alembic downgrade -1` | Undo the last migration |
| `alembic current` | Show which migration the DB is currently at |
| `alembic history` | List all migrations in order |

`DATABASE_URL` must be set and the DB container must be running before generating or applying migrations.

### Deleting records with foreign keys
`Sprint 4`

PostgreSQL blocks deletion if other tables still reference the record. Delete dependent records first, in order: `paper_questions → paper_authors → paper_content → papers`.

SQLAlchemy batches deletions and decides the order at `commit()` — use `db.flush()` after each group to force the correct execution order.

### NUL characters in PDFs
`Sprint 4`

PyMuPDF can extract `\x00` (NUL) characters from PDFs. PostgreSQL rejects them in text fields. Strip them right after extraction: `text.replace('\x00', '')`.

### flush() vs commit()
`Sprint 4`

| | `db.flush()` | `db.commit()` |
|---|---|---|
| Sends SQL to DB | Yes | Yes |
| Closes the transaction | No | Yes |
| Can be rolled back | Yes | No |
| Generates auto IDs | Yes | Yes |

Use `flush()` inside repository functions when you need a generated ID but aren't done yet. Use `commit()` once at the end of the operation.

### Atomic transactions
`Sprint 4`

Put validations **before** the `try` block — they should return 400, not 500. Wrap only DB and external operations inside `try/except`. Call `db.rollback()` on failure so nothing is left half-saved.

---

## AI & Embeddings

### What are embeddings?
`Sprint 4`

A vector of numbers that represents the **semantic meaning** of a text. Similar texts produce vectors that are close together in space. Enables semantic search — finding content by meaning, not exact words. Model used: `text-embedding-3-small` (1536 floats per text).

### Chunking
`Sprint 4`

A full paper is too long to embed as a single block. Split it into overlapping chunks (`chunk_size=1000`, `overlap=200`) and embed each separately. The overlap ensures sentences at boundaries aren't lost.

### ChromaDB
`Sprint 4`

Local vector database. Stores embeddings with metadata (`paper_id`, `user_id`) and supports similarity search with `where` filters. Use `PersistentClient` so data survives restarts.

### Semantic search flow
`Sprint 4`

```
query → embed query → search ChromaDB → extract paper_ids from metadata → fetch papers from PostgreSQL
```

ChromaDB returns chunks — use `paper_id` from metadata to look up the full paper in the relational database.

---

## HTTP & APIs

### Content-Type and multipart/form-data
`Sprint 0`

JSON is pure text — PDFs are binary and can't be embedded in JSON. Use `multipart/form-data` for file uploads: it splits the request into named parts, each with its own headers. Rule: JSON for data, `multipart/form-data` for files.

### UploadFile in FastAPI
`Sprint 0`

FastAPI unwraps the multipart request automatically. Key attributes: `file.filename`, `file.content_type`, `await file.read()`. No need to save to disk — read the bytes and pass them directly to whatever library needs them.

---

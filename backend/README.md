# Backend

FastAPI backend for the AI Research Assistant.

---

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) — package manager
- Docker — for the PostgreSQL database

---

## Setup

**1. Start the database**
```bash
docker run --name postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=papers -p 5432:5432 -d postgres
```

**2. Configure environment**
```bash
cp .env.example .env
# fill in your API keys and DATABASE_URL
```

**3. Install dependencies**
```bash
uv sync
```

**4. Run migrations**
```bash
alembic upgrade head
```

**5. Start the server**
```bash
uvicorn main:app --reload
```

API docs available at `http://localhost:8000/docs`

---

## Environment variables

| variable | description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `GEMINI_API_KEY` | Used for paper summarization and question generation |
| `OPENAI_API_KEY` | Used for embeddings (`text-embedding-3-small`) |

---

## API endpoints

| method | endpoint | description |
|--------|----------|-------------|
| `POST` | `/papers/uploadfile/` | Upload a PDF — extracts, analyzes, and embeds |
| `GET` | `/papers/` | List all papers for a user |
| `GET` | `/papers/search?q=...` | Semantic search across papers |
| `GET` | `/papers/{id}` | Get a single paper |
| `DELETE` | `/papers/{id}` | Delete a paper and all related data |
| `PUT` | `/papers/{id}/folder/{id}` | Move paper to a folder |
| `POST` | `/folders/` | Create a folder |
| `GET` | `/folders/` | List folders |
| `GET` | `/folders/{id}` | Get a folder |
| `POST` | `/questions/` | Generate and save questions for a paper |
| `GET` | `/questions/{paper_id}` | Get saved questions for a paper |
| `DELETE` | `/questions/{question_id}` | Delete a question |
| `DELETE` | `/questions/paper/{paper_id}/all` | Delete all questions for a paper |

---

## Project structure

```
backend/
├── main.py              — app entrypoint
├── database.py          — SQLAlchemy setup
├── models/models.py     — database models
├── schemas/paper.py     — Pydantic schemas for AI responses
├── repositories/        — database operations
├── routers/             — API endpoints
└── services/            — AI, PDF, chunking, vector store
```

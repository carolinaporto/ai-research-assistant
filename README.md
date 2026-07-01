# AI Research Assistant

A personal tool to read, understand, and explore academic papers — built as a learning project to study LLMs, RAG, embeddings, and AI engineering.

Upload a PDF and get a structured summary, critical questions, and semantic search across your paper library. The goal is to make reading research papers more active and analytical.

---

## What it does

- **Upload papers** — extract text from PDFs and generate structured analysis (title, authors, objective, methodology, findings, limitations)
- **Critical questions** — generate peer-reviewer-style questions with answers to test your understanding
- **Organize** — create folders and move papers between them
- **Semantic search** — search across all your papers by meaning, not just keywords
- **RAG chat** *(Sprint 5, coming)* — ask questions about a specific paper and get answers grounded in its content

---

## Tech stack

**Backend:** FastAPI · PostgreSQL · SQLAlchemy · Alembic · ChromaDB  
**AI:** Gemini 2.5 Flash (summarization + questions) · OpenAI text-embedding-3-small (semantic search)  
**Frontend:** React *(placeholder — to be built)*

---

## Docs

- [Architecture decisions](docs/architecture.md) — stack choices, data model, AI pipeline
- [Sprint planning](docs/sprints.md) — what was built in each sprint and what's next
- [Learnings](docs/learnings.md) — concepts learned while building this

---

## Project structure

```
ai-research-assistant/
├── backend/        — FastAPI API (see backend/README.md)
├── frontend/       — React app (placeholder)
└── docs/           — architecture, sprint planning, learnings
```

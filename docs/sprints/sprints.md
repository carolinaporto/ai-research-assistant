# Sprint Planning

Living document — updated as the project evolves. Sprints are defined and refined as we go, not set in stone upfront.

---

## Sprint 0 — PDF Upload + LLM Summary (no persistence)
**Status:** Completed.
**Goal:** Get the core loop working end-to-end: upload a PDF, extract its text, send it to Claude, return a summary.
**No database in this sprint.** The summary is returned in the API response and not saved.

### Deliverables
- [x] FastAPI project setup (dependencies, app entrypoint, dev server running)
- [x] `POST /papers/upload` endpoint — accepts a PDF file
- [x] PDF text extraction using PyMuPDF
- [x] Claude API call to summarize the extracted text
- [x] Return the summary as a JSON response

### Out of scope
- Database / persistence
- Folders / organization
- Frontend (placeholder only)
- Authentication

---

## Sprint 1 — Persistence + Structured Extraction
**Status:** Completed
**Goal:** Save uploaded papers to PostgreSQL with structured AI-extracted fields. Data model covers papers, folders, authors, and users.

### Notes
Structured extraction (originally Sprint 2) was pulled into this sprint — it emerged naturally while designing the data model and the AI response schema.

### Deliverables
- [x] Data model design: papers, folders, authors, paper_authors, paper_content, users
- [x] SQLAlchemy models (`models/models.py`)
- [x] Alembic setup + initial migration (all tables created in PostgreSQL)
- [x] Repository layer (`repositories/papers.py`)
- [x] Pydantic schema for AI response (`schemas/paper.py` — PaperAnalysis)
- [x] Structured output from Gemini (JSON with name, authors, objective, summary, methodology, dataset, main_findings, limitations)
- [x] Upload endpoint saves paper + raw text to DB
- [x] Loguru logging across router, services, and repositories (terminal + file sink)
- [x] Authors extracted and saved to `authors` + `paper_authors` tables
- [x] Duplicate detection via SHA256 content hash
- [x] `GET /papers` — list all papers for a user
- [x] `GET /papers/{id}` — retrieve a single paper
- [x] `GET /folders` — list folders
- [x] `POST /folders` — create a folder
- [x] `PUT /papers/{id}/folder` — move paper to a folder

---

## Sprint 3 — Critical Questions + Peer Review Mode
**Status:** Draft
**Goal:** Generate critical/analytical questions about the paper. Explore prompt engineering for a "peer reviewer" persona.

---

## Sprint 4 — Semantic Search
**Status:** Draft
**Goal:** Embed papers using OpenAI `text-embedding-3-small`, store vectors in ChromaDB, enable semantic search across uploaded papers. (Migrate from Gemini to OpenAI starting here.)

---

## Sprint 5 — RAG Chat
**Status:** Draft
**Goal:** Chat with a specific paper using Retrieval-Augmented Generation. Ask questions, get answers grounded in the paper's content.

---

## Ideas Backlog
> Things we want to build eventually, but haven't scheduled yet.

- Highlight / annotation system (save specific passages with notes)
- Reading progress tracking (pause and resume)
- Export summary as PDF or Markdown
- Frontend UI (to be designed when backend is stable)

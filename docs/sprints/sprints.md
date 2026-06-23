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

## Sprint 1 — Persistence: Papers + Folders
**Status:** Draft
**Goal:** Save uploaded papers to PostgreSQL. Introduce the data model: papers, folders, and the relationship between them.

### Tentative deliverables
- SQLAlchemy models + Alembic migrations
- `papers` table (id, title, filename, raw text, summary, uploaded_at, folder_id)
- `folders` table (id, name, created_at)
- Updated upload endpoint — saves paper + summary after LLM call
- `GET /papers` — list all papers
- `GET /papers/{id}` — retrieve a single paper with its summary
- `GET /folders` — list folders
- `POST /folders` — create a folder
- `PUT /papers/{id}/folder` — move paper to a folder

---

## Sprint 2 — Structured Extraction
**Status:** Draft
**Goal:** Instead of a free-text summary, extract structured information from the paper using Pydantic + Gemini's structured output.

### Tentative deliverables
- Define a Pydantic schema: objective, methodology, data used, conclusions, limitations
- Update LLM call to return structured JSON
- Store structured fields in the database
- `GET /papers/{id}/extraction` endpoint

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

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
**Status:** In Progress
**Goal:** Given a paper already in the database, generate a set of critical question+answer pairs — like a peer reviewer would ask. Displayed as cards in the frontend: click to reveal the answer.

### Decisions
- Questions **are saved** to the database — so the user can come back and review them without re-calling the LLM
- If questions already exist for a paper, return them from DB (no redundant API call)
- LLM generates both the question and the answer in one call
- Format: list of `{question, answer}` pairs

### Deliverables
- [ ] `paper_questions` table — `question_id`, `paper_id`, `question`, `answer`
- [ ] Alembic migration for the new table
- [ ] `PaperQuestion` Pydantic schema — `question: str`, `answer: str` + `PaperQuestions` with `questions: List[PaperQuestion]`
- [ ] `generate_questions(text: str) -> PaperQuestions` in `services/ai.py`
- [ ] Peer reviewer prompt — crafted and iterated until output is genuinely useful
- [ ] `questions` repository — save and retrieve questions for a paper
- [ ] `POST /papers/{paper_id}/questions` — generates, saves, and returns questions (skips LLM if already saved)
- [ ] `GET /papers/{paper_id}/questions` — returns saved questions for a paper

---

## Sprint 4 — Semantic Search
**Status:** Draft
**Goal:** Embed papers using OpenAI `text-embedding-3-small`, store vectors in ChromaDB, enable semantic search across uploaded papers. Migrate from Gemini to OpenAI starting here.

### Deliverables
- [ ] Switch AI provider from Gemini to OpenAI (`openai` SDK, update `.env`)
- [ ] Chunking strategy — split `paper_content` into overlapping chunks before embedding
- [ ] Generate embeddings for each chunk using `text-embedding-3-small`
- [ ] ChromaDB setup — local persistent vector store
- [ ] Store embeddings on paper upload (extend `POST /papers/uploadfile/`)
- [ ] `GET /papers/search?q=...` endpoint — embeds the query, retrieves top-k similar chunks, returns matching papers

---

## Sprint 5 — RAG Chat
**Status:** Draft
**Goal:** Chat with a specific paper using Retrieval-Augmented Generation. Questions are answered using content retrieved from the paper, not from the model's memory.

### Deliverables
- [ ] Chunked retrieval — given a user question, find the most relevant chunks of a specific paper from ChromaDB
- [ ] Context assembly — combine retrieved chunks into a prompt context window
- [ ] `POST /papers/{paper_id}/chat` endpoint — accepts `{"message": "..."}`, returns `{"answer": "..."}`
- [ ] Conversation history — keep track of the chat turns within a session (in-memory or simple DB table)
- [ ] Grounding rule in prompt — model must only answer from retrieved context, not hallucinate

---

## Ideas Backlog
> Things we want to build eventually, but haven't scheduled yet.

- Highlight / annotation system (save specific passages with notes)
- Reading progress tracking (pause and resume)
- Export summary as PDF or Markdown
- Frontend UI (to be designed when backend is stable)

# Learnings

Personal notes on concepts learned while building this project.

---

## Git

### Conventional Commits
Format: `type(scope): message` — scope is optional.

| type | when to use |
|------|-------------|
| `feat` | new feature |
| `fix` | bug fix |
| `docs` | documentation only |
| `chore` | setup, config, tooling |
| `refactor` | restructure without changing behavior |
| `style` | formatting, no logic change |

```
chore: add .gitignore for python and node
docs: add sprint planning
feat(backend): add PDF upload endpoint
feat(frontend): scaffold React app
```

---

## Logging

### loguru — log levels and when to use each

```python
from loguru import logger
```

| level | when to use |
|-------|-------------|
| `logger.debug()` | Internal details — variable values, sizes, flow tracing. Only useful during development. |
| `logger.info()` | Normal operations — request received, paper saved, API call made. |
| `logger.warning()` | Unexpected but recoverable — duplicate upload, empty PDF, missing field. |
| `logger.error()` | Something failed — API error, DB error, parse failure. |

**Rule:** log where something *happens*, not in every layer that calls it. If the AI service logs the Gemini call, the router doesn't need to repeat it.

```python
logger.info("Upload request: filename={}, user_id={}", filename, user_id)
logger.warning("Duplicate upload detected: hash={}", content_hash)
logger.error("Failed to parse Gemini response: {}", e)
```

Use `{}` placeholders instead of f-strings — loguru only formats the string if the log level is active, which is more efficient.

---

## HTTP & APIs

### Content-Type and multipart/form-data
Regular JSON (`Content-Type: application/json`) is pure text. But a PDF is **binary data**: raw bytes that don't map to readable text and can't be embedded in JSON cleanly.

`multipart/form-data` is an HTTP encoding that splits the request body into named "parts", each with its own mini-headers. One part can be a text field, another can be a binary file. This is what browsers use automatically when you submit an `<input type="file">` form.

**Rule of thumb:** JSON for data, `multipart/form-data` for files.

### UploadFile in FastAPI
FastAPI's `UploadFile` unwraps the multipart request for you. Key attributes:
- `file.filename` — original filename sent by the client
- `file.content_type` — MIME type (e.g. `application/pdf`) — useful for validation
- `file.file` — the underlying file-like object (SpooledTemporaryFile)
- `await file.read()` — async way to read all bytes into memory

You don't need to save the file to disk to process it. Just read the bytes and pass them to whatever library needs them (e.g. PyMuPDF for text extraction).

---


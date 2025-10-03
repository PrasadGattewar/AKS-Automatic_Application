# Document Type Detector

A minimal FastAPI application that lets you upload a file and returns a human-friendly document type. Detection is based primarily on file extension with a fallback to content (magic bytes) heuristics and a plain-text guess.

## Features
- Web form UI for quick manual testing
- JSON API endpoint (`POST /api/detect`)
- Extension to description mapping for common document, archive, image and config file types
- Basic magic-bytes detection via the `filetype` library
- Plain UTF-8 text heuristic fallback
- Simple tests for detector logic
- Container-ready with a lightweight Dockerfile

## Tech Stack
- Python 3.11+ (works with 3.9+ as well)
- FastAPI
- Uvicorn
- Jinja2 templates
- filetype library
- Pytest for tests

## Project Layout
```
requirements.txt
src/
  app/
    main.py          # FastAPI app & routes
    detect.py        # Detection utilities
    templates/
      index.html     # Simple upload form
Dockerfile           # Container build recipe
.dockerignore        # Exclusions for smaller image
tests/
  test_detect.py     # Unit tests for detection logic
```

## Installation (Local)
Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

## Running the App (Local)
```bash
uvicorn src.app.main:app --reload --port 8000
```
Open: http://127.0.0.1:8000

## Running with Docker
Build the image:
```bash
docker build -t doc-type-detector:latest .
```
Run the container:
```bash
docker run --rm -p 8000:8000 doc-type-detector:latest
```
(Then open http://127.0.0.1:8000 )

Add a tag for a registry (example):
```bash
docker tag doc-type-detector:latest your-dockerhub-user/doc-type-detector:1.0.0
```

Push it:
```bash
docker push your-dockerhub-user/doc-type-detector:1.0.0
```

## API Usage
`POST /api/detect` with multipart form-data, field name `file`.

Sample (with `curl`):
```bash
curl -F "file=@example.pdf" http://127.0.0.1:8000/api/detect
```

Response:
```json
{
  "filename": "example.pdf",
  "detected_type": "PDF Document",
  "method": "extension match (.pdf)"
}
```

## Tests
```bash
pytest -q
```

## Production Notes
- Dockerfile uses `python:3.12-slim` and runs as non-root user `appuser`.
- Healthcheck probes `/healthz` every 30s.
- Consider multi-stage builds if you later add build-time tooling.
- You can pin dependency versions more strictly for reproducibility.

## Limitations / Future Ideas
- Magic bytes coverage is intentionally minimal (delegated to `filetype` package).
- Could enrich with MIME type to friendly name mapping for more binary formats.
- Add size / security checks (max upload size, reject executables, etc.).
- Add CI pipeline for building & scanning container images.

## License
MIT (add a LICENSE file if you need explicit text).

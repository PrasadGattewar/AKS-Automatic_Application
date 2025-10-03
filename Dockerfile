# syntax=docker/dockerfile:1.7
# Lightweight production image for FastAPI app
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_HOME=/app

WORKDIR $APP_HOME

# System deps (if any future need: build-essential, libmagic, etc.) kept minimal
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies separately to leverage layer caching
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application source
COPY src ./src

# (Optional) copy templates only if outside src structure
# COPY src/app/templates ./src/app/templates

# Create non-root user
RUN useradd -u 10001 -m appuser
USER appuser

EXPOSE 8000

# Healthcheck (basic) hitting the health endpoint
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -f http://127.0.0.1:8000/healthz || exit 1

# Start uvicorn
CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

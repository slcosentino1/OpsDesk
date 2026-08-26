# OpsDesk

Internal support agent built with LangGraph. It answers employee questions using tools: document search, ticket lookup/create, and (later) policy lookup.

OpsDesk does **not** embed or copy AskDoc. AskDoc is a separate RAG service (FastAPI + Celery + pgvector). OpsDesk calls it over HTTP for retrieval only (`POST /api/askdoc/search-matches`). The agent, not AskDoc, writes the final answer — do not call AskDoc `/query` from the agent (that would run a second LLM).

## Status

Scaffold only: settings + AskDoc HTTP client. LangGraph, tools, and evaluation are not implemented yet.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

`.env` is gitignored. The only setting today is `OPSDESK_ASKDOC_BASE_URL` (default `http://127.0.0.1:8000`). Settings also work without a file.

## Tests

```bash
pytest
```

## Run (later)

The agent loop is not wired yet. After the graph exists, this README will document how to start it. AskDoc must already be running and ingesting documents via `POST /api/askdoc/documents` (outside the agent loop).

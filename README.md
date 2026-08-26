# OpsDesk

Internal support agent built with LangGraph. It answers employee questions using tools: document search, ticket lookup/create, and (later) policy lookup.

OpsDesk does **not** embed or copy AskDoc. AskDoc is a separate RAG service (FastAPI + Celery + pgvector). OpsDesk calls it over HTTP for retrieval only (`POST /api/askdoc/search-matches`). The agent, not AskDoc, writes the final answer — do not call AskDoc `/query` from the agent (that would run a second LLM).

## Status

Minimal ReAct graph with one tool: `search_docs` (AskDoc retrieval). Tickets and evaluation are not implemented yet.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Defaults assume AskDoc on `http://127.0.0.1:8000` and an OpenAI-compatible LLM (Ollama) on `http://localhost:11434/v1`.

AskDoc must already be running, with documents ingested via `POST /api/askdoc/documents` (outside the agent loop).

## Tests

```bash
pytest
```

## Run

```bash
python -m opsdesk "How do I reset the VPN?"
```

# ConvoMate AI

ConvoMate AI is a full-stack conversation assistant for understanding a conversation, writing a natural reply, continuing a discussion, brainstorming topics, and asking general communication questions.

## What works

The app includes a responsive dashboard, conversation onboarding, editable context, contextual reply/message generation, next-topic generation, independent advice chat, copy feedback, saved drafts, conversation history, tone controls, local persistence, request validation, rate limiting, prompt-injection-aware system prompts, and a LangGraph workflow. When `OPENAI_API_KEY` is available, the backend uses `langchain-openai`; without one, it uses a clearly bounded deterministic fallback so the demo remains runnable.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
npm install
npm run build
uvicorn backend.app.main:app --host 0.0.0.0 --port 3000
```

Open `http://localhost:3000`. For frontend-only iteration use `npm run dev`, which proxies `/api` to port 3000. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` for real model calls. The backend never sends secrets to the browser.

## Tests

```bash
pytest backend/tests
npm test
```

## API

The versioned API lives under `/api/v1`: sessions (`POST/GET/PATCH/DELETE`), `POST /chat/reply`, `POST /chat/message`, `POST /chat/next-topic`, `POST /chat/ask`, `POST /chat/revise`, and `GET /drafts`. `GET /health` is unauthenticated and suitable for container health checks.

## Persistence and deployment

Local development uses SQLite through a small store adapter. `migrations/001_initial.sql` defines the PostgreSQL/Supabase-compatible tables and indexes for profiles, sessions, messages, drafts, and preferences. In production, replace the adapter with SQLAlchemy/Postgres or Supabase and enforce RLS policies binding `auth.uid()` to `user_id`; anonymous ownership should use a server-issued session token. LangSmith tracing can be enabled with the documented environment variables without logging message contents.

The Dockerfile builds the Vite frontend and runs FastAPI on `PORT` (default `3000`). Drafts are suggestions only: ConvoMate never sends a message automatically.

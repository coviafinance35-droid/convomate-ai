# ConvoMate AI — implementation plan

## Approach

Build a production-oriented full-stack monorepo with a Vite + React + TypeScript frontend and a FastAPI backend. The frontend owns the responsive conversation workspace and navigation; the backend owns validation, persistence, rate limiting, model calls, prompt safety, and LangChain/LangGraph orchestration. The application uses an OpenAI-compatible model when `OPENAI_API_KEY` is configured and a deterministic, clearly labeled fallback for local development and demos.

The request flow is intentionally simple: create or update a session, send a typed generation request to a focused endpoint, persist the result as a draft/message, and render structured output. LangGraph provides a typed state graph with routing between reply, message, next-topic, and general-advice nodes. Pasted conversation text is wrapped as untrusted user data and never treated as instructions.

## Design direction

- **Design movement:** editorial SaaS / quiet luxury productivity tool.
- **Core principles:** calm over noisy, conversational over form-like, progressive disclosure, always review before sending.
- **Color philosophy:** warm paper neutrals reduce emotional friction; ink navy provides trust; violet-indigo is the ownable signal for “thoughtful assistance”; mint is reserved for healthy progress and success.
- **Layout paradigm:** a persistent left rail paired with an asymmetric workspace: compact context rail on the left, generous working canvas in the middle, and a slim guidance rail that appears only when it adds value.
- **Signature elements:** soft violet orb brand mark, “conversation pulse” eyebrow labels, and message cards with a subtle left-edge accent that communicates tone.
- **Interaction philosophy:** every AI action is explicit, reversible, and user-owned. Actions use direct labels, visible loading states, and inline edits rather than modal interruptions.
- **Animation:** 160–220ms ease-out transitions, card lift on hover, shimmer only for loading states, and reduced-motion support.
- **Typography:** Inter for interface copy with Fraunces italic for short editorial emphasis; hierarchy uses large, high-contrast headlines and compact uppercase metadata.
- **Brand essence:** a calm co-pilot for better conversations; thoughtful, practical, human.
- **Brand voice:** warm, clear, never overconfident. Example lines: “Let’s find the natural next step.” / “A draft is a starting point, not a script.”
- **Wordmark / logo:** a violet orbit around a small speech-tail cutout; the mark becomes the sidebar “pulse” icon.
- **Signature brand color:** `#6D5CE7` electric iris.

## Product scope

1. Dashboard shell with Dashboard, Message Builder, Ask AI Anything, Saved Drafts, Conversation History, and Settings views.
2. Conversation summary onboarding and editable context.
3. Message generation, reply generation, next-topic suggestions, revise/tone actions, copy feedback, and saved drafts.
4. Independent general AI chat with starter prompts and contextual follow-up.
5. FastAPI endpoints under `/api/v1`, health endpoint, request validation, bounded input lengths, simple per-IP rate limiting, and safe fallbacks.
6. Persistence with SQLite locally and a PostgreSQL-compatible schema/migration; ownership-aware session shape ready for auth integration.
7. Separate backend prompt modules and typed LangGraph state.
8. Unit and smoke tests plus setup/deployment documentation.

## Project structure

- `frontend/`: Vite app, `src/App.tsx`, `src/styles.css`, route-like view state, API client, typed UI components.
- `backend/app/main.py`: FastAPI app, routes, CORS, static serving, health check.
- `backend/app/agents/`: LangChain model factory and LangGraph workflow nodes.
- `backend/app/prompts/`: version-controlled system prompts.
- `backend/app/schemas.py`: Pydantic request/response contracts.
- `backend/app/store.py`: SQLite persistence with PostgreSQL-ready schema semantics.
- `backend/tests/`: deterministic API tests.
- `migrations/`: SQL schema for PostgreSQL/Supabase migration handoff.
- `public/manus-routes.json`: route manifest for the managed preview.

## Build and delivery workflow

1. Install Python and frontend dependencies from lockable manifests.
2. Run frontend checks/build and backend tests.
3. Run FastAPI on `0.0.0.0:3000`; it serves the built frontend and `/api/v1`.
4. Verify `/health`, `/manus-routes.json`, and the main workspace response.
5. Commit the working tree, create the requested public GitHub repository, push `main`, and keep secrets in `.env` only.
6. Configure managed deployment to build the frontend and run the backend container with `/health` as its health path.

## Known implementation boundary

Supabase Auth, LangSmith tracing, and PostgreSQL RLS are represented through environment hooks, schema/migration SQL, and ownership-aware APIs; the local app remains runnable without those external credentials. The frontend never receives model or database secrets.

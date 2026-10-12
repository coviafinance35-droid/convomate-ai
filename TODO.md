# ConvoMate AI outcomes

- [ ] The user can submit a conversation summary with optional relationship, goal, and tone context; the validated context is stored in the active session and shown in the workspace.
- [ ] The user can paste an incoming message and receive one best suggested reply plus meaningful alternatives grounded in the summary, latest message, relationship context, goal, tone, and recent session history.
- [ ] The user can generate an outgoing message from an intention using the existing conversation context.
- [ ] The user can generate a context-aware next topic with a suggested message, rationale, optional follow-up question, and alternative topic.
- [ ] The user can ask general questions in an independent AI chat without unnecessary message generation or forced relationship framing.
- [ ] Gift, relationship, communication, brainstorming, planning, writing, and unrelated general questions receive direct, balanced advice when appropriate.
- [ ] The user can copy, edit, regenerate, shorten, lengthen, make more natural, and change the tone of generated drafts; drafts are never sent automatically.
- [ ] Conversation state persists according to the selected storage and retention model, with local SQLite persistence and PostgreSQL-compatible migrations.
- [ ] User data is validated, ownership-aware, rate-limited, protected from prompt injection, and never exposes model/database secrets to the frontend.
- [ ] The responsive interface is polished, accessible, keyboard-friendly, and usable on mobile and desktop.
- [ ] Backend tests and frontend checks cover the main user journeys, safe fallbacks, invalid model outputs, timeouts, and unauthorized access shapes.
- [ ] Setup, environment, database migration, local development, testing, and deployment instructions are complete.

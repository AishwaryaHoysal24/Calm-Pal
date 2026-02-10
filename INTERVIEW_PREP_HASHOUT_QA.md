# Hashout Technologies Associate SDE Interview — Detailed Answer Bank

This file provides **detailed, interview-ready answers** for every question listed in `INTERVIEW_PREP_HASHOUT.md`.
Use these as templates and customize with your exact stack (e.g., Node/Express, Python/FastAPI, React, etc.).

---

## 1) Project Pitch & Fundamentals

### 1. Tell me about your project in 60–90 seconds.
**Answer:**
I built a conversational AI assistant using the Gemini API focused on safe, stable, and privacy-aware interactions. The frontend handles user chat input/output, while the backend manages intent routing, lightweight session context, and guarded LLM calls. I used NLP-based routing to direct user prompts through specialized paths, which improved response consistency and emotional alignment. A key design decision was non-persistent conversation handling by default to minimize privacy risk. I also added functional tests and structured debugging practices to validate behavior under normal, edge, and API-failure scenarios.

### 2. What problem does your conversational agent solve?
**Answer:**
It provides fast, context-aware conversational support while balancing user safety and privacy. Many bots either over-store data or produce unstable responses; this project addresses both by using modular routing and limited session state to keep interactions focused without storing long-term sensitive history.

### 3. Why did you choose Gemini API over other LLM providers?
**Answer:**
I chose Gemini for strong multimodal and conversational quality, good API ergonomics, and reliable latency for my prototype constraints. The selection was practical: response quality, integration speed, developer tooling, and cost-performance balance for rapid experimentation.

### 4. What do you mean by “ethical, non-persistent LLM interaction”?
**Answer:**
Ethical means adding safeguards: prompt constraints, refusal patterns for harmful asks, and escalation messaging for high-risk domains like medical/self-harm contexts. Non-persistent means avoiding default storage of raw chat content; only transient in-memory context is used per active session and discarded after timeout/end.

### 5. How is your architecture scalable?
**Answer:**
I separated concerns into independent modules (API layer, routing layer, session manager, LLM client). This allows horizontal scaling of stateless API servers while externalizing session state later (e.g., Redis) if needed. I also designed clear API contracts and failure handling so components can be scaled/replaced independently.

### 6. What were the core modules in your system?
**Answer:**
Core modules: UI client, backend REST API, request validator, intent router, session-state manager, Gemini service wrapper, and error/observability layer. This modular structure improves maintainability and testability.

### 7. Walk me through your request flow from user input to response.
**Answer:**
User sends message → frontend validates and calls backend `POST /chat` → backend authenticates/validates JSON → retrieves session context → routing module classifies intent → backend builds constrained prompt and calls Gemini → output safety checks + normalization → response returned to client with metadata (status, latency, safe fallback if needed).

### 8. What were your biggest technical challenges and how did you solve them?
**Answer:**
Main challenges: response inconsistency, context drift, and error handling for upstream API instability. I solved these by adding route-specific prompt templates, context windows with bounded memory, deterministic fallback prompts, timeout/retry strategies, and stronger validation/logging.

### 9. What trade-offs did you make while building this project?
**Answer:**
I prioritized privacy and reliability over deep personalization. Non-persistent design reduces risk but limits long-term memory and recommendations. I also kept routing logic interpretable (hybrid rule + lightweight NLP) over complex heavy models for easier debugging at this stage.

### 10. If you had two more months, what would you improve first?
**Answer:**
I’d add robust observability dashboards, automated regression tests for prompt/routing outputs, configurable policy engine for safety, and Redis-backed sessions with explicit user-consent controls.

---

## 2) Client–Server & Web Architecture

### 1. Explain your project using the client–server model.
**Answer:**
Client handles interaction and rendering; server handles business logic, routing, LLM invocation, safety checks, and secret management. This separation improves security and maintainability.

### 2. What parts run on client vs server?
**Answer:**
Client: UI state, input handling, loading/error states. Server: authentication, validation, routing, session lifecycle, API key use, model call orchestration, and response filtering.

### 3. Why should API keys never be exposed on frontend?
**Answer:**
Frontend code is inspectable. Exposed keys can be stolen and abused, causing quota exhaustion, billing risk, and data leakage. Server-side key handling enables strict access control and rotation.

### 4. How does frontend communicate with backend endpoints?
**Answer:**
Via HTTPS JSON APIs using `fetch/axios`. Requests include body, headers, session token/cookie, and receive structured JSON with success/error metadata.

### 5. How do you handle CORS?
**Answer:**
Configured backend CORS allowlist for trusted origins, controlled methods/headers, and credentials settings as needed. In production, CORS policy is strict per environment.

### 6. What happens from click “Send” to reply display?
**Answer:**
Input validation → UI shows loading → async POST call → backend processing + model call → receives response/error → UI updates chat and hides loading; if failure, displays graceful fallback.

### 7. How do you make system resilient to network failures?
**Answer:**
Timeouts, bounded retries with backoff, idempotent-safe retry conditions, circuit-breaker style fallback messaging, and clear user-visible retry options.

### 8. Stateless vs stateful communication in your app?
**Answer:**
HTTP endpoints are mostly stateless, but conversational context is stateful per session. Session state is intentionally minimal and short-lived.

### 9. Did you use REST APIs? Why?
**Answer:**
Yes. REST with JSON is simple, widely compatible, and ideal for junior-team collaboration and clear contracts.

### 10. Architecture change for 100x traffic?
**Answer:**
Add load balancer, autoscaling app instances, external session store, request queue for spikes, rate limiting, caching for safe repeated content, and distributed tracing.

---

## 3) API, JSON, HTTP

### 1. Explain API contract for chat endpoint.
**Answer:**
`POST /chat` expects `{sessionId, message, metadata?}` and returns `{reply, route, safetyFlags, requestId, latencyMs}` or structured error object.

### 2. Request JSON format?
**Answer:**
Required fields: `sessionId` (string), `message` (non-empty string). Optional fields: locale, channel, userPreferences.

### 3. Response JSON format?
**Answer:**
`success: true`, `data: {reply, route, confidence, timestamp}` and optional `warnings`. For failures: `success: false`, `error: {code, message}`.

### 4. Why POST for chat?
**Answer:**
Chat input can be sensitive/large and changes server-side context. POST keeps payload in request body and semantically fits non-idempotent operations.

### 5. When is GET suitable?
**Answer:**
For safe retrievals: health checks, model metadata, route config version, non-sensitive static settings.

### 6. Validation for incoming JSON?
**Answer:**
Schema validation (type, min/max length, sanitization, required fields) with immediate 400 responses for invalid payloads.

### 7. Status codes used?
**Answer:**
200 success, 400 validation error, 401/403 auth errors, 429 rate-limit, 500 internal, 502/503 upstream dependency issues.

### 8. Useful errors without exposing internals?
**Answer:**
Return stable public error codes/messages; log full internal stack separately with correlation IDs.

### 9. API versioning?
**Answer:**
Path-based (`/v1/chat`) or header-based. I prefer path versioning for clarity in junior teams.

### 10. Idempotency?
**Answer:**
Idempotent means repeated calls produce same state impact. GET endpoints usually idempotent; chat POST typically not, unless guarded with idempotency key.

---

## 4) Async/Await & Concurrency

### 1. Where async/await used?
**Answer:**
Frontend API calls and backend LLM/network operations; also DB/cache access if introduced.

### 2. What if you forget await?
**Answer:**
You get unresolved Promise objects, race bugs, wrong UI state updates, and hidden unhandled rejections.

### 3. Timeout handling for Gemini API?
**Answer:**
Use request timeout wrapper; on expiry, return graceful fallback and optionally queue telemetry for later analysis.

### 4. Prevent UI freeze?
**Answer:**
All network calls async, with loading indicators and non-blocking render flow.

### 5. Loading states importance?
**Answer:**
They improve UX by signaling progress and preventing duplicate submissions.

### 6. Rapid user messages/race conditions?
**Answer:**
Use sequence IDs, disable send while pending (or queue), and ignore stale responses.

### 7. Promise chaining vs async/await?
**Answer:**
Both represent async flow; async/await is generally more readable and easier for structured try/finally cleanup.

### 8. Safe retries?
**Answer:**
Retry only transient errors (timeouts/5xx), capped attempts, exponential backoff + jitter.

### 9. Cancel in-flight requests?
**Answer:**
Use AbortController/cancellation tokens when user edits context or navigates away.

### 10. Parallel processing?
**Answer:**
Use `Promise.all` for independent operations and `Promise.allSettled` when partial failure is acceptable.

---

## 5) NLP Routing & Response Stability

### 1. Meaning of NLP-based routing?
**Answer:**
A preprocessing step classifies user intent/sentiment and routes prompt to specialized handling path.

### 2. Intent classification approach?
**Answer:**
Keyword + embedding/semantic cues (or lightweight classifier), with confidence threshold and fallback route.

### 3. Rule-based, ML-based, or hybrid?
**Answer:**
Hybrid: deterministic rules for safety-critical intents, ML/NLP signals for broader flexibility.

### 4. Low confidence fallback?
**Answer:**
Ask clarifying question or route to safe-general assistant template.

### 5. Reduce hallucinations?
**Answer:**
Constrained prompts, role boundaries, explicit refusal conditions, and response post-checking.

### 6. Prompt strategies for stability?
**Answer:**
Fixed response format, system instructions, bounded context, and route-specific examples.

### 7. Evaluate emotional accuracy?
**Answer:**
Human review rubric + scenario test sets, measuring tone appropriateness and harmfulness avoidance.

### 8. Edge cases that broke routing?
**Answer:**
Sarcasm, mixed intents in one message, code-switched language, and very short ambiguous text.

### 9. Prevent unsafe/irrelevant responses?
**Answer:**
Safety classifier checks, policy prompts, refusal templates, and domain escalation messaging.

### 10. Handle ambiguous inputs?
**Answer:**
Return concise clarifying prompts before taking domain-specific action.

---

## 6) Session Management & State Design

### 1. Modular session states?
**Answer:**
Separate session concerns: identity metadata, short context buffer, routing hints, and cooldown/error state.

### 2. Track context without persistence?
**Answer:**
Use in-memory per-session buffer with TTL and strict size limits.

### 3. Data stored per session?
**Answer:**
Session ID, last N turns, active route, timestamps, and minimal flags—no sensitive long-term fields by default.

### 4. Reset/expire state?
**Answer:**
TTL expiry, manual reset endpoint, and session invalidation on inactivity.

### 5. Risks of too much in-memory history?
**Answer:**
Memory pressure, latency increase, privacy exposure, and context confusion.

### 6. Prevent cross-user leakage?
**Answer:**
Strict session-key scoping, isolation tests, and no shared mutable state without partition keys.

### 7. App restart effect?
**Answer:**
In-memory sessions are lost by design; user receives fresh session unless external store is used.

### 8. Maintainability of state modules?
**Answer:**
Clear interfaces: `getContext`, `appendTurn`, `resetSession`, `expireSession`, with dedicated tests.

### 9. Test state transitions?
**Answer:**
Unit tests for transitions and integration tests simulating realistic chat flows.

### 10. Migration to Redis?
**Answer:**
Replace in-memory adapter with Redis-backed repository implementing same interface.

---

## 7) Privacy, Security, Ethical AI

### 1. Privacy-centric architecture practically?
**Answer:**
Data minimization, short retention, redaction, consent-aware processing, and separation of PII from operational logs.

### 2. What collect vs avoid?
**Answer:**
Collect minimal operational metadata (timestamps, error codes). Avoid storing raw sensitive prompts by default.

### 3. Store transcripts?
**Answer:**
Not by default. If enabled, only with explicit consent and retention policy.

### 4. PII in prompts/logs?
**Answer:**
Pre-send redaction and post-receive log scrubbing with regex + allowlist strategy.

### 5. Logging redaction strategy?
**Answer:**
Mask email/phone/IDs, hash user identifiers, and remove high-risk tokens before persistence.

### 6. Secure secrets/API keys?
**Answer:**
Environment secrets manager, server-side usage only, rotation policy, and no hardcoding.

### 7. Ethical safeguards?
**Answer:**
Policy prompts, harmful-content detection, refusal guidance, and crisis-response redirection text.

### 8. Harmful/self-harm/medical-risk prompts?
**Answer:**
Do not provide dangerous instructions; provide empathetic, safety-focused response and recommend professional help.

### 9. Future healthcare compliance?
**Answer:**
Consent workflow, audit trails, encryption at rest/in transit, role-based access, and regulatory mapping (e.g., HIPAA-like controls where relevant).

### 10. Privacy vs security?
**Answer:**
Privacy = what data is collected/used. Security = how protected against unauthorized access/abuse.

---

## 8) Testing, Debugging, Reliability

### 1. What testing performed?
**Answer:**
Unit tests for helpers/routing/state, integration tests for API flow, and manual scenario testing for UX/safety prompts.

### 2. Hardest module to test?
**Answer:**
Routing + tone stability, because natural language edge cases are broad and non-deterministic.

### 3. One bug and fix example.
**Answer:**
Bug: stale async response overwrote newer message in UI. Fix: request IDs and ignore outdated responses.

### 4. Reproduce intermittent failures?
**Answer:**
Added request correlation IDs, replayed payloads, and introduced controlled latency simulation.

### 5. Reliability metrics?
**Answer:**
P95 latency, error rate, timeout rate, safe-fallback rate, and successful response ratio.

### 6. Test API failure scenarios?
**Answer:**
Mock upstream 429/500/timeouts and verify fallback handling plus user-visible error messaging.

### 7. Validate emotional response behavior?
**Answer:**
Scenario matrix with expected tone categories; human review for appropriateness/safety.

### 8. Debugging tools?
**Answer:**
Structured logs, Postman/curl, browser network tab, and server tracing with correlation IDs.

### 9. Prevent regressions for prompts/routing?
**Answer:**
Golden test cases + CI checks + route config versioning.

### 10. Basic test plan?
**Answer:**
Define critical flows, edge cases, failure injection, acceptance criteria, and repeatable regression suite.

---

## 9) OOP & Clean Code

### 1. OOP principles applied?
**Answer:**
Encapsulation in service classes, abstraction through interfaces, and polymorphic route handlers.

### 2. Example abstraction benefit?
**Answer:**
`LLMService` interface allows provider swap (Gemini/mock) without changing business logic.

### 3. Separation of concerns?
**Answer:**
Routing logic separate from transport/API controller and separate from session storage.

### 4. Maintainable code practices?
**Answer:**
Small functions, explicit naming, single responsibility, and shared utility modules.

### 5. Naming/folder conventions?
**Answer:**
Feature-based folders (`routes`, `services`, `models`, `utils`, `tests`) and consistent verb-noun naming.

### 6. Avoid god classes/coupling?
**Answer:**
Composition over monoliths; dependency injection for test-friendly module boundaries.

### 7. Refactor that improved quality?
**Answer:**
Extracted routing decisions from controller to dedicated router service with unit tests.

### 8. Interfaces/contracts in testing?
**Answer:**
Mocks/stubs can replace concrete implementations cleanly.

### 9. Dependency injection usage?
**Answer:**
Injected LLM client and session repository into chat service.

### 10. Coding standards followed?
**Answer:**
Linting, formatting, naming conventions, and PR review checklists.

---

## 10) Arrays, Strings, Core Programming

### 1. Sanitize user string before API?
**Answer:**
Trim whitespace, normalize unicode, remove control chars, enforce length bounds, and redact obvious PII patterns.

### 2. Tokenize/split for routing?
**Answer:**
Lowercase normalize → tokenize by whitespace/punctuation → optional stemming/keywords map.

### 3. Detect repeated messages in array?
**Answer:**
Hash normalized strings and track in a `Set/Map`; compare recent N entries.

### 4. Top N frequent intents?
**Answer:**
Frequency map + min-heap or sort map entries by count descending.

### 5. Reverse words not chars?
**Answer:**
Split by spaces, reverse token array, join with single spaces.

### 6. Merge two sorted arrays efficiently?
**Answer:**
Two-pointer O(n+m) merge.

### 7. Complexity of routing preprocessing?
**Answer:**
Usually O(n) in input length for normalization/token checks.

### 8. Remove duplicates preserve order?
**Answer:**
Iterate once; append unseen elements tracked by set.

### 9. Near-match/fuzzy intent compare?
**Answer:**
Levenshtein/Jaro similarity plus keyword overlap thresholds.

### 10. Handle unicode/emojis safely?
**Answer:**
Use unicode-aware string libraries and avoid byte-length assumptions.

---

## 11) SQL & Relational Basics

### 1. Why database needed in production chatbot?
**Answer:**
User accounts, consent records, analytics, rate-limits, and auditability need persistence.

### 2. Tables design?
**Answer:**
`users(id PK, email, created_at)`, `sessions(id PK, user_id FK, started_at, ended_at)`, `events(id PK, session_id FK, type, created_at)`.

### 3. Primary key importance?
**Answer:**
Unique row identity, indexing basis, integrity anchor.

### 4. Foreign key example?
**Answer:**
`sessions.user_id -> users.id` ensures sessions map to valid user.

### 5. SQL vs NoSQL for chat?
**Answer:**
SQL for strong relational integrity/reporting; NoSQL for flexible schema/high write scale. Often hybrid.

### 6. Query last 10 messages.
**Answer:**
`SELECT * FROM messages WHERE user_id=? ORDER BY created_at DESC LIMIT 10;`

### 7. Indexing strategy?
**Answer:**
Index common filters/sorts: `(user_id, created_at)` for recent-user retrieval.

### 8. JOIN usage?
**Answer:**
Use `INNER JOIN` for sessions with valid users; `LEFT JOIN` when optional relation should still return parent rows.

### 9. Transactions help?
**Answer:**
They guarantee atomic multi-step writes and consistency under failures.

### 10. Normalization vs denormalization?
**Answer:**
Normalize to reduce redundancy/update anomalies; denormalize selectively for read-heavy performance.

---

## 12) Git & Version Control

### 1. Git workflow?
**Answer:**
Feature branch → atomic commits → push → PR → review → merge.

### 2. Good commit message?
**Answer:**
Imperative, scoped, concise subject + optional body with why/impact.

### 3. Merge vs rebase?
**Answer:**
Merge preserves branch history; rebase creates linear history by replaying commits.

### 4. Resolve conflicts safely?
**Answer:**
Pull latest, inspect conflict markers carefully, run tests before finalizing.

### 5. Why code reviews?
**Answer:**
Catch bugs early, share knowledge, enforce standards.

### 6. `.gitignore` examples?
**Answer:**
Ignore secrets/env files, build artifacts, dependency dirs, IDE files.

### 7. Rollback bad commit?
**Answer:**
Use `git revert` for shared history; `reset` only when safe/local.

### 8. Checks before PR?
**Answer:**
Lint, tests, build, static checks, and manual sanity flow.

### 9. PR description structure?
**Answer:**
Problem, solution, impact, testing evidence, and risks.

### 10. Learning from reviews?
**Answer:**
I convert feedback into patterns/checklists and improve next commits proactively.

---

## 13) Behavioral + Collaboration

### 1. Critical feedback example?
**Answer:**
I once over-engineered an early module; feedback suggested simpler interfaces. I refactored into smaller services and improved review turnaround.

### 2. Estimate and deliver on time?
**Answer:**
Break tasks, estimate with buffers, prioritize dependencies, and update progress daily.

### 3. Requirement change mid-way?
**Answer:**
Reassessed scope, documented impact, aligned with mentor, then adjusted implementation in incremental milestones.

### 4. Communicate blockers?
**Answer:**
State issue, attempted fixes, logs/evidence, and what help is needed.

### 5. Debugging stuck story?
**Answer:**
I narrow issue with binary search-style isolation, add instrumentation, and request focused peer review when needed.

### 6. Learn new tool quickly?
**Answer:**
Official docs + small proof-of-concept + apply to current task immediately.

### 7. Quality vs speed?
**Answer:**
Protect non-negotiables (correctness/security), then optimize incremental delivery.

### 8. Team disagreement handling?
**Answer:**
I discuss trade-offs with data/prototypes and align on team objective, not personal preference.

### 9. Motivation for role?
**Answer:**
I want strong engineering fundamentals in a delivery-focused environment where I can build across stack under mentorship.

### 10. Why Hashout + Bengaluru?
**Answer:**
Hashout offers practical product engineering exposure, and Bengaluru provides high-growth ecosystem, mentorship, and cross-domain opportunities.

---

## 14) Deep Follow-ups on Resume Bullets

### A1. Scalability meaning here?
**Answer:**
Primarily latency consistency, concurrent session handling, and cost per request.

### A2. Token usage/cost monitoring?
**Answer:**
Track request counts, token estimates, and per-route usage telemetry with periodic cost dashboards.

### A3. Rate limiting implemented?
**Answer:**
Yes, basic per-user/session throttling to prevent abuse and quota spikes.

### A4. Cache safe repeated responses?
**Answer:**
Cache deterministic, non-sensitive FAQs with TTL and route scoping.

### A5. Multi-tenant support?
**Answer:**
Tenant ID scoping in auth, config, routing policies, and quotas.

### B1. No persistence but personalization?
**Answer:**
Short-session personalization via transient context and user-provided preferences in-session.

### B2. Audit harmful outputs without raw text?
**Answer:**
Store anonymized event labels and policy-trigger metadata, not full content.

### B3. Limitations of non-persistent design?
**Answer:**
Lower long-term personalization and weaker retrospective analytics.

### B4. Consent impact on retention?
**Answer:**
Retention strictly opt-in with clear policy, expiry windows, and revocation path.

### B5. Legal deletion requests?
**Answer:**
If persisted data exists, maintain indexed delete workflow and deletion audit trail.

### C1. Concrete route mapping example?
**Answer:**
“Feeling anxious” → emotional-support route; “What is HTTP GET?” → technical-learning route.

### C2. Confidence threshold and why?
**Answer:**
Example 0.70 to balance false positives/negatives; tuned via validation scenarios.

### C3. Routing with context?
**Answer:**
Current session topic biases route selection when new message is short/ambiguous.

### C4. Test false positives/negatives?
**Answer:**
Confusion-matrix style test set across intents and boundary phrases.

### C5. Evolve routes as intents grow?
**Answer:**
Version route taxonomy, monitor misroutes, and incrementally add route handlers.

### D1. Tests catching severe issues?
**Answer:**
Integration tests for session isolation and timeout fallback caught highest-risk bugs.

### D2. Baseline vs improved latency?
**Answer:**
Discuss as relative improvement if exact numbers unavailable (e.g., optimized prompt/context reduced p95).

### D3. Benchmark reliability?
**Answer:**
Run repeated scenario suites under simulated failures and compare pass/fallback rates.

### D4. Logs/dashboards used?
**Answer:**
Structured logs with correlation IDs and simple dashboards for latency/error trend.

### D5. Bug fix completion criteria?
**Answer:**
Repro eliminated, regression tests added, peer-reviewed, and monitored post-release.

---

## 15) Live Coding / Whiteboard — How to Answer

### 1. Validate chat request JSON.
**Answer approach:**
Check JSON parse, required fields, type checks, trim, min/max length, reject unknown high-risk fields.

### 2. API skeleton for `POST /chat`.
**Answer approach:**
Validate → load session → route intent → call model with timeout → safety check → return structured JSON.

### 3. Latest user message from array.
**Answer approach:**
Traverse from end and return first item with role `user`.

### 4. Debounce typing.
**Answer approach:**
Use timer reset on keystroke; call API only after inactivity threshold.

### 5. Retry with backoff.
**Answer approach:**
Loop attempts with delay `base * 2^n + jitter`, retry transient failures only.

### 6. Longest common prefix.
**Answer approach:**
Start with first string prefix, shrink until all strings start with it.

### 7. Group logs by user ID.
**Answer approach:**
Hash map where key=userId and value=array of logs.

### 8. Safe JSON string check.
**Answer approach:**
Try parse, confirm object type and not array/null.

### 9. SessionManager class design.
**Answer approach:**
Methods: `create/get/append/reset/expire`; include TTL and max-context constraints.

### 10. SQL DAU query.
**Answer approach:**
`SELECT DATE(started_at) d, COUNT(DISTINCT user_id) dau FROM sessions GROUP BY d ORDER BY d;`

---

## 16) Smart Questions to Ask Interviewer

(These are already good; here is why each matters.)

1. 90-day success → clarifies expectations.
2. Stack details → helps align your preparation.
3. Mentorship style → indicates growth support.
4. Code review process → reveals quality culture.
5. Testing standards → defines engineering rigor.
6. API contract ownership → cross-team clarity.
7. Common junior incidents → realistic readiness.
8. Growth path → career planning.
9. Feedback model → performance transparency.
10. Learning resources → upskilling support.

---

## 17) 30-Second High-Impact Answer Templates (Enhanced)

### Architecture
“My chatbot follows a clean client–server architecture: frontend manages UX and async rendering, backend handles validation, intent routing, session context, safety policies, and Gemini API calls. This keeps secrets secure and makes modules independently testable and scalable.”

### GET vs POST
“I use POST for chat because prompts are sensitive, potentially large, and can affect conversational state. GET is reserved for read-only resources like health checks or metadata, where idempotency and caching are beneficial.”

### Async/Await
“I use async/await for readable non-blocking flows in both client and server. Around it, I add timeout, bounded retries, cancellation, and clear loading/error UX to keep the app reliable under real network conditions.”

### OOP
“I apply OOP to separate responsibilities: session manager, router, and LLM client wrappers. Encapsulation and interfaces made testing easier and allowed me to swap implementations without touching core business flow.”

### Privacy
“My design minimizes retained user data: transient session context by default, redacted logs, and server-only secret handling. That gives a practical privacy baseline while still supporting reliability and debugging.”

---

## 18) Final Revision Checklist — Model Responses

1. **2-minute flow?** Yes: UI input → API validation → routing → model call → safety filter → response.
2. **Tech trade-offs?** Yes: privacy and reliability over deep long-term personalization.
3. **GET/POST examples?** Yes: `POST /chat`, `GET /health`.
4. **Async snippet memory?** Practice one with timeout + try/catch + fallback.
5. **STAR bug story?** Prepare one race-condition fix story.
6. **PK/FK example?** `users.id` PK, `sessions.user_id` FK.
7. **Architecture drawing?** Client, API server, session store, LLM provider.
8. **Why role?** Learning + ownership + full-stack exposure.
9. **Improvement roadmap?** Observability, test automation, policy engine.
10. **Core refresh?** Arrays/strings, OOP, SQL joins, Git conflict handling.

---

## Bonus: Trap Questions — Strong Answers

### 1. If no persistence, is app stateful?
Yes, session-level stateful during active interaction; non-persistent means no long-term retention after session lifecycle.

### 2. Prove emotional accuracy objectively?
Use scenario-based rubric scoring (tone appropriateness, empathy, harm avoidance) with reviewer agreement metrics.

### 3. Why not call Gemini from frontend?
Security risk (key exposure), no policy enforcement layer, and weaker observability/control.

### 4. What if model gives unsafe medical advice?
Safety policy intercepts and returns non-diagnostic guidance plus professional help recommendation.

### 5. API quota exhaustion behavior?
Detect provider errors, return graceful message, degrade non-critical features, and alert maintainers.

### 6. If routing fails, fallback path?
Route to safe-general assistant + ask clarifying question before giving domain-specific answer.

### 7. Where race conditions can happen?
Concurrent sends, stale response overwrite, session updates without ordering guarantees.

### 8. What can go wrong with retries?
Duplicate operations, thundering herd, increased load/cost; solved via caps, jitter, and idempotency keys where needed.

### 9. Explain architecture to non-technical person.
“The chat screen sends your message to our secure server, which decides the best response path and asks the AI safely, then sends back a clear response quickly.”

### 10. Least confident area and fix plan?
“Large-scale load behavior; I’d run stress tests, add queueing and observability, and tune timeout/retry/rate-limit policies.”

---

## Practice Strategy (Recommended)

- Round 1: Read each Q and answer aloud from memory in 45–60 seconds.
- Round 2: Add one real example from your implementation.
- Round 3: Record yourself and reduce filler words.
- Round 4: Mock interview with a friend focusing on follow-up depth.

You now have complete coverage for the full question set plus model answers.

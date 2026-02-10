# Hashout Technologies (Associate SDE) Interview Prep — Project-Focused Question Bank

Use this as a rapid-fire preparation sheet for your project:
- **Project context (from resume):** Gemini-based conversational AI, NLP routing, modular session states, privacy-first architecture, testing/debugging.
- **Role context:** Junior full-stack foundations, debugging, API usage, async, OOP, SQL basics, Git.

---

## 1) Project Pitch & Fundamentals (Most Likely Opening Questions)

1. Tell me about your project in 60–90 seconds.
2. What problem does your conversational agent solve?
3. Why did you choose Gemini API over other LLM providers?
4. What do you mean by “ethical, non-persistent LLM interaction”?
5. How is your architecture scalable?
6. What were the core modules in your system?
7. Walk me through your request flow from user input to response.
8. What were your biggest technical challenges and how did you solve them?
9. What trade-offs did you make while building this project?
10. If you had two more months, what would you improve first?

---

## 2) Client–Server & Web Architecture

1. Explain your project using the client–server model.
2. What parts run on the client and what runs on the server?
3. Why should API keys never be exposed on the frontend?
4. How does your frontend communicate with backend endpoints?
5. How do you handle CORS in your application?
6. What happens from the moment a user clicks “Send” until they see a reply?
7. How do you make the system resilient to network failures?
8. What is stateless vs stateful communication? Which one does your app use and where?
9. Did you use REST APIs? Why or why not?
10. How would this architecture change if traffic increased 100x?

---

## 3) API, JSON, and HTTP (GET vs POST)

1. Explain the API contract for your chat endpoint.
2. What does the request JSON look like?
3. What does the response JSON look like?
4. Why did you use POST for chat instead of GET?
5. When would GET be suitable in your project?
6. How did you handle validation for incoming JSON?
7. What HTTP status codes does your API return for common cases?
8. How do you return useful error messages without exposing internals?
9. How do you version APIs?
10. What is idempotency? Which of your endpoints are idempotent?

---

## 4) Async/Await & Concurrency

1. Where did you use async/await in your project?
2. What happens if you forget `await` on an API call?
3. How do you handle timeouts while calling Gemini API?
4. How do you prevent UI freeze during long responses?
5. Did you implement loading states/spinners? Why are they important?
6. How do you handle multiple rapid user messages (race conditions)?
7. What is promise chaining vs async/await?
8. How do you retry transient failures safely?
9. How do you cancel in-flight requests?
10. How would you process multiple independent tasks in parallel?

---

## 5) NLP Routing & Response Stability

1. What does “NLP-based routing” mean in your implementation?
2. How do you classify user intent before routing?
3. Did you use rule-based, ML-based, or hybrid routing?
4. What fallback logic is used if intent confidence is low?
5. How did you reduce hallucinations or unstable responses?
6. What prompt engineering strategies improved stability?
7. How did you evaluate emotional accuracy?
8. What edge cases broke your routing logic?
9. How do you prevent unsafe or irrelevant responses?
10. How do you handle ambiguous inputs from users?

---

## 6) Session Management & State Design

1. What are “modular session states” in your project?
2. How do you track context without persistent storage?
3. What data did you keep in memory per session?
4. How do you reset/expire session state?
5. What are risks of storing too much chat history in memory?
6. How do you prevent context leakage across users?
7. If app restarts, what happens to active sessions?
8. How did you design state modules for maintainability?
9. How do you test state transition correctness?
10. How would you migrate to Redis/session store if needed?

---

## 7) Privacy, Security, and Ethical AI

1. Define “privacy-centric architecture” in practical terms.
2. What user data do you collect, and what do you avoid collecting?
3. Did you store chat transcripts? If not, why?
4. How do you handle PII in prompts and logs?
5. What are your logging redaction strategies?
6. How do you secure secrets and API keys?
7. What ethical safeguards are in place for sensitive queries?
8. How do you manage harmful/self-harm/medical-risk prompts?
9. How would you make this healthcare-compliant in future?
10. What is the difference between privacy and security in your project?

---

## 8) Testing, Debugging, and Reliability

1. What testing did you perform (unit/integration/manual)?
2. Which module was hardest to test and why?
3. Give one bug you found and fixed.
4. How did you reproduce intermittent failures?
5. What metrics indicate system reliability?
6. How do you test API failure scenarios?
7. How did you validate expected behavior for emotional responses?
8. What tools did you use for debugging requests and responses?
9. How do you prevent regressions when changing prompts/routing?
10. How would you design a basic test plan for this app?

---

## 9) OOP & Clean Code (JD Alignment)

1. Which OOP principles did you apply (encapsulation/inheritance/polymorphism/abstraction)?
2. Show one class/module where abstraction improved maintainability.
3. How did you separate concerns in your codebase?
4. How did you keep code readable and maintainable?
5. What naming conventions and folder structure did you follow?
6. How do you avoid “god classes” or overly coupled modules?
7. What refactor improved your code quality most?
8. How do interfaces/contracts help in testing?
9. Where did you use dependency injection or similar patterns?
10. What coding standards did you follow in team/project?

---

## 10) Arrays, Strings, and Core Programming Checks

1. How would you sanitize a user string before sending to API?
2. How do you tokenize or split user input for routing?
3. How would you detect repeated messages in an array of chats?
4. How would you find top N frequent intents from logs?
5. How do you reverse words in a sentence without reversing characters?
6. How would you merge two sorted arrays efficiently?
7. What is time complexity of your routing pre-processing?
8. How do you remove duplicates while preserving order?
9. How do you compare two strings for near-match/fuzzy intent?
10. How do you handle unicode/emojis safely?

---

## 11) SQL & Relational Database Basics

Even if your current design is non-persistent, expect basics:

1. Why might you still need a database in production chatbot systems?
2. What tables would you design for users, sessions, and audit events?
3. What is a primary key? Why is it important?
4. What is a foreign key? Give an example from your project domain.
5. Difference between SQL and NoSQL for chat applications?
6. Write query: fetch last 10 messages for a user ordered by timestamp.
7. How would you index tables for faster retrieval?
8. What are JOINs? Which JOIN would you use for sessions + users?
9. How do transactions help maintain consistency?
10. What is normalization, and when can denormalization help?

---

## 12) Git, Version Control, and Team Practices

1. Describe your Git workflow (feature branch, commits, PR).
2. What makes a good commit message?
3. Difference between merge and rebase?
4. How do you resolve merge conflicts safely?
5. Why are code reviews valuable for juniors?
6. Have you used `.gitignore` effectively? Examples?
7. How do you rollback a bad release/commit?
8. What checks should run before creating a PR?
9. How do you structure PR descriptions?
10. What did you learn from peer feedback in reviews?

---

## 13) Behavioral + Collaboration (Very Common)

1. Explain a time you received critical feedback and applied it.
2. How do you estimate and complete tasks on time?
3. Describe a case where requirements changed mid-way.
4. How do you communicate blockers to senior developers?
5. Tell us about a debugging situation where you got stuck.
6. How do you learn a new tool quickly?
7. How do you prioritize quality vs delivery speed?
8. Describe a disagreement in a team and how you handled it.
9. What motivates you about this Associate SDE role?
10. Why Hashout Technologies and why Bengaluru ecosystem?

---

## 14) Deep Follow-up Questions on Your Resume Bullets

### A) “Scalable, AI conversational agent using Gemini API”
1. What does scalability mean here—RPS, latency, concurrency, or cost?
2. How did you monitor token usage and API costs?
3. Did you implement rate limiting?
4. How would you cache safe/repeated responses?
5. How would you support multi-tenant usage?

### B) “Ethical, non-persistent LLM interaction”
1. If there is no persistence, how do you personalize responses?
2. How do you audit harmful outputs without storing raw text?
3. What are limitations of non-persistent design?
4. How would user consent impact data retention choices?
5. How would you handle legal data deletion requests?

### C) “NLP routing + modular session states”
1. Show one concrete route mapping example.
2. What confidence threshold did you use and why?
3. How does routing interact with session context?
4. How do you test false positives/false negatives?
5. How do you evolve routes as intents grow?

### D) “Functional testing and debugging for reliability”
1. Which tests caught the most severe issues?
2. What was your baseline latency and improved latency?
3. How did you benchmark reliability?
4. Which logs/dashboards did you rely on?
5. How did you decide a bug fix is complete?

---

## 15) Live Coding / Whiteboard Questions You Should Expect

1. Implement a function to validate chat request JSON.
2. Write an API endpoint skeleton for `POST /chat`.
3. Parse an array of messages and return latest user message.
4. Implement debounce for user typing in frontend.
5. Implement retry with exponential backoff for failed API calls.
6. Find longest common prefix in array of strings.
7. Group chat logs by user ID.
8. Check if a string is a valid JSON object safely.
9. Design a class for `SessionManager` with clear methods.
10. SQL: count daily active users from session table.

---

## 16) Smart Questions *You* Should Ask the Interviewer

1. What does success look like in the first 90 days for this role?
2. What is your current frontend/backend stack?
3. How are tasks mentored for Associate SDEs?
4. How do you conduct code reviews for junior engineers?
5. What testing standards are expected before merge?
6. How do teams manage API contracts between frontend and backend?
7. What are common production issues juniors usually handle first?
8. What growth path exists from Associate SDE to SDE-1?
9. How is performance feedback structured?
10. Which learning resources are encouraged internally?

---

## 17) 30-Second High-Impact Answer Templates

1. **Architecture:** “My app follows client-server architecture where the frontend handles UI/state rendering and backend secures API calls, applies routing/session logic, and returns structured JSON responses.”
2. **GET vs POST:** “I use POST for chat because user input is payload-heavy and potentially sensitive; GET is suitable for safe retrieval operations like health/status or non-sensitive metadata.”
3. **Async/Await:** “Async/await keeps code readable while handling network-bound operations; I combine it with timeout, retries, and loading/error states for better UX and reliability.”
4. **OOP:** “I used OOP mainly for modularity—separating session management, routing, and LLM service wrappers to improve testability and reduce coupling.”
5. **Privacy:** “I designed for minimal data retention, avoided storing raw conversations by default, and focused on redaction plus secure secret management for user trust.”

---

## 18) Final Revision Checklist (Night Before Interview)

1. Can you explain your entire project flow without notes in under 2 minutes?
2. Can you justify each tech choice with one trade-off?
3. Can you explain GET vs POST with your own endpoint examples?
4. Can you write one async API call and error handling snippet from memory?
5. Can you explain one bug story using STAR format?
6. Can you define PK/FK with a table example?
7. Can you draw client-server architecture on paper quickly?
8. Can you answer “Why this role?” with confidence and specificity?
9. Can you discuss one improvement roadmap for your project?
10. Are your Git, SQL, and OOP basics refreshed?

---

## Bonus: 10 “Trap” Questions to Practice

1. If you don’t persist data, is your app truly stateful?
2. How do you prove emotional accuracy objectively?
3. Why not call Gemini directly from frontend for faster implementation?
4. What if the model gives medically unsafe advice?
5. How does your system behave under API quota exhaustion?
6. If intent routing fails, what exact fallback path triggers?
7. Where can race conditions happen in your app?
8. What can go wrong with retries?
9. How would you explain your architecture to a non-technical stakeholder?
10. What part of your project are you least confident about and how will you fix it?

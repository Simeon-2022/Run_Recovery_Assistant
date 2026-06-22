---
name: run-checks-and-tests
description: "Use when creating or modifying backend or frontend tasks. Ensures the backend is running, runs backend tests, and verifies the frontend is up and serving pages. Triggers on: backend changes, API endpoints, server config, frontend pages, build scripts, dev server commands."
argument-hint: "Optional: target — backend | frontend | all"
user-invocable: true
---

# Run Checks and Tests (Backend + Frontend)

## When to Use
- Working on server-side code (`backend/`, `api/`, `app/`) and need to verify the service is running and passing tests.
- Working on frontend code (`frontend/`, `public/`, `index.html`) and need to confirm the dev/build server serves the app.
- Creating CI smoke checks or debugging environment startup issues.

## What this Skill Does
1. Guides the agent through starting or detecting the backend server and running backend tests.
2. Guides the agent to start or detect the frontend dev server and perform a smoke HTTP check.
3. Provides concrete commands and verification steps tailored to common setups (Python/FastAPI, Node/Express, React/Vite, static sites).

## Procedure
1. Detect project layout: look for `backend/`, `frontend/`, `pyproject.toml`, `requirements.txt`, `package.json`, or `index.html`.

2. Backend — Typical checks
- If Python + FastAPI / Uvicorn:
  - Start: `uvicorn app:app --reload --port 8000` (or the project's equivalent)
  - Run tests: `pytest -q` or `python -m pytest tests/`
  - Smoke check: `curl -sS http://127.0.0.1:8000/health` or `http://127.0.0.1:8000/docs`
- If Node/Express:
  - Start: `npm run dev` or `node server.js`
  - Run tests: `npm test`
  - Smoke check: `curl -sS http://127.0.0.1:3000/health` or the API root

3. Frontend — Typical checks
- Static `index.html` served locally:
  - Serve: `python -m http.server 8000` from the `frontend/` or root folder
  - Smoke check: `curl -sS http://127.0.0.1:8000/index.html` and check for `200` and expected snippet
- Frameworks (Vite, React, Next, Angular):
  - Start: `npm install` (first time), then `npm run dev` or `npm start`
  - Smoke check: `curl -sS http://127.0.0.1:5173/` (Vite default) or `http://localhost:3000/` for CRA

4. Combined check flow
- Start backend (or verify an already-running process).
- Run backend tests; if tests fail, report failures and stop.
- Start frontend dev server (or verify it's running).
- Perform HTTP GET to the frontend root and ensure a `200` response and presence of an expected string (e.g., page title or a known element ID).

5. Verification & reporting
- For each step, capture and report: command run, exit code, stdout/stderr, and test results summary.
- If an expected port is occupied, suggest the likely cause and a command to view processes (`netstat -ano | findstr :8000`) or PowerShell `Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess`.

## Commands Examples
- Python backend (FastAPI):

```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
pytest -q
curl -I http://127.0.0.1:8000/
```

- Frontend (Vite / React):

```bash
npm install
npm run dev
curl -I http://127.0.0.1:5173/
```

- Static site:

```bash
cd frontend
python -m http.server 8000
curl -I http://127.0.0.1:8000/index.html
```

## Checklist Before Reporting Success
- [ ] Backend process is running on the expected port or an allowed alternative
- [ ] Backend tests passed (or the failing tests are documented)
- [ ] Frontend dev server or static server is serving the app
- [ ] HTTP smoke checks return `200` and expected content
- [ ] No hardcoded secrets were exposed when starting servers

## Tips for Agents
- Prefer `pytest` or the project's configured test runner for backend tests.
- For flaky tests, re-run with `-q -k <testname>` to isolate failures.
- When interacting with the browser, use Playwright or a headless `curl`/`wget` check for fast smoke validation.
- If ports differ from defaults, read `README.md`, `.env`, or `package.json` scripts to find the configured ports.

## Extending the Skill
- Place helper scripts under `./.github/skills/run-checks-and-tests/scripts/` (e.g., `start-backend.sh`, `start-frontend.sh`) and reference them here.
- Add a small Playwright script under `scripts/` for a richer end-to-end smoke test.


---

**Try prompts:**
- "Run backend checks and tests"
- "Verify frontend dev server is up"
- "Start backend, run tests, then start frontend and report results"

---
applyTo: "**/*"
---

After every implementation change, perform thorough verification before marking work complete.

Testing requirements:
- Always run tests that cover the modified area.
- If tests do not exist for new or changed behavior, add tests first, then run them.
- Run broader regression checks for adjacent functionality that could be affected.
- Treat any failing test as blocking; fix regressions and re-run until passing.

Project-specific checks:
- Backend changes (`backend/**`):
  - Run backend automated tests (for example, `python -m pytest` from the repository root or `backend` folder based on test location).
  - If no automated tests exist yet, at minimum run a backend smoke check that validates imports, app startup, and the changed endpoint/logic path.
- Frontend changes (`frontend/**` or `*.html|*.css|*.js`):
  - Run available frontend tests/lint checks if configured.
  - Perform a browser smoke test for the changed user flow and verify there are no console errors.

Execution and reporting:
- Prefer targeted tests first, then full-suite checks when risk is medium/high.
- In the final response, report exactly what was executed and the outcome (pass/fail), including any limitations when full automation is not available.

Frontend smoke-test guidance

- Manual steps:
  1. Start the backend (if using API):

```powershell
py -3 -m uvicorn backend.main:app --reload --port 8010
```

  2. Open `frontend/index.html` in a browser (or navigate to http://127.0.0.1:8010/ if serving from backend).
  3. Complete the main form and submit.
  4. Open browser DevTools Console and ensure there are no errors.
  5. Confirm displayed recommendations match expected structure (list items, meal plan sections).

- Quick automated checklist (suggested):
  - Load page, ensure HTTP 200 for main HTML and API endpoints used.
  - Ensure no console errors are emitted during the main flow.
  - Verify DOM contains expected result selectors (e.g., `#results`, `.recommendation-item`).

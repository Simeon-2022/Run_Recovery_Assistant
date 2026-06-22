# Testing Guide

This project uses `pytest` for backend unit tests and manual or automated smoke checks for the frontend.

Backend
- Install deps for backend:

```powershell
py -3 -m pip install -r backend/requirements.txt
```

- Run backend tests:

```powershell
py -3 -m pytest backend/tests
```

Frontend smoke checks (manual)
- Open `frontend/index.html` in a browser and exercise the main user flow: fill the form, submit, and verify results render with no console errors.
- Verify network requests to `http://127.0.0.1:8010/` (if backend is running) return 200 and expected JSON.

Optional automated frontend smoke (headless)
- If you want an automated option, install Playwright and run a short script to load the page and check for console errors. Example commands:

```powershell
py -3 -m pip install playwright
py -3 -m playwright install
node frontend/auto_smoke.js  # requires Node.js and Playwright for Node
```

Reporting
- Include the exact commands you ran and a short pass/fail summary when reporting verification in PR descriptions.

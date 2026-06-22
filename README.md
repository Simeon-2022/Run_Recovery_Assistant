# Run Recovery Assistant

## AI Assignment

This repository contains an AI Assignment project developed as part of the SoftUni **AI-Assisted Development** course (june 2026).

## Overview

The **Run Recovery Assistant** is an AI-powered tool designed to help runners recover effectively after their runs by providing personalized recovery recommendations based on run data and user input.

The project is a Run Recovery Assistant that helps recreational runners choose vegan foods to support post-run recovery. Through a browser-based user interface, the user enters the duration and intensity of their training session, and the assistant classifies the workout and recommends foods rich in carbohydrates, protein and antioxidants. Behind the scenes, a lightweight backend API (e.g. Python + FastAPI) stores a small database of vegan foods and exposes endpoints to calculate the runner's recovery needs and return matching foods. The frontend (built with HTML/CSS/JavaScript) provides a clean form for input and displays results in a user-friendly layout. Together, these two components create a self‑contained mini‑application that measures workout demands, maps them to nutritional requirements and delivers tailored food recommendations.

## Features

- **Post-run recovery recommendations** — Personalized advice based on your run data to optimize recovery
- **Vegan nutrition & meal suggestions** — Plant-based meal plans and nutritional guidance tailored for recovery
- **Sleep & rest tracking** — Monitor and improve sleep quality to enhance athletic performance
- **Injury risk assessment** — Identify potential injury risks based on training patterns and physical feedback
- **Training load / weekly mileage analysis** — Analyze cumulative training load and mileage trends over time
- **Chat interface** — Conversational assistant for interactive, natural-language recovery guidance
- **User-friendly layout** — Clean input form with results displayed in a clear, readable format

## Purpose

This project demonstrates the use of AI-assisted development techniques and tools to build a practical application that leverages artificial intelligence to improve athletic recovery.

## Deployment (Render - Single Service)

Recommended option: deploy backend and frontend together as one web service.

- Best for: fastest and simplest go-live
- What it does: runs FastAPI and serves the frontend from the same app
- Pros: one URL, easiest setup, fewer moving parts
- Cons: backend and frontend are coupled in one deploy

### Render settings

- Build command: pip install -r requirements.txt
- Start command: python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
- Environment variables:
	- SUPABASE_URL
	- SUPABASE_KEY

You can configure Render either manually in the dashboard with the values above, or by using the included render.yaml Blueprint file.

## Testing

See `TESTING.md` for detailed test and smoke-check guidance.

Quick commands:

```powershell
# Install backend deps
py -3 -m pip install -r backend/requirements.txt

# Run backend unit tests
py -3 -m pytest backend/tests
```

Makefile targets (Windows using `py`):

```powershell
py -3 -m pip install -r backend/requirements.txt  # install backend deps
make test-backend    # run backend tests
make smoke-frontend  # run frontend smoke (installs npm deps)
make test-all        # run backend tests and frontend smoke
```

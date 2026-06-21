import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

try:
    from .database import (
        seed_foods_if_empty,
        seed_fat_foods_if_missing,
        seed_pdf_foods_if_missing,
        populate_calorie_columns,
    )
    from .routes import router
except ImportError:  # pragma: no cover - supports running from backend/ directly
    from database import seed_foods_if_empty, seed_fat_foods_if_missing, seed_pdf_foods_if_missing, populate_calorie_columns
    from routes import router

app = FastAPI(title="Run Recovery Assistant API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    seed_foods_if_empty()
    seed_fat_foods_if_missing()
    seed_pdf_foods_if_missing()
    populate_calorie_columns()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(router)

# Serve frontend — root route must be registered before the static mount
_frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
_frontend_dir = os.path.abspath(_frontend_dir)


@app.get("/")
def serve_frontend() -> FileResponse:
    return FileResponse(os.path.join(_frontend_dir, "index.html"))


app.mount("/static", StaticFiles(directory=_frontend_dir), name="static")

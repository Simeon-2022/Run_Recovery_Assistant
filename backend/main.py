from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import seed_foods_if_empty
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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(router)

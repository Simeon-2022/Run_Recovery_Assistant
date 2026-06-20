---
name: fastapi-db-backend
description: "Use when creating a FastAPI backend with PostgreSQL or SQLite database, setting up database connections, configuring SQLAlchemy ORM, writing models and schemas, adding Alembic migrations, or wiring environment variables for external DB access. Triggers on: FastAPI project setup, database connection, SQLAlchemy model, Alembic migration, PostgreSQL config, SQLite config, backend scaffolding, CRUD endpoints, .env database URL."
argument-hint: "Specify DB type (postgresql/sqlite) and any existing project context"
---

# FastAPI + PostgreSQL / SQLite Backend

## When to Use
- Scaffolding a new FastAPI project with a relational database
- Adding database connectivity (PostgreSQL or SQLite) to an existing FastAPI app
- Setting up SQLAlchemy ORM models, sessions, and CRUD helpers
- Configuring Alembic for schema migrations
- Wiring `.env` / environment variables for external DB access
- Exposing REST endpoints that read from or write to the database

---

## Decision: PostgreSQL vs SQLite

| Criterion | PostgreSQL | SQLite |
|---|---|---|
| Deployment target | Production / cloud | Development / local / embedded |
| Concurrency | High | Low (single-writer) |
| External server required | Yes | No (file-based) |
| Driver | `psycopg2-binary` or `asyncpg` | built-in (`aiosqlite` for async) |

Ask the user which to use if not specified.

---

## Procedure

### Step 1 — Project Structure

Create the following layout (adjust names to the project):

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings via pydantic-settings
│   ├── database.py          # Engine, SessionLocal, Base
│   ├── models/
│   │   ├── __init__.py
│   │   └── <entity>.py      # SQLAlchemy ORM models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── <entity>.py      # Pydantic request/response schemas
│   ├── crud/
│   │   ├── __init__.py
│   │   └── <entity>.py      # DB CRUD helpers
│   └── routers/
│       ├── __init__.py
│       └── <entity>.py      # FastAPI routers
├── alembic/                 # Created by `alembic init`
├── alembic.ini
├── .env                     # Never commit — add to .gitignore
├── .env.example             # Safe to commit
└── requirements.txt
```

---

### Step 2 — Install Dependencies

See [requirements reference](./references/requirements.md) for the full list.

**Core (both DB types):**
```
fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic-settings
python-dotenv
```

**PostgreSQL only — add:**
```
psycopg2-binary       # sync driver
# OR
asyncpg               # async driver (use with databases[postgresql])
```

**SQLite async — add:**
```
aiosqlite
```

Install with: `pip install -r requirements.txt`

---

### Step 3 — Environment Variables

Create `.env` (never commit) and `.env.example` (safe to commit):

```env
# .env
DATABASE_URL=postgresql://user:password@host:5432/dbname
# OR for SQLite:
# DATABASE_URL=sqlite:///./app.db
```

```env
# .env.example
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

Add `.env` to `.gitignore` immediately.

---

### Step 4 — Settings (`app/config.py`)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
```

---

### Step 5 — Database Engine & Session (`app/database.py`)

**Synchronous (recommended for most projects):**
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

engine = create_engine(
    settings.database_url,
    # For SQLite only — prevents threading issues:
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    """FastAPI dependency that yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Async variant** — see [async database reference](./references/async-db.md).

---

### Step 6 — ORM Model

```python
# app/models/<entity>.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
```

---

### Step 7 — Pydantic Schema

```python
# app/schemas/<entity>.py
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int

    model_config = {"from_attributes": True}
```

---

### Step 8 — CRUD Helpers

```python
# app/crud/<entity>.py
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate

def get_item(db: Session, item_id: int) -> Item | None:
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

---

### Step 9 — Router

```python
# app/routers/<entity>.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import item as crud
from app.schemas.item import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=list[ItemRead])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=ItemRead, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)
```

---

### Step 10 — FastAPI App Entry Point (`app/main.py`)

```python
from fastapi import FastAPI
from app.routers import item as item_router
from app.database import Base, engine

# Create tables (use Alembic in production instead)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Run Recovery Assistant API")

app.include_router(item_router.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

### Step 11 — Alembic Migrations

```bash
# Initialize (run once)
alembic init alembic

# Edit alembic.ini — set sqlalchemy.url or use env var override
# Edit alembic/env.py — import Base and set target_metadata = Base.metadata

# Create a migration after changing models
alembic revision --autogenerate -m "initial tables"

# Apply
alembic upgrade head

# Roll back one step
alembic downgrade -1
```

See [alembic env.py reference](./references/alembic-env.md) for the required `env.py` edits.

---

### Step 12 — Run & Verify

```bash
uvicorn app.main:app --reload
# Visit: http://127.0.0.1:8000/docs  (Swagger UI)
# Visit: http://127.0.0.1:8000/health
```

---

## Security Checklist

- [ ] `.env` is in `.gitignore`
- [ ] Database credentials are never hardcoded
- [ ] `DATABASE_URL` is read from environment via `pydantic-settings`
- [ ] Input validated by Pydantic schemas before hitting the DB
- [ ] No raw SQL string formatting (use ORM or parameterized queries)
- [ ] CORS configured explicitly — avoid `allow_origins=["*"]` in production

---

## External PostgreSQL Connection Checklist

- [ ] Host, port, user, password, db name confirmed
- [ ] Network access / firewall rule allows connection from dev machine or server
- [ ] `psycopg2-binary` (or `asyncpg`) installed
- [ ] SSL mode set if required: append `?sslmode=require` to the URL
- [ ] Connection tested before running migrations: `alembic current`

---

## References

- [requirements.md](./references/requirements.md) — Full pinned dependency list
- [alembic-env.md](./references/alembic-env.md) — Required `alembic/env.py` edits
- [async-db.md](./references/async-db.md) — Async SQLAlchemy + asyncpg/aiosqlite setup

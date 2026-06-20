# Async SQLAlchemy Setup

Use when you need non-blocking DB access (e.g., high-concurrency APIs).

## Dependencies

- PostgreSQL: `sqlalchemy[asyncio]` + `asyncpg`
- SQLite: `sqlalchemy[asyncio]` + `aiosqlite`

## database.py (async)

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Convert sync URL to async driver prefix if needed:
# postgresql://  →  postgresql+asyncpg://
# sqlite:///     →  sqlite+aiosqlite:///
async_url = (
    settings.database_url
    .replace("postgresql://", "postgresql+asyncpg://")
    .replace("sqlite:///", "sqlite+aiosqlite:///")
)

engine = create_async_engine(async_url, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

## Create tables (async, for dev/SQLite)

```python
# In main.py lifespan event:
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
```

## Async CRUD example

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.item import Item

async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return result.scalars().all()

async def create_item(db: AsyncSession, name: str, description: str | None = None):
    item = Item(name=name, description=description)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
```

## Async Router dependency

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

@router.get("/items/")
async def read_items(db: AsyncSession = Depends(get_db)):
    return await crud.get_items(db)
```

## Alembic with async engine

Alembic does not support async natively. Use a sync wrapper in `env.py`:

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

def run_async_migrations():
    async def run():
        async_engine = create_async_engine(settings.database_url_async)
        async with async_engine.connect() as conn:
            await conn.run_sync(
                lambda sync_conn: context.configure(
                    connection=sync_conn,
                    target_metadata=target_metadata,
                )
            )
            async with conn.begin():
                await conn.run_sync(lambda _: context.run_migrations())
        await async_engine.dispose()

    asyncio.run(run())
```

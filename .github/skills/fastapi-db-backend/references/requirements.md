# Dependency Reference

## requirements.txt — PostgreSQL (sync)

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
sqlalchemy>=2.0.0
alembic>=1.13.0
psycopg2-binary>=2.9.9
pydantic-settings>=2.2.0
python-dotenv>=1.0.0
```

## requirements.txt — PostgreSQL (async)

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.13.0
asyncpg>=0.29.0
pydantic-settings>=2.2.0
python-dotenv>=1.0.0
```

## requirements.txt — SQLite (sync, development)

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
sqlalchemy>=2.0.0
alembic>=1.13.0
pydantic-settings>=2.2.0
python-dotenv>=1.0.0
```

## requirements.txt — SQLite (async)

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.13.0
aiosqlite>=0.20.0
pydantic-settings>=2.2.0
python-dotenv>=1.0.0
```

## Optional extras

```
# Testing
pytest>=8.0.0
httpx>=0.27.0        # async test client for FastAPI
pytest-asyncio>=0.23.0

# Dev tools
black
ruff
mypy
```

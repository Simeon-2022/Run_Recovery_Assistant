# Alembic env.py — Required Edits

After running `alembic init alembic`, edit `alembic/env.py` as follows.

## 1. Import your Base and settings

Add near the top of `env.py`, after the existing imports:

```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base          # your DeclarativeBase
from app.config import settings        # pydantic-settings instance
import app.models  # noqa: F401 — import all models so Alembic sees them
```

## 2. Set target_metadata

Replace:
```python
target_metadata = None
```
With:
```python
target_metadata = Base.metadata
```

## 3. Override the DB URL from the environment

In the `run_migrations_offline()` function, replace the `url = config.get_main_option("sqlalchemy.url")` line:

```python
url = settings.database_url
```

In the `run_migrations_online()` function, replace the `connectable = engine_from_config(...)` block:

```python
from sqlalchemy import create_engine

connectable = create_engine(settings.database_url)

with connectable.connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
```

## 4. alembic.ini — disable hardcoded URL

In `alembic.ini`, set:
```ini
sqlalchemy.url =
```
This prevents accidental plaintext credentials in the ini file; the URL is loaded from `.env` at runtime.

## Common Alembic Commands

```bash
alembic revision --autogenerate -m "describe change"   # generate migration
alembic upgrade head                                    # apply all pending
alembic downgrade -1                                    # roll back one step
alembic history --verbose                              # show migration history
alembic current                                        # show applied revision
```

# Database Migrations

This folder is reserved for Alembic migration scripts. 
Currently, the application uses SQLAlchemy's `Base.metadata.create_all()` for schema creation in SQLite, which is suitable for development.

## Setup Alembic (Future)

When transitioning to production or PostgreSQL, initialize Alembic here:

```bash
alembic init migrations
```

Then configure `migrations/env.py` to point to the `Base` metadata from `app.models`.

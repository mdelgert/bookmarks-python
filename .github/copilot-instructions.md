# Repository coding instructions

This project is a FastAPI application using:
- SQLAlchemy ORM
- Alembic migrations
- Jinja2 templates + HTMX
- Service and repository separation

## Architecture
- Routes live in `app/api/routes`.
- Business logic lives in `app/services`.
- Database access lives in `app/repositories`.
- SQLAlchemy ORM models live in `app/db/models`.
- Pydantic request/response schemas live in `app/schemas`.

## Rules
- Keep route handlers thin.
- Do not put business logic directly in routes.
- Do not access the database directly from templates or routes.
- Use Alembic for schema changes.
- Prefer explicit type hints.
- Add or update tests when behavior changes.
- Keep HTML in Jinja templates, not inline strings.
- Prefer clear, conventional Python over clever abstractions.

## API conventions
- Use response models where appropriate.
- Raise HTTP exceptions at the route/service boundary, not deep in repositories unless necessary.
- Keep validation in Pydantic schemas and service methods.

## Logging
- Use module-level loggers.
- Log meaningful lifecycle events and unexpected exceptions.
- Do not log secrets.

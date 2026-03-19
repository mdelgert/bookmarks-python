# Architecture

- FastAPI provides the HTTP and OpenAPI layer.
- SQLAlchemy provides ORM access.
- Alembic manages schema migrations.
- Jinja2 + HTMX provide the server-rendered UI.
- Services contain business logic.
- Repositories contain data access logic.

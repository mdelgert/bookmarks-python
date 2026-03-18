# Bookmarks Python – GitHub Copilot Instructions

## Project Overview
A bookmark manager / dashboard application built with FastAPI, SQLAlchemy 2.x, Alembic, Jinja2, HTMX, and SQLite.

## Tech Stack
- **Backend**: FastAPI with Python 3.12
- **Database ORM**: SQLAlchemy 2.x (async-ready, declarative base)
- **Migrations**: Alembic
- **Templates**: Jinja2 with HTMX for partial updates
- **Database**: SQLite (stored in `/app/data/bookmarks.db`)
- **Icons**: MDI, Simple Icons, selfh.st
- **Theme**: Dark theme throughout

## Directory Structure
```
app/
  main.py         – FastAPI app, lifespan, logging
  config.py       – Settings via python-dotenv
  database.py     – SQLAlchemy engine and session
  models.py       – SQLAlchemy ORM models
  schemas.py      – Pydantic request/response schemas
  crud.py         – Database CRUD helpers
  routers/
    pages.py      – HTML page routes (GET /  and GET /bookmarks)
    api.py        – HTMX/JSON API routes
  static/css/     – Custom dark-theme stylesheet
  templates/      – Jinja2 templates
```

## Coding Conventions
- Use SQLAlchemy 2.x `Session` with `sessionmaker` (synchronous for simplicity with SQLite)
- Use `Annotated` dependency injection for DB sessions
- Prefer `from __future__ import annotations`
- Route files use `APIRouter`; mount in `main.py`
- Templates extend `base.html`; use HTMX `hx-*` attributes for dynamic updates
- Always validate user input with Pydantic schemas
- Use Python `logging` (not `print`) everywhere
- All pages use dark theme; never use white backgrounds

## Icon Types
- `mdi`: Material Design Icons (`<i class="mdi mdi-{value}">`) via CDN
- `si`: Simple Icons (img from `https://cdn.simpleicons.org/{value}/white`)
- `selfhst`: selfh.st icons (img from `https://cdn.selfh.st/icons/png/{value}.png`)
- `url`: Custom image URL (`<img src="{value}">`)

## Key Routes
- `GET /` – Homepage: cards grid, icon display, HTMX status indicator per bookmark
- `GET /bookmarks` – Edit page: full CRUD table with HTMX search
- `GET /api/status?url=<url>` – Returns up/down status (used by HTMX on homepage)
- `GET /bookmarks/search?q=<query>` – HTMX partial: filtered bookmark rows
- `POST /bookmarks` – Create bookmark
- `GET /bookmarks/{id}/edit` – HTMX partial: edit form
- `PUT /bookmarks/{id}` – Update bookmark
- `DELETE /bookmarks/{id}` – Delete bookmark (HTMX swap outerHTML with empty)

# bookmarks-python

A production-clean bookmark manager / dashboard application.

## Tech Stack

- **FastAPI** – async web framework
- **SQLAlchemy 2.x** – ORM
- **Alembic** – database migrations
- **Jinja2 + HTMX** – server-side templates with dynamic partial updates
- **SQLite** – lightweight database stored in `./data/`
- **Bootstrap 5** (dark theme) + **MDI icons**
- **Dev Containers** + **Docker**

## Features

- 🏠 **Homepage** – bookmark cards grouped by category, icon display, live status indicator per site
- ✏️ **Edit page** – full CRUD (create / read / update / delete) with real-time search
- 🎨 **Icon support** from multiple sources:
  - [Material Design Icons](https://pictogrammers.com/library/mdi/) (`mdi`)
  - [Simple Icons](https://simpleicons.org/) (`si`)
  - [selfh.st icons](https://selfh.st/icons/) (`selfhst`)
  - Custom image URL (`url`)
- 🌙 **Dark theme** throughout
- 📡 **Status indicators** – HTMX live-checks whether each bookmarked URL is reachable

## Quick Start

### Docker Compose (recommended)

```bash
cp .env.example .env
docker compose up --build
```

Open http://localhost:8000

### Dev Container

Open in VS Code with the **Dev Containers** extension installed and click **"Reopen in Container"**.

### Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Database Migrations

```bash
# Apply migrations
alembic upgrade head

# Auto-generate a new migration after model changes
alembic revision --autogenerate -m "describe change"
```

## Project Structure

```
app/
  main.py          – FastAPI app, lifespan, logging
  config.py        – Settings (env vars)
  database.py      – SQLAlchemy engine/session
  models.py        – ORM models
  schemas.py       – Pydantic schemas
  crud.py          – Database helpers
  routers/
    pages.py       – HTML page routes
    bookmarks.py   – Bookmark CRUD + status API
  static/          – CSS & JS
  templates/       – Jinja2 HTML templates
alembic/           – Migration scripts
```

# Contributing

## Development

- Use the dev container or Python 3.12.
- Install dependencies with `pip install -e .[dev]`.
- Run DB migrations with `alembic upgrade head`.
- Start the app with `uvicorn app.main:app --reload`.

## Quality

- Format with `black .`
- Lint with `ruff check .`
- Run tests with `pytest`

## Pull requests

- Keep route handlers thin.
- Put business logic in `app/services`.
- Put DB logic in `app/repositories`.
- Add tests for behavior changes.

from __future__ import annotations

import logging
from itertools import groupby
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_grouped_bookmarks(db: Session) -> dict[str, list]:
    bookmarks = crud.get_bookmarks(db)
    grouped: dict[str, list] = {}
    for bm in bookmarks:
        cat = bm.category or "General"
        grouped.setdefault(cat, []).append(bm)
    return grouped


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    grouped = get_grouped_bookmarks(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "grouped_bookmarks": grouped},
    )

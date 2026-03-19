from __future__ import annotations

import logging
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.config import settings
from app.database import get_db
from app.schemas import BookmarkCreate, BookmarkUpdate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/bookmarks")
templates = Jinja2Templates(directory="app/templates")


# ── Edit page ────────────────────────────────────────────────────────────────

@router.get("", response_class=HTMLResponse)
async def bookmarks_page(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    bookmarks = crud.get_bookmarks(db)
    return templates.TemplateResponse(
        "bookmarks/list.html",
        {"request": request, "bookmarks": bookmarks},
    )


# ── Search (HTMX partial) ─────────────────────────────────────────────────────

@router.get("/search", response_class=HTMLResponse)
async def search_bookmarks(
    request: Request,
    q: str,
    db: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    bookmarks = crud.search_bookmarks(db, q) if q.strip() else crud.get_bookmarks(db)
    return templates.TemplateResponse(
        "bookmarks/partials/bookmark_rows.html",
        {"request": request, "bookmarks": bookmarks},
    )


# ── Create ────────────────────────────────────────────────────────────────────

@router.post("", response_class=HTMLResponse)
async def create_bookmark(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    title: str = Form(...),
    url: str = Form(...),
    description: str = Form(""),
    category: str = Form(""),
    icon_type: str = Form("mdi"),
    icon_value: str = Form(""),
    is_active: str | None = Form(None),
) -> HTMLResponse:
    data = BookmarkCreate(
        title=title,
        url=url,
        description=description or None,
        category=category or None,
        icon_type=icon_type or None,
        icon_value=icon_value or None,
        is_active=(is_active is not None),
    )
    crud.create_bookmark(db, data)
    bookmarks = crud.get_bookmarks(db)
    return templates.TemplateResponse(
        "bookmarks/partials/bookmark_rows.html",
        {"request": request, "bookmarks": bookmarks},
    )


# ── Edit form (HTMX partial) ──────────────────────────────────────────────────

@router.get("/{bookmark_id}/edit", response_class=HTMLResponse)
async def edit_form(
    request: Request,
    bookmark_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    bookmark = crud.get_bookmark(db, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return templates.TemplateResponse(
        "bookmarks/partials/bookmark_edit_row.html",
        {"request": request, "bookmark": bookmark},
    )


# ── Cancel edit (HTMX partial) ───────────────────────────────────────────────

@router.get("/{bookmark_id}/row", response_class=HTMLResponse)
async def bookmark_row(
    request: Request,
    bookmark_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    bookmark = crud.get_bookmark(db, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return templates.TemplateResponse(
        "bookmarks/partials/bookmark_row.html",
        {"request": request, "bookmark": bookmark},
    )


# ── Update ────────────────────────────────────────────────────────────────────

@router.put("/{bookmark_id}", response_class=HTMLResponse)
async def update_bookmark(
    request: Request,
    bookmark_id: int,
    db: Annotated[Session, Depends(get_db)],
    title: str = Form(...),
    url: str = Form(...),
    description: str = Form(""),
    category: str = Form(""),
    icon_type: str = Form("mdi"),
    icon_value: str = Form(""),
    is_active: str | None = Form(None),
) -> HTMLResponse:
    bookmark = crud.get_bookmark(db, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    data = BookmarkUpdate(
        title=title,
        url=url,
        description=description or None,
        category=category or None,
        icon_type=icon_type or None,
        icon_value=icon_value or None,
        is_active=(is_active is not None),
    )
    bookmark = crud.update_bookmark(db, bookmark, data)
    return templates.TemplateResponse(
        "bookmarks/partials/bookmark_row.html",
        {"request": request, "bookmark": bookmark},
    )


# ── Delete ────────────────────────────────────────────────────────────────────

@router.delete("/{bookmark_id}", response_class=HTMLResponse)
async def delete_bookmark(
    bookmark_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    bookmark = crud.get_bookmark(db, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    crud.delete_bookmark(db, bookmark)
    return Response(content="", status_code=200)


# ── Status check ──────────────────────────────────────────────────────────────

status_router = APIRouter(prefix="/api")


@status_router.get("/status/{bookmark_id}", response_class=HTMLResponse)
async def check_status(
    bookmark_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> HTMLResponse:
    """Check if a bookmarked URL is reachable.

    The URL is fetched from the database by ID (not from user input) to prevent SSRF.
    Returns an HTMX-friendly HTML badge.
    """
    bookmark = crud.get_bookmark(db, bookmark_id)
    if not bookmark:
        return HTMLResponse(
            content='<span class="status-badge status-down" title="Not found">'
            '<span class="status-dot"></span>?</span>'
        )

    url: str = bookmark.url
    error_message = "Unknown error"
    method_used = "HEAD"
    
    try:
        async with httpx.AsyncClient(
            timeout=settings.status_check_timeout,
            follow_redirects=True,
            verify=False,  # Allow self-signed certificates for local services
        ) as client:
            # Try HEAD first (faster, appropriate for status checks)
            resp = await client.head(url)
            
            # If HEAD is not supported, fall back to GET
            if resp.status_code in [405, 501]:  # Method Not Allowed or Not Implemented
                logger.info(f"HEAD not supported for {url} (got {resp.status_code}), trying GET")
                resp = await client.get(url)
                method_used = "GET"
            
            # Consider success codes (2xx, 3xx) as up, 4xx+ as potentially down
            is_up = resp.status_code < 400
            logger.info(f"Status check for {url}: {resp.status_code} (method: {method_used})")
            
    except httpx.TimeoutException:
        is_up = False
        error_message = "Connection timeout"
        logger.warning(f"Timeout checking {url}")
        
    except httpx.ConnectError as e:
        is_up = False
        error_message = "Connection failed"
        logger.warning(f"Connection error for {url}: {e}")
        
    except httpx.NetworkError as e:
        is_up = False
        error_message = "Network error" 
        logger.warning(f"Network error for {url}: {e}")
        
    except Exception as e:
        is_up = False
        error_message = f"Error: {type(e).__name__}"
        logger.error(f"Unexpected error checking {url}: {e}")

    css_class = "status-up" if is_up else "status-down"
    label = "Up" if is_up else "Down"
    title = label if is_up else f"{label} - {error_message}"
    
    return HTMLResponse(
        content=f'<span class="status-badge {css_class}" title="{title}">'
        f'<span class="status-dot"></span>{label}</span>'
    )

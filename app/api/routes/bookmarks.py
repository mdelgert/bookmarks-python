from fastapi import APIRouter, Depends, Form, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.bookmark import BookmarkCreate, BookmarkRead, BookmarkUpdate
from app.services.bookmark_service import BookmarkService

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])
templates = Jinja2Templates(directory="app/templates")
service = BookmarkService()


@router.get("", response_model=list[BookmarkRead])
def list_bookmarks(db: Session = Depends(get_db)) -> list[BookmarkRead]:
    return service.list_all(db)


@router.get("/{bookmark_id}", response_model=BookmarkRead)
def get_bookmark(bookmark_id: int, db: Session = Depends(get_db)) -> BookmarkRead:
    return service.get(db, bookmark_id)


@router.post("", response_model=BookmarkRead, status_code=status.HTTP_201_CREATED)
def create_bookmark(data: BookmarkCreate, db: Session = Depends(get_db)) -> BookmarkRead:
    return service.create(db, data)


@router.patch("/{bookmark_id}", response_model=BookmarkRead)
def update_bookmark(
    bookmark_id: int,
    data: BookmarkUpdate,
    db: Session = Depends(get_db),
) -> BookmarkRead:
    return service.update(db, bookmark_id, data)


@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(bookmark_id: int, db: Session = Depends(get_db)) -> Response:
    service.delete(db, bookmark_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/ui", response_class=HTMLResponse)
def create_bookmark_from_form(
    request: Request,
    title: str = Form(...),
    url: str = Form(...),
    notes: str = Form(default=""),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    bookmark = service.create(
        db,
        BookmarkCreate(title=title.strip(), url=url.strip(), notes=notes.strip() or None),
    )
    return templates.TemplateResponse(
        request=request,
        name="partials/bookmark_item.html",
        context={"bookmark": bookmark},
    )

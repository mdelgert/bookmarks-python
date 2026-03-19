from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.services.bookmark_service import BookmarkService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
service = BookmarkService()


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    bookmarks = service.list_all(db)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"bookmarks": bookmarks},
    )

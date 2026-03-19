from fastapi import APIRouter

from app.api.routes import bookmarks, home

api_router = APIRouter()
api_router.include_router(home.router)
api_router.include_router(bookmarks.router)

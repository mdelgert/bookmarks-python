"""
REST API endpoints for bookmarks with JSON payloads.
Provides standard CRUD operations with proper HTTP status codes.
"""
from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import BookmarkCreate, BookmarkRead, BookmarkUpdate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/bookmarks", 
    tags=["Bookmarks API"],
    responses={404: {"description": "Bookmark not found"}},
)


@router.get(
    "",
    response_model=list[BookmarkRead],
    summary="List all bookmarks",
    description="Retrieve a paginated list of bookmarks with optional search filtering",
)
async def get_bookmarks(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0, description="Number of bookmarks to skip"), 
    limit: int = Query(100, ge=1, le=500, description="Maximum number of bookmarks to return"),
    q: str | None = Query(None, description="Search query to filter bookmarks"),
) -> list[BookmarkRead]:
    """
    Get bookmarks with optional pagination and search.
    
    - **skip**: Number of bookmarks to skip for pagination (default: 0)
    - **limit**: Maximum number of bookmarks to return (default: 100, max: 500) 
    - **q**: Search query to filter by title, URL, description, or category
    """
    if q and q.strip():
        bookmarks = crud.search_bookmarks(db, q.strip())
        # Apply pagination to search results
        return bookmarks[skip:skip + limit]
    
    return crud.get_bookmarks(db, skip=skip, limit=limit)


@router.get(
    "/{bookmark_id}",
    response_model=BookmarkRead,
    summary="Get a bookmark by ID",
    description="Retrieve a specific bookmark by its ID",
)
async def get_bookmark(
    bookmark_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> BookmarkRead:
    """
    Get a specific bookmark by ID.
    
    - **bookmark_id**: The ID of the bookmark to retrieve
    """
    bookmark = crud.get_bookmark(db, bookmark_id)
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Bookmark not found"
        )
    return bookmark


@router.post(
    "",
    response_model=BookmarkRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new bookmark",
    description="Create a new bookmark with the provided data",
)
async def create_bookmark(
    bookmark_data: BookmarkCreate,
    db: Annotated[Session, Depends(get_db)],
) -> BookmarkRead:
    """
    Create a new bookmark.
    
    - **bookmark_data**: The bookmark data to create
    """
    try:
        bookmark = crud.create_bookmark(db, bookmark_data)
        return bookmark
    except Exception as e:
        logger.error("Error creating bookmark: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create bookmark"
        )


@router.put(
    "/{bookmark_id}",
    response_model=BookmarkRead,
    summary="Update a bookmark",
    description="Update an existing bookmark with new data",
)
async def update_bookmark(
    bookmark_id: int,
    bookmark_data: BookmarkUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> BookmarkRead:
    """
    Update an existing bookmark.
    
    - **bookmark_id**: The ID of the bookmark to update
    - **bookmark_data**: The updated bookmark data
    """
    bookmark = crud.get_bookmark(db, bookmark_id)
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Bookmark not found"
        )
    
    try:
        updated_bookmark = crud.update_bookmark(db, bookmark, bookmark_data)
        return updated_bookmark
    except Exception as e:
        logger.error("Error updating bookmark %d: %s", bookmark_id, e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update bookmark"
        )


@router.delete(
    "/{bookmark_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a bookmark", 
    description="Delete an existing bookmark by ID",
)
async def delete_bookmark(
    bookmark_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> None:
    """
    Delete a bookmark by ID.
    
    - **bookmark_id**: The ID of the bookmark to delete
    """
    bookmark = crud.get_bookmark(db, bookmark_id)
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Bookmark not found"
        )
    
    try:
        crud.delete_bookmark(db, bookmark)
    except Exception as e:
        logger.error("Error deleting bookmark %d: %s", bookmark_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete bookmark"
        )


# Health check endpoint
@router.get(
    "/health",
    tags=["Health"],
    summary="API Health Check",
    description="Simple health check endpoint to verify API is running",
)
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "bookmarks-api"}
from __future__ import annotations

import logging
from typing import Sequence

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models import Bookmark
from app.schemas import BookmarkCreate, BookmarkUpdate

logger = logging.getLogger(__name__)


def get_bookmarks(db: Session, skip: int = 0, limit: int = 200) -> Sequence[Bookmark]:
    stmt = select(Bookmark).order_by(Bookmark.category, Bookmark.title).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def search_bookmarks(db: Session, query: str) -> Sequence[Bookmark]:
    q = f"%{query}%"
    stmt = (
        select(Bookmark)
        .where(
            or_(
                Bookmark.title.ilike(q),
                Bookmark.url.ilike(q),
                Bookmark.description.ilike(q),
                Bookmark.category.ilike(q),
            )
        )
        .order_by(Bookmark.category, Bookmark.title)
    )
    return db.scalars(stmt).all()


def get_bookmark(db: Session, bookmark_id: int) -> Bookmark | None:
    return db.get(Bookmark, bookmark_id)


def create_bookmark(db: Session, data: BookmarkCreate) -> Bookmark:
    bookmark = Bookmark(**data.model_dump())
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    logger.info("Created bookmark id=%d title=%r", bookmark.id, bookmark.title)
    return bookmark


def update_bookmark(db: Session, bookmark: Bookmark, data: BookmarkUpdate) -> Bookmark:
    for field, value in data.model_dump().items():
        setattr(bookmark, field, value)
    db.commit()
    db.refresh(bookmark)
    logger.info("Updated bookmark id=%d title=%r", bookmark.id, bookmark.title)
    return bookmark


def delete_bookmark(db: Session, bookmark: Bookmark) -> None:
    logger.info("Deleted bookmark id=%d title=%r", bookmark.id, bookmark.title)
    db.delete(bookmark)
    db.commit()

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.bookmark import Bookmark
from app.schemas.bookmark import BookmarkCreate


class BookmarkRepository:
    def create(self, db: Session, data: BookmarkCreate) -> Bookmark:
        item = Bookmark(**data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def list_all(self, db: Session) -> list[Bookmark]:
        statement = select(Bookmark).order_by(Bookmark.is_pinned.desc(), Bookmark.title.asc())
        return list(db.scalars(statement).all())

    def get_by_id(self, db: Session, bookmark_id: int) -> Bookmark | None:
        return db.get(Bookmark, bookmark_id)

    def delete(self, db: Session, bookmark: Bookmark) -> None:
        db.delete(bookmark)
        db.commit()

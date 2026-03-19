import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.bookmark_repository import BookmarkRepository
from app.schemas.bookmark import BookmarkCreate, BookmarkUpdate

logger = logging.getLogger(__name__)


class BookmarkService:
    def __init__(self, repository: BookmarkRepository | None = None) -> None:
        self.repository = repository or BookmarkRepository()

    def create(self, db: Session, data: BookmarkCreate):
        logger.info("Creating bookmark", extra={"title": data.title})
        return self.repository.create(db, data)

    def list_all(self, db: Session):
        return self.repository.list_all(db)

    def get(self, db: Session, bookmark_id: int):
        bookmark = self.repository.get_by_id(db, bookmark_id)
        if bookmark is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bookmark not found")
        return bookmark

    def update(self, db: Session, bookmark_id: int, data: BookmarkUpdate):
        bookmark = self.get(db, bookmark_id)
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(bookmark, key, value)
        db.add(bookmark)
        db.commit()
        db.refresh(bookmark)
        return bookmark

    def delete(self, db: Session, bookmark_id: int) -> None:
        bookmark = self.get(db, bookmark_id)
        self.repository.delete(db, bookmark)
        logger.info("Deleted bookmark", extra={"bookmark_id": bookmark_id})

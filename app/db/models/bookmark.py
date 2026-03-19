from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text(), nullable=True)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_utc: Mapped[datetime] = mapped_column(DateTime(), default=lambda: datetime.now(UTC))
    updated_utc: Mapped[datetime] = mapped_column(
        DateTime(), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

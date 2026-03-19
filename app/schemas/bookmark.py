from datetime import datetime

from pydantic import BaseModel, Field


class BookmarkCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    url: str = Field(min_length=1, max_length=1000)
    notes: str | None = None
    is_pinned: bool = False


class BookmarkUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    url: str | None = Field(default=None, min_length=1, max_length=1000)
    notes: str | None = None
    is_pinned: bool | None = None


class BookmarkRead(BaseModel):
    id: int
    title: str
    url: str
    notes: str | None
    is_pinned: bool
    created_utc: datetime
    updated_utc: datetime

    model_config = {"from_attributes": True}

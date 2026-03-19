from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator


class BookmarkBase(BaseModel):
    title: str
    url: str
    description: str | None = None
    category: str | None = None
    icon_type: str | None = "mdi"
    icon_value: str | None = None
    is_active: bool = True

    @field_validator("icon_type")
    @classmethod
    def validate_icon_type(cls, v: str | None) -> str | None:
        allowed = {"mdi", "si", "selfhst", "url", None, ""}
        if v not in allowed:
            raise ValueError(f"icon_type must be one of: mdi, si, selfhst, url")
        return v or None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("url")
    @classmethod
    def url_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("URL cannot be empty")
        return v.strip()


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkUpdate(BookmarkBase):
    pass


class BookmarkRead(BookmarkBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

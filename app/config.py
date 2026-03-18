from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/bookmarks.db")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    status_check_timeout: int = int(os.getenv("STATUS_CHECK_TIMEOUT", "5"))
    app_title: str = "Bookmarks"
    app_description: str = "Bookmark manager and dashboard"


settings = Settings()

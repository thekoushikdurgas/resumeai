"""Pytest configuration — set env before app imports so SQLite schema matches models."""

import os

os.environ.setdefault("API_KEY", "test-key")
# Fresh schema each run (avoids stale resume.db with old columns)
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

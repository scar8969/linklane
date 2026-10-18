"""Compatibility shim - the real Link/Click models live in the project-root models.py.

Every module in this project imports the models from the root module
('from models import Link, Click'). This file exists so that external callers
written against the old package-relative path ('from short.models import
Link') keep working; it forwards to the single declaration instead of
defining a second model bound to a different SQLAlchemy metadata object.
"""

from ..models import Click, Link, db

__all__ = ["Click", "Link", "db"]

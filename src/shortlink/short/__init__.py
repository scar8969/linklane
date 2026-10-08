"""short - URL shortener package.

Contents
    links.py      create / resolve short links, expiry handling
    analytics.py  click recording and per-link stats aggregation
    api.py        the /api/links blueprint
    models.py     compatibility shim, see below

Link, Click and the SQLAlchemy handle are declared once in the PROJECT-ROOT
models.py so web/app.py, cli.py and wsgi.py share them. db lives in that root
module, so the correct import inside this package is

    from models import db, Link, Click

and NOT 'from . import db', which would look for a non-existent short/db.py.
The handle is re-exported here only so 'from short import db' keeps working.
"""
from ..models import Click, Link, db  # noqa: F401

__all__ = ["db", "Link", "Click"]

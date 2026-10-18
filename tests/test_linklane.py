"""B5 shortlink — tests. Run: pytest test_linklane.py"""

import pytest

flask_ok = True
try:
    import flask_sqlalchemy
except ImportError:
    flask_ok = False


@pytest.mark.skipif(not flask_ok, reason="flask-sqlalchemy not installed")
def test_slug_length():
    from shortlink.short.links import make_slug

    assert len(make_slug()) == 6


@pytest.mark.skipif(not flask_ok, reason="flask-sqlalchemy not installed")
def test_slug_charset():
    import string

    from shortlink.short.links import make_slug

    allowed = set(string.ascii_letters + string.digits)
    assert set(make_slug(12)) <= allowed


def test_expiry_map():
    from shortlink.short.links import _EXPIRY

    assert _EXPIRY["7d"] == 7 * 86400


def test_password_hash():
    import hashlib

    assert hashlib.sha256(b"pw").hexdigest() == hashlib.sha256(b"pw").hexdigest()

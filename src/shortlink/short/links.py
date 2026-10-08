import hashlib
from datetime import datetime, timedelta

import secrets, string

_ALPHABET = string.ascii_letters + string.digits

def make_slug(n=6):
    from ..models import Link
    while True:
        slug = "".join(secrets.choice(_ALPHABET) for _ in range(n))
        if not Link.query.filter_by(slug=slug).first():
            return slug

def create(url, slug="", expiry="", password=""):
    from ..models import Link
    from ..models import db
    if not slug:
        slug = make_slug()
    expires = None
    if expiry in _EXPIRY:
        expires = datetime.utcnow() + timedelta(seconds=_EXPIRY[expiry])
    pw = hashlib.sha256(password.encode()).hexdigest() if password else None
    link = Link(slug=slug, url=url, password_hash=pw, expires_at=expires)
    db.session.add(link); db.session.commit()
    return link

def resolve(slug, password=""):
    from ..models import Link
    from ..models import db
    link = Link.query.filter_by(slug=slug, enabled=1).first()
    if not link:
        return None, "not found"
    if link.expires_at and link.expires_at < datetime.utcnow():
        link.enabled = 0
        db.session.commit()
        return None, "expired"
    if link.password_hash:
        if hashlib.sha256(password.encode()).hexdigest() != link.password_hash:
            return None, "bad password"
    return link, None

_EXPIRY = {"1h": 3600, "1d": 86400, "7d": 7 * 86400, "30d": 30 * 86400}

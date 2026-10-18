from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(16), unique=True)
    url = db.Column(db.String(1024), default="")
    password_hash = db.Column(db.String(128), nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    enabled = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Click(db.Model):
    __tablename__ = "clicks"
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey("links.id"), index=True)
    ip = db.Column(db.String(64), default="")
    referrer = db.Column(db.String(256), default="")
    ua = db.Column(db.String(256), default="")
    at = db.Column(db.DateTime, default=datetime.utcnow)

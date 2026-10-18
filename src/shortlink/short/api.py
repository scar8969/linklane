from flask import Blueprint, abort, jsonify, redirect, request

from ..models import Link, db
from .analytics import record_click, stats
from .links import create, resolve

bp = Blueprint("short", __name__)


@bp.post("/api/links")
def create_link():
    d = request.get_json(force=True, silent=True) or {}
    if not d.get("url"):
        return jsonify({"error": "url required"}), 400
    link = create(d["url"], d.get("slug", ""), d.get("expiry", ""), d.get("password", ""))
    return jsonify({"slug": link.slug, "url": f"/{link.slug}"})


@bp.get("/<slug>")
def go(slug):
    link, err = resolve(slug, request.args.get("password", ""))
    if err:
        abort(410 if err == "expired" else 404 if err == "not found" else 403)
    record_click(link, request)
    return redirect(link.url)


@bp.get("/api/links/<slug>/stats")
def link_stats(slug):
    link = Link.query.filter_by(slug=slug).first_or_404()
    return jsonify(stats(link.id, request.args.get("days", 30, type=int)))


@bp.delete("/api/links/<slug>")
def disable(slug):
    link = Link.query.filter_by(slug=slug).first_or_404()
    link.enabled = 0
    db.session.commit()
    return jsonify({"status": "disabled"})

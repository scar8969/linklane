"""linklane — Flask application entry point.

Templates live in the project-root templates/ directory, not under web/, so the
template folder is passed explicitly; Flask(__name__) alone would look in
web/templates/ and raise TemplateNotFound on "/".
The SQLite file also lives in the project-root instance/ directory.

The browser pages read the same rows as the JSON API: short.links.resolve() and
short.analytics.stats().
"""

from flask import Flask, abort, jsonify, redirect, render_template, request, url_for

from . import paths
from .models import Click, Link, db
from .short.analytics import stats
from .short.api import bp
from .short.links import _EXPIRY, create

paths.ensure_runtime_dirs()


def build_app():
    """Build the application: configuration, database, then routes."""
    app = Flask(
        __name__, template_folder=str(paths.TEMPLATES_DIR), instance_path=str(paths.INSTANCE_DIR)
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(paths.INSTANCE_DIR / "shortlink.db")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(bp)

    DAYS = 30

    @app.get("/")
    def index():
        links = Link.query.order_by(Link.id.desc()).all()
        counts = {l.id: Click.query.filter_by(link_id=l.id).count() for l in links}
        return render_template(
            "index.html", links=links, counts=counts, expiry_choices=list(_EXPIRY.keys())
        )

    @app.post("/create")
    def create_page():
        """Create a link from the HTML form (the JSON route is POST /api/links)."""
        url = request.form.get("url", "").strip()
        if not url:
            return redirect(url_for("index"))
        link = create(
            url,
            request.form.get("slug", "").strip(),
            request.form.get("expiry", ""),
            request.form.get("password", ""),
        )
        return redirect(url_for("stats_page", slug=link.slug))

    @app.get("/s/<slug>")
    def stats_page(slug):
        """Human-readable analytics page for a link (JSON is /api/links/SLUG/stats)."""
        link = Link.query.filter_by(slug=slug).first()
        if link is None:
            abort(404)
        return render_template(
            "stats.html", link=link, data=stats(link.id, DAYS), days=DAYS, error=None
        )

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "links": Link.query.count(), "clicks": Click.query.count()})

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5000)

    return app


app = build_app()

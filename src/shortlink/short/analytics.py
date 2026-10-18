from datetime import datetime, timedelta
from typing import Any


def record_click(link, request):
    from ..models import Click, db

    db.session.add(
        Click(
            link_id=link.id,
            ip=request.remote_addr or "",
            referrer=request.referrer or "",
            ua=request.headers.get("User-Agent", ""),
        )
    )
    db.session.commit()


def stats(link_id, days=30):
    from ..models import Click

    since = datetime.utcnow() - timedelta(days=days)
    clicks = Click.query.filter(Click.link_id == link_id, Click.at >= since).all()
    series: dict[str, Any] = {}
    for c in clicks:
        d = c.at.date().isoformat()
        series[d] = series.get(d, 0) + 1
    refs: dict[str, int] = {}
    for c in clicks:
        r = c.referrer or "direct"
        refs[r] = refs.get(r, 0) + 1
    return {
        "clicks": len(clicks),
        "unique": len({c.ip for c in clicks}),
        "series": [{"date": d, "count": n} for d, n in sorted(series.items())],
        "referrers": refs,
    }

== curl ==
# POST /api/links  {"url":"https://example.com/very/long/path","slug":"x9f2","expiry":"7d"}
# curl -L http://127.0.0.1:5000/x9f2   (302 → target)
# GET  /api/links/x9f2/stats?days=30
# DELETE /api/links/x9f2
# CLI: short create https://example.com --slug x9f2 --expiry 7d

== session plan ==
# Session 1: links (slug/expiry/password) → tests
# Session 2: analytics + api → tests
# Session 3: web templates + cli + QR → screenshots → README → CI/Docker/Pages → tag

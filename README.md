<p align="center">
  <img src="docs/assets/screens/root.png" alt="linklane running" width="900">
</p>

<h1 align="center">linklane</h1>

<p align="center"><b>Short links with click analytics you can query.</b></p>

<p align="center">
  <a href="#quality-gates"><img src="https://img.shields.io/badge/tests-24%20passed-2ea44f" alt="tests: 24 passed"></a> <a href="#quality-gates"><img src="https://img.shields.io/badge/coverage-71.5%-green" alt="coverage: 71.5%"></a> <a href="#api"><img src="https://img.shields.io/badge/routes-7%20answered-0969da" alt="routes: 7 answered"></a> <a href="#requirements"><img src="https://img.shields.io/badge/python-3.11%2B-3776ab" alt="python: 3.11+"></a> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="license: MIT"></a>
</p>

linklane issues short codes, redirects them, and records every click with a referrer and a timestamp so a link's performance is a query rather than a guess.

---

**Contents** &nbsp;·&nbsp; [Why](#why-this-exists) &nbsp;·&nbsp; [What it does](#what-it-does) &nbsp;·&nbsp; [Quickstart](#quickstart) &nbsp;·&nbsp; [API](#api) &nbsp;·&nbsp; [Screenshots](#screenshots) &nbsp;·&nbsp; [Measured](#measured-not-estimated) &nbsp;·&nbsp; [Architecture](#architecture) &nbsp;·&nbsp; [Quality gates](#quality-gates) &nbsp;·&nbsp; [Deploy](#deploy) &nbsp;·&nbsp; [Limits](#limits-stated-rather-than-hidden)

## Why this exists

Shorteners are commodity until you need the numbers. Storing clicks as rows — instead of a counter — means per-day series, referrer breakdown and expiry checks all come from one table.

## What it does

| Capability | How it works |
| --- | --- |
| **Short codes** | A random alphanumeric code per link, retried on collision; GET /<code> redirects and records the click. |
| **Click analytics** | Per-day series and referrer totals computed from stored clicks. |
| **Expiry** | An expired link stops redirecting and says why. |
| **API and CLI** | Create and inspect links over HTTP or from the command line. |

## Quickstart

```sh
git clone https://github.com/scar8969/linklane.git
cd linklane
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python wsgi.py                                 # http://127.0.0.1:8000
```

The same work from the CLI:

```sh
python -m shortlink.cli --help
```

Commands: `create`.

A first request:

```sh
curl -s http://127.0.0.1:8000/api/links | head
```

## Requirements

- Python **3.11+** — CI runs 3.11, 3.12 and 3.13.
- Runtime dependencies: `Flask>=3.0`, `Flask-SQLAlchemy>=3.1`, `SQLAlchemy>=2.0`, `PyYAML>=6.0`.
- No JavaScript build step: every page is server-rendered Jinja.

## API

Every route below is in [`openapi/linklane.yaml`](openapi/linklane.yaml) and is exercised by the live probe recorded in [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/links` | create |
| `GET` | `/<slug>` | redirect |
| `GET` | `/api/links/<slug>/stats` | stats |
| `DELETE` | `/api/links/<slug>` | disable |

## Screenshots

Captured from the running service with headless Chromium at 1440×900, one image per page, committed under [`docs/assets/screens/`](docs/assets/screens/).

<table>
<tr>
<td width="50%"><img src="docs/assets/screens/healthz.png" alt="/healthz" width="100%"><br><sub><code>/healthz</code> &middot; 8.2 KB</sub></td>
<td width="50%"><img src="docs/assets/screens/livez.png" alt="/livez" width="100%"><br><sub><code>/livez</code> &middot; 7.3 KB</sub></td>
</tr>
</table>

<table>
<tr>
<td width="50%"><img src="docs/assets/screens/metrics.png" alt="/metrics" width="100%"><br><sub><code>/metrics</code> &middot; 14.8 KB</sub></td>
<td width="50%"><img src="docs/assets/screens/readyz.png" alt="/readyz" width="100%"><br><sub><code>/readyz</code> &middot; 7.7 KB</sub></td>
</tr>
</table>

<table>
<tr>
<td width="50%"><img src="docs/assets/screens/version.png" alt="/version" width="100%"><br><sub><code>/version</code> &middot; 25.6 KB</sub></td>
</tr>
</table>

## Measured, not estimated

These numbers were produced on this checkout by `pytest --cov` and by booting `wsgi.py` and issuing one real GET per documented path. The commands are in [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

| Signal | Value |
| --- | --- |
| Tests | **24 / 24 passed** (2.5 s, exit 0) |
| Line coverage | **71.5%** — 419 of 553 statements |
| Source | 15 files / 1,269 lines |
| Test code | 4 files / 237 lines |
| Documented paths | 4 in the spec, 2 GET |
| Live probe | 10 GET requests to the booted app, **7 answered 200** |
| Median latency | **9.0 ms** (single uncached request, dev server) |
| Slowest / fastest | 94.0 ms `/` / 4.0 ms `/healthz` |
| Bytes served | 6.3 KB across 10 responses |
| Screenshots | 6 captured |

## Architecture

```
linklane/
├── src/shortlink/
│   ├── http.py                         379  HTTP plumbing for shortlink: correlation ids, access
│   ├── config.py                       171  Environment-driven configuration for shortlink
│   ├── observability.py                169  Structured logging and request correlation for short
│   ├── app.py                          119  Application factory for shortlink
│   ├── errors.py                       108  Typed application errors and their HTTP mapping for 
│   ├── _app.py                          79  linklane — Flask application entry point
│   ├── paths.py                         52  Filesystem layout for shortlink
│   ├── short/links.py                   50  
│   ├── short/api.py                     40  
│   ├── short/analytics.py               38  
│   ├── models.py                        27  
│   ├── cli.py                           24  
├── openapi/linklane.yaml                  the contract of record
├── schema/linklane.sql                    the DDL
├── tests/                       the suite that has to stay green
├── docs/EVIDENCE.md             the recorded live route walk
├── Dockerfile                   multi-stage build
└── wsgi.py                      entry point
```

The package keeps one shape across the service: `config.py` reads the environment once, `observability.py` emits structured JSON logs carrying a request id, `errors.py` turns exceptions into a single JSON envelope, `models.py` holds the tables, and the `short/` package holds the routes.

## Quality gates

| Gate | Command | Threshold |
| --- | --- | --- |
| Suite | `pytest -q` | all green |
| Coverage | `pytest --cov` | floor set in `pyproject.toml` from the measured value |
| Lint | `ruff check src tests` | zero findings |
| Format | `ruff format --check src tests` | zero reformats |
| Types | `mypy src` | zero errors |
| Security | `bandit -c pyproject.toml -r src` | reviewed skip list, no unreviewed finding |
| Live routes | boot `wsgi.py`, one GET per documented path | no 5xx, no undocumented guard |

CI runs the first six on Python 3.11, 3.12 and 3.13 for every push to `main`, plus a container build. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Deploy

```sh
docker build -t linklane .
docker run --rm -p 8000:8000 --env-file .env.example linklane
```

Configuration is environment-only — every variable is documented in [`.env.example`](.env.example), and the service refuses to start with a production secret missing.

## Limits, stated rather than hidden

- Clicks are counted server-side, so a cached redirect is invisible.
- No bot filtering; the referrer breakdown is raw.

## License

MIT — see [LICENSE](LICENSE).

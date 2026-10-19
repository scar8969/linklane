<p align="center">
  <img src="docs/assets/screens/root.png" alt="linklane running" width="900">
</p>

<h1 align="center">linklane</h1>

<p align="center"><b>Short links with click analytics you can query.</b></p>

<p align="center">
  <a href="https://github.com/scar8969/linklane/actions/workflows/ci.yml"><img src="https://github.com/scar8969/linklane/actions/workflows/ci.yml/badge.svg" alt="ci"></a> <a href="#quality-gates"><img src="https://img.shields.io/badge/tests-24%20passed-2ea44f" alt="tests: 24 passed"></a> <a href="#quality-gates"><img src="https://img.shields.io/badge/coverage-71.5%-green" alt="coverage: 71.5%"></a> <a href="#api"><img src="https://img.shields.io/badge/routes-7%20live-0969da" alt="routes: 7 live"></a> <a href="#requirements"><img src="https://img.shields.io/badge/python-3.11%2B-3776ab" alt="python: 3.11+"></a> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2ea44f" alt="license: MIT"></a>
</p>

linklane issues short codes, redirects them, and records every click with a referrer and a timestamp so a link's performance is a query rather than a guess.

---

**Contents** &nbsp;·&nbsp; [Why](#why-this-exists) &nbsp;·&nbsp; [What it does](#what-it-does) &nbsp;·&nbsp; [Quickstart](#quickstart) &nbsp;·&nbsp; [Screenshots](#screenshots) &nbsp;·&nbsp; [API](#api) &nbsp;·&nbsp; [CLI](#cli) &nbsp;·&nbsp; [Configuration](#configuration) &nbsp;·&nbsp; [Measured](#measured-not-estimated) &nbsp;·&nbsp; [How a request flows](#how-a-request-flows) &nbsp;·&nbsp; [Architecture](#architecture) &nbsp;·&nbsp; [Quality gates](#quality-gates) &nbsp;·&nbsp; [Development](#development) &nbsp;·&nbsp; [Deploy](#deploy) &nbsp;·&nbsp; [Limits](#limits-stated-rather-than-hidden)

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

## API

Every route below is declared in [`openapi/linklane.yaml`](openapi/linklane.yaml) and exercised by the live probe recorded in [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/links` | create |
| `GET` | `/<slug>` | redirect |
| `GET` | `/api/links/<slug>/stats` | stats |
| `DELETE` | `/api/links/<slug>` | disable |

## CLI

The same operations without an HTTP client. Installed as `linklane`, and runnable from a checkout with no install:

```sh
python -m shortlink.cli --help
```

```text
usage: short [-h] {create} ...

positional arguments:
  {create}

options:
  -h, --help  show this help message and exit
```

## Configuration

Environment only — there is no config file. Copy `.env.example` to `.env` and edit; `APP_ENV=production` refuses to start without `SECRET_KEY`.

| Variable | Default | Meaning |
| --- | --- | --- |
| `APP_ENV` | `development` | development \| staging \| production; production enforces the secret. |
| `SECRET_KEY` | `change-me-in-production` | Session/CSRF signing key. Required when APP_ENV=production. |
| `HOST` | `0.0.0.0` | Interface the dev server binds. |
| `PORT` | `8000` | Port the dev server and the container listen on. |
| `DEBUG` | `false` | Flask debug mode. Never true in production. |
| `MAX_CONTENT_LENGTH` | `8388608` | Largest accepted request body, in bytes. |
| `DATA_DIR` | `(empty)` | Where uploaded and generated files live. |
| `INSTANCE_DIR` | `(empty)` | Where the SQLite file and instance state live. |
| `LOG_DIR` | `(empty)` | Where rotated log files are written, if file logging is on. |
| `LOG_LEVEL` | `INFO` | DEBUG \| INFO \| WARNING \| ERROR. |
| `LOG_JSON` | `true` | true emits one JSON object per line; false is human-readable. |
| `REQUEST_ID_HEADER` | `X-Request-ID` | Header echoed on every response and stamped on every log line. |

## Measured, not estimated

Produced on this checkout by `pytest --cov` and by booting `wsgi.py` and issuing one real GET per documented path. The commands are recorded in [`docs/EVIDENCE.md`](docs/EVIDENCE.md).

| Signal | Value |
| --- | --- |
| Tests | **24 / 24 passed** (2.5 s, exit 0) |
| Line coverage | **71.5%** — 419 of 553 statements |
| Source | 15 files / 1,292 lines |
| Test code | 4 files / 237 lines |
| Documented paths | 4 in the spec, 2 GET |
| Live probe | 10 GET requests to the booted app, **7 answered 200** |
| Median latency | **9.0 ms** (single uncached request, dev server) |
| Slowest / fastest | 94.0 ms `/` / 4.0 ms `/healthz` |
| Bytes served | 6.3 KB across 10 responses |
| Screenshots | 6 captured |

## How a request flows

```text
client
  │  HTTP
  ▼
wsgi.py ──▶ shortlink/app.py:get_app()
                │  reads config once (shortlink/config.py)
                │  registers the `short` blueprint
                ▼
           route handler
             ├──▶ shortlink/models.py        tables, via Flask-SQLAlchemy
             ├──▶ shortlink/errors.py        raises typed errors → one JSON envelope
             └──▶ shortlink/observability.py JSON log line + X-Request-ID
```

Every response carries `X-Request-ID`, and the matching log line is written once at the end of the request with the status and duration, so a report of "it failed" is one `grep` away from the traceback.

## Architecture

```
linklane/
├── src/shortlink/
│   ├── http.py                         379  HTTP plumbing for shortlink: correlation ids, access
│   ├── observability.py                169  Structured logging and request correlation for short
│   ├── config.py                       168  Environment-driven configuration for shortlink
│   ├── app.py                          119  Application factory for shortlink
│   ├── errors.py                       108  Typed application errors and their HTTP mapping for 
│   ├── _app.py                          79  linklane — Flask application entry point
│   ├── paths.py                         52  Filesystem layout for shortlink
│   ├── short/links.py                   52  
│   ├── short/analytics.py               40  
│   ├── short/api.py                     40  
│   ├── cli.py                           28  
│   ├── models.py                        27  
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
| Coverage | `pytest --cov` | floor in `pyproject.toml`, set below the measured value |
| Lint | `ruff check src tests` | zero findings |
| Format | `ruff format --check src tests` | zero reformats |
| Types | `mypy src` | zero errors |
| Security | `bandit -c pyproject.toml -r src` | reviewed skip list, no unreviewed finding |
| Live routes | boot `wsgi.py`, one GET per documented path | no 5xx, no undocumented guard |

CI runs the first six on Python 3.11, 3.12 and 3.13 on every push to `main`, plus a container build — [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Development

```sh
pip install -e ".[dev]"
python -m pytest -q                      # the suite
python -m pytest --cov                   # with the coverage floor
python -m ruff check src tests           # lint
python -m ruff format --check src tests  # formatting
python -m mypy src                       # types
python -m bandit -c pyproject.toml -r src  # security
pre-commit install                       # the same checks on commit
```

Dependabot opens grouped PRs for the dev tooling weekly and for actions and the base image monthly.

## Deploy

```sh
docker build -t linklane .
docker run --rm -p 8000:8000 --env-file .env.example linklane
```

A `docker-compose.yml` is included for a local run with a volume for the SQLite file. The image runs as a non-root user and serves through gunicorn.

## Limits, stated rather than hidden

- Clicks are counted server-side, so a cached redirect is invisible.
- No bot filtering; the referrer breakdown is raw.

## License

MIT — see [LICENSE](LICENSE).

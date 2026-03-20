# AI Impact Claims API

> **COMP3011 — Web Services and Web Data · Coursework 1**
> A production-deployed, data-driven RESTful API for storing and analysing claims about the societal impact of artificial intelligence.

[![Tests](https://github.com/hasini08/ai-impact-api/actions/workflows/tests.yml/badge.svg)](https://github.com/hasini08/ai-impact-api/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-teal)](https://fastapi.tiangolo.com)
[![Live](https://img.shields.io/badge/live-render-brightgreen)](https://ai-impact-api.onrender.com/docs)

---

## 🌐 Live Deployment

| Resource | URL |
|----------|-----|
| **Live API** | https://ai-impact-api.onrender.com |
| **Interactive Docs (Swagger UI)** | https://ai-impact-api.onrender.com/docs |
| **Health Check** | https://ai-impact-api.onrender.com/health |

> The Swagger UI allows you to explore and test all endpoints interactively — no local setup required.

---

## 📋 Project Overview

The AI Impact Claims API provides a structured way to record, validate, and analyse claims about AI's societal and occupational impact across five domains: **jobs**, **creativity**, **environment**, **education**, and **ethics**.

Rather than a basic CRUD service, this project deliberately extends beyond minimum requirements:

- ✅ Full CRUD with Pydantic v2 schema validation
- ✅ API key authentication for protected write operations
- ✅ Rich filtering, keyword search, sorting, and pagination on `GET /claims`
- ✅ Imported occupational exposure dataset (`ai_exposure_scores` table)
- ✅ Five analytics endpoints leveraging the exposure dataset
- ✅ 18 pytest tests covering auth, CRUD, validation, filtering, and analytics
- ✅ GitHub Actions CI running on every push to `main`
- ✅ Live deployment on Render with environment-variable configuration

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11 | Runtime |
| **FastAPI** | 0.110+ | API framework — chosen for automatic Swagger UI and native Pydantic v2 integration |
| **SQLAlchemy** | 2.x | ORM — separates persistence logic; enables future PostgreSQL migration |
| **SQLite** | — | Relational database — zero-setup, satisfies SQL requirement for coursework scope |
| **Pydantic v2** | 2.x | Schema validation — runtime type enforcement, enum constraints, URL validation |
| **pytest** | 7+ | Automated testing |
| **GitHub Actions** | — | CI — runs full test suite on push and pull requests |
| **Render** | — | Cloud deployment platform |

---

## 📁 Repository Structure

```
ai-impact-api/
├── .github/
│   └── workflows/
│       └── tests.yml           # GitHub Actions CI — runs pytest on push/PR
├── docs/
│   ├── api-docs.pdf            # Swagger UI documentation export
│   ├── technical-report.pdf    # Technical report (submitted via Minerva)
│   └── genai-logs/             # Exported GenAI conversation logs (Appendix A)
├── scripts/
│   ├── ai_exposure_sample.csv  # Occupational AI exposure dataset (SOC codes + scores)
│   └── import_ai_exposure.py   # Script to populate ai_exposure_scores table from CSV
├── slides/
│   └── presentation.pptx       # Oral examination presentation slides
├── tests/
│   ├── conftest.py             # Pytest fixtures — isolated in-memory test DB
│   ├── test_analytics.py       # Analytics endpoint tests
│   ├── test_auth.py            # Authentication tests (valid/invalid/missing key)
│   └── test_claims.py          # CRUD, filtering, search, pagination tests
├── .env.example                # Environment variable template (no secrets)
├── .gitignore                  # Excludes .env, __pycache__, .venv, *.db
├── database.py                 # SQLAlchemy engine and session configuration
├── main.py                     # FastAPI app — all route definitions
├── models.py                   # SQLAlchemy ORM models (Claim, AIExposureScore)
├── requirements-dev.txt        # Development dependencies (pytest, httpx, etc.)
├── requirements.txt            # Production dependencies
├── schemas.py                  # Pydantic schemas (ClaimCreate, ClaimOut, ClaimUpdate)
└── security.py                 # API key authentication middleware
```

---

## ⚙️ Local Setup

### Prerequisites

- Python 3.11+
- Git

### 1 — Clone the repository

```bash
git clone https://github.com/hasini08/ai-impact-api.git
cd ai-impact-api
```

### 2 — Create and activate a virtual environment

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4 — Configure environment variables

```bash
# macOS / Linux
cp .env.example .env

# Windows
Copy-Item .env.example .env
```

Edit `.env` so it contains:

```env
API_KEY=super-secret-coursework-key
DATABASE_URL=sqlite:///./ai_impact.db
```

### 5 — Import the exposure dataset (optional but enables analytics)

```bash
python scripts/import_ai_exposure.py
```

### 6 — Run the API

```bash
uvicorn main:app --reload --port 8001
```

Then open:
- **Swagger UI:** http://127.0.0.1:8001/docs
- **Health check:** http://127.0.0.1:8001/health

---

## 🔐 Authentication

Write operations require an API key in the request header:

```http
X-API-Key: super-secret-coursework-key
```

| Endpoint | Auth Required |
|----------|--------------|
| `POST /claims` | ✅ Yes |
| `PATCH /claims/{id}` | ✅ Yes |
| `DELETE /claims/{id}` | ✅ Yes |
| All `GET` and analytics endpoints | ❌ No (public) |

Missing or invalid key returns `401 Unauthorized`.

---

## 📡 API Endpoints

### Claims (CRUD)

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|-------------|
| `POST` | `/claims` | Create a new claim | 201 / 422 |
| `GET` | `/claims` | List claims with filtering, search, sort, pagination | 200 |
| `GET` | `/claims/{id}` | Retrieve a single claim | 200 / 404 |
| `PATCH` | `/claims/{id}` | Partial update (only provided fields updated) | 200 / 404 / 422 |
| `DELETE` | `/claims/{id}` | Delete a claim | 204 / 404 |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/analytics/summary` | Total claims, average impact score, occupation count |
| `GET` | `/analytics/by-category` | Claim counts grouped by category |
| `GET` | `/analytics/high-exposure` | Occupations above a configurable `min_score` threshold |
| `GET` | `/analytics/occupation/{code}` | Claims and exposure data for a specific occupation |

### Other

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Liveness probe — used by Render for deployment health monitoring |

---

## 🔍 Filtering, Search, and Pagination

The `GET /claims` endpoint supports eight query parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | Filter by category enum value |
| `occupation_code` | string | Filter by occupation code |
| `verification_status` | string | Filter by verification status |
| `search` | string | Case-insensitive keyword search across `title` and `description` |
| `sort_by` | string | Field to sort by (default: `id`) |
| `sort_order` | string | `asc` or `desc` (default: `desc`) |
| `skip` | integer | Pagination offset (default: `0`) |
| `limit` | integer | Page size, max 100 (default: `10`) |

**Example — combined query:**

```http
GET /claims?category=jobs&verification_status=reviewed&sort_by=impact_score&sort_order=desc&limit=5
```

---

## 📊 Data Model

### Claim Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | integer | Auto-increment primary key |
| `title` | string | Required, min 3 characters |
| `category` | enum | `jobs` \| `creativity` \| `environment` \| `education` \| `ethics` |
| `description` | string | Required, min 10 characters |
| `source_url` | URL | Validated by Pydantic `HttpUrl` — rejects malformed URLs |
| `occupation_code` | string | Optional — links claim to occupational exposure dataset |
| `verification_status` | enum | `unverified` \| `reviewed` \| `supported` \| `disputed` |
| `impact_score` | float | Range 0.0–1.0, enforced by Pydantic `Field(ge=0, le=1)` |
| `source_type` | enum | `article` \| `report` \| `blog` \| `research` \| `news` |
| `created_at` | datetime | Server-generated UTC timestamp |

### Example Request Body

```json
{
  "title": "AI changes graphic design work",
  "category": "creativity",
  "description": "Generative AI is reshaping design workflows and speeding up visual content production.",
  "source_url": "https://example.com/design",
  "occupation_code": "2451",
  "verification_status": "reviewed",
  "impact_score": 0.82,
  "source_type": "report"
}
```

### Example Response

```json
{
  "id": 1,
  "title": "AI changes graphic design work",
  "category": "creativity",
  "description": "Generative AI is reshaping design workflows and speeding up visual content production.",
  "source_url": "https://example.com/design",
  "occupation_code": "2451",
  "verification_status": "reviewed",
  "impact_score": 0.82,
  "source_type": "report",
  "created_at": "2026-03-20T12:00:00+00:00"
}
```

### Example Error Responses

```json
// 401 — Missing or invalid API key
{ "detail": "Invalid API key" }

// 404 — Resource not found
{ "detail": "Claim not found" }

// 422 — Validation error (example: impact_score out of range)
{
  "detail": [
    {
      "loc": ["body", "impact_score"],
      "msg": "Input should be less than or equal to 1",
      "type": "less_than_equal"
    }
  ]
}
```

---

## 🧪 Testing

The test suite covers authentication, CRUD, validation edge cases, filtering, and analytics.

```bash
# Run all tests
pytest -q

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run a specific module
pytest tests/test_analytics.py -v
```

**Current status:** 18 tests passing ✅

| Module | What it tests |
|--------|--------------|
| `test_auth.py` | Valid key accepted; missing key returns 401; invalid key returns 401 |
| `test_claims.py` | Full CRUD lifecycle; partial PATCH; 404 on missing ID; enum validation; pagination boundaries |
| `test_analytics.py` | Summary aggregation; category grouping; high-exposure threshold filtering |

Tests use an isolated in-memory SQLite database configured in `conftest.py` — no production data is affected.

---

## 🔄 Continuous Integration

GitHub Actions runs the full test suite automatically on every push to `main` and on pull requests:

```yaml
# .github/workflows/tests.yml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

CI status is visible on the badge at the top of this README.

---

## 🚀 Deployment

Deployed on **Render** with automatic deployment on push to `main`.

| Setting | Value |
|---------|-------|
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Environment variables | `API_KEY`, `DATABASE_URL` — set in Render dashboard (not in repo) |

**Live URLs:**
- API: https://ai-impact-api.onrender.com
- Docs: https://ai-impact-api.onrender.com/docs

---

## ⚠️ Known Limitations

| Limitation | Context |
|------------|---------|
| SQLite concurrency | Not suitable for concurrent write operations; PostgreSQL migration path is via `DATABASE_URL` change only |
| Single API key | No per-user identity or token revocation; JWT is the identified upgrade path |
| Dataset scope | The exposure CSV is a curated subset; analytics are illustrative rather than statistically representative |
| Ephemeral storage | SQLite file on Render does not persist across dyno restarts |

---

## 🔮 Future Improvements

- Migrate to **PostgreSQL** (resolves concurrency and persistence — requires only `DATABASE_URL` change due to SQLAlchemy ORM)
- Replace API key with **JWT authentication** (enables per-user identity and role-based access)
- Add **rate limiting** via `slowapi` (FastAPI-compatible)
- Expand the exposure dataset with the full Frey & Osborne or OECD automation probability dataset
- Add a **frontend dashboard** consuming the analytics endpoints

---

## 📄 Submitted Documents

All submitted materials are available in the `/docs` folder of this repository:

| Document | Location |
|----------|----------|
| API Documentation (Swagger export) | `docs/api-docs.pdf` |
| Technical Report | `docs/technical-report.pdf` |
| GenAI Conversation Logs | `docs/genai-logs/` |
| Presentation Slides | `slides/presentation.pptx` |

---

## 👤 Author

**Hasini Yahampath** — COMP3011 Coursework 1, University of Leeds
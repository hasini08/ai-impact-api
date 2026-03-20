# AI Impact Claims API

A FastAPI-based REST API for storing, managing, and analysing claims about the impact of artificial intelligence on jobs, creativity, education, ethics, and the environment.

This project was developed for coursework and demonstrates backend API development, validation, authentication, testing, analytics, deployment, and structured API design.

---

## Live Deployment

- **Live API:** `https://ai-impact-api.onrender.com`
- **Swagger Docs:** `https://ai-impact-api.onrender.com/docs`
- **Health Check:** `https://ai-impact-api.onrender.com/health`

---

## Project Overview

The purpose of this API is to provide a structured way to record and analyse claims about AI’s societal and occupational impact.

Rather than building only a basic CRUD service, this project includes:

- Full CRUD functionality for claims
- Validation using enums, field constraints, and URL checks
- API key authentication for write operations
- Filtering, search, sorting, and pagination
- Analytics endpoints for category summaries and occupation-level insights
- Automated testing with `pytest`
- Continuous integration using GitHub Actions
- Live deployment on Render

---

## Features

- Create, read, update, and delete AI impact claims
- Categorise claims into:
  - `jobs`
  - `creativity`
  - `environment`
  - `education`
  - `ethics`
- Validate request data using Pydantic
- Require API key authentication for protected endpoints
- Filter claims by category, occupation code, and verification status
- Search claims by keyword
- Sort claims by fields such as impact score
- Paginate claim results using `skip` and `limit`
- Analyse claims by category
- Analyse claims linked to occupational exposure data
- View interactive documentation through Swagger UI

---

## Tech Stack

- **FastAPI** — API framework
- **SQLAlchemy** — ORM and database access
- **SQLite** — relational database for coursework scope
- **Pydantic** — schema validation
- **Pytest** — automated testing
- **GitHub Actions** — continuous integration
- **Render** — deployment platform

---

## Project Structure

```text
ai-impact-api/
├── .github/
│   └── workflows/
│       └── tests.yml
├── docs/
│   ├── api-docs.pdf
│   └── technical-report.pdf
├── scripts/
│   ├── ai_exposure_sample.csv
│   └── import_ai_exposure.py
├── tests/
│   ├── conftest.py
│   ├── test_analytics.py
│   ├── test_auth.py
│   └── test_claims.py
├── .env.example
├── .gitignore
├── database.py
├── main.py
├── models.py
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── schemas.py
└── security.py
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/hasini08/ai-impact-api.git
cd ai-impact-api
```

### 2. Create and activate a virtual environment

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Create the environment variables file

#### macOS / Linux

```bash
cp .env.example .env
```

#### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Make sure your `.env` file contains:

```env
API_KEY=super-secret-coursework-key
DATABASE_URL=sqlite:///./ai_impact.db
```

### 5. Run the API locally

```bash
uvicorn main:app --reload --port 8001
```

Then open:

- **Docs:** `http://127.0.0.1:8001/docs`
- **Health Check:** `http://127.0.0.1:8001/health`

---

## Authentication

Write endpoints require an API key in the request header:

```http
X-API-Key: super-secret-coursework-key
```

### Protected Endpoints

- `POST /claims`
- `PATCH /claims/{claim_id}`
- `DELETE /claims/{claim_id}`

Read-only endpoints such as `GET /claims` and analytics routes do not require authentication.

---

## Data Model

Each claim includes the following fields:

- `id`
- `title`
- `category`
- `description`
- `source_url`
- `occupation_code`
- `verification_status`
- `impact_score`
- `source_type`
- `created_at`

### Category Values

- `jobs`
- `creativity`
- `environment`
- `education`
- `ethics`

### Verification Status Values

- `unverified`
- `reviewed`
- `supported`
- `disputed`

### Source Type Values

- `article`
- `report`
- `blog`
- `research`
- `news`

---

## API Endpoints

### Core Routes

- `GET /` — root endpoint
- `GET /health` — health check
- `POST /claims` — create a claim
- `GET /claims` — retrieve all claims
- `GET /claims/{claim_id}` — retrieve a single claim
- `PATCH /claims/{claim_id}` — update a claim
- `DELETE /claims/{claim_id}` — delete a claim

### Analytics Routes

- `GET /analytics/high-exposure`
- `GET /analytics/by-category`
- `GET /analytics/occupation/{occupation_code}`
- `GET /analytics/summary`

---

## Filtering, Search, Sorting, and Pagination

The `GET /claims` endpoint supports the following query parameters:

- `category`
- `occupation_code`
- `verification_status`
- `search`
- `skip`
- `limit`
- `sort_by`
- `sort_order`

### Example Queries

Filter by category:

```http
/claims?category=creativity
```

Filter by verification status:

```http
/claims?verification_status=reviewed
```

Search by keyword:

```http
/claims?search=design
```

Sort by impact score descending:

```http
/claims?sort_by=impact_score&sort_order=desc
```

Paginate results:

```http
/claims?skip=0&limit=5
```

Combined example:

```http
/claims?category=jobs&verification_status=reviewed&limit=5&sort_by=impact_score&sort_order=desc
```

---

## Example Request

### Create Claim Request Body

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

### Example Successful Response

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

Invalid API key:

```json
{
  "detail": "Invalid API key"
}
```

Missing resource:

```json
{
  "detail": "Claim not found"
}
```

Validation errors such as malformed input, invalid enum values, or bad URLs return a `422 Unprocessable Entity` response.

---

## Analytics

### High Exposure Occupations

**Endpoint:** `GET /analytics/high-exposure`

Returns occupations whose AI exposure score is above a chosen threshold.

Example:

```http
/analytics/high-exposure?min_score=0.7&limit=5
```

### Claims by Category

**Endpoint:** `GET /analytics/by-category`

Returns grouped counts of claims by category.

### Occupation-Level Analytics

**Endpoint:** `GET /analytics/occupation/{occupation_code}`

Returns:

- Occupation code
- Claim count
- Associated claims
- Exposure score
- Occupation title

### Summary Analytics

**Endpoint:** `GET /analytics/summary`

Returns:

- Total number of claims
- Average impact score
- Total number of occupations in the exposure dataset

---

## Testing

This project includes automated tests covering:

- Authentication
- CRUD operations
- Validation and error handling
- Filtering and search
- Analytics endpoints

### Run Tests Locally

```bash
pytest -q
```

### Run Coverage

```bash
pytest --cov=.
```

At the time of writing, the test suite passes with **18 tests**.

---

## Continuous Integration

GitHub Actions is configured to automatically run the test suite on:

- Every push to `main`
- Pull requests targeting `main`

This helps ensure that the API remains stable as the codebase changes.

---

## Deployment

The API is deployed on Render.

### Deployment Details

**Build command**

```bash
pip install -r requirements.txt
```

**Start command**

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Live URLs

- **API:** `https://ai-impact-api.onrender.com`
- **Docs:** `https://ai-impact-api.onrender.com/docs`
- **Health:** `https://ai-impact-api.onrender.com/health`

---

## Limitations

- SQLite is not ideal for large-scale production systems
- API key authentication does not support user accounts or roles
- The dataset is limited and could be expanded
- No frontend dashboard is included

---

## Future Improvements

- Migrate from SQLite to PostgreSQL
- Replace API key authentication with JWT
- Add rate limiting
- Add user accounts and roles
- Expand the dataset
- Build dashboards or visual analytics
- Add more advanced claim credibility metrics

---

## Author

**Student:** Hasini Yahampath   
**Module:** COMP3011 Coursework 1
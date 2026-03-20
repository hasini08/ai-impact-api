# AI Impact Claims API

## Overview

AI Impact Claims API is a data-driven web API that explores the effects of artificial intelligence on jobs, creativity, and the environment.

The project supports full CRUD operations for structured impact claims and includes a sample imported dataset of occupation-level AI exposure scores for simple analytics.

## Features

- Create, read, update, and delete impact claims
- SQL database integration using SQLite
- JSON request and response handling
- Analytics endpoint for high AI exposure occupations
- Interactive API documentation using FastAPI Swagger UI

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite

## Project Structure

- `main.py` - FastAPI routes and endpoint logic
- `database.py` - database connection configuration
- `models.py` - SQLAlchemy models
- `schemas.py` - request and response schemas
- `scripts/import_ai_exposure.py` - sample dataset import script
- `scripts/ai_exposure_sample.csv` - sample AI exposure dataset
- `docs/api-docs.pdf` - API documentation PDF
- `docs/technical-report.pdf` - technical report PDF
- `slides/AI_Impact_Claims_API_Presentation.pptx` - oral presentation slides

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/hasini08/ai-impact-api.git
cd ai-impact-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
uvicorn main:app --reload --port 8001
```

### 4. Open the API documentation

Open this in your browser:

```text
http://127.0.0.1:8001/docs
```

## API Endpoints

### Claims CRUD

- `POST /claims`
- `GET /claims`
- `GET /claims/{claim_id}`
- `PATCH /claims/{claim_id}`
- `DELETE /claims/{claim_id}`

### Analytics

- `GET /analytics/high-exposure`

## Example Request

### Create a claim

**POST** `/claims`

```json
{
  "title": "AI replacing copywriting tasks",
  "category": "jobs",
  "description": "Large language models can automate marketing text generation.",
  "source_url": "https://example.com",
  "occupation_code": "3541"
}
```

## Example Response

```json
{
  "id": 1,
  "title": "AI replacing copywriting tasks",
  "category": "jobs",
  "description": "Large language models can automate marketing text generation.",
  "source_url": "https://example.com",
  "occupation_code": "3541",
  "created_at": "2026-03-20T12:00:00"
}
```

## Example Analytics Response

**GET** `/analytics/high-exposure`

```json
[
  {
    "occupation_code": "2451",
    "occupation_title": "Graphic designers",
    "exposure_score": 0.82
  },
  {
    "occupation_code": "3541",
    "occupation_title": "Writers and authors",
    "exposure_score": 0.79
  }
]
```

## Dataset

This project includes a small sample imported dataset of occupation-level AI exposure scores located in:

```text
scripts/ai_exposure_sample.csv
```

To import the dataset, run:

```bash
python scripts/import_ai_exposure.py
```

## API Documentation

- API documentation PDF: `docs/api-docs.pdf`

## Supporting Documents

- Technical report: `docs/technical-report.pdf`
- Presentation slides: `slides/AI_Impact_Claims_API_Presentation.pptx`

## Notes

This project was developed for COMP3011 Coursework 1 as a data-driven web API with database integration, supporting both CRUD functionality and basic analytics.

## Generative AI Declaration and Reflection

Generative AI tools were used during the planning and development of this project. AI assistance was used for brainstorming the project idea, comparing possible technology stacks, shaping the API structure, troubleshooting implementation issues, and improving documentation.

In particular, AI support was used to:
- compare FastAPI with alternative web frameworks such as Django REST Framework;
- explore suitable database-backed designs for a dissertation-aligned topic;
- refine the schema for the `claims` and `ai_exposure_scores` tables;
- troubleshoot Python import path issues during development of the dataset import script;
- draft and improve README content and supporting coursework documents.

All AI-generated suggestions were treated as advisory rather than authoritative. Final code, documentation, and design choices were reviewed, adapted, and tested manually before inclusion in the submission. The final implementation, structure, and submitted materials reflect the author’s own judgement and verification.

## Testing

This project includes automated tests for authentication, CRUD operations, filtering, and analytics.

### Run tests locally

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest -q
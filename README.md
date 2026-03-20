# AI Impact Claims API

## Overview
This project is a data-driven web API exploring the impact of artificial intelligence on jobs, creativity, and the environment.

## Features
- CRUD operations for impact claims
- SQL database integration
- Analytics endpoint for high AI exposure occupations
- Interactive API documentation via Swagger UI

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Run the application:
   uvicorn main:app --reload --port 8001
4. Open API docs:
   http://127.0.0.1:8001/docs

## Endpoints
- POST /claims
- GET /claims
- GET /claims/{claim_id}
- PATCH /claims/{claim_id}
- DELETE /claims/{claim_id}
- GET /analytics/high-exposure

## Documentation
- API docs PDF: `docs/api-docs.pdf`
- Technical report: `docs/technical-report.pdf`
- Presentation slides: `slides/AI_Impact_Claims_API_Presentation.pptx`

## Dataset
This project includes a sample imported AI exposure dataset in the `scripts` folder for demonstrating analytics functionality.
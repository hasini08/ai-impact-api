# GenAI Log 1 — Framework Architecture Decision

**Tool:** Claude (Anthropic)  
**Date:** March 2026  
**Purpose:** Selecting the API framework and justifying the technology stack  
**Outcome:** Adopted FastAPI; decision documented in technical report Section 2

---

## Conversation

### Prompt

> I am building a data-driven RESTful API for a university module called COMP3011 Web Services and Web Data. The requirements are: full CRUD on a claims resource, Pydantic validation, automatic Swagger documentation, deployment to Render or PythonAnywhere, a suite of analytics endpoints using an imported dataset, and a maximum 5-page technical report. I need to choose between FastAPI and Django REST Framework. Can you compare both for this specific use case and argue for each before making a recommendation?

---

### Claude's Response (summarised)

Claude structured the comparison across five dimensions:

**In favour of Django REST Framework:**
- Larger ecosystem with more third-party packages
- Built-in admin interface for data management
- More established in enterprise environments
- More tutorials and community resources available

**In favour of FastAPI:**
- Automatic OpenAPI/Swagger UI generation at `/docs` with no additional configuration — satisfies the documentation requirement natively
- Native Pydantic v2 integration means validation schemas double as serialisation schemas, eliminating duplication
- ASGI foundation enables async endpoints without a framework rewrite if load requirements grow
- Significantly less boilerplate for API-only projects where Django's ORM and admin are irrelevant
- Type hints throughout improve IDE support and reduce runtime bugs

**Recommendation:** FastAPI for this use case.

Claude also flagged a specific gotcha: Pydantic v2 introduced breaking changes from v1, including renaming `orm_mode = True` to `model_config = ConfigDict(from_attributes=True)`. Many FastAPI tutorials still use the v1 syntax, which would cause silent failures when integrating with SQLAlchemy models.

---

### My Evaluation and Decision

I verified the Pydantic v2 breaking change by checking the official migration guide at https://docs.pydantic.dev/latest/migration/. The warning was accurate — the v1 syntax would have caused an integration bug with SQLAlchemy that would have been difficult to diagnose.

I also cross-referenced FastAPI's documentation to confirm that Swagger UI is generated automatically at `/docs` without any additional library (unlike DRF which requires `drf-spectacular` or similar).

**Decision adopted:** FastAPI with SQLAlchemy and SQLite. The Pydantic v2 warning directly prevented a debugging issue during development.

**Decision rejected:** Django REST Framework — the admin interface and broader ORM ecosystem provide no benefit for an API-only project without a frontend.

---

## Impact on Project

- FastAPI was selected as the application framework (documented in `main.py` and technical report Section 2)
- The Pydantic v2 `ConfigDict` pattern was used throughout `schemas.py` from the start
- The technology stack justification in the technical report directly references the trade-offs surfaced in this conversation

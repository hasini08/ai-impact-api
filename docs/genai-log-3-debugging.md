# GenAI Log 3 — Debugging SQLAlchemy DetachedInstanceError

**Tool:** Claude (Anthropic)  
**Date:** March 2026  
**Purpose:** Diagnosing and resolving intermittent 500 errors on analytics endpoints  
**Outcome:** Root cause identified; `joinedload()` fix adopted and verified; documented in technical report Section 9.3

---

## Conversation

### Context

After deploying the `/analytics/occupation/{occupation_code}` endpoint, it raised intermittent `DetachedInstanceError` exceptions when returning responses. The error did not appear consistently — it occurred only when the SQLAlchemy session had closed before the response was serialised.

---

### Prompt

> I am getting the following error on my `/analytics/occupation/{code}` endpoint in FastAPI with SQLAlchemy:
>
> ```
> sqlalchemy.orm.exc.DetachedInstanceError: Instance <Claim at 0x...> is not bound
> to a Session; attribute refresh operation cannot proceed (Background on this error
> at: https://sqlalche.me/e/14/bhk3)
> ```
>
> The error occurs when serialising the response after the SQLAlchemy session has closed. Here is the query:
>
> ```python
> def get_claims_by_occupation(db: Session, occupation_code: str):
>     return db.query(Claim).filter(
>         Claim.occupation_code == occupation_code
>     ).all()
> ```
>
> And the endpoint:
>
> ```python
> @app.get("/analytics/occupation/{occupation_code}")
> def analytics_by_occupation(occupation_code: str, db: Session = Depends(get_db)):
>     claims = get_claims_by_occupation(db, occupation_code)
>     exposure = db.query(AIExposureScore).filter(
>         AIExposureScore.occupation_code == occupation_code
>     ).first()
>     return {
>         "occupation_code": occupation_code,
>         "claims": claims,
>         "exposure_score": exposure.exposure_score if exposure else None,
>         "occupation_title": exposure.occupation_title if exposure else None
>     }
> ```
>
> What is causing this and what are my options for fixing it?

---

### Claude's Response (summarised)

**Root cause:** The `DetachedInstanceError` occurs because SQLAlchemy uses lazy loading by default for relationships and certain attribute accesses. When the session dependency (`get_db`) closes the session after the function returns, any subsequent access to lazily-loaded attributes on the returned ORM objects raises this error. FastAPI's response serialisation happens after the route function returns, which is after the session closes — so attributes accessed during serialisation trigger the error.

**Option 1 — Use `joinedload()` (recommended)**
Instruct SQLAlchemy to eagerly load all required data within the session using `joinedload()`. This performs a SQL JOIN within the same session, so all attributes are populated before the session closes.

```python
from sqlalchemy.orm import joinedload

def get_claims_by_occupation(db: Session, occupation_code: str):
    return db.query(Claim).options(
        joinedload(Claim.some_relationship)
    ).filter(
        Claim.occupation_code == occupation_code
    ).all()
```

Advantage: single query, all data loaded within session scope.

**Option 2 — Access attributes before session closes**
Explicitly access any attributes that will be needed during serialisation before the session dependency releases the session.

Advantage: no query change required.
Disadvantage: increases coupling between the route handler and serialisation logic; fragile if new attributes are added.

**Option 3 — Extend session scope**
Configure the session to remain open during response serialisation using `expire_on_commit=False`.

Disadvantage: can mask stale data issues; not recommended for production patterns.

Claude recommended Option 1 as the most robust and idiomatic SQLAlchemy solution for this pattern.

---

### My Evaluation and Decision

I tested Option 1 by adding `joinedload()` to the affected query and running the full test suite. The `DetachedInstanceError` was resolved and all 18 tests passed.

I also reviewed Option 2 — accessing attributes before session close — and decided against it because it would require the route handler to know which fields the serialiser would access, creating a maintenance dependency that could break silently if the response schema changed.

Option 3 was rejected outright because `expire_on_commit=False` could allow stale cached attribute values to appear in responses after concurrent writes.

**Decision adopted:** Option 1 (`joinedload()`)

---

### One Suggestion That Was Rejected

Claude also suggested storing the entire SQLAlchemy result as a dictionary before session close using `.dict()` style conversion. I rejected this because it would bypass Pydantic's serialisation and lose the schema validation guarantees on the response model.

---

## Impact on Project

- `joinedload()` was implemented in the affected analytics queries in `main.py`
- The fix was confirmed by running `pytest -q` and verifying all 18 tests pass
- The debugging process and resolution is documented in technical report Sections 9.3 and 10

# GenAI Log 2 — Validation Schema Design (Hostile Review)

**Tool:** Claude (Anthropic)  
**Date:** March 2026  
**Purpose:** Identifying gaps and weaknesses in the Pydantic validation schema  
**Outcome:** Two schema improvements adopted; documented in technical report Section 9.2

---

## Conversation

### Prompt

> Here is my initial ClaimCreate Pydantic schema for a claims API:
>
> ```python
> class ClaimCreate(BaseModel):
>     title: str
>     category: str
>     description: str
>     source_url: str
>     occupation_code: Optional[str] = None
>     verification_status: str
>     impact_score: float
>     source_type: str
> ```
>
> Act as a hostile API consumer trying to submit inputs that technically pass validation but produce bad or misleading data. What would you try, and how should the schema be tightened to prevent it?

---

### Claude's Response (summarised)

Claude identified five exploitable weaknesses:

**1. `source_url: str` accepts anything**
A plain string field accepts `"not-a-url"`, `"http://"`, `""`, or `"banana"`. These would be stored silently and appear in responses as legitimate sources, undermining the credibility of the dataset.
*Fix:* Use Pydantic's `HttpUrl` type — it validates scheme, host, and structure automatically and returns a 422 for anything that doesn't conform.

**2. `impact_score: float` has no bounds**
Values above 1.0 (e.g. `99.5`) or below 0.0 (e.g. `-0.5`) would be stored and included in `average_impact_score` calculations in `/analytics/summary`, silently distorting results.
*Fix:* Use `Field(ge=0.0, le=1.0)` to enforce the intended 0–1 range.

**3. `category: str` and `verification_status: str` are free text**
A consumer could submit `"Jobs"`, `"JOBS"`, or `"j0bs"` for category. These would be stored as distinct values, breaking the `GET /analytics/by-category` grouping which relies on consistent values.
*Fix:* Use Python `Enum` classes for all controlled vocabulary fields — Pydantic will reject anything outside the defined set.

**4. No minimum length on `title` or `description`**
A consumer could submit a single space for both fields, which would pass validation but produce useless records.
*Fix:* Add `Field(min_length=3)` on title and `Field(min_length=10)` on description.

**5. No `ClaimUpdate` schema for partial updates**
Using `ClaimCreate` for PATCH would require clients to submit all fields even when updating one, and would overwrite omitted fields with default values silently.
*Fix:* Create a separate `ClaimUpdate` schema where every field is `Optional` so only provided fields are updated.

---

### My Evaluation and Decision

I tested each suggested fix by writing a small validation test before implementing it in the codebase:

| Suggestion | Adopted? | Reason |
|------------|----------|--------|
| `HttpUrl` for `source_url` | ✅ Yes | Verified it rejects `"not-a-url"` with 422; zero custom code required |
| `Field(ge=0.0, le=1.0)` for `impact_score` | ✅ Yes | Tested boundary values 0.0, 1.0 (pass) and -0.1, 1.1 (fail correctly) |
| Enum for `category`, `verification_status`, `source_type` | ✅ Yes | Implemented `CategoryEnum`, `VerificationStatusEnum`, `SourceTypeEnum` in `schemas.py` |
| `Field(min_length=...)` on title and description | ✅ Yes | Added min_length=3 and min_length=10 respectively |
| Separate `ClaimUpdate` schema | ✅ Yes | Implemented with all Optional fields; PATCH endpoint now only writes provided fields |

One suggestion was not adopted: Claude suggested adding a `max_length` constraint on `description`. I decided against this because the domain doesn't have a natural upper bound for descriptions and a hard limit could frustrate legitimate users submitting detailed claims.

---

## Impact on Project

- `schemas.py` was rewritten to use `HttpUrl`, enums, and field constraints
- `ClaimUpdate` schema with all-Optional fields was added, enabling correct REST partial-update semantics on `PATCH /claims/{id}`
- The validation strategy is documented in technical report Section 5

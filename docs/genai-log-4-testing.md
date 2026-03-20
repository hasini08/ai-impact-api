# GenAI Log 4 — Test Coverage Gap Analysis

**Tool:** Claude (Anthropic)  
**Date:** March 2026  
**Purpose:** Identifying missing test scenarios after completing initial test suite  
**Outcome:** 4 of 6 identified gaps addressed; 2 deprioritised; documented in technical report Section 9.4

---

## Conversation

### Context

After writing an initial test suite covering basic CRUD and authentication, I asked Claude to act as a code reviewer and identify scenarios that were not covered.

---

### Prompt

> Here is my current pytest test suite for my FastAPI claims API. Act as a code reviewer. Identify any test scenarios that are missing — focus on edge cases, boundary conditions, and failure paths that my current tests do not cover.
>
> ```python
> # test_auth.py
> def test_create_claim_without_api_key(client):
>     response = client.post("/claims", json={...})
>     assert response.status_code == 401
>
> def test_create_claim_with_valid_api_key(client):
>     response = client.post("/claims", json={...}, headers={"X-API-Key": "test-key"})
>     assert response.status_code == 201
>
> # test_claims.py
> def test_create_claim(client):
>     response = client.post("/claims", json={...}, headers={...})
>     assert response.status_code == 201
>
> def test_get_claims(client):
>     response = client.get("/claims")
>     assert response.status_code == 200
>
> def test_get_claim_by_id(client):
>     response = client.get("/claims/1")
>     assert response.status_code == 200
>
> def test_update_claim(client):
>     response = client.patch("/claims/1", json={"title": "Updated"}, headers={...})
>     assert response.status_code == 200
>
> def test_delete_claim(client):
>     response = client.delete("/claims/1", headers={...})
>     assert response.status_code == 204
> ```

---

### Claude's Response (summarised)

Claude identified six missing scenarios:

**Gap 1 — GET non-existent ID returns 404**
The current tests only test GET on an ID that exists. There is no test confirming that `GET /claims/9999` returns 404. Without this, a bug that returns 500 or 200 with null data for missing IDs would not be caught.

**Gap 2 — DELETE on already-deleted ID returns 404**
After `DELETE /claims/1`, a second `DELETE /claims/1` should return 404. The current test only checks the first delete. A bug that returns 204 on repeated deletes (e.g. no existence check) would not be caught.

**Gap 3 — Filter returning no results returns empty list, not 404**
`GET /claims?category=ethics` when no ethics claims exist should return `[]` with status 200, not a 404. This is a common REST semantics mistake — 404 means the endpoint doesn't exist, not that no records matched.

**Gap 4 — PATCH with invalid enum value returns 422**
`PATCH /claims/1` with `{"category": "invalid_category"}` should return 422. Without this test, a regression that accepts invalid enum values in updates would not be caught.

**Gap 5 — Pagination boundary: skip=0 limit=1**
The current tests never test pagination parameters. `GET /claims?skip=0&limit=1` should return exactly one claim. This tests that the pagination logic doesn't accidentally return all records when limit=1 is specified.

**Gap 6 — impact_score boundary values 0.0 and 1.0**
The exact boundary values for `impact_score` should be tested — `0.0` and `1.0` should pass, while `-0.1` and `1.1` should return 422. Without boundary tests, an off-by-one error in the validation constraint would not be caught.

---

### My Evaluation and Decision

I reviewed each gap and categorised them by priority:

| Gap | Adopted? | Reason |
|-----|----------|--------|
| GET 404 for missing ID | ✅ Yes | High risk — missing this could mask a serious regression |
| DELETE 404 on repeat | ✅ Yes | Important for data integrity semantics |
| Filter empty list vs 404 | ✅ Yes | Common REST mistake; important to pin correct behaviour |
| PATCH invalid enum 422 | ✅ Yes | Directly tests validation on the update path |
| Pagination skip=0 limit=1 | ✅ Yes | Added as part of a broader pagination boundary test |
| impact_score boundaries | ❌ Deprioritised | Lower risk given Pydantic Field constraints are already tested via the schema; deferred due to time |

The unauthenticated DELETE test suggested in gap 2 was also extended to cover unauthenticated PATCH, which was not in my original auth tests.

---

### One Suggestion That Was Modified

Claude suggested testing `GET /claims?skip=100&limit=10` when fewer than 100 records exist as a pagination edge case. I modified this slightly — rather than using a fixed skip value, I wrote the test to seed exactly 3 records and then assert that `skip=5&limit=10` returns an empty list. This is more robust because it doesn't depend on the number of records in the test database.

---

## Impact on Project

- 5 new test scenarios added to `test_claims.py` and `test_auth.py`
- Total test count increased from 13 to 18
- All 18 tests pass confirmed via `pytest -q`
- The gap analysis process is documented in technical report Section 9.4

---

## GenAI Declaration Summary

This file is one of four conversation logs demonstrating the use of Generative AI during this project. All suggestions were independently evaluated and tested before adoption. No code was copied directly from any GenAI response without independent implementation. GenAI tool used: Claude (Anthropic). All usage declared in accordance with the COMP3011 Green Light Assessment policy.

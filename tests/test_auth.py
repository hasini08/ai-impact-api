def valid_claim_payload():
    return {
        "title": "AI changes graphic design work",
        "category": "creativity",
        "description": "Generative AI is reshaping design workflows and speeding up visual content production.",
        "source_url": "https://example.com/design",
        "occupation_code": "2451",
        "verification_status": "reviewed",
        "impact_score": 0.82,
        "source_type": "report",
    }


def test_post_claim_requires_api_key(client):
    response = client.post("/claims", json=valid_claim_payload())
    assert response.status_code == 401
    assert "Missing" in response.json()["detail"] or "Invalid" in response.json()["detail"]


def test_post_claim_rejects_invalid_api_key(client):
    response = client.post(
        "/claims",
        json=valid_claim_payload(),
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_post_claim_accepts_valid_api_key(client):
    response = client.post(
        "/claims",
        json=valid_claim_payload(),
        headers={"X-API-Key": "super-secret-coursework-key"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "AI changes graphic design work"
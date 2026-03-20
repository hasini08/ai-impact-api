def create_sample_claim(client):
    payload = {
        "title": "AI affects software testing",
        "category": "jobs",
        "description": "AI tools are changing software testing processes across development teams.",
        "source_url": "https://example.com/testing",
        "occupation_code": "2133",
        "verification_status": "reviewed",
        "impact_score": 0.76,
        "source_type": "research",
    }
    response = client.post(
        "/claims",
        json=payload,
        headers={"X-API-Key": "super-secret-coursework-key"},
    )
    assert response.status_code == 201
    return response.json()


def test_create_claim_success(client):
    payload = {
        "title": "AI affects teachers",
        "category": "education",
        "description": "AI tools are beginning to change lesson planning and assessment workflows.",
        "source_url": "https://example.com/education",
        "occupation_code": "2314",
        "verification_status": "unverified",
        "impact_score": 0.61,
        "source_type": "article",
    }
    response = client.post(
        "/claims",
        json=payload,
        headers={"X-API-Key": "super-secret-coursework-key"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["category"] == payload["category"]
    assert body["verification_status"] == payload["verification_status"]


def test_create_claim_invalid_payload_returns_422(client):
    payload = {
        "title": "Bad",
        "category": "not-valid",
        "description": "short",
        "source_url": "not-a-url",
    }
    response = client.post(
        "/claims",
        json=payload,
        headers={"X-API-Key": "super-secret-coursework-key"},
    )
    assert response.status_code == 422


def test_get_all_claims(client):
    create_sample_claim(client)
    response = client.get("/claims")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1


def test_get_single_claim(client):
    created = create_sample_claim(client)
    claim_id = created["id"]

    response = client.get(f"/claims/{claim_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == claim_id


def test_get_missing_claim_returns_404(client):
    response = client.get("/claims/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"


def test_update_claim_success(client):
    created = create_sample_claim(client)
    claim_id = created["id"]

    response = client.patch(
        f"/claims/{claim_id}",
        json={
            "verification_status": "supported",
            "impact_score": 0.91,
        },
        headers={"X-API-Key": "super-secret-coursework-key"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["verification_status"] == "supported"
    assert body["impact_score"] == 0.91


def test_update_missing_claim_returns_404(client):
    response = client.patch(
        "/claims/99999",
        json={"verification_status": "supported"},
        headers={"X-API-Key": "super-secret-coursework-key"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"


def test_delete_claim_success(client):
    created = create_sample_claim(client)
    claim_id = created["id"]

    delete_response = client.delete(
        f"/claims/{claim_id}",
        headers={"X-API-Key": "super-secret-coursework-key"},
    )
    assert delete_response.status_code == 204

    get_response = client.get(f"/claims/{claim_id}")
    assert get_response.status_code == 404


def test_delete_missing_claim_returns_404(client):
    response = client.delete(
        "/claims/99999",
        headers={"X-API-Key": "super-secret-coursework-key"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"


def test_claim_filters_by_category(client):
    create_sample_claim(client)

    response = client.get("/claims?category=jobs")
    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 1
    assert all(item["category"] == "jobs" for item in body)


def test_claim_search(client):
    create_sample_claim(client)

    response = client.get("/claims?search=testing")
    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 1
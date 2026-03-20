from models import AIExposureScore


def create_claim_for_analytics(client):
    payload = {
        "title": "AI impacts designers",
        "category": "creativity",
        "description": "AI image generation tools are affecting design-related tasks.",
        "source_url": "https://example.com/designers",
        "occupation_code": "2451",
        "verification_status": "reviewed",
        "impact_score": 0.88,
        "source_type": "report",
    }
    response = client.post(
        "/claims",
        json=payload,
        headers={"X-API-Key": "super-secret-coursework-key"},
    )
    assert response.status_code == 201
    return response.json()


def seed_exposure_data(db_session):
    row = AIExposureScore(
        occupation_code="2451",
        occupation_title="Graphic Designers",
        exposure_score=0.84,
    )
    db_session.add(row)
    db_session.commit()


def test_high_exposure_returns_results(client, db_session):
    seed_exposure_data(db_session)

    response = client.get("/analytics/high-exposure?min_score=0.7&limit=5")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    assert body[0]["occupation_code"] == "2451"


def test_claims_by_category(client):
    create_claim_for_analytics(client)

    response = client.get("/analytics/by-category")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(item["category"] == "creativity" for item in body)


def test_analytics_by_occupation(client, db_session):
    create_claim_for_analytics(client)
    seed_exposure_data(db_session)

    response = client.get("/analytics/occupation/2451")
    assert response.status_code == 200
    body = response.json()
    assert body["occupation_code"] == "2451"
    assert body["claim_count"] >= 1
    assert body["occupation_title"] == "Graphic Designers"
    assert body["exposure_score"] == 0.84


def test_analytics_summary(client, db_session):
    create_claim_for_analytics(client)
    seed_exposure_data(db_session)

    response = client.get("/analytics/summary")
    assert response.status_code == 200
    body = response.json()
    assert "total_claims" in body
    assert "average_impact_score" in body
    assert "total_occupations" in body
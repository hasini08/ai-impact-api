from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import AIExposureScore, Claim
from schemas import (
    AIExposureOut,
    CategoryCountOut,
    ClaimCreate,
    ClaimOut,
    ClaimUpdate,
    SummaryOut,
)
from security import require_api_key


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Impact Claims API",
    description="A data-driven FastAPI project exploring AI's impact on jobs, creativity, and the environment.",
    version="1.2.0",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/claims", response_model=ClaimOut, status_code=status.HTTP_201_CREATED)
def create_claim(
    claim: ClaimCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    db_claim = Claim(
        title=claim.title,
        category=claim.category.value,
        description=claim.description,
        source_url=str(claim.source_url),
        occupation_code=claim.occupation_code,
        created_at=datetime.utcnow().isoformat(),
        verification_status=claim.verification_status.value,
        impact_score=claim.impact_score,
        source_type=claim.source_type.value,
    )

    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim


@app.get("/claims", response_model=list[ClaimOut])
def get_claims(
    category: str | None = None,
    occupation_code: str | None = None,
    verification_status: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("id"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
):
    query = db.query(Claim)

    if category:
        query = query.filter(Claim.category == category)

    if occupation_code:
        query = query.filter(Claim.occupation_code == occupation_code)

    if verification_status:
        query = query.filter(Claim.verification_status == verification_status)

    if search:
        query = query.filter(
            (Claim.title.ilike(f"%{search}%")) |
            (Claim.description.ilike(f"%{search}%"))
        )

    allowed_sort_fields = {
        "id": Claim.id,
        "title": Claim.title,
        "category": Claim.category,
        "created_at": Claim.created_at,
        "impact_score": Claim.impact_score,
    }

    sort_column = allowed_sort_fields.get(sort_by, Claim.id)

    if sort_order.lower() == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    return query.offset(skip).limit(limit).all()


@app.get("/claims/{claim_id}", response_model=ClaimOut)
def get_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")

    return claim


@app.patch("/claims/{claim_id}", response_model=ClaimOut)
def update_claim(
    claim_id: int,
    update: ClaimUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")

    update_data = update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(value, "value"):
            setattr(claim, field, value.value)
        elif field == "source_url" and value is not None:
            setattr(claim, field, str(value))
        else:
            setattr(claim, field, value)

    db.commit()
    db.refresh(claim)
    return claim


@app.delete("/claims/{claim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")

    db.delete(claim)
    db.commit()
    return None


@app.get("/analytics/high-exposure", response_model=list[AIExposureOut])
def high_exposure(
    min_score: float = Query(0.7, ge=0, le=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    results = (
        db.query(AIExposureScore)
        .filter(AIExposureScore.exposure_score >= min_score)
        .order_by(AIExposureScore.exposure_score.desc())
        .limit(limit)
        .all()
    )

    return results


@app.get("/analytics/by-category", response_model=list[CategoryCountOut])
def claims_by_category(db: Session = Depends(get_db)):
    results = (
        db.query(Claim.category, func.count(Claim.id).label("count"))
        .group_by(Claim.category)
        .order_by(func.count(Claim.id).desc())
        .all()
    )

    return [{"category": row.category, "count": row.count} for row in results]


@app.get("/analytics/occupation/{occupation_code}")
def analytics_by_occupation(occupation_code: str, db: Session = Depends(get_db)):
    claims = db.query(Claim).filter(Claim.occupation_code == occupation_code).all()
    exposure = (
        db.query(AIExposureScore)
        .filter(AIExposureScore.occupation_code == occupation_code)
        .first()
    )

    return {
        "occupation_code": occupation_code,
        "claim_count": len(claims),
        "claims": claims,
        "exposure_score": exposure.exposure_score if exposure else None,
        "occupation_title": exposure.occupation_title if exposure else None,
    }


@app.get("/analytics/summary", response_model=SummaryOut)
def analytics_summary(db: Session = Depends(get_db)):
    total_claims = db.query(func.count(Claim.id)).scalar() or 0
    avg_impact = db.query(func.avg(Claim.impact_score)).scalar() or 0.0
    total_occupations = db.query(func.count(AIExposureScore.id)).scalar() or 0

    return {
        "total_claims": total_claims,
        "average_impact_score": round(float(avg_impact), 2),
        "total_occupations": total_occupations,
    }
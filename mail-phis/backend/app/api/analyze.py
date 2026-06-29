import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.analysis import Analysis, AnalysisType, AnalysisStatus
from app.utils.validators import validate_url, validate_eml_size
from app.workers.tasks import run_email_pipeline, run_url_pipeline
from pydantic import BaseModel

router = APIRouter(tags=["analyze"])


class URLRequest(BaseModel):
    url: str


@router.post("/analyze/email")
async def analyze_email(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    try:
        validate_eml_size(len(content))
    except ValueError as e:
        raise HTTPException(status_code=413, detail=str(e))

    analysis_id = str(uuid.uuid4())
    analysis = Analysis(
        id=analysis_id,
        type=AnalysisType.EMAIL,
        target=file.filename or "upload.eml",
        status=AnalysisStatus.PENDING,
    )
    db.add(analysis)
    await db.commit()

    run_email_pipeline.apply_async(
        args=[analysis_id, content.hex()],
        queue="email",
    )
    return {"analysis_id": analysis_id, "status": "pending"}


@router.post("/analyze/url")
async def analyze_url(
    body: URLRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        url = validate_url(body.url)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    analysis_id = str(uuid.uuid4())
    analysis = Analysis(
        id=analysis_id,
        type=AnalysisType.URL,
        target=url,
        status=AnalysisStatus.PENDING,
    )
    db.add(analysis)
    await db.commit()

    run_url_pipeline.apply_async(
        args=[analysis_id, url],
        queue="url",
    )
    return {"analysis_id": analysis_id, "status": "pending"}


@router.get("/analysis/{analysis_id}")
async def get_analysis_status(
    analysis_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {
        "analysis_id": analysis.id,
        "status": analysis.status,
        "verdict": analysis.verdict,
        "score": analysis.score,
        "created_at": analysis.created_at,
        "completed_at": analysis.completed_at,
    }


@router.get("/analyses")
async def list_analyses(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Analysis).order_by(Analysis.created_at.desc()).limit(limit)
    )
    analyses = result.scalars().all()
    return [
        {
            "analysis_id": a.id,
            "type": a.type,
            "target": a.target,
            "status": a.status,
            "verdict": a.verdict,
            "score": a.score,
            "created_at": a.created_at,
        }
        for a in analyses
    ]

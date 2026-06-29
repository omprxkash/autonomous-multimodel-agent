import json
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.analysis import Analysis, AnalysisStatus

router = APIRouter(tags=["reports"])


@router.get("/report/{analysis_id}")
async def get_report(
    analysis_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Report not found")
    if analysis.status not in (AnalysisStatus.COMPLETE, AnalysisStatus.FAILED):
        raise HTTPException(status_code=202, detail="Analysis still running")

    return {
        "analysis_id": analysis.id,
        "type": analysis.type,
        "target": analysis.target,
        "verdict": analysis.verdict,
        "score": analysis.score,
        "completed_at": analysis.completed_at,
        "pipeline": analysis.pipeline_results or {},
        "top_features": _top_features(analysis.feature_vector),
        "iocs": analysis.iocs or {},
        "error": analysis.error,
    }


@router.get("/report/{analysis_id}/export")
async def export_report(
    analysis_id: str,
    format: str = "json",
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Report not found")

    iocs = analysis.iocs or {}

    if format == "json":
        return Response(
            content=json.dumps(iocs, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{analysis_id}.json"'},
        )
    elif format == "csv":
        rows = ["type,value"]
        for ioc_type, values in iocs.items():
            for v in (values if isinstance(values, list) else [values]):
                rows.append(f"{ioc_type},{v}")
        return Response(
            content="\n".join(rows),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{analysis_id}.csv"'},
        )
    elif format == "stix2":
        bundle = _build_stix2_bundle(analysis_id, iocs)
        return Response(
            content=json.dumps(bundle, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{analysis_id}.stix2.json"'},
        )
    else:
        raise HTTPException(status_code=400, detail="format must be json, csv, or stix2")


def _top_features(feature_vector: dict | None, n: int = 10) -> list[dict]:
    if not feature_vector:
        return []
    sorted_features = sorted(feature_vector.items(), key=lambda x: abs(x[1]), reverse=True)
    return [{"feature": k, "weight": v} for k, v in sorted_features[:n]]


def _build_stix2_bundle(analysis_id: str, iocs: dict) -> dict:
    import uuid as _uuid
    indicators = []
    for ioc_type, values in iocs.items():
        for v in (values if isinstance(values, list) else [values]):
            indicators.append({
                "type": "indicator",
                "id": f"indicator--{_uuid.uuid4()}",
                "spec_version": "2.1",
                "name": f"{ioc_type}: {v}",
                "pattern": f"[{ioc_type}:value = '{v}']",
                "pattern_type": "stix",
                "valid_from": "2024-01-01T00:00:00Z",
            })
    return {
        "type": "bundle",
        "id": f"bundle--{analysis_id}",
        "spec_version": "2.1",
        "objects": indicators,
    }

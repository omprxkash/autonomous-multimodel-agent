from __future__ import annotations
from pathlib import Path
from typing import TypedDict
import yaml

from pipeline.enricher import EnrichedLead

CONFIG_PATH = Path(__file__).parent.parent / "data" / "icp_config.yaml"


class ScoreResult(TypedDict):
    score: int
    breakdown: dict[str, dict]


def _load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def score(lead: EnrichedLead, config: dict | None = None) -> ScoreResult:
    if config is None:
        config = _load_config()

    weights = config["weights"]
    ideal = config["ideal"]

    breakdown: dict[str, dict] = {}

    # --- industry_match (30 pts) ---
    matched_industry = lead.industry_category in ideal["industries"]
    industry_pts = weights["industry_match"] if matched_industry else 0
    breakdown["industry_match"] = {
        "points": industry_pts,
        "max": weights["industry_match"],
        "matched": matched_industry,
        "value": lead.industry_category,
    }

    # --- size_fit (25 pts) ---
    ec = lead.employee_count
    size_pts = 0
    if ec is not None:
        if ideal["size_min"] <= ec <= ideal["size_max"]:
            size_pts = weights["size_fit"]
        elif ec < ideal["size_min"]:
            size_pts = round(weights["size_fit"] * 0.4)
        else:
            size_pts = round(weights["size_fit"] * 0.1)
    breakdown["size_fit"] = {
        "points": size_pts,
        "max": weights["size_fit"],
        "value": ec,
        "bucket": lead.size_bucket,
    }

    # --- seniority (20 pts) ---
    sen_match = lead.seniority in ideal["seniorities"]
    sen_pts = weights["seniority"] if sen_match else (
        round(weights["seniority"] * 0.5) if lead.seniority in ("manager", "lead") else 0
    )
    breakdown["seniority"] = {
        "points": sen_pts,
        "max": weights["seniority"],
        "matched": sen_match,
        "value": lead.seniority,
    }

    # --- tech_match (15 pts) ---
    ideal_tech = set(ideal["tech"])
    lead_tech = set(lead.tech_stack)
    overlap = ideal_tech & lead_tech
    tech_ratio = len(overlap) / len(ideal_tech) if ideal_tech else 0
    tech_pts = round(weights["tech_match"] * tech_ratio)
    breakdown["tech_match"] = {
        "points": tech_pts,
        "max": weights["tech_match"],
        "matched": sorted(overlap),
        "value": sorted(lead_tech),
    }

    # --- geo_fit (10 pts) ---
    geo_match = lead.region in ideal["regions"]
    geo_pts = weights["geo_fit"] if geo_match else 0
    breakdown["geo_fit"] = {
        "points": geo_pts,
        "max": weights["geo_fit"],
        "matched": geo_match,
        "value": lead.region,
    }

    total = industry_pts + size_pts + sen_pts + tech_pts + geo_pts
    return ScoreResult(score=min(total, 100), breakdown=breakdown)


def score_all(leads: list[EnrichedLead]) -> list[tuple[EnrichedLead, ScoreResult]]:
    config = _load_config()
    return [(lead, score(lead, config)) for lead in leads]


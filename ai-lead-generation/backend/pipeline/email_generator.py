from __future__ import annotations
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from pipeline.enricher import EnrichedLead

TEMPLATES_DIR = Path(__file__).parent.parent / "data" / "email_templates"

_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=False)

SENDER_NAME = os.environ.get("SENDER_NAME", "Om")

_PAIN_POINTS: dict[str, str] = {
    "saas": "scaling customer onboarding without growing the ops team",
    "fintech": "reducing friction in the payment and compliance workflow",
    "devtools": "cutting release cycle time while keeping quality high",
    "data": "turning raw pipeline output into decisions teams actually trust",
    "cloud": "keeping infrastructure costs predictable as you scale",
    "ecommerce": "converting more sessions without bloating the tech stack",
    "other": "moving faster without adding complexity",
}

_SUBJECTS: dict[str, str] = {
    "hot_founder": "Quick idea for {company}",
    "warm_founder": "Loved learning about {company}",
    "warm_vp": "Worth a quick chat?",
    "cold_director": "One thing for {company}",
}


def _pick_template(score: int, seniority: str) -> str:
    is_founder = seniority in ("founder",)
    is_senior = seniority in ("vp", "head", "director", "chief")

    if score >= 70:
        return "hot_founder" if is_founder else "warm_vp"
    if score >= 45:
        return "warm_founder" if is_founder else "warm_vp"
    return "warm_founder" if is_founder else "cold_director"


def generate(lead: EnrichedLead, score: int) -> str:
    template_key = _pick_template(score, lead.seniority)
    template_file = f"{template_key}.j2"
    subject = _SUBJECTS.get(template_key, "Quick note").format(company=lead.company)
    pain_point = _PAIN_POINTS.get(lead.industry_category, _PAIN_POINTS["other"])

    try:
        template = _env.get_template(template_file)
    except Exception:
        template = _env.get_template("cold_director.j2")

    return template.render(
        first_name=lead.first_name,
        company=lead.company,
        industry=lead.industry_category,
        pain_point=pain_point,
        sender_name=SENDER_NAME,
        subject=subject,
    )


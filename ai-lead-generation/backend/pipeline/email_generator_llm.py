from __future__ import annotations
import os
from pipeline.enricher import EnrichedLead

_PAIN_POINTS: dict[str, str] = {
    "saas": "scaling customer onboarding without growing the ops team",
    "fintech": "reducing friction in the payment and compliance workflow",
    "devtools": "cutting release cycle time while keeping quality high",
    "data": "turning raw pipeline output into decisions teams actually trust",
    "cloud": "keeping infrastructure costs predictable as you scale",
    "ecommerce": "converting more sessions without bloating the tech stack",
    "other": "moving faster without adding complexity",
}


def _build_llm():
    provider = os.getenv("ACTIVE_LLM_PROVIDER", "gemini")
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0.7,
                          openai_api_key=os.getenv("OPENAI_API_KEY", ""))
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
                                  temperature=0.7,
                                  google_api_key=os.getenv("GEMINI_API_KEY", ""))


def generate_llm(lead: EnrichedLead, score: int, score_breakdown: dict) -> str:
    """Generate a personalised outreach email using an LLM."""
    from langchain_core.messages import HumanMessage, SystemMessage

    pain_point = _PAIN_POINTS.get(lead.industry_category, _PAIN_POINTS["other"])
    top_factors = sorted(
        score_breakdown.items(),
        key=lambda kv: kv[1]["points"] if isinstance(kv[1], dict) else 0,
        reverse=True,
    )[:2]
    factor_notes = "; ".join(
        f"{k} ({v['points']}/{v['max']} pts)" for k, v in top_factors if isinstance(v, dict)
    )

    system = SystemMessage(content=(
        "You are an expert B2B sales copywriter. Write short, direct cold outreach emails. "
        "No generic openers. No 'I hope this email finds you well'. Never mention AI or tools. "
        "Sound like a real person."
    ))
    human = HumanMessage(content=f"""Write a cold outreach email for this prospect.

Company: {lead.company}
Contact: {lead.first_name} ({lead.title})
Industry: {lead.industry_category}
ICP fit score: {score}/100 (top factors: {factor_notes})
Key pain point for this industry: {pain_point}
Tech stack: {', '.join(lead.tech_stack[:4]) or 'unknown'}

Requirements:
- Subject line on the first line, then a blank line, then the email body
- 3–4 sentences max in the body
- Reference the company or role specifically
- End with a soft CTA (e.g. "Worth a quick call?")
- Sign off as: Om""")

    llm = _build_llm()
    result = llm.invoke([system, human])
    return result.content.strip()

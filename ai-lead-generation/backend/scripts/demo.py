"""
End-to-end demo: one lead through the full pipeline.
Usage: cd ai-lead-generation/backend && python scripts/demo.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import asyncio
from pipeline.scraper import scrape_mock
from pipeline.enricher import enrich_all
from pipeline.icp_scorer import score_all
from pipeline.email_generator import generate

SAMPLE_URL = "https://acmecorp.example.com"

async def run_demo():
    print("=== ai-lead-generation demo ===\n")

    print("1. Scraping (mock)...")
    raw_leads = scrape_mock()
    print(f"   Got {len(raw_leads)} raw lead(s)\n")

    print("2. Enriching...")
    enriched = enrich_all(raw_leads)
    for lead in enriched:
        print(f"   {lead.company} | {lead.first_name} ({lead.title}) | {lead.industry_category}\n")

    print("3. Scoring (ICP)...")
    scored = score_all(enriched)
    for lead, result in scored:
        print(f"   Score: {result['score']}/100")
        print(f"   Breakdown:")
        for factor, detail in result.get("breakdown", {}).items():
            if isinstance(detail, dict):
                print(f"     {factor}: {detail.get('points', 0)}/{detail.get('max', 0)} pts")
        print()

    print("4. Drafting outreach email (Jinja2 template)...")
    for lead, result in scored:
        email = generate(lead, result["score"])
        print(f"   ---\n{email}\n   ---\n")

    print("5. Follow-up sequence (scheduled steps):")
    for i, delay in enumerate([3, 7, 14], start=1):
        print(f"   Step {i}: scheduled +{delay} days after initial send")

    print("\nDemo complete. To run with LLM email drafting, set GEMINI_API_KEY and pass use_llm=True via POST /pipeline/run.")

if __name__ == "__main__":
    asyncio.run(run_demo())

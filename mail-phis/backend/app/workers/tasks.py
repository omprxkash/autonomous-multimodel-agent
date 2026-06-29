import asyncio
import re
from datetime import datetime
from app.core.celery_app import celery
from app.core.database import AsyncSessionLocal
from app.models.analysis import Analysis, AnalysisStatus
from app.services.email_parser import parse_email
from app.services.header_forensics import analyze_headers
from app.services.auth_verifier import verify_auth
from app.services.url_analyzer import analyze_url
from app.services.domain_intel import analyze_domain
from app.services.threat_intel import query_threat_intel
from app.services.nlp_detector import analyze_nlp
from app.services.risk_scorer import compute_score
from app.services.report_generator import generate_report
from app.services.attachment_risk_detector import analyze_attachments
from app.services.redirect_tracker import trace_redirect_chain
from app.services.ioc_exporter import extract_iocs


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


@celery.task(bind=True, max_retries=1)
def run_email_pipeline(self, analysis_id: str, raw_hex: str):
    raw = bytes.fromhex(raw_hex)
    _run(_email_pipeline(analysis_id, raw))


@celery.task(bind=True, max_retries=1)
def run_url_pipeline(self, analysis_id: str, url: str):
    _run(_url_pipeline(analysis_id, url))


async def _email_pipeline(analysis_id: str, raw: bytes):
    async with AsyncSessionLocal() as db:
        analysis = await db.get(Analysis, analysis_id)
        if not analysis:
            return
        analysis.status = AnalysisStatus.RUNNING
        await db.commit()

        try:
            parsed = parse_email(raw)
            headers = analyze_headers(parsed)
            auth = await verify_auth(parsed, headers)
            nlp = analyze_nlp(parsed)

            urls = _extract_urls_from_body(parsed)
            url_results = None
            domain_results = None
            threat_results = None
            redirect_result = None

            if urls:
                first_url = urls[0]
                url_results, domain_results, threat_results, redirect_result = await asyncio.gather(
                    analyze_url(first_url),
                    analyze_domain(first_url.split("/")[2] if "/" in first_url else first_url),
                    query_threat_intel(first_url),
                    trace_redirect_chain(first_url),
                    return_exceptions=True,
                )
                # Degrade gracefully on individual failures
                if isinstance(url_results, Exception): url_results = None
                if isinstance(domain_results, Exception): domain_results = None
                if isinstance(threat_results, Exception): threat_results = None
                if isinstance(redirect_result, Exception): redirect_result = None

            raw_attachments = parsed.get("attachments", [])
            attachment_risk = analyze_attachments(raw_attachments)
            all_attachments = raw_attachments

            scoring = compute_score(
                headers, auth, url_results, domain_results,
                threat_results, nlp, all_attachments,
            )

            report = generate_report(
                analysis_id, "email", parsed.get("from", ""),
                parsed, headers, auth, url_results, domain_results,
                threat_results, nlp, scoring,
            )

            # Enrich pipeline results with attachment risk and redirect details
            report["pipeline"]["attachment_risk"] = {
                "has_executable": attachment_risk.has_executable,
                "has_macro_document": attachment_risk.has_macro_document,
                "double_extension_detected": attachment_risk.double_extension_detected,
                "rtlo_attack": attachment_risk.rtlo_attack,
                "risk_score": attachment_risk.risk_score,
                "risky_attachments": attachment_risk.risky_attachments,
            }
            if redirect_result and not isinstance(redirect_result, Exception):
                if hasattr(redirect_result, "redirect_count"):
                    report["pipeline"]["redirect_chain"] = {
                        "redirect_count": redirect_result.redirect_count,
                        "final_domain_mismatch": redirect_result.final_domain_mismatch,
                        "redirect_to_ip": redirect_result.redirect_to_ip,
                        "meta_refresh_detected": redirect_result.meta_refresh_detected,
                    }
                else:
                    report["pipeline"]["redirect_chain"] = redirect_result

            report["indicators"] = scoring.get("indicators", [])

            full_iocs = extract_iocs(
                analysis_id, report["pipeline"], scoring["verdict"], scoring["score"]
            )

            analysis.status = AnalysisStatus.COMPLETE
            analysis.verdict = scoring["verdict"]
            analysis.score = scoring["score"]
            analysis.pipeline_results = report["pipeline"]
            analysis.feature_vector = scoring["feature_vector"]
            analysis.iocs = full_iocs
            analysis.completed_at = datetime.utcnow()

        except Exception as e:
            analysis.status = AnalysisStatus.FAILED
            analysis.error = str(e)[:500]
            analysis.completed_at = datetime.utcnow()

        await db.commit()


async def _url_pipeline(analysis_id: str, url: str):
    async with AsyncSessionLocal() as db:
        analysis = await db.get(Analysis, analysis_id)
        if not analysis:
            return
        analysis.status = AnalysisStatus.RUNNING
        await db.commit()

        try:
            domain = url.split("/")[2] if "//" in url else url

            url_results, domain_results, threat_results = await asyncio.gather(
                analyze_url(url),
                analyze_domain(domain),
                query_threat_intel(url),
            )

            empty_parsed = {"subject": "", "from": "", "body_parts": [], "attachments": []}
            empty_headers = {"reply_to_mismatch": False, "display_name_spoof": False, "sender_domain": domain}
            empty_auth = {
                "spf": {"result": "none"}, "dkim": {"result": "none"},
                "dmarc": {"result": "none"}, "display_name_spoof": False, "auth_score": 0,
            }
            nlp = analyze_nlp(empty_parsed)

            scoring = compute_score(
                empty_headers, empty_auth, url_results, domain_results,
                threat_results, nlp, [],
            )

            report = generate_report(
                analysis_id, "url", url,
                None, None, None, url_results, domain_results,
                threat_results, nlp, scoring,
            )

            analysis.status = AnalysisStatus.COMPLETE
            analysis.verdict = scoring["verdict"]
            analysis.score = scoring["score"]
            analysis.pipeline_results = report["pipeline"]
            analysis.feature_vector = scoring["feature_vector"]
            analysis.iocs = report["iocs"]
            analysis.completed_at = datetime.utcnow()

        except Exception as e:
            analysis.status = AnalysisStatus.FAILED
            analysis.error = str(e)[:500]
            analysis.completed_at = datetime.utcnow()

        await db.commit()


def _extract_urls_from_body(parsed: dict) -> list[str]:
    url_re = re.compile(r"https?://[^\s\"'<>]+")
    urls = []
    for part in parsed.get("body_parts", []):
        found = url_re.findall(part.get("content", ""))
        urls.extend(found)
    return list(dict.fromkeys(urls))[:5]

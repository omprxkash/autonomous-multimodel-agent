"""
Threat intelligence orchestrator.
Fans out to OpenPhish, PhishTank, URLhaus, and AbuseIPDB concurrently.
Aggregates results into a typed ThreatIntelResult.
"""
import asyncio
from dataclasses import dataclass, field
from typing import Optional

from app.services.threat_intelligence.openphish_client import check_openphish, OpenPhishResult
from app.services.threat_intelligence.phishtank_client import check_phishtank, PhishTankResult
from app.services.threat_intelligence.urlhaus_client import check_urlhaus, URLhausResult
from app.services.threat_intelligence.ip_reputation_client import check_ip_reputation, IPReputationResult


@dataclass
class ThreatIntelResult:
    url: str
    any_hit: bool = False

    openphish: Optional[OpenPhishResult] = None
    phishtank: Optional[PhishTankResult] = None
    urlhaus: Optional[URLhausResult] = None
    ip_reputation: Optional[IPReputationResult] = None

    # Flattened fields for risk_scorer compatibility
    openphish_status: str = "unknown"
    phishtank_status: str = "unknown"
    urlhaus_status: str = "unknown"
    ip_blacklisted: bool = False
    country_risk_score: float = 0.0

    def to_legacy_dict(self) -> dict:
        """Return the flat dict format expected by the legacy compute_score() wrapper."""
        return {
            "openphish": {"status": self.openphish_status},
            "phishtank": {"status": self.phishtank_status},
            "urlhaus": {"status": self.urlhaus_status},
            "any_hit": self.any_hit,
            "ip_blacklisted": self.ip_blacklisted,
            "country_risk_score": self.country_risk_score,
        }


class ThreatIntelService:
    async def analyze(self, url: str, originating_ip: Optional[str] = None) -> ThreatIntelResult:
        tasks = [
            check_openphish(url),
            check_phishtank(url),
            check_urlhaus(url),
        ]
        if originating_ip:
            tasks.append(check_ip_reputation(originating_ip))
        else:
            tasks.append(asyncio.sleep(0, result=None))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        op = results[0] if not isinstance(results[0], Exception) else OpenPhishResult(status="error")
        pt = results[1] if not isinstance(results[1], Exception) else PhishTankResult(status="error")
        uh = results[2] if not isinstance(results[2], Exception) else URLhausResult(status="error")
        ip = results[3] if (not isinstance(results[3], Exception) and results[3] is not None) else None

        any_hit = (
            getattr(op, "status", "") == "hit"
            or getattr(pt, "status", "") == "hit"
            or getattr(uh, "status", "") == "hit"
        )

        return ThreatIntelResult(
            url=url,
            any_hit=any_hit,
            openphish=op,
            phishtank=pt,
            urlhaus=uh,
            ip_reputation=ip,
            openphish_status=getattr(op, "status", "unknown"),
            phishtank_status=getattr(pt, "status", "unknown"),
            urlhaus_status=getattr(uh, "status", "unknown"),
            ip_blacklisted=getattr(ip, "is_blacklisted", False),
            country_risk_score=1.0 if getattr(ip, "country_risk", False) else 0.0,
        )

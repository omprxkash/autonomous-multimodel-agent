# mail-phis

SOC-grade phishing detection pipeline for email and URL analysis. Parses raw MIME messages through a 9-stage forensic pipeline — authentication verification, URL threat intelligence, NLP social engineering detection, and attachment risk scoring — and returns a structured verdict with an exportable IOC bundle.

---

## What it does

- **9-stage analysis pipeline** — each stage runs independently; failures degrade gracefully
- **Dual-bucket risk scoring** — `risk_score = suspicion_score − trust_score`, clamped 0–100
- **Content-only false positive protection** — NLP signals alone cannot produce a PHISHING verdict (capped at SUSPICIOUS/74)
- **STIX2-compatible IOC export** — IPs, domains, URLs, hashes, and threat indicators in a structured bundle
- **Concurrent threat intel** — OpenPhish + PhishTank + URLhaus queried in parallel, graceful degradation on API failure
- **Attachment forensics** — RTLO attack detection, double-extension, MIME mismatch, macro document flagging
- **Unicode homograph detection** — Cyrillic/Unicode confusables mapped to ASCII, Levenshtein typosquatting threshold 0.75
- **Async redirect chain tracing** — up to 10 hops, detects meta-refresh HTML redirects, IP destinations, and final domain mismatches

---

## Architecture

```
Raw email (MIME bytes)
        │
        ▼
┌───────────────────────────────────────────────────┐
│                  9-Stage Pipeline                  │
│                                                   │
│  1. Email Parser          ← RFC 5322 / MIME       │
│  2. Header Forensics      ← SMTP chain, IPs       │
│  3. Auth Verifier         ← SPF / DKIM / DMARC    │
│  4. URL Analyzer          ← entropy, obfuscation  │
│  5. Domain Intel          ← WHOIS, DNS, homograph │
│  6. Threat Intel          ← OpenPhish/PhishTank   │
│  7. NLP Detector          ← urgency, credentials  │
│  8. Attachment Risk       ← RTLO, MIME mismatch   │
│  9. Risk Scorer           ← dual-bucket engine    │
│                                                   │
│  → IOC Exporter           ← structured IOC bundle │
└───────────────────────────────────────────────────┘
        │
        ▼
  Verdict: SAFE / MARKETING / SUSPICIOUS / PHISHING
  Score: 0–100
  IOCs: { ips, domains, urls, hashes, indicators }
```

---

## Verdict tiers

| Score | Verdict | Meaning |
|---|---|---|
| 0–19 | `SAFE` | No significant signals |
| 20–49 | `MARKETING` | Bulk/promotional indicators |
| 50–74 | `SUSPICIOUS` | Multiple moderate signals; investigate |
| 75–100 | `PHISHING` | High-confidence threat; block/quarantine |

**Content-only protection:** If all suspicion comes exclusively from NLP signals (urgency keywords, credential requests, financial lures), the effective score is capped at 74 — a PHISHING verdict requires at least one non-content signal (auth failure, threat intel hit, domain anomaly, or attachment risk).

---

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI (async) |
| Task queue | Celery + Redis |
| Database | PostgreSQL (async SQLAlchemy) |
| Frontend | Next.js 14 |
| DNS / auth | dnspython, python-whois |
| Threat intel | OpenPhish, PhishTank, URLhaus |
| NLP | Custom keyword + density scoring |
| Infra | Docker Compose, Nginx |

---

## File structure

```
mail-phis/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/           analyze.py · reports.py · health.py
│   │   ├── core/          config.py · database.py · celery_app.py · security.py · logging.py
│   │   ├── models/        analysis.py
│   │   ├── services/
│   │   │   ├── email_parser.py
│   │   │   ├── header_forensics.py
│   │   │   ├── auth_verifier.py
│   │   │   ├── url_analyzer.py
│   │   │   ├── domain_intel.py
│   │   │   ├── threat_intel.py
│   │   │   ├── nlp_detector.py
│   │   │   ├── attachment_risk_detector.py  ← RTLO, double-ext, MIME mismatch
│   │   │   ├── homograph_detector.py        ← Unicode confusables, Levenshtein
│   │   │   ├── redirect_tracker.py          ← async redirect chain, meta-refresh
│   │   │   ├── feature_builder.py           ← 80+ features across 12 categories
│   │   │   ├── risk_scorer.py               ← dual-bucket engine + legacy wrapper
│   │   │   ├── ioc_exporter.py              ← structured IOC bundle
│   │   │   └── report_generator.py
│   │   └── workers/       tasks.py
│   └── requirements.txt
├── frontend/src/
│   ├── app/               layout · page · submit/page · report/[id]/page
│   └── components/        VerdictBadge · PipelineStatus · FeatureBreakdown · ReportCard
├── infrastructure/nginx/nginx.conf
├── tests/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Risk scoring engine

The dual-bucket engine computes:

```
suspicion_score = Σ (weight × feature_value)   for all suspicion features
trust_score     = Σ (weight × feature_value)    for all trust features
risk_score      = clamp(suspicion_score − trust_score, 0, 100)
```

**Suspicion weights (selected):**

| Signal | Weight |
|---|---|
| OpenPhish / PhishTank / URLhaus hit | 50.0 each |
| Domain blacklisted | 50.0 |
| DMARC fail | 30.0 |
| DKIM fail | 25.0 |
| Domain < 7 days old | 40.0 |
| Executable attachment | 40.0 |
| Double-extension detected | 40.0 |
| Display name brand spoofing | 35.0 |
| Contains IP address | 30.0 |
| Brand homograph detected | 30.0 |
| SPF fail | 20.0 |

**Trust weights (selected):**

| Signal | Weight |
|---|---|
| DMARC pass | 20.0 |
| DKIM pass | 15.0 |
| All auth pass (SPF+DKIM+DMARC) | 15.0 |
| Bulk mail / ESP detected | 10–15.0 |
| Has unsubscribe link | 5.0 |
| Domain age (capped at 30pts) | 0.01/day |

---

## Attachment forensics

The `attachment_risk_detector` scans each attachment for:

- **RTLO attack** — byte scan for U+202E (Right-to-Left Override) and U+202D characters
- **Double extension** — outer extension in executable list (`.exe`, `.msi`, `.bat`, `.ps1`, etc.)
- **MIME mismatch** — declared Content-Type vs actual file magic bytes
- **Macro documents** — `.docm`, `.xlsm`, `.pptm` flagged even without content analysis
- **Archive content** — `.zip`/`.rar`/`.7z` containing executables

---

## Homograph detection

The `homograph_detector` uses a 30-character CONFUSABLE_MAP (Cyrillic, Greek, and other Unicode look-alikes → ASCII equivalents) to normalize domains, then:

1. Compares against a brand keyword list
2. Runs Levenshtein similarity on the ASCII-normalized domain vs known brand domains (threshold: 0.75)
3. Flags IDN/punycode domains (xn-- prefix) for manual review

---

## IOC export format

```json
{
  "analysis_id": "uuid",
  "verdict": "PHISHING",
  "risk_score": 87,
  "ioc_count": 5,
  "iocs": {
    "ips": [{ "value": "1.2.3.4", "context": "smtp_originating_ip", "severity": "HIGH" }],
    "domains": [{ "value": "evil.tk", "context": "url_domain", "newly_registered": true }],
    "urls": [{ "value": "http://evil.tk/login", "threat_hit": true }],
    "email_addresses": [{ "value": "noreply@evil.tk", "context": "from_header" }],
    "hashes": [{ "value": "sha256...", "filename": "invoice.exe" }],
    "indicators": [{ "type": "url_in_threat_feed", "source": "openphish", "severity": "CRITICAL" }]
  }
}
```

---

## Quick start (local)

```bash
cd mail-phis
cp .env.example .env
docker compose up --build
# API at http://localhost:8000
# Frontend at http://localhost:3000
```

Submit an email for analysis:

```bash
curl -X POST http://localhost:8000/api/analyze/email \
  -H "Content-Type: application/json" \
  -d '{"raw_email": "<base64-encoded MIME message>"}'
```

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `REDIS_URL` | Yes | Celery broker + result backend |
| `OPENPHISH_API_KEY` | No | OpenPhish premium feed (degrades gracefully if absent) |
| `PHISHTANK_API_KEY` | No | PhishTank API key |
| `SECRET_KEY` | Yes | App secret for signing |

---

## Relation to deskpilot

Both `mail-phis` and `deskpilot` live in this monorepo because they share the same domain — Google Workspace email. `deskpilot` is the **assistant layer** (user-facing agent for reading, drafting, and sending email). `mail-phis` is the **security layer** (automated forensic analysis of incoming messages for phishing detection). They are complementary: a production deployment could pipe incoming email through mail-phis before surfacing it in deskpilot's inbox view.

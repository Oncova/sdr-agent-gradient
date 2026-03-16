# Antigravity Workspace Directives for Claude Opus 4.6

## Google-First Mandate

All internal operations MUST be executed within Google Workspace:
- Outbound SDR emails sent through Gmail natively
- Google Sheets acts as the live CRM
- Google Drive stores all enriched CSVs
- Google Calendar handles all demo scheduling
- Internal alerts and notifications route to Gmail

## Active vs. Benched MCPs

**Active MCPs (deployed immediately):**
Vault, Google Workspace, n8n, Bright Data, ElevenLabs, Playwright,
Apollo/PDL Enrichment, Temporal, OneTrust, Datadog,
New Relic, Redis, OWASP ZAP, Snyk, Cloudflare WAF, DMARC Analyzer,
MailReach, Lemon Squeezy

**Benched MCPs (white-label scale-out ONLY — do NOT activate in
internal pipelines):**
Kafka, Postmark, HubSpot, SendGrid, PandaDoc, Terraform Provisioner, Vapi

## Three-Phase Build Plan

- Phase 1: Antigravity local build ✅ COMPLETE
- Phase 2: OpenClaw App Platform deployment & evaluation ✅ COMPLETE
- Phase 3: n8n orchestration activation

## 3-Agent Architecture (OpenClaw App Platform)

The SDR army runs as 3 isolated agent workspaces on a single
DigitalOcean App Platform deployment via OpenClaw:

1. **sdr-scraper** — Lead scraping & enrichment (Playwright, Apollo/PDL, Redis, BrightData, OneTrust)
2. **sdr-pitcher** — Pitch generation & delivery (Mailreach, DMARC, Workspace, Lemon Squeezy)
3. **sdr-closer** — Follow-up & closing (ElevenLabs, Temporal, PandaDoc, n8n, Lemon Squeezy)

## Strict Security Deny List

The following require EXPLICIT user confirmation before execution:
- rm
- sudo rm
- git reset --hard

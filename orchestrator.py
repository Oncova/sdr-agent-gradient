#!/usr/bin/env python3
"""
orchestrator.py — MCP Orchestration Controller
DigitalOcean Gradient ADK Agent: gpt54-sdr-brain

Imports all 25 MCPs from mcp_stack.py and executes them
according to deployment classification:

  ACTIVE (14): Initialized and running in core deployment.
  BENCHED (4): Imported but NOT called — white-label scale-out only.
  WHITE-LABEL (2): Imported but NOT called — external client deployments only.
"""

import sys

from gradient_adk import GradientAgent

# ── ACTIVE MCPs (14) — initialized and called ────────────
from mcp_stack import (
    initialize_vault_mcp,
    initialize_google_workspace_mcp,
    initialize_bright_data_mcp,
    initialize_elevenlabs_mcp,
    initialize_n8n_router_mcp,
    initialize_playwright_mcp,
    initialize_enrichment_mcp,
    initialize_telephony_mcp,
    initialize_temporal_mcp,
    initialize_onetrust_mcp,
    initialize_datadog_mcp,
    initialize_newrelic_mcp,
    initialize_redis_mcp,
    initialize_owasp_zap_mcp,
    initialize_snyk_mcp,
    initialize_cloudflare_waf_mcp,
    initialize_dmarc_analyzer_mcp,
    initialize_mailreach_mcp,
    initialize_lemon_squeezy_mcp,
)

# BENCHED — white-label scale-out only
from mcp_stack import (  # noqa: F401
    initialize_kafka_mcp,
    initialize_postmark_mcp,
    initialize_hubspot_mcp,
    initialize_sendgrid_mcp,
)

# WHITE-LABEL ONLY — not active in core deployment
from mcp_stack import (  # noqa: F401
    initialize_pandadoc_mcp,
    initialize_terraform_mcp,
)


def orchestrate():
    """Boot all active MCPs in strict dependency order."""

    # ── Layer 0: Cryptographic zero-node ──
    print("[ORCHESTRATOR] Layer 0 — Vault (zero-node)...")
    vault_mcp, vault_client = initialize_vault_mcp()
    if not vault_client.is_authenticated():
        print("[FATAL] Vault authentication failed.")
        sys.exit(1)
    print("[ORCHESTRATOR] Vault authenticated ✓")

    # ── Layer 1: Google Workspace backbone ──
    print("[ORCHESTRATOR] Layer 1 — Google Workspace backbone...")
    workspace_mcp = initialize_google_workspace_mcp(vault_mcp)

    # ── Layer 2: Core infrastructure ──
    print("[ORCHESTRATOR] Layer 2 — Core infrastructure...")
    brightdata_mcp = initialize_bright_data_mcp(vault_mcp)
    elevenlabs_mcp = initialize_elevenlabs_mcp(vault_mcp, workspace_mcp)
    n8n_mcp = initialize_n8n_router_mcp(vault_mcp)

    # ── Layer 3: Scraping & enrichment ──
    print("[ORCHESTRATOR] Layer 3 — Scraping & enrichment...")
    playwright_mcp = initialize_playwright_mcp(vault_mcp)
    enrichment_mcp = initialize_enrichment_mcp(vault_mcp)
    redis_mcp = initialize_redis_mcp(vault_mcp)

    # ── Layer 4: Telephony & durable execution ──
    print("[ORCHESTRATOR] Layer 4 — Telephony & durable execution...")
    telephony_mcp = initialize_telephony_mcp(vault_mcp)
    temporal_mcp = initialize_temporal_mcp(vault_mcp)

    # ── Layer 5: Compliance ──
    print("[ORCHESTRATOR] Layer 5 — Compliance...")
    onetrust_mcp = initialize_onetrust_mcp(vault_mcp)

    # ── Layer 6: Observability ──
    print("[ORCHESTRATOR] Layer 6 — Observability...")
    datadog_mcp = initialize_datadog_mcp(vault_mcp)
    newrelic_mcp = initialize_newrelic_mcp(vault_mcp)

    # ── Layer 7: Security ──
    print("[ORCHESTRATOR] Layer 7 — Security...")
    owasp_zap_mcp = initialize_owasp_zap_mcp(vault_mcp)
    snyk_mcp = initialize_snyk_mcp(vault_mcp)
    cloudflare_waf_mcp = initialize_cloudflare_waf_mcp(vault_mcp)

    # ── Layer 8: Deliverability & domain health ──
    print("[ORCHESTRATOR] Layer 8 — Deliverability & domain health...")
    dmarc_mcp = initialize_dmarc_analyzer_mcp(vault_mcp)
    mailreach_mcp = initialize_mailreach_mcp(vault_mcp)

    # ── Layer 9: Revenue ──
    print("[ORCHESTRATOR] Layer 9 — Revenue...")
    lemon_squeezy_mcp = initialize_lemon_squeezy_mcp(vault_mcp)

    # BENCHED — white-label scale-out only
    # initialize_kafka_mcp       → Event streaming (overkill for core n8n routing)
    # initialize_postmark_mcp    → Transactional email (Gmail API handles internally)
    # initialize_hubspot_mcp     → External CRM (Sheets is the core CRM)
    # initialize_sendgrid_mcp    → External SMTP (Gmail API is mandated internally)

    # WHITE-LABEL ONLY — not active in core deployment
    # initialize_pandadoc_mcp    → Contract generation (Google Docs API handles internally)
    # initialize_terraform_mcp   → IaC provisioning (only for client environment spin-up)

    # ── Assemble the Gradient Agent ──
    agent = GradientAgent(name="gpt54-sdr-brain", entrypoint="orchestrator.py")

    active_mcps = [
        vault_mcp, workspace_mcp, brightdata_mcp, elevenlabs_mcp, n8n_mcp,
        playwright_mcp, enrichment_mcp, redis_mcp,
        telephony_mcp, temporal_mcp,
        onetrust_mcp,
        datadog_mcp, newrelic_mcp,
        owasp_zap_mcp, snyk_mcp, cloudflare_waf_mcp,
        dmarc_mcp, mailreach_mcp,
        lemon_squeezy_mcp,
    ]

    for mcp in active_mcps:
        agent.register_mcp(mcp)

    print("\n" + "=" * 64)
    print("  GPT-5.4 SDR BRAIN — ALL 19 ACTIVE MCPs NOMINAL")
    print("  4 BENCHED (white-label scale-out only)")
    print("  2 WHITE-LABEL ONLY (not active in core deployment)")
    print("  Total: 25 MCP scripts loaded")
    print("=" * 64)
    print("  Target: Solo PI & Criminal Defense Attorneys")
    print("  Offer: $199/month Hyper-Specialized AI Legal Receptionist")
    print("=" * 64 + "\n")

    agent.run()


if __name__ == "__main__":
    orchestrate()

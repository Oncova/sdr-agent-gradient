"""
mcp_stack.py — Complete MCP Initialization Stack (25 Scripts)
OpenClaw App Platform Agent: gpt54-sdr-brain

Contains all 25 MCP initialization functions:
  Original 5 (Phase 1):
    1.  Vault MCP             — Cryptographic zero-node
    2.  Google Workspace MCP  — Operational backbone
    3.  Bright Data MCP       — Proxy rotation
    4.  ElevenLabs MCP        — Voice synthesis
    5.  n8n Router MCP        — Traffic controller

  Batch 2 — Scraping & Enrichment:
    6.  Playwright MCP        — DOM extraction (PROXY FIX applied)
    7.  Enrichment MCP        — Apollo + PDL skip-tracing
    8.  Telephony MCP         — Vapi SIP routing
    9.  Temporal MCP          — Durable execution
    10. OneTrust MCP          — PII compliance audit

  Batch 3 — Observability & Security:
    11. Datadog MCP           — APM tracing
    12. New Relic MCP         — LLM drift detection
    13. Kafka MCP             — Event streaming        (BENCHED)
    14. Redis MCP             — Scrape caching
    15. OWASP ZAP MCP         — DAST scanning
    16. Snyk MCP              — Dependency scanning
    17. Cloudflare WAF MCP    — Rate limiting
    18. DMARC Analyzer MCP    — Domain reputation

  Final Batch — Revenue & Scale-Out:
    19. Postmark MCP          — Transactional email     (BENCHED)
    20. PandaDoc MCP          — Contract generation     (WHITE-LABEL)
    21. Mailreach MCP         — Deliverability rotation
    22. HubSpot MCP           — External CRM sync       (BENCHED)
    23. SendGrid MCP          — External SMTP routing    (BENCHED)
    24. Lemon Squeezy MCP     — $99/week billing
    25. Terraform MCP         — IaC provisioning         (WHITE-LABEL)
"""

import os
from datetime import datetime

import hvac
import requests
from openclaw_sdk import MCPClient


# ═══════════════════════════════════════════════════════════
#  ORIGINAL 5 — Phase 1 Core Stack
# ═══════════════════════════════════════════════════════════


# ── 1. HashiCorp Vault MCP ────────────────────────────────
def initialize_vault_mcp():
    """Cryptographic zero-node. All downstream MCPs depend on this."""
    vault_client = hvac.Client(
        url=os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200"),
        token=os.environ.get("VAULT_TOKEN", "dev-root-token"),
    )

    vault_mcp = MCPClient(
        name="hashicorp-vault-core",
        capabilities=["secret_management", "dynamic_injection"],
    )

    @vault_mcp.register_tool(
        description="Fetch operational secrets for authorized ADK deployments."
    )
    def fetch_secret(path: str) -> dict:
        response = vault_client.secrets.kv.v2.read_secret_version(
            path=f"enterprise-revops/{path}"
        )
        return response["data"]["data"]

    return vault_mcp, vault_client


# ── 2. Google Workspace MCP ──────────────────────────────
def initialize_google_workspace_mcp(vault_mcp):
    """Non-negotiable operational backbone: Gmail, Sheets, Drive."""
    gcp_creds = vault_mcp.execute_tool("fetch_secret", path="google_workspace")

    workspace_mcp = MCPClient(
        name="google-first-ops",
        capabilities=["gmail_routing", "sheets_crm", "drive_storage"],
        environment={
            "GCP_SERVICE_ACCOUNT": gcp_creds.get("service_account_json", ""),
            "ADMIN_INBOX": "revops@yourdomain.com",
        },
    )

    @workspace_mcp.register_tool(
        description="Route all telemetry, pipeline alerts, and notifications to Gmail."
    )
    def route_alert_to_inbox(agent_id: str, severity: str, payload: str) -> str:
        email_body = (
            f"<h2>Gradient Alert: {agent_id} ({severity})</h2>"
            f"<pre>{payload}</pre>"
        )
        return workspace_mcp.execute_internal(
            "gmail.send",
            {
                "to": "revops@yourdomain.com",
                "subject": f"[{severity.upper()}] SDR Army Alert",
                "html": email_body,
            },
        )

    @workspace_mcp.register_tool(
        description="Upload a file to Google Drive and return the share link."
    )
    def upload_to_drive(filename: str, content: bytes) -> str:
        return workspace_mcp.execute_internal(
            "drive.upload",
            {"filename": filename, "mime_type": "audio/mpeg", "content_length": len(content)},
        )

    return workspace_mcp


# ── 3. Bright Data MCP ───────────────────────────────────
def initialize_bright_data_mcp(vault_mcp):
    """Residential proxy rotation for Florida legal directory scraping."""
    bd_creds = vault_mcp.execute_tool("fetch_secret", path="brightdata")

    bd_mcp = MCPClient(
        name="brightdata-evasion-engine",
        capabilities=["residential_proxy", "captcha_solving"],
        environment={
            "BD_ACCOUNT": bd_creds.get("account_id", ""),
            "BD_ZONE": "florida_legal_scraper",
            "BD_TOKEN": bd_creds.get("api_token", ""),
        },
    )

    @bd_mcp.register_tool(
        description="Generate rotating proxy for Avvo and FindLaw DOM extraction."
    )
    def get_residential_proxy() -> str:
        username = bd_creds.get("username", "")
        password = bd_creds.get("password", "")
        return f"http://{username}:{password}@zproxy.lum-superproxy.io:22225"

    return bd_mcp


# ── 4. ElevenLabs MCP ────────────────────────────────────
def initialize_elevenlabs_mcp(vault_mcp, workspace_mcp):
    """Voice synthesis engine — generates $99/week trial pitches, streams to Drive."""
    el_creds = vault_mcp.execute_tool("fetch_secret", path="elevenlabs")

    eleven_mcp = MCPClient(
        name="voice-synth-engine",
        capabilities=["text_to_speech"],
    )

    @eleven_mcp.register_tool(
        description="Synthesize personalized $99 trial pitch and stream to Drive."
    )
    def synthesize_pitch(attorney_name: str, practice_area: str) -> str:
        script = (
            f"Hi {attorney_name}, I saw you handle a lot of {practice_area} cases "
            f"down here in South Florida. I've built an AI receptionist that handles "
            f"intake 24/7. I'm offering a $99 per week trial."
        )
        headers = {
            "xi-api-key": el_creds.get("api_key", ""),
            "Content-Type": "application/json",
        }
        payload = {
            "text": script,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{el_creds.get('voice_id', '')}",
            json=payload,
            headers=headers,
        )
        if response.status_code == 200:
            filename = f"{attorney_name.replace(' ', '_')}_pitch.mp3"
            drive_link = workspace_mcp.execute_tool(
                "upload_to_drive", filename=filename, content=response.content
            )
            return drive_link
        raise Exception(f"Synthesis engine failure: {response.text}")

    return eleven_mcp


# ── 5. n8n Router MCP ────────────────────────────────────
def initialize_n8n_router_mcp(vault_mcp):
    """Traffic controller — routes internal (Google) vs external (white-label)."""
    n8n_creds = vault_mcp.execute_tool("fetch_secret", path="n8n_orchestration")

    n8n_mcp = MCPClient(
        name="n8n-traffic-controller",
        capabilities=["payload_routing", "conditional_logic"],
        environment={
            "N8N_URL": n8n_creds.get("base_url", ""),
            "N8N_API_KEY": n8n_creds.get("api_key", ""),
        },
    )

    @n8n_mcp.register_tool(
        description="Route execution logic based on deployment context."
    )
    def route_lead_payload(client_id: str, lead_data: dict) -> str:
        if client_id == "internal_ops":
            endpoint = "/webhook/google-sheets-crm"
        else:
            endpoint = f"/webhook/client-deploy/{client_id}"
        return n8n_mcp.execute_internal(
            "webhook.trigger",
            {"path": endpoint, "method": "POST", "payload": lead_data},
        )

    return n8n_mcp


# ═══════════════════════════════════════════════════════════
#  BATCH 2 — Scraping, Enrichment, Telephony, Execution,
#            Compliance (Scripts 6–10)
# ═══════════════════════════════════════════════════════════


# ── 6. Playwright MCP (Scraper Engine) ───────────────────
#    PROXY FIX: proxy_url sourced from brightdata secret,
#    NOT from playwright_engine (no redundant secret path).
def initialize_playwright_mcp(vault_mcp):
    """Headless Playwright for Florida Bar / Avvo DOM extraction."""
    playwright_creds = vault_mcp.execute_tool("fetch_secret", path="playwright_engine")
    bd_creds = vault_mcp.execute_tool("fetch_secret", path="brightdata")

    scraper_mcp = MCPClient(
        name="florida-bar-scraper",
        capabilities=["dom_extraction", "headless_browser"],
    )

    @scraper_mcp.register_tool(
        description="Scrape Avvo and Florida Bar directories for solo practitioners."
    )
    def scrape_attorney_directory(target_url: str) -> list:
        proxy_url = f"http://{bd_creds.get('username', '')}:{bd_creds.get('password', '')}@zproxy.lum-superproxy.io:22225"
        return scraper_mcp.execute_internal("browser.navigate_and_extract", {
            "url": target_url,
            "proxy": proxy_url,
            "stealth_mode": True,
            "selectors": {
                "name": ".v-lawyer-card .name",
                "firm": ".v-lawyer-card .firm-name",
            },
        })

    return scraper_mcp


# ── 7. Enrichment MCP (Apollo & People Data Labs) ────────
def initialize_enrichment_mcp(vault_mcp):
    """B2B intelligence via Apollo + skip-tracing via PDL."""
    enrich_creds = vault_mcp.execute_tool("fetch_secret", path="data_enrichment")

    enrich_mcp = MCPClient(
        name="sdr-enrichment-engine",
        capabilities=["b2b_routing", "skip_tracing"],
    )

    @enrich_mcp.register_tool(
        description="Cross-reference firm and execute skip-trace for direct contact data."
    )
    def enrich_lead(name: str, firm: str) -> dict:
        apollo_data = enrich_mcp.execute_internal("apollo.organization.enrich", {
            "api_key": enrich_creds["apollo_key"],
            "organization_name": firm,
        })
        pdl_data = enrich_mcp.execute_internal("pdl.person.enrich", {
            "api_key": enrich_creds["pdl_key"],
            "name": name,
            "company": firm,
        })
        return {
            "name": name,
            "firm": firm,
            "professional_email": apollo_data.get("primary_email"),
            "mobile_number": pdl_data.get("mobile_phone"),
        }

    return enrich_mcp


# ── 8. Telephony MCP (Vapi SIP Router) ──────────────────
def initialize_telephony_mcp(vault_mcp):
    """SIP orchestration — links ElevenLabs to telecom for $99/week trials."""
    vapi_creds = vault_mcp.execute_tool("fetch_secret", path="vapi_telephony")

    vapi_mcp = MCPClient(
        name="sip-telephony-router",
        capabilities=["inbound_routing", "outbound_dialing", "agent_provisioning"],
    )

    @vapi_mcp.register_tool(
        description="Deploy inbound SIP endpoint for the $99 ElevenLabs trial."
    )
    def provision_trial_number(elevenlabs_voice_id: str, attorney_name: str) -> str:
        return vapi_mcp.execute_internal("vapi.assistant.create", {
            "api_key": vapi_creds["private_api_key"],
            "name": f"Trial_{attorney_name.replace(' ', '_')}",
            "voice": {"provider": "elevenlabs", "voiceId": elevenlabs_voice_id},
            "model": {"provider": "openai", "model": "gpt-5.4"},
            "systemPrompt": "You are a highly capable legal intake receptionist.",
        })

    return vapi_mcp


# ── 9. Temporal MCP (Durable Execution) ─────────────────
def initialize_temporal_mcp(vault_mcp):
    """Survives container restarts — no dropped prospects."""
    temporal_creds = vault_mcp.execute_tool("fetch_secret", path="temporal_cluster")

    temporal_mcp = MCPClient(
        name="durable-execution-layer",
        capabilities=["state_management", "fault_tolerance"],
    )

    @temporal_mcp.register_tool(
        description="Queue an indestructible SDR sequence workflow."
    )
    def start_durable_sequence(lead_id: str, lead_data: dict) -> str:
        return temporal_mcp.execute_internal("temporal.workflow.start", {
            "target_url": temporal_creds["target_url"],
            "namespace": temporal_creds["namespace"],
            "tls_cert": temporal_creds["cert"],
            "tls_key": temporal_creds["key"],
            "workflow_name": "SDR_Outbound_Sequence",
            "args": [lead_data],
            "workflow_id": f"sequence-{lead_id}",
            "task_queue": "gpt54-sdr-tasks",
        })

    return temporal_mcp


# ── 10. OneTrust MCP (PII Compliance) ───────────────────
def initialize_onetrust_mcp(vault_mcp):
    """Immutable audit trails for Florida Bar solicitation compliance."""
    ot_creds = vault_mcp.execute_tool("fetch_secret", path="onetrust_compliance")

    onetrust_mcp = MCPClient(
        name="pii-compliance-auditor",
        capabilities=["audit_logging", "dsar_management"],
    )

    @onetrust_mcp.register_tool(
        description="Log PII extraction event for Bar compliance audit trails."
    )
    def log_pii_event(attorney_email: str, data_sources: list) -> str:
        return onetrust_mcp.execute_internal("onetrust.consent.receipt", {
            "api_key": ot_creds["api_token"],
            "base_url": ot_creds["base_url"],
            "identifier": attorney_email,
            "processingActivity": "SDR_Cold_Outreach",
            "dataElements": data_sources,
            "lawfulBasis": "Legitimate Interest",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        })

    return onetrust_mcp


# ═══════════════════════════════════════════════════════════
#  BATCH 3 — Observability & Security (Scripts 11–18)
# ═══════════════════════════════════════════════════════════


# ── 11. Datadog MCP (APM Tracing) ────────────────────────
def initialize_datadog_mcp(vault_mcp):
    """Full-stack APM spans across Gradient and n8n."""
    dd_creds = vault_mcp.execute_tool("fetch_secret", path="datadog_apm")

    datadog_mcp = MCPClient(
        name="telemetry-engine",
        capabilities=["apm_tracing", "log_aggregation"],
        environment={
            "DD_API_KEY": dd_creds["api_key"],
            "DD_APP_KEY": dd_creds["app_key"],
            "DD_SITE": "datadoghq.com",
        },
    )

    @datadog_mcp.register_tool(
        description="Inject APM spans for full-stack tracing across Gradient and n8n."
    )
    def inject_apm_trace(service_name: str, operation_name: str, duration_ms: int, metadata: dict) -> str:
        return datadog_mcp.execute_internal("datadog.apm.trace_push", {
            "service": service_name,
            "name": operation_name,
            "duration": duration_ms * 1000000,
            "meta": metadata,
        })

    return datadog_mcp


# ── 12. New Relic MCP (LLM Drift Detection) ─────────────
def initialize_newrelic_mcp(vault_mcp):
    """Flags off-brand GPT-5.4 email generation."""
    nr_creds = vault_mcp.execute_tool("fetch_secret", path="newrelic_telemetry")

    newrelic_mcp = MCPClient(
        name="anomaly-detection-engine",
        capabilities=["ai_monitoring", "anomaly_detection"],
        environment={
            "NEW_RELIC_LICENSE_KEY": nr_creds["license_key"],
            "NEW_RELIC_ACCOUNT_ID": nr_creds["account_id"],
        },
    )

    @newrelic_mcp.register_tool(
        description="Flag when GPT-5.4 starts generating off-brand emails."
    )
    def analyze_llm_drift(prompt: str, generated_email: str) -> dict:
        return newrelic_mcp.execute_internal("newrelic.mlops.evaluate_response", {
            "model_name": "gpt-5.4",
            "input": prompt,
            "output": generated_email,
            "evaluation_metric": "brand_voice_deviation",
            "confidence_threshold": 0.85,
        })

    return newrelic_mcp


# ── 13. Kafka MCP (Event Streaming) ─────────────────────
#    BENCHED — white-label scale-out only
def initialize_kafka_mcp(vault_mcp):
    """Pub/sub event broker — decouples scraping from enrichment."""
    kafka_creds = vault_mcp.execute_tool("fetch_secret", path="apache_kafka")

    kafka_mcp = MCPClient(
        name="event-stream-broker",
        capabilities=["pubsub_messaging", "event_streaming"],
        environment={
            "KAFKA_BROKERS": kafka_creds["broker_url"],
            "KAFKA_SASL_USERNAME": kafka_creds["username"],
            "KAFKA_SASL_PASSWORD": kafka_creds["password"],
        },
    )

    @kafka_mcp.register_tool(
        description="Publish scraping events to decouple DOM extraction from the enrichment layer."
    )
    def publish_scrape_event(topic: str, scrape_payload: dict) -> str:
        return kafka_mcp.execute_internal("kafka.producer.send", {
            "topic": topic,
            "message": scrape_payload,
            "partition_key": scrape_payload.get("firm_name", "unassigned"),
        })

    return kafka_mcp


# ── 14. Redis MCP (Scrape Caching) ──────────────────────
def initialize_redis_mcp(vault_mcp):
    """Caches Florida Bar scrape results to prevent redundant hits."""
    redis_creds = vault_mcp.execute_tool("fetch_secret", path="redis_cache")

    redis_mcp = MCPClient(
        name="scrape-caching-layer",
        capabilities=["key_value_store", "ttl_management"],
        environment={
            "REDIS_URL": redis_creds["connection_string"],
        },
    )

    @redis_mcp.register_tool(
        description="Cache Florida Bar scrape results to prevent redundant directory hits."
    )
    def cache_attorney_scrape(bar_number: str, profile_data: dict) -> dict:
        return redis_mcp.execute_internal("redis.setex", {
            "key": f"fl_bar_scrape:{bar_number}",
            "seconds": 2592000,
            "value": profile_data,
        })

    return redis_mcp


# ── 15. OWASP ZAP MCP (DAST Scanning) ───────────────────
def initialize_owasp_zap_mcp(vault_mcp):
    """Automated injection tests against n8n webhooks."""
    zap_creds = vault_mcp.execute_tool("fetch_secret", path="owasp_zap")

    zap_mcp = MCPClient(
        name="penetration-tester",
        capabilities=["dast_scanning", "vulnerability_assessment"],
        environment={
            "ZAP_API_KEY": zap_creds["api_key"],
            "ZAP_PROXY_URL": zap_creds["proxy_url"],
        },
    )

    @zap_mcp.register_tool(
        description="Run automated injection tests against n8n orchestrator webhooks."
    )
    def execute_webhook_scan(target_webhook_url: str) -> dict:
        return zap_mcp.execute_internal("zap.ascan.scan", {
            "url": target_webhook_url,
            "recurse": False,
            "inScopeOnly": True,
            "scanPolicyName": "Strict_API_Injection",
        })

    return zap_mcp


# ── 16. Snyk MCP (Dependency Scanning) ──────────────────
def initialize_snyk_mcp(vault_mcp):
    """SAST/IaC scanning before deployment."""
    snyk_creds = vault_mcp.execute_tool("fetch_secret", path="snyk_security")

    snyk_mcp = MCPClient(
        name="dependency-scanner",
        capabilities=["sast_scanning", "iac_analysis"],
        environment={
            "SNYK_TOKEN": snyk_creds["api_token"],
        },
    )

    @snyk_mcp.register_tool(
        description="Scan Python ADK and n8n JSON configs for vulnerabilities before deployment."
    )
    def scan_deployment_artifacts(repository_path: str) -> dict:
        return snyk_mcp.execute_internal("snyk.test.repository", {
            "path": repository_path,
            "fail_on_issues": True,
            "severity_threshold": "high",
        })

    return snyk_mcp


# ── 17. Cloudflare WAF MCP (Rate Limiting) ──────────────
def initialize_cloudflare_waf_mcp(vault_mcp):
    """Rate-limits competitor scraping bots on the agency dashboard."""
    cf_creds = vault_mcp.execute_tool("fetch_secret", path="cloudflare_waf")

    cf_mcp = MCPClient(
        name="web-application-firewall",
        capabilities=["rate_limiting", "bot_management"],
        environment={
            "CF_API_TOKEN": cf_creds["api_token"],
            "CF_ZONE_ID": cf_creds["zone_id"],
        },
    )

    @cf_mcp.register_tool(
        description="Rate-limit competitors trying to scrape the agency dashboard."
    )
    def deploy_rate_limit_rule(ip_address: str) -> str:
        return cf_mcp.execute_internal("cloudflare.firewall.rules.create", {
            "action": "block",
            "filter": {
                "expression": f"(ip.src eq {ip_address}) and (http.request.uri.path contains '/dashboard')"
            },
            "description": "Auto-blocked competitor scraping bot",
        })

    return cf_mcp


# ── 18. DMARC Analyzer MCP (Domain Reputation) ──────────
def initialize_dmarc_analyzer_mcp(vault_mcp):
    """Alerts if Workspace sending domains drop below 95% alignment."""
    dmarc_creds = vault_mcp.execute_tool("fetch_secret", path="dmarc_analyzer")

    dmarc_mcp = MCPClient(
        name="domain-reputation-monitor",
        capabilities=["domain_health", "dns_monitoring"],
        environment={
            "DMARC_API_KEY": dmarc_creds["api_key"],
        },
    )

    @dmarc_mcp.register_tool(
        description="Alert if Workspace sending domains drop below 95% alignment."
    )
    def check_domain_alignment(domain: str) -> dict:
        health_data = dmarc_mcp.execute_internal("dmarc.domain.health", {
            "domain": domain,
        })
        if health_data.get("alignment_score", 0) < 95:
            dmarc_mcp.execute_internal("alert.trigger", {
                "severity": "CRITICAL",
                "message": f"Domain {domain} dropped to {health_data.get('alignment_score')}% alignment.",
            })
        return health_data

    return dmarc_mcp


# ═══════════════════════════════════════════════════════════
#  FINAL BATCH — Revenue & Scale-Out (Scripts 19–25)
# ═══════════════════════════════════════════════════════════


# ── 19. Postmark MCP (Transactional Email) ──────────────
#    BENCHED — white-label scale-out only
def initialize_postmark_mcp(vault_mcp):
    """Handles onboarding/receipt emails post-payment."""
    postmark_creds = vault_mcp.execute_tool("fetch_secret", path="postmark_router")

    postmark_mcp = MCPClient(
        name="transactional-router",
        capabilities=["transactional_email", "receipt_routing"],
        environment={
            "POSTMARK_SERVER_TOKEN": postmark_creds["server_token"],
        },
    )

    @postmark_mcp.register_tool(
        description="Handle onboarding/receipt emails once an attorney pays via Stripe."
    )
    def send_payment_receipt(attorney_email: str, receipt_url: str, attorney_name: str) -> str:
        return postmark_mcp.execute_internal("postmark.email.send_with_template", {
            "From": "billing@yourdomain.com",
            "To": attorney_email,
            "TemplateAlias": "trial-onboarding-receipt",
            "TemplateModel": {
                "name": attorney_name,
                "receipt_link": receipt_url,
                "trial_price": "$99.00",
            },
            "MessageStream": "outbound-transactional",
        })

    return postmark_mcp


# ── 20. PandaDoc MCP (Contract Generation) ──────────────
#    WHITE-LABEL ONLY — not active in core deployment
def initialize_pandadoc_mcp(vault_mcp):
    """Auto-generates $99/week trial agreements for e-signature."""
    panda_creds = vault_mcp.execute_tool("fetch_secret", path="pandadoc_contracts")

    panda_mcp = MCPClient(
        name="contract-generator",
        capabilities=["document_generation", "esignature_routing"],
        environment={
            "PANDADOC_API_KEY": panda_creds["api_key"],
        },
    )

    @panda_mcp.register_tool(
        description="Auto-generate the $99/week trial agreement when an attorney replies 'yes'."
    )
    def generate_trial_agreement(attorney_name: str, attorney_email: str, firm_name: str) -> str:
        return panda_mcp.execute_internal("pandadoc.document.create", {
            "name": f"AI Receptionist Trial Agreement - {firm_name}",
            "template_uuid": panda_creds["trial_template_id"],
            "recipients": [
                {
                    "email": attorney_email,
                    "first_name": attorney_name.split()[0],
                    "last_name": attorney_name.split()[-1] if " " in attorney_name else "",
                    "role": "Client",
                }
            ],
            "tokens": [
                {"name": "Firm_Name", "value": firm_name},
                {"name": "Trial_Price", "value": "$99.00/week"},
            ],
            "send_document": True,
        })

    return panda_mcp


# ── 21. Mailreach MCP (Deliverability Rotation) ─────────
def initialize_mailreach_mcp(vault_mcp):
    """Rotates secondary Workspace aliases to bypass Gmail 2K/day limit."""
    mr_creds = vault_mcp.execute_tool("fetch_secret", path="mailreach_deliverability")

    mailreach_mcp = MCPClient(
        name="deliverability-load-balancer",
        capabilities=["inbox_placement", "sender_rotation"],
        environment={
            "MAILREACH_API_KEY": mr_creds["api_key"],
        },
    )

    @mailreach_mcp.register_tool(
        description="Rotate secondary Workspace aliases to bypass the 2,000/day Gmail sending limit."
    )
    def get_warmed_sender_alias(target_volume: int) -> str:
        active_senders = mailreach_mcp.execute_internal("mailreach.senders.list_healthy", {
            "min_health_score": 95,
            "required_capacity": target_volume,
        })
        if not active_senders:
            raise Exception("No warmed Workspace aliases available above 95% health.")
        return active_senders[0]["smtp_alias"]

    return mailreach_mcp


# ── 22. HubSpot MCP (External CRM Sync) ─────────────────
#    BENCHED — white-label scale-out only
def initialize_hubspot_mcp(vault_mcp):
    """Syncs enriched leads to external white-label client CRMs."""
    hs_creds = vault_mcp.execute_tool("fetch_secret", path="hubspot_whitelabel")

    hubspot_mcp = MCPClient(
        name="whitelabel-crm-router",
        capabilities=["external_crm_sync", "contact_management"],
        environment={
            "HUBSPOT_ACCESS_TOKEN": hs_creds["access_token"],
        },
    )

    @hubspot_mcp.register_tool(
        description="BENCHED: Sync enriched lead data strictly for external white-label client deployments."
    )
    def sync_to_client_crm(client_id: str, lead_data: dict) -> dict:
        return hubspot_mcp.execute_internal("hubspot.crm.contacts.create", {
            "properties": {
                "firstname": lead_data.get("name", "").split()[0],
                "lastname": lead_data.get("name", "").split()[-1] if " " in lead_data.get("name", "") else "",
                "email": lead_data.get("professional_email"),
                "company": lead_data.get("firm"),
                "phone": lead_data.get("mobile_number"),
                "lead_source": "AI_SDR_Engine",
            },
        })

    return hubspot_mcp


# ── 23. SendGrid MCP (External SMTP Routing) ────────────
#    BENCHED — white-label scale-out only
def initialize_sendgrid_mcp(vault_mcp):
    """Routes outbound pitches for non-Workspace white-label clients."""
    sg_creds = vault_mcp.execute_tool("fetch_secret", path="sendgrid_whitelabel")

    sendgrid_mcp = MCPClient(
        name="whitelabel-smtp-router",
        capabilities=["external_smtp_routing", "bulk_email"],
        environment={
            "SENDGRID_API_KEY": sg_creds["api_key"],
        },
    )

    @sendgrid_mcp.register_tool(
        description="BENCHED: Route outbound pitches for white-label clients who do not use Google Workspace."
    )
    def route_external_outreach(client_domain: str, to_email: str, subject: str, html_content: str) -> dict:
        return sendgrid_mcp.execute_internal("sendgrid.mail.send", {
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": f"ai-receptionist@{client_domain}"},
            "subject": subject,
            "content": [{"type": "text/html", "value": html_content}],
        })

    return sendgrid_mcp


# ── 24. Lemon Squeezy MCP ($99/week Billing) ────────────
def initialize_lemon_squeezy_mcp(vault_mcp):
    """Generates secure checkout links for the $99/week trial."""
    ls_creds = vault_mcp.execute_tool("fetch_secret", path="lemon_squeezy_billing")

    lemon_mcp = MCPClient(
        name="trial-billing-engine",
        capabilities=["subscription_management", "payment_processing"],
        environment={
            "LEMON_SQUEEZY_API_KEY": ls_creds["api_key"],
        },
    )

    @lemon_mcp.register_tool(
        description="Generate a secure checkout link for the $99/week AI receptionist trial."
    )
    def create_trial_checkout(attorney_email: str, attorney_name: str) -> str:
        checkout_data = lemon_mcp.execute_internal("lemonsqueezy.checkouts.create", {
            "store_id": ls_creds["store_id"],
            "variant_id": ls_creds["trial_variant_id"],
            "checkout_data": {
                "email": attorney_email,
                "name": attorney_name,
                "custom_price": 9900,
            },
        })
        return checkout_data.get("url")

    return lemon_mcp


# ── 25. Terraform MCP (IaC Provisioner) ─────────────────
#    WHITE-LABEL ONLY — not active in core deployment
def initialize_terraform_mcp(vault_mcp):
    """Deploys isolated infrastructure for white-label client onboarding."""
    tf_creds = vault_mcp.execute_tool("fetch_secret", path="terraform_infrastructure")

    terraform_mcp = MCPClient(
        name="infrastructure-provisioner",
        capabilities=["iac_deployment", "state_management"],
        environment={
            "TF_API_TOKEN": tf_creds["api_token"],
        },
    )

    @terraform_mcp.register_tool(
        description="Deploy isolated infrastructure environments for white-label client onboarding."
    )
    def provision_client_environment(client_id: str) -> dict:
        return terraform_mcp.execute_internal("terraform.workspace.apply", {
            "workspace_name": f"client-{client_id}",
            "auto_approve": True,
            "variables": {
                "deploy_n8n_instance": True,
                "deploy_postgres_db": True,
            },
        })

    return terraform_mcp

#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────
# vault_init.sh — Spin up HashiCorp Vault dev server and
# pre-populate ALL 25 secret paths for the SDR Army MCPs.
# ──────────────────────────────────────────────────────────
set -euo pipefail

VAULT_DEV_ROOT_TOKEN="dev-root-token"
VAULT_PORT=8200

echo "═══════════════════════════════════════════════════════"
echo "  Vault Dev Server — SDR Army Secret Initialization"
echo "  25 Secret Paths (5 Original + 20 New)"
echo "═══════════════════════════════════════════════════════"

# ── Check if Vault is installed ──
if ! command -v vault &>/dev/null; then
  echo "[INFO] Vault CLI not found. Attempting Docker fallback..."

  # Kill any existing vault dev container
  docker rm -f sdr-vault-dev 2>/dev/null || true

  docker run -d \
    --name sdr-vault-dev \
    --cap-add=IPC_LOCK \
    -p ${VAULT_PORT}:8200 \
    -e "VAULT_DEV_ROOT_TOKEN_ID=${VAULT_DEV_ROOT_TOKEN}" \
    -e "VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200" \
    hashicorp/vault:latest server -dev

  echo "[INFO] Waiting for Vault container to become healthy..."
  sleep 3

  VAULT_CMD="docker exec -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=${VAULT_DEV_ROOT_TOKEN} sdr-vault-dev vault"
else
  echo "[INFO] Vault CLI detected. Starting dev server..."
  pkill -f "vault server -dev" 2>/dev/null || true
  sleep 1

  vault server -dev \
    -dev-root-token-id="${VAULT_DEV_ROOT_TOKEN}" \
    -dev-listen-address="127.0.0.1:${VAULT_PORT}" &

  sleep 2
  VAULT_CMD="vault"
  export VAULT_ADDR="http://127.0.0.1:${VAULT_PORT}"
  export VAULT_TOKEN="${VAULT_DEV_ROOT_TOKEN}"
fi

echo ""
echo "[STEP 1/25] Enabling KV v2 secrets engine at enterprise-revops/..."
${VAULT_CMD} secrets enable -path=enterprise-revops kv-v2 2>/dev/null || \
  echo "  └── Already enabled (skipping)"

# ═══════════════════════════════════════════════════════════
#  ORIGINAL 5 SECRET PATHS
# ═══════════════════════════════════════════════════════════

echo ""
echo "[STEP 2/25] Seeding Google Workspace secrets..."
${VAULT_CMD} kv put enterprise-revops/google_workspace \
  service_account_json='{"type":"service_account","project_id":"sdr-army-prod"}' \
  admin_inbox="revops@yourdomain.com"

echo ""
echo "[STEP 3/25] Seeding Bright Data proxy credentials..."
${VAULT_CMD} kv put enterprise-revops/brightdata \
  account_id="PLACEHOLDER_BD_ACCOUNT" \
  api_token="PLACEHOLDER_BD_TOKEN" \
  username="PLACEHOLDER_BD_USER" \
  password="PLACEHOLDER_BD_PASS"

echo ""
echo "[STEP 4/25] Seeding ElevenLabs voice synthesis credentials..."
${VAULT_CMD} kv put enterprise-revops/elevenlabs \
  api_key="PLACEHOLDER_ELEVENLABS_KEY" \
  voice_id="PLACEHOLDER_VOICE_ID"

echo ""
echo "[STEP 5/25] Seeding n8n orchestration credentials..."
${VAULT_CMD} kv put enterprise-revops/n8n_orchestration \
  base_url="https://n8n.yourdomain.com" \
  api_key="PLACEHOLDER_N8N_API_KEY"

# ═══════════════════════════════════════════════════════════
#  20 NEW SECRET PATHS
# ═══════════════════════════════════════════════════════════

echo ""
echo "[STEP 6/25] Seeding Playwright engine config..."
${VAULT_CMD} kv put enterprise-revops/playwright_engine \
  browser_type="chromium" \
  headless="true" \
  stealth_mode="true" \
  viewport_width="1920" \
  viewport_height="1080"

echo ""
echo "[STEP 7/25] Seeding Data Enrichment (Apollo + PDL) credentials..."
${VAULT_CMD} kv put enterprise-revops/data_enrichment \
  apollo_key="PLACEHOLDER_APOLLO_KEY" \
  pdl_key="PLACEHOLDER_PDL_KEY"

echo ""
echo "[STEP 8/25] Seeding Vapi Telephony credentials..."
${VAULT_CMD} kv put enterprise-revops/vapi_telephony \
  private_api_key="PLACEHOLDER_VAPI_KEY" \
  phone_number_id="PLACEHOLDER_PHONE_ID"

echo ""
echo "[STEP 9/25] Seeding Temporal cluster credentials..."
${VAULT_CMD} kv put enterprise-revops/temporal_cluster \
  target_url="PLACEHOLDER_TEMPORAL_URL" \
  namespace="sdr-production" \
  cert="PLACEHOLDER_TLS_CERT" \
  key="PLACEHOLDER_TLS_KEY"

echo ""
echo "[STEP 10/25] Seeding OneTrust compliance credentials..."
${VAULT_CMD} kv put enterprise-revops/onetrust_compliance \
  api_token="PLACEHOLDER_ONETRUST_TOKEN" \
  base_url="https://app.onetrust.com"

echo ""
echo "[STEP 11/25] Seeding Datadog APM credentials..."
${VAULT_CMD} kv put enterprise-revops/datadog_apm \
  api_key="PLACEHOLDER_DD_API_KEY" \
  app_key="PLACEHOLDER_DD_APP_KEY"

echo ""
echo "[STEP 12/25] Seeding New Relic telemetry credentials..."
${VAULT_CMD} kv put enterprise-revops/newrelic_telemetry \
  license_key="PLACEHOLDER_NR_LICENSE" \
  account_id="PLACEHOLDER_NR_ACCOUNT"

echo ""
echo "[STEP 13/25] Seeding Apache Kafka credentials..."
${VAULT_CMD} kv put enterprise-revops/apache_kafka \
  broker_url="PLACEHOLDER_KAFKA_BROKER" \
  username="PLACEHOLDER_KAFKA_USER" \
  password="PLACEHOLDER_KAFKA_PASS"

echo ""
echo "[STEP 14/25] Seeding Redis cache credentials..."
${VAULT_CMD} kv put enterprise-revops/redis_cache \
  connection_string="redis://default:PLACEHOLDER@redis.yourdomain.com:6379/0"

echo ""
echo "[STEP 15/25] Seeding OWASP ZAP credentials..."
${VAULT_CMD} kv put enterprise-revops/owasp_zap \
  api_key="PLACEHOLDER_ZAP_KEY" \
  proxy_url="http://127.0.0.1:8090"

echo ""
echo "[STEP 16/25] Seeding Snyk security credentials..."
${VAULT_CMD} kv put enterprise-revops/snyk_security \
  api_token="PLACEHOLDER_SNYK_TOKEN"

echo ""
echo "[STEP 17/25] Seeding Cloudflare WAF credentials..."
${VAULT_CMD} kv put enterprise-revops/cloudflare_waf \
  api_token="PLACEHOLDER_CF_TOKEN" \
  zone_id="PLACEHOLDER_CF_ZONE"

echo ""
echo "[STEP 18/25] Seeding DMARC analyzer credentials..."
${VAULT_CMD} kv put enterprise-revops/dmarc_analyzer \
  api_key="PLACEHOLDER_DMARC_KEY"

echo ""
echo "[STEP 19/25] Seeding Postmark router credentials..."
${VAULT_CMD} kv put enterprise-revops/postmark_router \
  server_token="PLACEHOLDER_POSTMARK_TOKEN"

echo ""
echo "[STEP 20/25] Seeding PandaDoc contracts credentials..."
${VAULT_CMD} kv put enterprise-revops/pandadoc_contracts \
  api_key="PLACEHOLDER_PANDADOC_KEY" \
  trial_template_id="PLACEHOLDER_TEMPLATE_ID"

echo ""
echo "[STEP 21/25] Seeding Mailreach deliverability credentials..."
${VAULT_CMD} kv put enterprise-revops/mailreach_deliverability \
  api_key="PLACEHOLDER_MAILREACH_KEY"

echo ""
echo "[STEP 22/25] Seeding HubSpot white-label credentials..."
${VAULT_CMD} kv put enterprise-revops/hubspot_whitelabel \
  access_token="PLACEHOLDER_HUBSPOT_TOKEN"

echo ""
echo "[STEP 23/25] Seeding SendGrid white-label credentials..."
${VAULT_CMD} kv put enterprise-revops/sendgrid_whitelabel \
  api_key="PLACEHOLDER_SENDGRID_KEY"

echo ""
echo "[STEP 24/25] Seeding Lemon Squeezy billing credentials..."
${VAULT_CMD} kv put enterprise-revops/lemon_squeezy_billing \
  api_key="PLACEHOLDER_LEMON_KEY" \
  store_id="PLACEHOLDER_STORE_ID" \
  trial_variant_id="PLACEHOLDER_VARIANT_ID"

echo ""
echo "[STEP 25/25] Seeding Terraform infrastructure credentials..."
${VAULT_CMD} kv put enterprise-revops/terraform_infrastructure \
  api_token="PLACEHOLDER_TF_TOKEN"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  ✓ Vault dev server running on http://127.0.0.1:${VAULT_PORT}"
echo "  ✓ Root token: ${VAULT_DEV_ROOT_TOKEN}"
echo "  ✓ 25 secret paths pre-populated under enterprise-revops/"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Export these to your shell:"
echo "  export VAULT_ADDR=http://127.0.0.1:${VAULT_PORT}"
echo "  export VAULT_TOKEN=${VAULT_DEV_ROOT_TOKEN}"

#!/bin/bash
set -e

# ═══════════════════════════════════════════════════════════
#  n8n Droplet Workflow Management Script
#  Instance : https://n8n.kaytral.com (Cloudflare Tunnel)
#  Tunnel   : n8n-kaytral (86d57e57-e85d-4eb1-be75-ca13c9bdf410)
#
#  Usage:
#    ./n8n_import.sh              # Full run: set descriptions, activate, validate
#    ./n8n_import.sh --desc-only  # Only update workflow descriptions
#    ./n8n_import.sh --validate   # Only run validation
#
#  Credentials are loaded from .env (if readable) or from
#  N8N_DROPLET_URL / N8N_DROPLET_API_KEY env vars.
# ═══════════════════════════════════════════════════════════

# --- Load secrets from .env (best-effort) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ] && [ -r "$SCRIPT_DIR/.env" ]; then
  set -a
  source "$SCRIPT_DIR/.env"
  set +a
fi

# --- Resolve connection vars ---
N8N_URL="${N8N_DROPLET_URL:-https://n8n.kaytral.com/api/v1}"
API_KEY="${N8N_DROPLET_API_KEY}"

if [ -z "$API_KEY" ]; then
  echo "ERROR: N8N_DROPLET_API_KEY is not set."
  echo "       Export it, or ensure .env is readable."
  exit 1
fi

HEADERS=(-H "X-N8N-API-KEY: $API_KEY" -H "Content-Type: application/json")

# --- Workflow registry (parallel arrays — macOS bash 3 safe) ---
WF_IDS=(   "Dm0cx2eTqoBhVyzX"    "pMCBaZxdwWYRaKib"           "QnuPnwRp0bqKkace" )
WF_NAMES=( "Failure Telemetry & Alerting Router" \
           "Daily Scrape & Enrich Pipeline" \
           "GPT-5.4 Email Generator & Sender" )
WF_DESCS=( \
  "Cross-agent error handler. Catches failures from Scraper and Pitcher workflows, classifies severity, routes alerts to Gmail/Slack, logs telemetry to Datadog and New Relic, and triggers automatic retry logic via Temporal where applicable." \
  "SDR-Scraper agent workflow. Runs daily via cron to scrape leads from Apollo/PDL via Bright Data proxies, enrich contact data, deduplicate against Redis, apply OneTrust compliance checks, and push qualified leads to Google Sheets CRM." \
  "SDR-Pitcher agent workflow. Generates hyper-personalised outbound emails using GPT-5.4, validates deliverability through MailReach and DMARC checks, and sends via Gmail (Google Workspace). Tracks open/reply signals back to Google Sheets CRM." \
)

# ── Helpers ──────────────────────────────────────────────

patch_descriptions() {
  echo "=== Setting workflow descriptions ==="
  for i in "${!WF_IDS[@]}"; do
    local WF_ID="${WF_IDS[$i]}"
    local NAME="${WF_NAMES[$i]}"
    local DESC="${WF_DESCS[$i]}"
    echo -n "  ${NAME}... "

    # n8n API v1 requires PUT with full workflow body — GET → inject desc → PUT
    UPDATED=$(curl -s "$N8N_URL/workflows/$WF_ID" "${HEADERS[@]}" | python3 -c "
import sys, json
wf = json.load(sys.stdin)
wf['description'] = '''$DESC'''
# Remove read-only fields that the PUT endpoint rejects
for key in ['id', 'createdAt', 'updatedAt', 'versionId']:
    wf.pop(key, None)
print(json.dumps(wf))
")

    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
      -X PUT "$N8N_URL/workflows/$WF_ID" \
      "${HEADERS[@]}" \
      -d "$UPDATED")

    if [ "$HTTP_CODE" = "200" ]; then
      echo "✓ description set"
    else
      echo "⚠ HTTP $HTTP_CODE"
    fi
  done
  echo ""
}

activate_workflows() {
  echo "=== Activating workflows ==="
  for i in "${!WF_IDS[@]}"; do
    local WF_ID="${WF_IDS[$i]}"
    local NAME="${WF_NAMES[$i]}"
    echo -n "  ${NAME}... "
    curl -s -X POST "$N8N_URL/workflows/$WF_ID/activate" "${HEADERS[@]}" 2>&1 | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if d.get('active'):
        print('ACTIVE ✓')
    elif 'message' in d:
        print(f'ERROR: {d[\"message\"]}')
    else:
        print('unknown response')
except Exception as e:
    print(f'parse error: {e}')
" 2>&1
  done
  echo ""
}

validate_workflows() {
  echo "=== Validation ==="
  curl -s "$N8N_URL/workflows" "${HEADERS[@]}" 2>&1 | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    for wf in d.get('data', []):
        http = [n['name'] for n in wf.get('nodes',[]) if 'httpRequest' in n.get('type','')]
        err  = wf.get('settings',{}).get('errorWorkflow','—')
        desc = wf.get('description','') or '(none)'
        desc_preview = (desc[:60] + '…') if len(desc) > 60 else desc
        status = '✓' if wf['active'] else '✗'
        print(f'  [{status}] {wf[\"name\"]} [{wf[\"id\"]}]')
        print(f'      active={wf[\"active\"]}, httpNodes={http}, errorWF={err}')
        print(f'      desc: {desc_preview}')
        print()
except Exception as e:
    print(f'Validation error: {e}')
" 2>&1
}

# ── Main ─────────────────────────────────────────────────

echo "╔════════════════════════════════════════════════════════╗"
echo "║   n8n Droplet Workflow Management                     ║"
echo "║   https://n8n.kaytral.com                             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

case "${1:-}" in
  --desc-only)
    patch_descriptions
    ;;
  --validate)
    validate_workflows
    ;;
  *)
    patch_descriptions
    activate_workflows
    validate_workflows
    ;;
esac

echo "DONE."

#!/bin/bash
set -e

# ═══════════════════════════════════════════════════════════
#  n8n Droplet Workflow Management Script
#  Instance : https://n8n.kaytral.com (Cloudflare Tunnel)
#  Owner    : admin@caytral.com / Zuldeira2026!SDR
#  Tunnel   : n8n-kaytral (86d57e57-e85d-4eb1-be75-ca13c9bdf410)
# ═══════════════════════════════════════════════════════════

N8N_URL="https://n8n.kaytral.com/api/v1"
API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkMTA2YmMwNy01ODY4LTQ0ZDYtYmYwZC1lYzY0YjIwMGU1YzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZTIxOGFmMmMtYjFmYy00YjU3LWFhMTEtY2VmY2Y0NzQ2OWNjIiwiaWF0IjoxNzczNjk1NjQ3LCJleHAiOjE3NzYyMjU2MDB9.vRhYYj2TPEQn1fbXN-pwc1Y724plnapbHZbErAOjrXM"
HEADERS=(-H "X-N8N-API-KEY: $API_KEY" -H "Content-Type: application/json")

# Workflow IDs on Droplet n8n
WF_SCRAPER="pMCBaZxdwWYRaKib"      # Daily Scrape & Enrich Pipeline
WF_PITCHER="QnuPnwRp0bqKkace"      # GPT-5.4 Email Generator & Sender
WF_ERROR="Dm0cx2eTqoBhVyzX"        # Failure Telemetry & Alerting Router

echo "╔════════════════════════════════════════════════════════╗"
echo "║   n8n Droplet Workflow Activation                     ║"
echo "║   https://n8n.kaytral.com                             ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

echo "=== Activating workflows ==="
for WF_ID in $WF_ERROR $WF_SCRAPER $WF_PITCHER; do
  echo -n "Activating $WF_ID... "
  curl -s -X POST "$N8N_URL/workflows/$WF_ID/activate" "${HEADERS[@]}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('active'):
    print(f'{d[\"name\"]} → ACTIVE ✓')
elif 'message' in d:
    print(f'ERROR: {d[\"message\"]}')
" 2>&1
done

echo ""
echo "=== Validation ==="
curl -s "$N8N_URL/workflows" "${HEADERS[@]}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for wf in d.get('data', []):
    http = [n['name'] for n in wf.get('nodes',[]) if 'httpRequest' in n.get('type','')]
    err  = wf.get('settings',{}).get('errorWorkflow','—')
    print(f'  {wf[\"name\"]} [{wf[\"id\"]}]')
    print(f'    active={wf[\"active\"]}, httpNodes={http}, errorWF={err}')
    print()
" 2>&1

echo "DONE."

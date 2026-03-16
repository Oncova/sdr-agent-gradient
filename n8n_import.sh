#!/bin/bash
set -e

# ═══════════════════════════════════════════════════════════
#  n8n Cloud Workflow Import & Activation Script
#  Target: oncova.app.n8n.cloud
#  Workflows: Scraper, Pitcher, Error Handler
# ═══════════════════════════════════════════════════════════

N8N_URL="https://oncova.app.n8n.cloud/api/v1"
API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0ZjMwMzcyYS0zODYyLTQxZmUtYTdmMC1mYTBlYWE2ZTcxYmUiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZmFlNzMwMTQtZDJhNi00M2FiLTkwOTctM2RmM2JiZjYyNWM1IiwiaWF0IjoxNzczNjkxMzY2LCJleHAiOjE3ODE0MDk2MDB9.HhzW28PCGU0Tbh6eByA85Zbu7XaqRJIIaokb4E1L72w"
HEADERS=(-H "X-N8N-API-KEY: $API_KEY" -H "Content-Type: application/json")

# Existing workflow IDs on oncova.app.n8n.cloud
WF_SCRAPER="r6VX14J1YVXzuVWQ"     # Daily Scrape & Enrich Pipeline
WF_PITCHER="UThLg0MSBBG0ZVir"     # GPT-5.4 Email Generator & Sender
WF_ERROR="WwSr5o6LDnrldC3E"       # Failure Telemetry & Alerting Router

echo "=== Activating workflows ==="

# Activate all 3 (requires OAuth2 credentials to be connected in UI first)
for WF_ID in $WF_SCRAPER $WF_PITCHER $WF_ERROR; do
  echo -n "Activating $WF_ID... "
  curl -s -X POST "$N8N_URL/workflows/$WF_ID/activate" "${HEADERS[@]}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'active={d.get(\"active\", d.get(\"message\", \"?\"))}')
" 2>&1
done

echo ""
echo "=== Setting error workflow ==="

# Set Error Handler as the error workflow for Scraper and Pitcher
for WF_ID in $WF_SCRAPER $WF_PITCHER; do
  echo -n "Setting errorWorkflow on $WF_ID... "
  CURRENT=$(curl -s "$N8N_URL/workflows/$WF_ID" "${HEADERS[@]}")
  UPDATED=$(echo "$CURRENT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
s = d.get('settings', {})
s['errorWorkflow'] = '$WF_ERROR'
clean = {k: v for k, v in s.items() if k in {'executionOrder','errorWorkflow'}}
payload = {'name': d['name'], 'nodes': d['nodes'], 'connections': d['connections'], 'settings': clean}
print(json.dumps(payload))
")
  curl -s -X PUT "$N8N_URL/workflows/$WF_ID" "${HEADERS[@]}" -d "$UPDATED" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'errorWorkflow={d.get(\"settings\",{}).get(\"errorWorkflow\",\"NOT SET\")}')
" 2>&1
done

echo ""
echo "=== Validation ==="
for WF_ID in $WF_SCRAPER $WF_PITCHER $WF_ERROR; do
  curl -s "$N8N_URL/workflows/$WF_ID" "${HEADERS[@]}" | python3 -c "
import sys, json
d = json.load(sys.stdin)
nodes = d['nodes']
http_nodes = [n['name'] for n in nodes if 'httpRequest' in n.get('type','')]
conns = sum(len(v.get('main',[[]])[0]) for v in d.get('connections',{}).values())
err = d.get('settings',{}).get('errorWorkflow','NOT SET')
print(f'{d[\"name\"]}: active={d[\"active\"]}, nodes={len(nodes)}, conns={conns}, httpRequest={http_nodes}, errorWF={err}')
" 2>&1
done

echo ""
echo "DONE."

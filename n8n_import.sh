#!/bin/bash
set -e

N8N_URL="http://127.0.0.1:5678/api/v1"
API_KEY="PLACEHOLDER_N8N_API_KEY"
HEADERS=(-H "X-N8N-API-KEY: $API_KEY" -H "Content-Type: application/json")

WF1_ID=$(curl -s -X POST "$N8N_URL/workflows" "${HEADERS[@]}" -d @workflow_1.json | jq -r '.id')
WF2_ID=$(curl -s -X POST "$N8N_URL/workflows" "${HEADERS[@]}" -d @workflow_2.json | jq -r '.id')
WF3_ID=$(curl -s -X POST "$N8N_URL/workflows" "${HEADERS[@]}" -d @workflow_3.json | jq -r '.id')

curl -s -X POST "$N8N_URL/workflows/$WF1_ID/activate" "${HEADERS[@]}"
curl -s -X POST "$N8N_URL/workflows/$WF2_ID/activate" "${HEADERS[@]}"
curl -s -X POST "$N8N_URL/workflows/$WF3_ID/activate" "${HEADERS[@]}"

curl -s -X PUT "$N8N_URL/workflows/$WF1_ID" "${HEADERS[@]}" \
  -d "{\"settings\": {\"errorWorkflow\": \"$WF3_ID\"}}"
curl -s -X PUT "$N8N_URL/workflows/$WF2_ID" "${HEADERS[@]}" \
  -d "{\"settings\": {\"errorWorkflow\": \"$WF3_ID\"}}"

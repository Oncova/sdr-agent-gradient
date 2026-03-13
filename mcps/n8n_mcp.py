"""
n8n / Webhook MCP — Intelligent traffic controller.
Evaluates execution context to route payloads internally
(Google Workspace stack) or externally (white-label client infra).
"""

from gradient_adk import MCPClient


def initialize_n8n_router_mcp(vault_mcp):
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
        # Internal context forces execution into Google Workspace constraint
        if client_id == "internal_ops":
            endpoint = "/webhook/google-sheets-crm"
        else:
            # External context triggers white-label toolchain (e.g., HubSpot)
            endpoint = f"/webhook/client-deploy/{client_id}"

        return n8n_mcp.execute_internal(
            "webhook.trigger",
            {"path": endpoint, "method": "POST", "payload": lead_data},
        )

    return n8n_mcp

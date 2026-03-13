"""
Google Workspace MCP — Non-negotiable operational backbone.
Enforces strict failure-alert routing to Gmail, CRM updates to Sheets,
and MP3 streaming to Drive.
"""

from gradient_adk import MCPClient


def initialize_google_workspace_mcp(vault_mcp):
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

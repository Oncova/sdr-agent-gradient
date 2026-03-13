"""
HashiCorp Vault MCP — Cryptographic zero-node.
Secure credential injection for the Gradient ADK runtime.
All downstream MCPs depend on this for dynamic secret loading.
"""

import os
import hvac
from gradient_adk import MCPClient


def initialize_vault_mcp():
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

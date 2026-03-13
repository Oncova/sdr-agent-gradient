"""
Bright Data MCP — Residential proxy rotation engine.
Required for Puppeteer-based DOM extraction on rate-limited
Florida legal directories (Avvo, FindLaw, Florida Bar).
"""

from gradient_adk import MCPClient


def initialize_bright_data_mcp(vault_mcp):
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

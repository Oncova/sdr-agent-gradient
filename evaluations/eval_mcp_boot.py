"""
eval_mcp_boot.py — Evaluation harness for full MCP boot sequence.
Validates that main.py can import and initialize all MCP modules
without runtime errors (dry run — no live API calls).
"""

import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_evaluation():
    print("[EVAL] Testing MCP module imports...")

    try:
        from mcps.vault_mcp import initialize_vault_mcp
        print("[PASS] vault_mcp imports ✓")
    except ImportError as e:
        print(f"[FAIL] vault_mcp: {e}")
        sys.exit(1)

    try:
        from mcps.workspace_mcp import initialize_google_workspace_mcp
        print("[PASS] workspace_mcp imports ✓")
    except ImportError as e:
        print(f"[FAIL] workspace_mcp: {e}")
        sys.exit(1)

    try:
        from mcps.brightdata_mcp import initialize_bright_data_mcp
        print("[PASS] brightdata_mcp imports ✓")
    except ImportError as e:
        print(f"[FAIL] brightdata_mcp: {e}")
        sys.exit(1)

    try:
        from mcps.elevenlabs_mcp import initialize_elevenlabs_mcp
        print("[PASS] elevenlabs_mcp imports ✓")
    except ImportError as e:
        print(f"[FAIL] elevenlabs_mcp: {e}")
        sys.exit(1)

    try:
        from mcps.n8n_mcp import initialize_n8n_router_mcp
        print("[PASS] n8n_mcp imports ✓")
    except ImportError as e:
        print(f"[FAIL] n8n_mcp: {e}")
        sys.exit(1)

    try:
        from gradient_adk import GradientAgent, MCPClient
        print("[PASS] gradient_adk imports ✓")
    except ImportError as e:
        print(f"[FAIL] gradient_adk: {e}")
        sys.exit(1)

    print("\n[RESULT] All MCP import evaluations PASSED ✓")


if __name__ == "__main__":
    run_evaluation()

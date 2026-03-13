"""
eval_vault.py — Evaluation harness for Vault MCP connectivity.
Validates that the dev Vault server is reachable and all
secret paths are populated with expected keys.
"""

import os
import sys
import hvac


EXPECTED_PATHS = {
    "google_workspace": ["service_account_json", "admin_inbox"],
    "brightdata": ["account_id", "api_token", "username", "password"],
    "elevenlabs": ["api_key", "voice_id"],
    "n8n_orchestration": ["base_url", "api_key"],
}


def run_evaluation():
    vault_addr = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
    vault_token = os.environ.get("VAULT_TOKEN", "dev-root-token")

    print(f"[EVAL] Connecting to Vault at {vault_addr}...")
    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        print("[FAIL] Vault authentication failed.")
        sys.exit(1)
    print("[PASS] Vault authenticated ✓")

    all_passed = True
    for path, expected_keys in EXPECTED_PATHS.items():
        try:
            response = client.secrets.kv.v2.read_secret_version(
                path=path, mount_point="enterprise-revops"
            )
            data = response["data"]["data"]
            missing = [k for k in expected_keys if k not in data]
            if missing:
                print(f"[FAIL] {path}: missing keys {missing}")
                all_passed = False
            else:
                print(f"[PASS] {path}: all {len(expected_keys)} keys present ✓")
        except Exception as e:
            print(f"[FAIL] {path}: {e}")
            all_passed = False

    if all_passed:
        print("\n[RESULT] All Vault evaluations PASSED ✓")
    else:
        print("\n[RESULT] Some evaluations FAILED ✗")
        sys.exit(1)


if __name__ == "__main__":
    run_evaluation()

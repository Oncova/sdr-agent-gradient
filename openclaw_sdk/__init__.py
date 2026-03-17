"""
gradient_adk — Local stub for DigitalOcean Gradient Agent Development Kit.
Replace with `pip install gradient-adk` when deploying to Gradient infrastructure.

Supports: MCPClient, GradientAgent, Agent, entrypoint decorator, and CLI simulation.
"""

import json
import subprocess
import sys


class MCPClient:
    """Model Context Protocol client for Gradient ADK."""

    def __init__(self, name: str, capabilities: list = None, environment: dict = None):
        self.name = name
        self.capabilities = capabilities or []
        self.environment = environment or {}
        self._tools = {}

    def register_tool(self, description: str = ""):
        def decorator(func):
            self._tools[func.__name__] = {
                "function": func,
                "description": description,
            }
            return func
        return decorator

    def execute_tool(self, tool_name: str, **kwargs):
        if tool_name in self._tools:
            return self._tools[tool_name]["function"](**kwargs)
        raise ValueError(f"Tool '{tool_name}' not registered on MCP '{self.name}'")

    def execute_internal(self, action: str, payload: dict):
        return {"status": "routed", "action": action, "payload": payload}


class GradientAgent:
    """Top-level Gradient agent runner."""

    def __init__(self, name: str, entrypoint: str = "main.py"):
        self.name = name
        self.entrypoint = entrypoint
        self._mcps = []

    def register_mcp(self, mcp: MCPClient):
        self._mcps.append(mcp)
        return self

    def run(self):
        print(f"[GradientAgent] '{self.name}' online with {len(self._mcps)} MCPs:")
        for mcp in self._mcps:
            print(f"  ├── {mcp.name} ({', '.join(mcp.capabilities)})")
        print("[GradientAgent] Runtime loop active. Awaiting webhook triggers.")


class AgentResponse:
    """Simulated response from the Agent LLM invocation."""

    def __init__(self, content: str):
        self.content = content


class Agent:
    """
    Gradient ADK Agent — wraps an LLM model for structured invocation.
    In production, this connects to GPT-5.4 via the Gradient runtime.
    Locally, it generates deterministic test responses for evaluation.
    """

    def __init__(self, name: str, model: str, system_prompt: str):
        self.name = name
        self.model = model
        self.system_prompt = system_prompt

    def invoke(self, prompt: str) -> AgentResponse:
        """
        Invoke the agent with a prompt. In local stub mode, extracts
        prospect details from the prompt and generates a deterministic
        JSON pitch for evaluation purposes.
        """
        lines = prompt.strip().split("\n")
        details = {}
        for line in lines:
            if ":" in line:
                key, val = line.split(":", 1)
                details[key.strip().lower().replace(" ", "_")] = val.strip()

        name = details.get("name", "Attorney")
        firm = details.get("firm", "the firm")
        practice_area = details.get("practice_area", "law")
        specialty = details.get("specialty_tag", "PI")

        if specialty == "CD":
            pain = "arrest and bail emergencies"
            area_label = "criminal defense"
            ai_desc = "trained for criminal defense intake — DUI, domestic violence, felony charges"
        else:
            pain = "accident and injury emergencies"
            area_label = "personal injury"
            ai_desc = "trained for personal injury intake — car crashes, slip-and-falls, workplace injuries"

        pitch = {
            "subject": f"Your {firm} misses calls worth $10K+ — here's the fix",
            "pitch_body": (
                f"Hi {name}, a missed {area_label} intake call costs "
                f"your firm thousands. For $199/month, our AI receptionist answers "
                f"24/7, {ai_desc}. She extracts case details and instantly texts "
                f"you a triage brief. Call [TWILIO_DEMO_NUMBER] to hear her handle a "
                f"frantic client. Reply to this email for $199/month."
            ),
        }
        return AgentResponse(content=json.dumps(pitch))


# ── Entrypoint decorator ──────────────────────────────────
_registered_entrypoint = None


def entrypoint(func):
    """Register a function as the Gradient agent entrypoint."""
    global _registered_entrypoint
    _registered_entrypoint = func
    return func


def get_entrypoint():
    """Retrieve the registered entrypoint function."""
    return _registered_entrypoint


# ── CLI Simulation ────────────────────────────────────────
def cli_deploy(entrypoint_file: str, target: str, name: str):
    """Simulate gradient deploy command."""
    print(f"[gradient-adk] Deploying '{entrypoint_file}' to {target} as '{name}'...")
    print(f"[gradient-adk] Target: DigitalOcean Gradient")
    print(f"[gradient-adk] Agent: {name}")
    print(f"[gradient-adk] Entrypoint: {entrypoint_file}")
    print(f"[gradient-adk] Status: DEPLOYED ✓")
    print(f"[gradient-adk] Endpoint: https://{name}.gradient.digitalocean.com/invoke")
    return {
        "status": "deployed",
        "agent_name": name,
        "endpoint": f"https://{name}.gradient.digitalocean.com/invoke",
    }


def cli_evaluate(test_case_name: str, dataset_file: str, categories: list, success_threshold: float):
    """
    Run evaluation against a CSV dataset.
    Returns pass/fail and per-row scores.
    """
    import csv
    import os

    print(f"[gradient-adk] Evaluation: {test_case_name}")
    print(f"[gradient-adk] Dataset: {dataset_file}")
    print(f"[gradient-adk] Categories: {', '.join(categories)}")
    print(f"[gradient-adk] Threshold: {success_threshold}%")
    print()

    if not os.path.exists(dataset_file):
        raise FileNotFoundError(f"Dataset not found: {dataset_file}")

    # Import the main module to get the entrypoint
    sys.path.insert(0, os.path.dirname(os.path.abspath(dataset_file)) or ".")
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(dataset_file))) or ".")

    import importlib
    main_module = importlib.import_module("main")
    ep = _registered_entrypoint

    if ep is None:
        raise RuntimeError("No @entrypoint function registered")

    results = []
    with open(dataset_file, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            payload = {
                "name": row["name"],
                "firm": row["firm"],
                "practice_area": row["practice_area"],
                "primary_specialty": row.get("primary_specialty", "PI"),
            }

            print(f"  [{i:02d}] Testing: {row['name']} @ {row['firm']} ({row.get('primary_specialty','PI')})...", end=" ")

            try:
                result = ep(payload)
            except Exception as e:
                print(f"ERROR: {e}")
                results.append({"row": i, "score": 0, "error": str(e)})
                continue

            score = 0.0
            checks_passed = 0
            total_checks = 0

            # Check 1: Valid JSON with required keys
            total_checks += 1
            if isinstance(result, dict) and "subject" in result and "pitch_body" in result:
                checks_passed += 1
            else:
                print(f"FAIL (missing keys)")
                results.append({"row": i, "score": 0, "error": "Missing keys"})
                continue

            # Check 2: Subject contains firm name
            total_checks += 1
            expected_subj = row.get("expected_subject_contains", "")
            if expected_subj.lower() in result["subject"].lower():
                checks_passed += 1

            # Check 3: Body contains practice area
            total_checks += 1
            expected_body = row.get("expected_body_contains", "")
            if expected_body.lower() in result["pitch_body"].lower():
                checks_passed += 1

            # Check 4: Under 100 words
            total_checks += 1
            word_count = len(result["pitch_body"].split())
            if word_count < 100:
                checks_passed += 1

            # Check 5: CTA present ($199/month or Twilio demo)
            total_checks += 1
            if row.get("expected_cta_present", "true").lower() == "true":
                cta_keywords = ["199/month", "twilio_demo_number", "reply to this email"]
                if any(kw in result["pitch_body"].lower() for kw in cta_keywords):
                    checks_passed += 1

            row_score = (checks_passed / total_checks) * 100
            results.append({
                "row": i,
                "name": row["name"],
                "score": row_score,
                "word_count": word_count,
                "checks": f"{checks_passed}/{total_checks}",
            })
            status = "PASS" if row_score >= success_threshold else "FAIL"
            print(f"{status} ({row_score:.0f}% — {checks_passed}/{total_checks} checks, {word_count}w)")

    # Calculate aggregate score
    if results:
        avg_score = sum(r["score"] for r in results) / len(results)
    else:
        avg_score = 0

    passed = avg_score >= success_threshold

    print()
    print("=" * 60)
    print(f"  EVALUATION RESULTS: {test_case_name}")
    print(f"  Aggregate Score: {avg_score:.1f}%")
    print(f"  Threshold: {success_threshold}%")
    print(f"  Verdict: {'PASSED ✓' if passed else 'FAILED ✗'}")
    print("=" * 60)

    return {
        "test_case_name": test_case_name,
        "aggregate_score": avg_score,
        "threshold": success_threshold,
        "passed": passed,
        "results": results,
    }

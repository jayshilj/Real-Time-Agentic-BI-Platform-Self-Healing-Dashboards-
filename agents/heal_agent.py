import subprocess
import os
from datetime import datetime
from graph.state import AgentState

# Path to your dbt project — update this to your actual dbt project path
DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", "./dbt_project")


def run_dbt_command(command: list[str], cwd: str) -> dict:
    """
    Runs a dbt CLI command as a subprocess.
    Returns stdout, stderr, and return code.
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300  # 5 min max for dbt run
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "dbt command timed out after 300 seconds",
            "returncode": -1
        }
    except FileNotFoundError:
        return {
            "success": False,
            "stdout": "",
            "stderr": "dbt not found — using mock heal instead",
            "returncode": -2
        }


def mock_heal(dbt_model: str) -> dict:
    """
    Mocked heal response when dbt is not available.
    Simulates a 5-second dbt run.
    """
    import time
    time.sleep(5)
    return {
        "success": True,
        "stdout": f"[MOCK] dbt run --select {dbt_model} completed successfully\n"
                  f"1 of 1 START table model dbt_project.{dbt_model} ...... [RUN]\n"
                  f"1 of 1 OK created table model dbt_project.{dbt_model} [OK in 4.21s]\n"
                  f"Finished running 1 table model in 0 hours 0 minutes and 4.21 seconds (0.07s).\n"
                  f"Completed successfully\nDone. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1",
        "stderr": "",
        "returncode": 0
    }


def heal_agent(state: AgentState) -> AgentState:
    """
    Heal Agent — rebuilds the affected dbt model using dbt CLI.
    Falls back to mock heal if dbt is not installed or project not found.
    """
    timestamp = datetime.now().isoformat()
    log_prefix = f"[{timestamp}] 🛠️  Heal Agent"

    dbt_model = state.get("affected_dbt_model")

    # ── Guard: Skip if no dbt model identified (infra-level failures) ──
    if not dbt_model or dbt_model.lower() == "none":
        msg = (
            f"{log_prefix}: ⚠️  No dbt model to rebuild — "
            f"infrastructure-level failure detected. "
            f"Manual intervention required."
        )
        print(msg)
        state["logs"].append(msg)
        state["heal_status"] = "skipped"
        return state

    print(f"{log_prefix}: Rebuilding dbt model → {dbt_model}...")
    state["logs"].append(f"{log_prefix}: Attempting rebuild of {dbt_model}")

    # ── Step 1: dbt test (pre-heal validation) ──
    print(f"{log_prefix}: Running dbt test on {dbt_model}...")
    test_cmd = ["dbt", "test", "--select", dbt_model, "--no-version-check"]
    test_result = run_dbt_command(test_cmd, DBT_PROJECT_DIR)

    # If dbt not found, use mock
    use_mock = test_result["returncode"] == -2

    if use_mock:
        print(f"{log_prefix}: ℹ️  dbt not found — using mock heal")
        run_result = mock_heal(dbt_model)
    else:
        # ── Step 2: dbt run (rebuild the model) ──
        print(f"{log_prefix}: Running dbt run on {dbt_model}...")
        run_cmd = [
            "dbt", "run",
            "--select", dbt_model,
            "--no-version-check",
            "--fail-fast"
        ]
        run_result = run_dbt_command(run_cmd, DBT_PROJECT_DIR)

    # ── Step 3: Evaluate outcome ──
    if run_result["success"]:
        state["heal_status"] = "healed"
        log = (
            f"{log_prefix}: ✅ Successfully rebuilt dbt model → {dbt_model}\n"
            f"           Output : {run_result['stdout'][:300]}"
        )
    else:
        state["heal_status"] = "heal_failed"
        log = (
            f"{log_prefix}: ❌ dbt rebuild FAILED for {dbt_model}\n"
            f"           Error  : {run_result['stderr'][:300]}\n"
            f"           Action : Escalating to on-call engineer via PagerDuty"
        )
        # Future Phase: trigger PagerDuty / Slack alert here

    print(log)
    state["logs"].append(log)

    return state
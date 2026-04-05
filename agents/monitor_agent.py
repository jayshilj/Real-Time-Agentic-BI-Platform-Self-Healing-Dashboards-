from graph.state import AgentState
from tools.powerbi_tools import get_dashboard_health
from datetime import datetime

def monitor_agent(state: AgentState) -> AgentState:
    """
    Monitor Agent — polls Power BI REST API for dashboard health.
    Updates AgentState with health status and failure context.
    """
    timestamp = datetime.now().isoformat()
    log_prefix = f"[{timestamp}] 🔍 Monitor Agent"

    print(f"{log_prefix}: Polling health for {state['dashboard_id']}...")
    state["logs"].append(f"{log_prefix}: Polling {state['dashboard_id']}")

    # Call Power BI REST API mock
    health = get_dashboard_health(state["dashboard_id"])

    status = health["status"]
    state["health_status"] = status
    state["dashboard_name"] = health.get("dashboard_name", state["dashboard_id"])

    if status == "healthy":
        log = f"{log_prefix}: ✅ {state['dashboard_name']} — HEALTHY"
        print(log)
        state["logs"].append(log)

    elif status == "degraded":
        state["failure_reason"] = health["failure_reason"]
        state["affected_dbt_model"] = health["affected_dbt_model"]
        log = (
            f"{log_prefix}: ⚠️  {state['dashboard_name']} — DEGRADED\n"
            f"           Reason : {health['failure_reason']}\n"
            f"           Model  : {health['affected_dbt_model']}"
        )
        print(log)
        state["logs"].append(log)

    elif status == "failed":
        state["failure_reason"] = health["failure_reason"]
        state["affected_dbt_model"] = health["affected_dbt_model"]
        log = (
            f"{log_prefix}: 🔴 {state['dashboard_name']} — FAILED\n"
            f"           Reason : {health['failure_reason']}\n"
            f"           Model  : {health['affected_dbt_model']}"
        )
        print(log)
        state["logs"].append(log)

    return state
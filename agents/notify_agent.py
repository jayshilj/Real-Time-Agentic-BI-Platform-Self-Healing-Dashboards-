from datetime import datetime
from graph.state import AgentState
from tools.email_tools import send_email_notification


def notify_agent(state: AgentState) -> AgentState:
    """
    Notify Agent — sends HTML email alert for failed/degraded dashboards.
    Skips notification for healthy dashboards.
    """
    timestamp  = datetime.now().isoformat()
    log_prefix = f"[{timestamp}] 📣 Notify Agent"

    health_status = state.get("health_status", "unknown")

    # ── Skip healthy dashboards ──
    if health_status == "healthy":
        msg = f"{log_prefix}: ✅ Dashboard healthy — no notification needed"
        print(msg)
        state["logs"].append(msg)
        state["notify_status"] = "skipped"
        return state

    print(f"{log_prefix}: Sending email alert for {state['dashboard_name']}...")

    result = send_email_notification(
        dashboard_name     = state["dashboard_name"],
        health_status      = state.get("health_status", "unknown"),
        heal_status        = state.get("heal_status", "unknown"),
        root_cause         = state.get("root_cause", "Unknown"),
        affected_dbt_model = state.get("affected_dbt_model", "N/A"),
        confidence_score   = state.get("confidence_score", 0.0),
        severity           = state.get("severity", "high"),
        fix_recommendation = state.get("fix_recommendation", "")
    )

    if result["success"]:
        state["notify_status"] = "sent"
        log = (
            f"{log_prefix}: ✅ Email notification sent → "
            f"{state['dashboard_name']} | {result['message']}"
        )
    else:
        state["notify_status"] = "failed"
        log = (
            f"{log_prefix}: ❌ Email notification FAILED | {result['message']}"
        )

    print(log)
    state["logs"].append(log)
    return state
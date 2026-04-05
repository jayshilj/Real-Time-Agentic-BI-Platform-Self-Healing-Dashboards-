from graph.state import AgentState
from datetime import datetime

def monitor_agent(state: AgentState) -> AgentState:
    log = f"[{datetime.now().isoformat()}] Monitor Agent: Checking {state['dashboard_id']}"
    print(log)
    state["logs"].append(log)
    # Phase 2 will replace this with real Power BI mock
    state["health_status"] = "failed"
    state["failure_reason"] = "Dataset refresh timeout after 30 mins"
    return state
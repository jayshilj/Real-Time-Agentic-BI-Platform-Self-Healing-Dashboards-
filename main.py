from config import GEMINI_API_KEY, GEMINI_MODEL
from graph.bi_agent_graph import build_graph
from graph.state import AgentState
from tools.powerbi_tools import DASHBOARD_REGISTRY
from datetime import datetime

def run_dashboard(dashboard_id: str, dashboard_name: str):
    graph = build_graph()

    initial_state: AgentState = {
        "dashboard_id": dashboard_id,
        "dashboard_name": dashboard_name,
        "health_status": "healthy",
        "failure_reason": None,
        "affected_dbt_model": None,
        "root_cause": None,
        "confidence_score": None,
        "heal_status": "idle",
        "heal_start_time": datetime.now().isoformat(),
        "heal_end_time": None,
        "recovery_time_seconds": None,
        "retry_count": 0,
        "logs": []
    }

    result = graph.invoke(initial_state)
    return result

def run():
    print(f"✅ Gemini API loaded: {GEMINI_API_KEY[:8]}****")
    print(f"✅ Model: {GEMINI_MODEL}")
    print("\n🚀 Starting Agentic BI Platform — Polling all dashboards...\n")
    print("=" * 60)

    for dashboard in DASHBOARD_REGISTRY:
        print(f"\n📊 Checking: {dashboard['dashboard_name']}")
        print("-" * 60)
        result = run_dashboard(
            dashboard["dashboard_id"],
            dashboard["dashboard_name"]
        )
        print(f"\n📋 Result:")
        print(f"   Health Status : {result['health_status']}")
        print(f"   Heal Status   : {result['heal_status']}")
        print(f"   Root Cause    : {result['root_cause']}")
        print("=" * 60)

if __name__ == "__main__":
    run()
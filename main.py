from config import GEMINI_API_KEY, GEMINI_MODEL
from graph.bi_agent_graph import build_graph
from graph.state import AgentState
from datetime import datetime

def run():
    # Confirm API key loaded
    print(f"✅ Gemini API loaded: {GEMINI_API_KEY[:8]}****")
    print(f"✅ Model: {GEMINI_MODEL}")

    graph = build_graph()

    initial_state: AgentState = {
        "dashboard_id": "dashboard_001",
        "dashboard_name": "Order Lifecycle Executive Dashboard",
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

    print("\n🚀 Starting Agentic BI Platform...")
    result = graph.invoke(initial_state)

    print("\n✅ Final State:")
    for log in result["logs"]:
        print(log)
    print(f"Heal Status  : {result['heal_status']}")
    print(f"Root Cause   : {result['root_cause']}")

if __name__ == "__main__":
    run()
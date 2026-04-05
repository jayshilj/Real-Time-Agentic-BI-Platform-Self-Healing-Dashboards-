from graph.state import AgentState
from datetime import datetime

def diagnose_agent(state: AgentState) -> AgentState:
    log = f"[{datetime.now().isoformat()}] Diagnose Agent: Analyzing failure..."
    print(log)
    state["logs"].append(log)
    # Phase 3 will wire Gemini 2.5 Flash here
    state["root_cause"] = "Null values in fct_orders dbt model"
    state["affected_dbt_model"] = "fct_orders"
    state["confidence_score"] = 0.94
    return state
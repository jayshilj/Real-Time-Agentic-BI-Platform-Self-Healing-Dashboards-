from graph.state import AgentState
from datetime import datetime

def heal_agent(state: AgentState) -> AgentState:
    log = f"[{datetime.now().isoformat()}] Heal Agent: Rebuilding {state['affected_dbt_model']}..."
    print(log)
    state["logs"].append(log)
    # Phase 4 will wire dbt Core Python API here
    state["heal_status"] = "healed"
    state["heal_end_time"] = datetime.now().isoformat()
    return state
from langgraph.graph import StateGraph, END
from graph.state import AgentState
from agents.monitor_agent import monitor_agent
from agents.diagnose_agent import diagnose_agent
from agents.heal_agent import heal_agent

def route_after_monitor(state: AgentState) -> str:
    if state["health_status"] == "healthy":
        return "end"
    elif state["health_status"] in ["degraded", "failed"]:
        return "diagnose"
    return "end"

def route_after_heal(state: AgentState) -> str:
    if state["heal_status"] == "healed":
        return "end"
    elif state["retry_count"] < 3:
        return "monitor"
    return "end"

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("monitor", monitor_agent)
    graph.add_node("diagnose", diagnose_agent)
    graph.add_node("heal", heal_agent)

    # Entry point
    graph.set_entry_point("monitor")

    # Edges
    graph.add_conditional_edges(
        "monitor",
        route_after_monitor,
        {"end": END, "diagnose": "diagnose"}
    )
    graph.add_edge("diagnose", "heal")
    graph.add_conditional_edges(
        "heal",
        route_after_heal,
        {"end": END, "monitor": "monitor"}
    )

    return graph.compile()
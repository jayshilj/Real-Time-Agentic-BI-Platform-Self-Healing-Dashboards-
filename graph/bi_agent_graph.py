from langgraph.graph import StateGraph, END
from graph.state import AgentState
from agents.monitor_agent import monitor_agent
from agents.diagnose_agent import diagnose_agent
from agents.heal_agent import heal_agent
from agents.notify_agent import notify_agent


def should_diagnose(state: AgentState) -> str:
    """
    Conditional edge — only run Diagnose + Heal + Notify
    if dashboard is NOT healthy.
    """
    if state.get("health_status") == "healthy":
        return "skip"
    return "diagnose"


def build_graph() -> StateGraph:
    """
    Builds and compiles the full LangGraph agent pipeline:

    monitor → [conditional] → diagnose → heal → notify → END
                    ↓ (healthy)
                   END
    """
    graph = StateGraph(AgentState)

    # ── Register all agent nodes ──
    graph.add_node("monitor",  monitor_agent)
    graph.add_node("diagnose", diagnose_agent)
    graph.add_node("heal",     heal_agent)
    graph.add_node("notify",   notify_agent)

    # ── Entry point ──
    graph.set_entry_point("monitor")

    # ── Conditional edge: skip pipeline if healthy ──
    graph.add_conditional_edges(
        "monitor",
        should_diagnose,
        {
            "diagnose": "diagnose",  # failed/degraded → run full pipeline
            "skip":     END          # healthy → stop here
        }
    )

    # ── Linear pipeline: diagnose → heal → notify → END ──
    graph.add_edge("diagnose", "heal")
    graph.add_edge("heal",     "notify")
    graph.add_edge("notify",   END)

    return graph.compile()
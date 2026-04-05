from graph.state import AgentState
from tools.gemini_tools import diagnose_failure
from datetime import datetime

def diagnose_agent(state: AgentState) -> AgentState:
    """
    Diagnose Agent — uses Gemini 2.5 Flash to identify root cause
    of dashboard failures and recommend dbt model fixes.
    """
    timestamp = datetime.now().isoformat()
    log_prefix = f"[{timestamp}] 🧠 Diagnose Agent"

    print(f"{log_prefix}: Calling Gemini 2.5 Flash for root cause analysis...")
    state["logs"].append(f"{log_prefix}: Analyzing failure with Gemini 2.5 Flash")

    # Call Gemini 2.5 Flash
    diagnosis = diagnose_failure(
        dashboard_name=state["dashboard_name"],
        failure_reason=state["failure_reason"],
        affected_dbt_model=state["affected_dbt_model"]
    )

    # Update state with Gemini diagnosis
    state["root_cause"] = diagnosis["root_cause"]
    state["affected_dbt_model"] = diagnosis["affected_dbt_model"] or state["affected_dbt_model"]
    state["confidence_score"] = diagnosis["confidence_score"]

    log = (
        f"{log_prefix}: ✅ Diagnosis complete\n"
        f"           Root Cause   : {diagnosis['root_cause']}\n"
        f"           dbt Model    : {diagnosis['affected_dbt_model']}\n"
        f"           Severity     : {diagnosis['severity']}\n"
        f"           Confidence   : {diagnosis['confidence_score']:.0%}\n"
        f"           Fix          : {diagnosis['fix_recommendation']}"
    )
    print(log)
    state["logs"].append(log)

    return state
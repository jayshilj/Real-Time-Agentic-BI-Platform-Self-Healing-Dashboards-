from graph.state import AgentState
from tools.gemini_tools import diagnose_failure
from tools.lineage_governance import get_lineage_path, get_governance_metadata
from datetime import datetime

def diagnose_agent(state: AgentState) -> AgentState:
    """
    Diagnose Agent — uses Gemini 2.5 Flash to identify root cause
    of dashboard failures and recommend dbt model fixes, utilizing
    data lineage and governance metadata.
    """
    timestamp = datetime.now().isoformat()
    log_prefix = f"[{timestamp}] 🧠 Diagnose Agent"

    # Fetch lineage path and governance metadata
    lineage = get_lineage_path(state["dashboard_id"])
    gov_meta = get_governance_metadata(state["dashboard_id"])

    state["lineage_path"] = lineage
    state["governance_metadata"] = gov_meta

    print(f"{log_prefix}: Resolved data lineage tree ({len(lineage)} nodes).")
    state["logs"].append(f"{log_prefix}: Traced upstream lineage to raw source systems")

    print(f"{log_prefix}: Calling Gemini 2.5 Flash for root cause analysis with lineage context...")
    state["logs"].append(f"{log_prefix}: Analyzing failure with Gemini 2.5 Flash + Lineage Context")

    # Call Gemini 2.5 Flash
    diagnosis = diagnose_failure(
        dashboard_name=state["dashboard_name"],
        failure_reason=state["failure_reason"],
        affected_dbt_model=state["affected_dbt_model"],
        lineage_path=lineage,
        governance_metadata=gov_meta
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
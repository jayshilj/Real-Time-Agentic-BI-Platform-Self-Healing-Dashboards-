from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage   # ← fixed
from config import GEMINI_API_KEY, GEMINI_MODEL
import json
import re

# Initialize Gemini 2.5 Flash model
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,  # Low temp for consistent diagnostic reasoning
)

SYSTEM_PROMPT = """
You are an expert BI Platform Engineer and dbt Core specialist.
Your job is to diagnose failures in Power BI and Looker dashboards
by analyzing error logs, identifying root causes in the data pipeline,
and leveraging upstream data lineage and asset governance metadata.

When given a dashboard failure, you must return a JSON response with:
- root_cause: A clear, specific explanation of what caused the failure, tracing it back to the proper layer in the data lineage (e.g. Bronze source, Silver staging, Gold mart).
- affected_dbt_model: The exact dbt model name that needs to be rebuilt
- fix_recommendation: Step-by-step fix instructions
- confidence_score: Your confidence level between 0.0 and 1.0
- severity: one of [critical, high, medium, low]

Always respond with valid JSON only. No markdown, no extra text.
"""

def diagnose_failure(
    dashboard_name: str,
    failure_reason: str,
    affected_dbt_model: str,
    lineage_path: list = None,
    governance_metadata: dict = None
) -> dict:
    """
    Calls Gemini 2.5 Flash to diagnose dashboard failure root cause.
    Uses data lineage and governance metadata to enrich failure context.
    Returns structured diagnostic output.
    """
    # Format lineage and governance context if available
    lineage_str = ""
    if lineage_path:
        lineage_str = "\nUpstream Data Lineage Path:\n"
        for i, node in enumerate(lineage_path):
            lineage_str += f"  - [{node['type'].upper()}] {node['name']} (ID: {node['id']}) | Owner: {node['owner']} | Tier: {node['tier']} | Sensitivity: {node['sensitivity']}\n"
            lineage_str += f"    Description: {node['description']}\n"

    gov_str = ""
    if governance_metadata:
        gov_str = (
            f"\nDashboard Governance Metadata:\n"
            f"  Owner: {governance_metadata.get('owner')}\n"
            f"  Tier: {governance_metadata.get('tier')}\n"
            f"  Sensitivity: {governance_metadata.get('sensitivity')}\n"
            f"  Description: {governance_metadata.get('description')}\n"
        )

    user_prompt = f"""
Dashboard Name: {dashboard_name}
Failure Reason: {failure_reason}
Suspected dbt Model: {affected_dbt_model}
{gov_str}
{lineage_str}
Analyze this BI dashboard failure and return your diagnosis as JSON. Trace the failure to the earliest upstream culprit if possible.
"""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_prompt)
    ]

    try:
        response = llm.invoke(messages)
        raw = response.content.strip()

        # Strip markdown code blocks if present
        raw = re.sub(r"```json|```", "", raw).strip()

        diagnosis = json.loads(raw)
        return {
            "root_cause": diagnosis.get("root_cause", "Unknown"),
            "affected_dbt_model": diagnosis.get(
                "affected_dbt_model", affected_dbt_model
            ),
            "fix_recommendation": diagnosis.get("fix_recommendation", ""),
            "confidence_score": float(
                diagnosis.get("confidence_score", 0.85)
            ),
            "severity": diagnosis.get("severity", "high"),
            "raw_response": raw
        }

    except json.JSONDecodeError as e:
        return {
            "root_cause": f"Gemini response parse error: {str(e)}",
            "affected_dbt_model": affected_dbt_model,
            "fix_recommendation": "Manual investigation required",
            "confidence_score": 0.0,
            "severity": "critical",
            "raw_response": raw if 'raw' in locals() else ""
        }
    except Exception as e:
        return {
            "root_cause": f"Gemini API error: {str(e)}",
            "affected_dbt_model": affected_dbt_model,
            "fix_recommendation": "Check API key and network connection",
            "confidence_score": 0.0,
            "severity": "critical",
            "raw_response": ""
        }
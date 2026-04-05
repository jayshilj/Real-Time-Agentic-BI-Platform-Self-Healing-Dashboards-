from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from graph.bi_agent_graph import build_graph
from graph.state import AgentState

router = APIRouter()

# ── In-memory store for latest results ────────────────────────────
dashboard_results: dict = {}

# ── Pydantic Models ───────────────────────────────────────────────
class DashboardRunRequest(BaseModel):
    dashboard_id:        str
    dashboard_name:      str
    force_failure:       bool = False
    failure_reason:      Optional[str] = None
    affected_dbt_model:  Optional[str] = None

class DashboardResult(BaseModel):
    dashboard_id:        str
    dashboard_name:      str
    health_status:       str
    heal_status:         str
    notify_status:       str
    root_cause:          Optional[str]
    affected_dbt_model:  Optional[str]
    confidence_score:    float
    severity:            Optional[str]
    timestamp:           str
    logs:                list[str]


# ── Background task: run full agent pipeline ───────────────────────
def run_pipeline(state: AgentState):
    graph = build_graph()
    result = graph.invoke(state)
    dashboard_results[state["dashboard_id"]] = {
        **result,
        "timestamp": datetime.now().isoformat()
    }


# ── GET /dashboards — list all known results ──────────────────────
@router.get("/dashboards")
def list_dashboards():
    return {
        "count":      len(dashboard_results),
        "dashboards": list(dashboard_results.values())
    }


# ── GET /dashboards/{id} — get single dashboard result ────────────
@router.get("/dashboards/{dashboard_id}")
def get_dashboard(dashboard_id: str):
    result = dashboard_results.get(dashboard_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"No results found for dashboard_id: {dashboard_id}"
        )
    return result


# ── POST /dashboards/run — trigger single dashboard pipeline ───────
@router.post("/dashboards/run")
def run_dashboard(req: DashboardRunRequest, background_tasks: BackgroundTasks):
    initial_state: AgentState = {
        "dashboard_id":        req.dashboard_id,
        "dashboard_name":      req.dashboard_name,
        "health_status":       "unknown",
        "failure_reason":      req.failure_reason or "",
        "affected_dbt_model":  req.affected_dbt_model or "",
        "root_cause":          "",
        "confidence_score":    0.0,
        "severity":            "",
        "fix_recommendation":  "",
        "heal_status":         "idle",
        "notify_status":       "idle",
        "logs":                []
    }

    # Override health status if force_failure is set
    if req.force_failure:
        initial_state["health_status"]      = "failed"
        initial_state["failure_reason"]     = req.failure_reason or "Forced failure via API"
        initial_state["affected_dbt_model"] = req.affected_dbt_model or "fct_unknown"

    background_tasks.add_task(run_pipeline, initial_state)

    return {
        "message":      f"Pipeline triggered for {req.dashboard_name}",
        "dashboard_id": req.dashboard_id,
        "status":       "running"
    }


# ── POST /dashboards/run-all — trigger all 3 dashboards ───────────
@router.post("/dashboards/run-all")
def run_all_dashboards(background_tasks: BackgroundTasks):
    dashboards = [
        {
            "dashboard_id":   "dashboard_001",
            "dashboard_name": "Order Lifecycle Executive Dashboard",
            "affected_dbt_model": "fct_orders"
        },
        {
            "dashboard_id":   "dashboard_002",
            "dashboard_name": "Revenue Analytics Dashboard",
            "affected_dbt_model": "fct_revenue"
        },
        {
            "dashboard_id":   "dashboard_003",
            "dashboard_name": "Supply Chain KPI Dashboard",
            "affected_dbt_model": "fct_supply_chain"
        }
    ]

    for d in dashboards:
        state: AgentState = {
            "dashboard_id":       d["dashboard_id"],
            "dashboard_name":     d["dashboard_name"],
            "health_status":      "unknown",
            "failure_reason":     "",
            "affected_dbt_model": d["affected_dbt_model"],
            "root_cause":         "",
            "confidence_score":   0.0,
            "severity":           "",
            "fix_recommendation": "",
            "heal_status":        "idle",
            "notify_status":      "idle",
            "logs":               []
        }
        background_tasks.add_task(run_pipeline, state)

    return {
        "message": "Pipeline triggered for all 3 dashboards",
        "count":   3,
        "status":  "running"
    }
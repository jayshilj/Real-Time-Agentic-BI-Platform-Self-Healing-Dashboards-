import random
from datetime import datetime
from typing import TypedDict

# Simulated Power BI dashboard registry
DASHBOARD_REGISTRY = [
    {
        "dashboard_id": "dashboard_001",
        "dashboard_name": "Order Lifecycle Executive Dashboard",
        "dataset_id": "dataset_001",
        "dbt_model": "fct_orders",
        "owner": "BI Platform Team",
    },
    {
        "dashboard_id": "dashboard_002",
        "dashboard_name": "Revenue Analytics Dashboard",
        "dataset_id": "dataset_002",
        "dbt_model": "fct_revenue",
        "owner": "Finance Team",
    },
    {
        "dashboard_id": "dashboard_003",
        "dashboard_name": "Supply Chain KPI Dashboard",
        "dataset_id": "dataset_003",
        "dbt_model": "fct_supply_chain",
        "owner": "Operations Team",
    },
]

# Weighted failure simulation
# 60% healthy, 20% degraded, 20% failed
HEALTH_WEIGHTS = {
    "healthy": 0.60,
    "degraded": 0.20,
    "failed": 0.20,
}

FAILURE_REASONS = [
    "Dataset refresh timeout after 30 mins",
    "Null values detected in fact table join key",
    "Snowflake warehouse suspended — query timeout",
    "dbt model fct_orders failed — upstream source missing",
    "Power BI gateway connection lost",
    "Row-level security filter returned 0 rows",
    "Memory limit exceeded during DAX calculation",
]

def get_dashboard_health(dashboard_id: str) -> dict:
    """
    Simulates Power BI REST API call:
    GET https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/refreshes
    Returns health status with failure context if degraded/failed.
    """
    dashboard = next(
        (d for d in DASHBOARD_REGISTRY if d["dashboard_id"] == dashboard_id),
        None
    )

    if not dashboard:
        return {
            "dashboard_id": dashboard_id,
            "status": "failed",
            "failure_reason": f"Dashboard {dashboard_id} not found in registry",
            "affected_dbt_model": None,
            "checked_at": datetime.now().isoformat(),
        }

    # Simulate API health response
    status = random.choices(
        list(HEALTH_WEIGHTS.keys()),
        weights=list(HEALTH_WEIGHTS.values())
    )[0]

    failure_reason = None
    if status in ["degraded", "failed"]:
        failure_reason = random.choice(FAILURE_REASONS)

    return {
        "dashboard_id": dashboard["dashboard_id"],
        "dashboard_name": dashboard["dashboard_name"],
        "dataset_id": dashboard["dataset_id"],
        "affected_dbt_model": dashboard["dbt_model"] if status != "healthy" else None,
        "status": status,
        "failure_reason": failure_reason,
        "owner": dashboard["owner"],
        "checked_at": datetime.now().isoformat(),
    }

def trigger_dataset_refresh(dataset_id: str) -> dict:
    """
    Simulates Power BI REST API call:
    POST https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/refreshes
    Returns refresh trigger confirmation.
    """
    return {
        "dataset_id": dataset_id,
        "refresh_status": "triggered",
        "triggered_at": datetime.now().isoformat(),
        "message": f"Dataset {dataset_id} refresh triggered successfully"
    }

def get_all_dashboard_statuses() -> list[dict]:
    """Poll health for all dashboards in registry."""
    return [
        get_dashboard_health(d["dashboard_id"])
        for d in DASHBOARD_REGISTRY
    ]
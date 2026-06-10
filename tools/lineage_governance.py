# tools/lineage_governance.py
from typing import Dict, Any, List, Optional

# Static governance and lineage catalog definition
CATALOG: Dict[str, Dict[str, Any]] = {
    # --- DASHBOARD 001 LINEAGE ---
    "dashboard_001": {
        "id": "dashboard_001",
        "name": "Order Lifecycle Executive Dashboard",
        "type": "dashboard",
        "owner": "BI Platform Team",
        "tier": "Tier 1 - Gold",
        "sensitivity": "Internal",
        "description": "Executive dashboard showing daily order volume, lifecycle stages, and fulfillment rates.",
        "upstream": ["dataset_001"]
    },
    "dataset_001": {
        "id": "dataset_001",
        "name": "Order Lifecycle Dataset",
        "type": "dataset",
        "owner": "Data Engineering Team",
        "tier": "Tier 1 - Gold",
        "sensitivity": "Internal",
        "description": "Tabular model serving order lifecycle metrics.",
        "upstream": ["fct_orders"]
    },
    "fct_orders": {
        "id": "fct_orders",
        "name": "fct_orders",
        "type": "dbt_model",
        "owner": "Analytics Engineering Team",
        "tier": "Tier 1 - Gold",
        "sensitivity": "Internal",
        "description": "Fact table containing order-level records and statuses.",
        "upstream": ["stg_orders", "stg_customers"]
    },
    "stg_orders": {
        "id": "stg_orders",
        "name": "stg_orders",
        "type": "dbt_model",
        "owner": "Analytics Engineering Team",
        "tier": "Tier 2 - Silver",
        "sensitivity": "Internal",
        "description": "Staging table for raw orders data.",
        "upstream": ["raw_orders"]
    },
    "stg_customers": {
        "id": "stg_customers",
        "name": "stg_customers",
        "type": "dbt_model",
        "owner": "Analytics Engineering Team",
        "tier": "Tier 2 - Silver",
        "sensitivity": "PII / Restricted",
        "description": "Staging table for customer profile data.",
        "upstream": ["raw_customers"]
    },
    "raw_orders": {
        "id": "raw_orders",
        "name": "raw_orders",
        "type": "raw_source",
        "owner": "Source Systems Team",
        "tier": "Tier 3 - Bronze",
        "sensitivity": "Restricted",
        "description": "Raw database table ingested from the transactional orders service database.",
        "upstream": []
    },
    "raw_customers": {
        "id": "raw_customers",
        "name": "raw_customers",
        "type": "raw_source",
        "owner": "Source Systems Team",
        "tier": "Tier 3 - Bronze",
        "sensitivity": "Restricted",
        "description": "Raw database table ingested from the CRM database.",
        "upstream": []
    },

    # --- DASHBOARD 002 LINEAGE ---
    "dashboard_002": {
        "id": "dashboard_002",
        "name": "Revenue Analytics Dashboard",
        "type": "dashboard",
        "owner": "Finance Team",
        "tier": "Tier 1 - Gold",
        "sensitivity": "Restricted",
        "description": "Financial analytics dashboard tracking margins, order revenues, and transactional health.",
        "upstream": ["dataset_002"]
    },
    "dataset_002": {
        "id": "dataset_002",
        "name": "Revenue Analytics Dataset",
        "type": "dataset",
        "owner": "Data Engineering Team",
        "tier": "Tier 1 - Gold",
        "sensitivity": "Restricted",
        "description": "Tabular model serving financial transactions.",
        "upstream": ["fct_revenue"]
    },
    "fct_revenue": {
        "id": "fct_revenue",
        "name": "fct_revenue",
        "type": "dbt_model",
        "owner": "Analytics Engineering Team",
        "tier": "Tier 1 - Gold",
        "sensitivity": "Restricted",
        "description": "Fact table for transaction ledger and billing information.",
        "upstream": ["stg_payments", "stg_orders"]
    },
    "stg_payments": {
        "id": "stg_payments",
        "name": "stg_payments",
        "type": "dbt_model",
        "owner": "Analytics Engineering Team",
        "tier": "Tier 2 - Silver",
        "sensitivity": "Restricted",
        "description": "Staging payments logs from Stripe webhook receiver.",
        "upstream": ["raw_payments"]
    },
    "raw_payments": {
        "id": "raw_payments",
        "name": "raw_payments",
        "type": "raw_source",
        "owner": "Stripe Integrations",
        "tier": "Tier 3 - Bronze",
        "sensitivity": "Restricted",
        "description": "Raw Stripe payments log table.",
        "upstream": []
    },

    # --- DASHBOARD 003 LINEAGE ---
    "dashboard_003": {
        "id": "dashboard_003",
        "name": "Supply Chain KPI Dashboard",
        "type": "dashboard",
        "owner": "Operations Team",
        "tier": "Tier 1 - Gold",
        "sensitivity": "Internal",
        "description": "Supply chain and fulfillment metrics dashboard tracing shipments and distribution timelines.",
        "upstream": ["dataset_003"]
    },
    "dataset_003": {
        "id": "dataset_003",
        "name": "Supply Chain Dataset",
        "type": "dataset",
        "owner": "Data Engineering Team",
        "tier": "Tier 1 - Gold",
        "sensitivity": "Internal",
        "description": "Tabular model serving warehouse stock and shipments.",
        "upstream": ["fct_supply_chain"]
    },
    "fct_supply_chain": {
        "id": "fct_supply_chain",
        "name": "fct_supply_chain",
        "type": "dbt_model",
        "owner": "Analytics Engineering Team",
        "tier": "Tier 1 - Gold",
        "sensitivity": "Internal",
        "description": "Fact table tracking shipping dispatches and transit metrics.",
        "upstream": ["stg_shipments", "stg_inventory"]
    },
    "stg_shipments": {
        "id": "stg_shipments",
        "name": "stg_shipments",
        "type": "dbt_model",
        "owner": "Analytics Engineering Team",
        "tier": "Tier 2 - Silver",
        "sensitivity": "Internal",
        "description": "Staging logs for carrier dispatches.",
        "upstream": ["raw_shipments"]
    },
    "stg_inventory": {
        "id": "stg_inventory",
        "name": "stg_inventory",
        "type": "dbt_model",
        "owner": "Analytics Engineering Team",
        "tier": "Tier 2 - Silver",
        "sensitivity": "Internal",
        "description": "Staging stock records from warehouse management system.",
        "upstream": ["raw_inventory"]
    },
    "raw_shipments": {
        "id": "raw_shipments",
        "name": "raw_shipments",
        "type": "raw_source",
        "owner": "Logistics API Integrations",
        "tier": "Tier 3 - Bronze",
        "sensitivity": "Internal",
        "description": "Raw payload dumps from Carrier APIs.",
        "upstream": []
    },
    "raw_inventory": {
        "id": "raw_inventory",
        "name": "raw_inventory",
        "type": "raw_source",
        "owner": "Warehouse WMS Server",
        "tier": "Tier 3 - Bronze",
        "sensitivity": "Internal",
        "description": "Raw DB tables from local warehouse WMS databases.",
        "upstream": []
    }
}


def get_governance_metadata(asset_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves governance metadata for a specific catalog asset."""
    asset = CATALOG.get(asset_id)
    if not asset:
        return None
    return {
        "id": asset["id"],
        "name": asset["name"],
        "type": asset["type"],
        "owner": asset["owner"],
        "tier": asset["tier"],
        "sensitivity": asset["sensitivity"],
        "description": asset["description"]
    }


def get_lineage_path(dashboard_id: str) -> List[Dict[str, Any]]:
    """
    Traces upstream lineage starting from a given dashboard.
    Returns a ordered list of dictionaries containing asset metadata from top (dashboard) to bottom (raw sources).
    """
    path: List[Dict[str, Any]] = []
    visited = set()

    def traverse(node_id: str):
        if node_id in visited:
            return
        visited.add(node_id)
        
        asset = CATALOG.get(node_id)
        if not asset:
            return

        # Record this node's metadata
        metadata = get_governance_metadata(node_id)
        if metadata:
            path.append(metadata)

        # Traverse upstream dependencies
        for upstream_id in asset.get("upstream", []):
            traverse(upstream_id)

    traverse(dashboard_id)
    return path

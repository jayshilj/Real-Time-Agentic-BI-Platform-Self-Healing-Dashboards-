# tools/expectations_tool.py
import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Tuple
import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeUnique,
    ExpectColumnValuesToBeInSet,
    ExpectColumnValuesToBeBetween
)

# Folder to store historical validation runs for governance auditing
GX_RUNS_DIR = "./logs/great_expectations_runs"
os.makedirs(GX_RUNS_DIR, exist_ok=True)


def generate_mock_dataframe(model_name: str, has_failure: bool) -> pd.DataFrame:
    """
    Generates a Pandas DataFrame matching the schema of the target dbt model.
    If has_failure is True, it injects invalid data to trigger a GX validation failure.
    """
    if model_name == "fct_orders":
        # Scheme: order_id, customer_id, order_date, status, total_amount
        data = {
            "order_id": [1001, 1002, 1003, 1004, 1005],
            "customer_id": [201, 202, 203, 204, 205],
            "status": ["ordered", "shipped", "delivered", "ordered", "shipped"],
            "total_amount": [150.00, 45.50, 99.99, 1200.00, 310.20]
        }
        if has_failure:
            # Inject null in primary key (represents null values in fact table join key)
            data["order_id"][2] = None
            data["status"][3] = "pending_invalid"
            data["total_amount"][4] = -50.0  # Invalid negative amount

    elif model_name == "fct_revenue":
        # Scheme: transaction_id, order_id, payment_method, amount
        data = {
            "transaction_id": ["tx_101", "tx_102", "tx_103", "tx_104", "tx_105"],
            "order_id": [1001, 1002, 1003, 1004, 1005],
            "payment_method": ["credit_card", "paypal", "stripe", "stripe", "credit_card"],
            "amount": [150.00, 45.50, 99.99, 1200.00, 310.20]
        }
        if has_failure:
            # Inject duplicate transaction ID or null
            data["transaction_id"][1] = "tx_101"  # Duplicate key
            data["transaction_id"][3] = None      # Null transaction
            data["amount"][4] = -10.0

    elif model_name == "fct_supply_chain":
        # Scheme: shipment_id, carrier, days_in_transit, shipment_status
        data = {
            "shipment_id": ["shp_001", "shp_002", "shp_003", "shp_004", "shp_005"],
            "carrier": ["FedEx", "UPS", "DHL", "FedEx", "UPS"],
            "days_in_transit": [3, 5, 2, 7, 4],
            "shipment_status": ["delivered", "shipped", "delivered", "pending", "shipped"]
        }
        if has_failure:
            # Inject invalid carrier and negative days_in_transit
            data["carrier"][2] = "Carrier_Unknown"
            data["days_in_transit"][3] = -2
            data["shipment_id"][4] = None

    else:
        # Default fallback
        data = {
            "id": [1, 2, 3],
            "status": ["active", "active", "inactive"]
        }
        if has_failure:
            data["id"][2] = None

    return pd.DataFrame(data)


def run_gx_validation(model_name: str, has_failure: bool = False) -> Dict[str, Any]:
    """
    Initializes Great Expectations v1.x, defines the Expectation Suite for the model,
    runs the validation definition using a checkpoint, and registers the validation
    run as a JSON audit trail inside logs/great_expectations_runs.
    """
    timestamp = datetime.now().isoformat()
    run_id = f"run_{model_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    print(f"[Expectations Tool]: Running Great Expectations for {model_name} (fail_state={has_failure})...")
    
    # 1. Initialize ephemeral context
    context = gx.get_context()
    
    # 2. Add pandas datasource & asset
    ds_name = f"ds_{model_name}_{datetime.now().microsecond}"
    asset_name = f"asset_{model_name}"
    ds = context.data_sources.add_pandas(name=ds_name)
    asset = ds.add_dataframe_asset(name=asset_name)
    batch_def = asset.add_batch_definition_whole_dataframe(name=f"batch_def_{model_name}")

    # 3. Create expectation suite
    suite_name = f"suite_{model_name}_{datetime.now().microsecond}"
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))

    # 4. Configure expectation rules based on the dbt model
    if model_name == "fct_orders":
        suite.add_expectation(ExpectColumnValuesToNotBeNull(column="order_id"))
        suite.add_expectation(ExpectColumnValuesToBeUnique(column="order_id"))
        suite.add_expectation(ExpectColumnValuesToBeInSet(
            column="status", 
            value_set=["ordered", "shipped", "delivered", "returned"]
        ))
        suite.add_expectation(ExpectColumnValuesToBeBetween(column="total_amount", min_value=0.0))

    elif model_name == "fct_revenue":
        suite.add_expectation(ExpectColumnValuesToNotBeNull(column="transaction_id"))
        suite.add_expectation(ExpectColumnValuesToBeUnique(column="transaction_id"))
        suite.add_expectation(ExpectColumnValuesToBeBetween(column="amount", min_value=0.0))

    elif model_name == "fct_supply_chain":
        suite.add_expectation(ExpectColumnValuesToNotBeNull(column="shipment_id"))
        suite.add_expectation(ExpectColumnValuesToBeInSet(
            column="carrier", 
            value_set=["FedEx", "UPS", "DHL", "USPS"]
        ))
        suite.add_expectation(ExpectColumnValuesToBeBetween(column="days_in_transit", min_value=0))

    else:
        suite.add_expectation(ExpectColumnValuesToNotBeNull(column="id"))

    # 5. Define validation definition
    val_def_name = f"val_def_{model_name}_{datetime.now().microsecond}"
    val_def = context.validation_definitions.add(
        gx.ValidationDefinition(
            name=val_def_name,
            data=batch_def,
            suite=suite
        )
    )

    # 6. Define checkpoint
    cp_name = f"checkpoint_{model_name}_{datetime.now().microsecond}"
    checkpoint = context.checkpoints.add(
        gx.Checkpoint(
            name=cp_name,
            validation_definitions=[val_def]
        )
    )

    # 7. Generate dataframe (clean or failure injected)
    df = generate_mock_dataframe(model_name, has_failure)

    # 8. Run checkpoint
    res = checkpoint.run(batch_parameters={"dataframe": df})
    
    # 9. Parse validation results
    validation_results_list = []
    for val_res_def, run_results in res.run_results.items():
        results = run_results.get("results", [])
        for r in results:
            exp_config = getattr(r, "expectation_config", None)
            exp_type = "unknown"
            column = None
            if exp_config:
                exp_type = getattr(exp_config, "type", None) or getattr(exp_config, "expectation_type", "unknown")
                if hasattr(exp_config, "kwargs") and isinstance(exp_config.kwargs, dict):
                    column = exp_config.kwargs.get("column")
            
            # Extract observed/unexpected values
            observed = None
            if r.result:
                observed = r.result.get("observed_value")
                if observed is None:
                    unexpected_cnt = r.result.get("unexpected_count")
                    if unexpected_cnt is not None:
                        observed = f"{unexpected_cnt} unexpected rows"
            if observed is None:
                observed = "N/A"

            validation_results_list.append({
                "expectation_type": exp_type,
                "success": bool(r.success),
                "observed_value": observed,
                "column": column,
                "details": r.result if hasattr(r, "result") else {}
            })

    # Compile final execution record
    execution_record = {
        "run_id": run_id,
        "model_name": model_name,
        "timestamp": timestamp,
        "success": bool(res.success),
        "total_checks": len(validation_results_list),
        "passed_checks": sum(1 for c in validation_results_list if c["success"]),
        "failed_checks": sum(1 for c in validation_results_list if not c["success"]),
        "results": validation_results_list
    }

    # Save to local store for audit lineage
    report_file = os.path.join(GX_RUNS_DIR, f"{run_id}.json")
    with open(report_file, "w") as f:
        json.dump(execution_record, f, indent=2)

    execution_record["report_path"] = report_file
    print(f"[Expectations Tool]: Saved execution audit trail to {report_file} (Success={res.success})")

    return execution_record

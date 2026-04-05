from typing import TypedDict, Literal, Optional
from datetime import datetime

class AgentState(TypedDict):
    dashboard_id: str
    dashboard_name: str
    health_status: Literal["healthy", "degraded", "failed"]
    failure_reason: Optional[str]
    affected_dbt_model: Optional[str]
    root_cause: Optional[str]
    confidence_score: Optional[float]
    heal_status: Literal["idle", "healing", "healed", "failed"]
    heal_start_time: Optional[str]
    heal_end_time: Optional[str]
    recovery_time_seconds: Optional[float]
    retry_count: int
    logs: list[str]
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status":    "healthy",
        "timestamp": datetime.now().isoformat(),
        "service":   "Real-Time Agentic BI Platform"
    }
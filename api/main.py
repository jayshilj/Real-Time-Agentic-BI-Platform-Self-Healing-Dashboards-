from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import dashboards, health

app = FastAPI(
    title="Real-Time Agentic BI Platform",
    description="Self-Healing Dashboard API powered by LangGraph + Gemini 2.5 Flash",
    version="1.0.0"
)

# ── CORS ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────
app.include_router(health.router,      prefix="/api/v1", tags=["Health"])
app.include_router(dashboards.router,  prefix="/api/v1", tags=["Dashboards"])

@app.get("/")
def root():
    return {
        "name":    "Real-Time Agentic BI Platform",
        "version": "1.0.0",
        "status":  "running",
        "docs":    "/docs"
    }

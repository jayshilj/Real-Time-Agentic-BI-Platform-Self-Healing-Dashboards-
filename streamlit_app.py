import streamlit as st
import requests
import time
from datetime import datetime

# ── Page Config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic BI Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "http://localhost:8000/api/v1"

# ── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #313244;
        margin-bottom: 12px;
    }
    .status-healthy  { color: #a6e3a1; font-weight: bold; }
    .status-failed   { color: #f38ba8; font-weight: bold; }
    .status-degraded { color: #fab387; font-weight: bold; }
    .status-unknown  { color: #cdd6f4; font-weight: bold; }
    .heal-healed     { color: #a6e3a1; }
    .heal-failed     { color: #f38ba8; }
    .heal-skipped    { color: #fab387; }
    .heal-idle       { color: #6c7086; }
    .log-box {
        background: #11111b;
        border-radius: 8px;
        padding: 12px;
        font-family: monospace;
        font-size: 12px;
        color: #cdd6f4;
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #313244;
    }
    .header-badge {
        background: #313244;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        color: #cba6f7;
    }
</style>
""", unsafe_allow_html=True)


# ── Helper Functions ──────────────────────────────────────────────
def get_api_health():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        return r.status_code == 200
    except:
        return False

def get_all_dashboards():
    try:
        r = requests.get(f"{API_BASE}/dashboards", timeout=5)
        return r.json().get("dashboards", [])
    except:
        return []

def trigger_run_all():
    try:
        r = requests.post(f"{API_BASE}/dashboards/run-all", timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def trigger_run_one(dashboard_id, dashboard_name, force_failure=False,
                    failure_reason="", affected_dbt_model=""):
    try:
        payload = {
            "dashboard_id":       dashboard_id,
            "dashboard_name":     dashboard_name,
            "force_failure":      force_failure,
            "failure_reason":     failure_reason,
            "affected_dbt_model": affected_dbt_model
        }
        r = requests.post(f"{API_BASE}/dashboards/run",
                          json=payload, timeout=5)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def status_color(status: str) -> str:
    colors = {
        "healthy":  "🟢",
        "failed":   "🔴",
        "degraded": "🟡",
        "unknown":  "⚪",
        "healed":   "✅",
        "skipped":  "⚠️",
        "idle":     "💤",
        "sent":     "📧",
    }
    return colors.get(status, "❓")


# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Agentic BI Platform")
    st.markdown("**Self-Healing Dashboards**")
    st.divider()

    api_ok = get_api_health()
    if api_ok:
        st.success("🟢 API Online — localhost:8000")
    else:
        st.error("🔴 API Offline — start uvicorn")

    st.divider()
    st.markdown("### ⚙️ Controls")

    auto_refresh = st.toggle("Auto-Refresh (10s)", value=False)
    if st.button("🚀 Run All Dashboards", use_container_width=True, type="primary"):
        with st.spinner("Triggering pipeline..."):
            result = trigger_run_all()
            st.success(f"✅ {result.get('message', 'Triggered!')}")

    st.divider()
    st.markdown("### 🔧 Force Failure Test")

    test_dashboard = st.selectbox("Dashboard", [
        "dashboard_001 — Order Lifecycle",
        "dashboard_002 — Revenue Analytics",
        "dashboard_003 — Supply Chain KPI"
    ])
    test_reason = st.text_input(
        "Failure Reason",
        "Null values in join key"
    )
    test_model = st.text_input("dbt Model", "fct_orders")

    if st.button("💥 Force Failure", use_container_width=True):
        did = test_dashboard.split(" — ")[0]
        dname = test_dashboard.split(" — ")[1]
        with st.spinner("Triggering forced failure..."):
            result = trigger_run_one(
                dashboard_id=did,
                dashboard_name=dname,
                force_failure=True,
                failure_reason=test_reason,
                affected_dbt_model=test_model
            )
            st.success(f"✅ Pipeline triggered!")

    st.divider()
    st.caption(f"🕐 Last refresh: {datetime.now().strftime('%H:%M:%S')}")


# ── Main Header ───────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🤖 Real-Time Agentic BI Platform")
    st.markdown("**Self-Healing Dashboards** powered by LangGraph + Gemini 2.5 Flash")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<span class="header-badge">Phase 7 — Live UI</span>',
        unsafe_allow_html=True
    )

st.divider()

# ── KPI Summary Row ───────────────────────────────────────────────
dashboards = get_all_dashboards()
total      = len(dashboards)
healthy    = sum(1 for d in dashboards if d.get("health_status") == "healthy")
failed     = sum(1 for d in dashboards if d.get("health_status") == "failed")
degraded   = sum(1 for d in dashboards if d.get("health_status") == "degraded")
healed     = sum(1 for d in dashboards if d.get("heal_status")   == "healed")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📊 Total Dashboards",  total)
k2.metric("🟢 Healthy",           healthy)
k3.metric("🔴 Failed",            failed)
k4.metric("🟡 Degraded",          degraded)
k5.metric("✅ Auto-Healed",       healed)

st.divider()

# ── Dashboard Cards ───────────────────────────────────────────────
st.markdown("## 📋 Dashboard Status")

if not dashboards:
    st.info("💤 No results yet — click **Run All Dashboards** in the sidebar to start.")
else:
    for d in dashboards:
        health  = d.get("health_status", "unknown")
        heal    = d.get("heal_status", "idle")
        notify  = d.get("notify_status", "idle")
        conf    = d.get("confidence_score", 0.0)
        cause   = d.get("root_cause", "N/A")
        model   = d.get("affected_dbt_model", "N/A")
        sev     = d.get("severity", "N/A")
        logs    = d.get("logs", [])
        ts      = d.get("timestamp", "")

        with st.expander(
            f"{status_color(health)} {d.get('dashboard_name')} "
            f"| Health: {health.upper()} "
            f"| Heal: {heal.upper()}",
            expanded=(health != "healthy")
        ):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Health",     f"{status_color(health)} {health.upper()}")
            c2.metric("Heal",       f"{status_color(heal)} {heal.upper()}")
            c3.metric("Notify",     f"{status_color(notify)} {notify.upper()}")
            c4.metric("Confidence", f"{conf:.0%}")

            if cause and cause != "N/A":
                st.markdown("**🧠 Root Cause (Gemini 2.5 Flash):**")
                st.warning(cause)

            col_a, col_b, col_c = st.columns(3)
            col_a.markdown(f"**dbt Model:** `{model}`")
            col_b.markdown(f"**Severity:** `{sev.upper() if sev else 'N/A'}`")
            col_c.markdown(f"**Timestamp:** `{ts[:19] if ts else 'N/A'}`")

            if logs:
                st.markdown("**📜 Agent Logs:**")
                log_text = "\n".join(logs)
                st.markdown(
                    f'<div class="log-box">{log_text}</div>',
                    unsafe_allow_html=True
                )

# ── Auto Refresh ──────────────────────────────────────────────────
if auto_refresh:
    time.sleep(10)
    st.rerun()
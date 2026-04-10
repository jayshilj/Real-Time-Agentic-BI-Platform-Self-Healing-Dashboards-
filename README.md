# 🤖 Real-Time Agentic BI Platform — Self-Healing Dashboards

Autonomous LangGraph multi-agent system that monitors, diagnoses, and self-heals governed BI dashboards across Power BI using dbt-core APIs — powered by Gemini 2.5 Flash.

## 🏗️ Architecture

```text
┌───────────────────────────────────────────────────────────────┐
│                  AGENTIC BI PLATFORM                          │
│                                                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐    │
│  │   MONITOR   │───▶│   DIAGNOSE  │───▶│      HEAL       │    │
│  │    AGENT    │    │    AGENT    │    │     AGENT       │    │
│  │             │    │             │    │                 │    │
│  │ Polls Power │    │ Gemini 2.5  │    │ dbt model       │    │
│  │ BI REST API │    │ Flash root  │    │ rebuild +       │    │
│  │ every cycle │    │ cause       │    │ data validation │    │
│  └─────────────┘    └─────────────┘    └─────────────────┘    │
│         │                                       │             │
│         │ (If healthy, skip)                    ▼             │
│         │                               ┌─────────────────┐   │
│         └──────────────────────────────▶│     NOTIFY      │   │
│                                         │      AGENT      │   │
│         LangGraph StateGraph            └─────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

## ✨ Features

*   **Multi-Agent Orchestration** — LangGraph `StateGraph` wiring 4 specialized agents.
*   **Autonomous Monitoring** — Polls Power BI REST API for dashboard health and dataset refresh timeouts.
*   **AI-Powered Diagnosis** — Gemini 2.5 Flash identifies the exact root cause in the dbt pipeline layer with confidence scoring.
*   **Self-Healing** — Automatically triggers `dbt run` and `dbt test` via CLI to rebuild incremental models.
*   **Automated Alerting** — Dispatches rich HTML emails with diagnosis and remediation steps via Gmail SMTP.
*   **REST API Layer** — FastAPI backend to trigger force-failures and retrieve dashboard states.
*   **Live UI** — Streamlit dashboard showing real-time agent status, heal history, and force-failure testing.

## 🗂️ Project Structure

```text
agentic-bi-platform/
├── tools/
│   ├── monitor_agent.py       # Power BI REST API health polling
│   ├── diagnose_agent.py      # Gemini 2.5 Flash root cause analysis
│   ├── heal_agent.py          # dbt Core rebuild + refresh trigger
│   └── notify_agent.py        # SMTP Email alerts
├── graph/
│   ├── state.py               # AgentState TypedDict definition
│   └── graph_builder.py       # LangGraph StateGraph wiring
├── api/
│   └── main.py                # FastAPI REST API endpoints
├── dbt_project/
│   ├── models/                # Raw sources and dimensional models
│   ├── profiles.yml           # Database connection config
│   └── dbt_project.yml        # dbt project configurations
├── streamlit_app.py           # Streamlit live monitoring UI
├── main.py                    # CLI Entry point
├── requirements.txt           # Python dependencies
└── .env.example               # Environment variable template
```

## 🚀 Quick Start

### Prerequisites
*   Python 3.12+
*   PostgreSQL (Local or Docker)
*   Gemini API Key → [Get one here](https://aistudio.google.com/)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/jayshilj/Real-Time-Agentic-BI-Platform-Self-Healing-Dashboards-.git
cd Real-Time-Agentic-BI-Platform-Self-Healing-Dashboards-

# 2. Create virtual environment
python -m venv venv

# 3. Activate venv
# Mac/Linux:
source venv/bin/activate
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
cp .env.example .env
```

### Configure Environment
Add your API keys and database credentials to the `.env` file:

```env
# .env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=analytics

EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=target_email@gmail.com
```

### Run the Platform

**Start the FastAPI Backend (Terminal 1):**
```bash
uvicorn api.main:app --reload --port 8000
```

**Start the Streamlit UI (Terminal 2):**
```bash
streamlit run streamlit_app.py
```

### Expected CLI Output (Running `python main.py`)
```text
✅ Gemini API loaded: AIzaSyXX****
✅ Model: gemini-2.5-flash

🚀 Starting Agentic BI Platform...
[timestamp] Monitor Agent: Checking dashboard_001
[timestamp] Diagnose Agent: Analyzing failure...
[timestamp] Heal Agent: Rebuilding fct_orders...
[timestamp] Notify Agent: Email dispatched successfully.

✅ Final State:
Heal Status  : healed
Root Cause   : Null values in fct_orders join key
```

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Agent Orchestration** | LangGraph `StateGraph` |
| **LLM** | Gemini 2.5 Flash via LangChain |
| **BI Platform** | Power BI REST API |
| **Data Transformation** | dbt Core CLI |
| **Database** | PostgreSQL |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **Live UI** | Streamlit |

## 📍 Build Phases

| Phase | Description | Status |
| :--- | :--- | :--- |
| **Phase 1** | LangGraph StateGraph + Agent State Definition | ✅ Complete |
| **Phase 2** | Monitor Agent (Power BI polling logic) | ✅ Complete |
| **Phase 3** | Diagnose Agent (Gemini 2.5 Flash RCA Integration) | ✅ Complete |
| **Phase 4** | Heal Agent (dbt Core Integration) | ✅ Complete |
| **Phase 5** | Notify Agent (Gmail SMTP Integration) | ✅ Complete |
| **Phase 6** | FastAPI REST API Layer | ✅ Complete |
| **Phase 7** | Streamlit Real-Time Live UI | ✅ Complete |
| **Phase 8** | Real Power BI REST API Auth (Azure AD) | 🔄 Mocked / Ready |
| **Phase 9** | Real PostgreSQL + dbt Core implementation | ✅ Complete |
| **Phase 10**| Dockerization & Cloud Deployment | ⏳ Planned |

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
1. Fork the repo
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/jayshilj/Real-Time-Agentic-BI-Platform-Self-Healing-Dashboards-/blob/master/LICENSE) file for details.

## 👤 Author

**Jayshil Jain**
* LinkedIn: [jayshiljain](https://www.linkedin.com/in/jayshiljain/)
* GitHub: [jayshilj](https://github.com/jayshilj)

⭐ *Star this repo if you find it useful!*
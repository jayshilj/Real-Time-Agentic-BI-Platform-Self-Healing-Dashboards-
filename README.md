# 🤖 Real-Time Agentic BI Platform — Self-Healing Dashboards

[
[
[
[
[

> Autonomous LangGraph multi-agent system that monitors, diagnoses, and self-heals governed BI dashboards across Power BI and Looker using dbt-core APIs — powered by Gemini 2.5 Flash.

***

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AGENTIC BI PLATFORM                        │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │   MONITOR   │───▶│   DIAGNOSE  │───▶│      HEAL       │  │
│  │    AGENT    │    │    AGENT    │    │     AGENT       │  │
│  │             │    │             │    │                 │  │
│  │ Polls Power │    │ Gemini 2.5  │    │ dbt model       │  │
│  │ BI REST API │    │ Flash root  │    │ rebuild +       │  │
│  │ every 5min  │    │ cause       │    │ dashboard       │  │
│  └─────────────┘    └─────────────┘    │ refresh         │  │
│                                        └─────────────────┘  │
│                        LangGraph StateGraph                  │
└─────────────────────────────────────────────────────────────┘
```

***

## ✨ Features

- **Multi-Agent Orchestration** — LangGraph `StateGraph` wiring 3 specialized agents
- **Autonomous Monitoring** — Polls Power BI REST API for dashboard health every N minutes
- **AI-Powered Diagnosis** — Gemini 2.5 Flash identifies root cause in dbt pipeline layer
- **Self-Healing** — Automatically triggers dbt model rebuilds and dashboard refreshes
- **Live UI** — Streamlit dashboard showing real-time agent status and heal history *(Phase 5)*
- **Production CI/CD** — GitHub Actions running dbt tests on every push *(Phase 6)*

***

## 🗂️ Project Structure

```
agentic-bi-platform/
├── agents/
│   ├── monitor_agent.py       # Power BI REST API health polling
│   ├── diagnose_agent.py      # Gemini 2.5 Flash root cause analysis
│   └── heal_agent.py          # dbt Core rebuild + refresh trigger
├── graph/
│   ├── state.py               # AgentState TypedDict definition
│   └── bi_agent_graph.py      # LangGraph StateGraph wiring
├── tools/
│   ├── powerbi_tools.py       # Power BI API wrappers (Phase 2)
│   ├── dbt_tools.py           # dbt Core Python API wrappers (Phase 4)
│   └── snowflake_tools.py     # Snowflake connector utils (Phase 4)
├── ui/
│   └── dashboard.py           # Streamlit live monitoring UI (Phase 5)
├── dbt_project/
│   ├── models/staging/        # Raw source models
│   ├── models/marts/          # BI-ready dimensional models
│   └── tests/                 # dbt data quality tests
├── .github/workflows/
│   └── ci.yml                 # GitHub Actions CI pipeline (Phase 6)
├── tests/
│   ├── test_monitor.py
│   ├── test_diagnose.py
│   └── test_heal.py
├── config.py                  # ENV vars, API configs
├── main.py                    # Entry point
├── requirements.txt
├── Dockerfile
└── .env.example               # Environment variable template
```

***

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Gemini API Key → [Get one here](https://ai.google.dev)

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
# Windows:
venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
cp .env.example .env
# Add your Gemini API key to .env
```

### Configure Environment

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Run

```bash
python main.py
```

### Expected Output

```
✅ Gemini API loaded: AIzaSyXX****
✅ Model: gemini-2.5-flash

🚀 Starting Agentic BI Platform...
[timestamp] Monitor Agent: Checking dashboard_001
[timestamp] Diagnose Agent: Analyzing failure...
[timestamp] Heal Agent: Rebuilding fct_orders...

✅ Final State:
Heal Status  : healed
Root Cause   : Null values in fct_orders dbt model
```

***

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph `StateGraph` |
| LLM | Gemini 2.5 Flash via LangChain |
| BI Platform | Power BI REST API |
| Data Transformation | dbt Core Python API |
| Cloud Warehouse | Snowflake |
| UI | Streamlit |
| CI/CD | GitHub Actions |
| Containerization | Docker |

***

## 📍 Build Phases

| Phase | Description | Status |
|---|---|---|
| **Phase 1** | LangGraph StateGraph + Agent Stubs | ✅ Complete |
| **Phase 2** | Monitor Agent + Power BI REST API Mock | 🔄 In Progress |
| **Phase 3** | Diagnose Agent + Gemini 2.5 Flash Integration | ⏳ Planned |
| **Phase 4** | Heal Agent + dbt Core Python API | ⏳ Planned |
| **Phase 5** | Streamlit Live Monitoring UI | ⏳ Planned |
| **Phase 6** | GitHub Actions CI/CD + Docker | ⏳ Planned |

***

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

***

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

***

## 👤 Author

**Jayshil Jain**
- LinkedIn: [jayshiljain](https://www.linkedin.com/in/jayshiljain/)
- GitHub: [jayshilj](https://github.com/jayshilj)

***

⭐ **Star this repo if you find it useful!**
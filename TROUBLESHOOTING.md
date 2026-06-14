# Troubleshooting Guide

Welcome to the troubleshooting guide for the Real-Time Agentic BI Platform. This document provides actionable solutions for diagnosing and fixing common setup and runtime issues.

## 1. Environment Configuration

If you encounter errors related to missing environment variables or API keys:
* Ensure that a `.env` file exists in the root directory.
* Ensure that `OPENAI_API_KEY`, `DBT_PROFILES_DIR`, and other critical credentials are set correctly.
* Reload your terminal or restart the application to apply the environment changes.

## 2. Streamlit Dashboard Connection Issues

If you cannot connect to the Streamlit UI dashboard:
* Check if the Streamlit app is running using `streamlit run streamlit_app.py`.
* Ensure that the host and port (default: `localhost:8501`) are not blocked by local firewalls.
* If running in a container or remote server, make sure ports are forwarded correctly.

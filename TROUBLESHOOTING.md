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

## 3. DBT Database Connection Troubleshooting

For errors related to dbt project configuration or profiles:
* Verify that your `profiles.yml` is in the directory specified by `DBT_PROFILES_DIR`.
* Run `dbt debug` from the dbt project directory to test database connections and configuration.
* Ensure database credentials and host availability are correctly configured in `profiles.yml`.

## 4. Great Expectations Validation Error Handling

For validation rule errors or checkpoint failures:
* Check the generated HTML documentation or validation results log in the Great Expectations output directory.
* Verify your expectations configurations under `great_expectations/expectations/`.
* Re-run validation manually using `pytest` or target execution scripts to isolate rule failures.

## 5. Gmail SMTP Notification Troubleshooting

If the email notification system fails to send alerts:
* Verify that you have created a valid Google App Password (not your standard Gmail login password) if using Gmail SMTP.
* Verify port configurations in your settings (typically `587` for STARTTLS or `465` for SSL).
* Check terminal/agent logs to see if SMTP connection timeouts or authentication failures occurred.

## 6. Agent Diagnosis and Healing Failure Handling

If the self-healing LLM agent loop encounters failure or hangs:
* Check for API rate limiting or quota issues from the LLM provider (e.g. OpenAI).
* Inspect the agent graph execution logs to identify which node (Monitor, Diagnose, Heal, Validate) failed.
* Make sure that the dbt Core CLI is accessible by the agent subprocess (i.e. correct path and permissions).

## 7. Python Package Dependency Mismatch Guidance

For package import errors or version mismatches during execution:
* Verify that you are running within the correct python virtual environment (`venv`).
* Check dependencies in `requirements.txt` and ensure they are locked to supported versions.
* Run `pip install -r requirements.txt` to align your environment with the baseline requirements.

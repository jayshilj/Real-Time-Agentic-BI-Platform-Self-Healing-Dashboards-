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

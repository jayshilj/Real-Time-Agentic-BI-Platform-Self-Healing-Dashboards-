# Usage Guide

Welcome to the Usage Guide.

## Prerequisites

Ensure you have Docker and Python 3.12 installed.

## Configuration

Configure your .env file with appropriate API keys.

## Basic Commands

Run the platform using python main.py.

## Advanced Usage

Explore advanced configuration options below.

### Agent Monitoring

To monitor the LLM agent, check the logs/agent.log file.

### Dashboard Navigation

Use the sidebar in the Streamlit app to filter views.

### Data Transformation

To manually trigger a dbt build, run dbt build in the terminal.

### Validation Checkpoints

Great Expectations checkpoints can be verified in great_expectations/uncommitted/.

### Alert Notifications

Ensure SMTP_PORT is set to 587 to receive email alerts.

# System Architecture

Welcome to the architecture documentation for the Real-Time Agentic BI Platform. This document outlines the key components and data flow of the system.

## 1. High-Level Overview

The system consists of a modern data pipeline integrated with an autonomous LLM agent. Data flows from source systems into a data warehouse, is transformed using dbt, validated with Great Expectations, and finally visualized in a Streamlit dashboard.

## 2. Data Ingestion Layer

The data ingestion layer is responsible for extracting data from various operational databases and external APIs. This raw data is loaded into staging tables within the primary analytical data warehouse, preserving the original schema and granularity.



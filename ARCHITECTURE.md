# System Architecture

Welcome to the architecture documentation for the Real-Time Agentic BI Platform. This document outlines the key components and data flow of the system.

## 1. High-Level Overview

The system consists of a modern data pipeline integrated with an autonomous LLM agent. Data flows from source systems into a data warehouse, is transformed using dbt, validated with Great Expectations, and finally visualized in a Streamlit dashboard.

## 2. Data Ingestion Layer

The data ingestion layer is responsible for extracting data from various operational databases and external APIs. This raw data is loaded into staging tables within the primary analytical data warehouse, preserving the original schema and granularity.

## 3. Transformation Layer (dbt)

Data transformation is handled by dbt (Data Build Tool). Models are constructed using modular SQL to cleanse, join, and aggregate staging data into analysis-ready facts and dimensions (marts). This layer ensures business logic is version-controlled and testable.

## 4. Validation Layer (Great Expectations)

Before data reaches the dashboard, it is rigorously tested using Great Expectations. Data quality checkpoints execute assertions on data volume, null values, referential integrity, and statistical distributions, blocking bad data from entering downstream layers.

## 5. Visualization Layer (Streamlit)

The user-facing component is a dynamic dashboard built with Streamlit. It queries the validated dbt marts to display interactive visualizations, key performance indicators, and real-time operational metrics for decision makers.

## 6. Agentic Self-Healing Loop

A core innovation of this platform is the LLM-powered self-healing loop. If a pipeline failure occurs (e.g. dbt build error or validation failure), an autonomous agent intercepts the error, diagnoses the root cause using context and metadata, automatically implements a fix, and triggers a re-run without human intervention.



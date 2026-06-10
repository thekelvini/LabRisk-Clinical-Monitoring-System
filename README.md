# LabRisk Clinical Monitoring System

## Overview
LabRisk Clinical Monitoring System is an end-to-end healthcare analytics platform designed to automate laboratory data processing, risk classification, operational alerting, and clinical monitoring.

The project demonstrates a complete data engineering workflow from data ingestion through analytics delivery. The system extracts healthcare laboratory records through an API, performs data transformation and validation, loads data into a relational database, generates operational reports, sends automated alerts, and provides interactive business intelligence dashboards for clinical decision support.

## Power BI Dashboard
<img width="1443" height="809" alt="image" src="https://github.com/user-attachments/assets/bf823e87-6d05-48ff-93e1-f26c7c4afbde" />

---

## Business Problem

Healthcare organizations process thousands of laboratory results daily. Critical abnormalities can be difficult to identify quickly when data is fragmented across systems.

Delayed identification of abnormal laboratory results may result in:

* Delayed clinical intervention
* Increased patient risk
* Reduced operational efficiency
* Increased workload for clinical staff

The LabRisk Clinical Monitoring System addresses these challenges by automatically identifying abnormal and high-risk laboratory results and providing actionable insights through dashboards and automated notifications.

---

## Project Objectives

The system was designed to:

* Automate healthcare laboratory data ingestion
* Standardize and validate incoming records
* Classify laboratory results by risk level
* Create analytics-ready datasets
* Support operational alerting workflows
* Provide interactive dashboards for monitoring and decision making
* Demonstrate an end-to-end data engineering pipeline

---

## System Architecture

```text
Healthcare API
       │
       ▼
Data Extraction
       │
       ▼
Data Transformation
       │
       ▼
Data Validation
       │
       ▼
SQL Server Warehouse
       │
       ├────────► Telegram Clinical Alerts
       │
       ├────────► Power BI Dashboard
       │
       └────────► Dash Analytics Dashboard
```

---

## Technology Stack

### Programming

* Python

### Data Processing

* Pandas
* NumPy

### Database

* Microsoft SQL Server
* SQL

### API Layer

* FastAPI

### Dashboarding

* Dash
* Plotly
* Power BI

### Automation

* Telegram Bot API

### Development Tools

* Visual Studio Code
* Git
* GitHub

---

## Database Design

The healthcare warehouse consists of the following normalized tables:

### Patients

Stores patient demographic information.

### Diagnoses

Stores diagnosis codes and descriptions.

### Departments

Stores healthcare departments.

### Providers

Stores healthcare provider information.

### Encounters

Stores patient encounter records.

### Lab Tests

Stores laboratory test definitions and reference ranges.

### Lab Results

Stores laboratory test results and risk classifications.

---

## ETL Pipeline Components

### 1. Data Extraction

Laboratory records are extracted through a FastAPI endpoint.

Example fields include:

* Patient ID
* Encounter ID
* Diagnosis
* Laboratory Test
* Laboratory Value
* Provider
* Department
* Result Date

---

### 2. Data Transformation

The transformation layer performs:

* Data cleaning
* Data normalization
* Type conversion
* Result classification
* Risk classification

Each laboratory result is classified as:

* Normal
* High
* Low

Risk categories include:

* Routine
* High Risk
* Critical

---

### 3. Data Validation

Multiple validation checks ensure data quality.

Implemented validations include:

#### API Response Validation

Verifies successful data extraction.

#### Schema Validation

Verifies required columns exist.

#### Null Value Validation

Checks for missing values in critical fields.

#### Range Validation

Verifies laboratory values fall within valid ranges.

#### Duplicate Validation

Identifies duplicate encounter records.

#### Row Count Validation

Confirms no unexpected data loss during processing.

---

### 4. Database Loading

Validated records are loaded into SQL Server.

Loading process includes:

* Dimension table updates
* Fact table population
* Referential integrity preservation
* Incremental loading logic

---

### 5. Reporting

The system automatically generates:

* Daily laboratory summary reports
* High-risk patient reports
* Operational monitoring outputs

Reports are stored within the reports directory.

---

### 6. Operational Alerting

Critical and high-risk laboratory findings can be automatically transmitted through Telegram.

This functionality supports:

* Operational alerting
* Clinical escalation
* Rapid response workflows

---

## Power BI Dashboard

The Power BI dashboard provides executive-level monitoring through:

### KPI Metrics

* Total Lab Results
* Total Patients
* Critical Results
* High-Risk Results
* Department Coverage

### Visualizations

* Risk Level Distribution
* Lab Results by Department
* Critical Results by Department
* Lab Trend Analysis
* Department Risk Heatmap
* High-Risk Patient Monitoring

---

## Dash Analytics Dashboard

The project includes a fully interactive Dash web application connected to the healthcare warehouse.

### Dashboard Features

#### KPI Summary Cards

* Total Lab Results
* Total Patients
* Abnormal Results
* Critical Results
* High-Risk Results
* Departments Monitored

#### Interactive Filters

* Department
* Diagnosis
* Risk Level
* Gender
* Laboratory Test
* Date Range

#### Visual Analytics

* Risk Level Distribution
* Laboratory Results Trend
* Laboratory Results by Department
* Critical Results by Department
* Diagnosis Distribution
* Age Distribution

#### Monitoring Table

Interactive High-Risk Patient Monitoring table with filtering and sorting capabilities.

---

## Business Value

The LabRisk Clinical Monitoring System demonstrates how data engineering can support healthcare operations through:

* Improved laboratory monitoring
* Faster identification of critical findings
* Automated operational alerts
* Improved clinical visibility
* Enhanced decision support
* Reduced manual review workload

---

## Project Structure

```text
LAB-RISK-ALERT-PIPELINE
│
├── api
│   └── healthcare_api.py
│
├── Dashboard
│   ├── dash_app.py
│   ├── LabRiskDashboard.png
│   └── dashboard assets
│
├── data
│   ├── raw
│   └── processed
│
├── reports
│   ├── daily_lab_report.txt
│   └── pipeline.log
│
├── src
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   ├── report.py
│   └── send_alert.py
│
├── main.py
├── requirements.txt
├── README.md
└── .env
```

---

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the API

```bash
uvicorn api.healthcare_api:app --reload
```

### 3. Execute ETL Pipeline

```bash
python main.py
```

### 4. Launch Dash Dashboard

```bash
python Dashboard/dash_app.py
```

### 5. Open Dashboard

```text
http://127.0.0.1:8050
```

---

## Future Enhancements

Planned enhancements include:

* Real-time streaming ingestion
* Cloud deployment
* Automated scheduling with Airflow
* Predictive risk scoring
* Machine learning integration
* Electronic Health Record integration
* Real-time notification services



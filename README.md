# LabRisk Clinical Monitoring System

## Overview

LabRisk Clinical Monitoring System is an end-to-end healthcare data engineering project that automates laboratory risk monitoring and clinical reporting.

The system extracts laboratory data from a healthcare REST API, transforms and validates laboratory results, classifies patient risk levels, stores processed data in Microsoft SQL Server, sends automated Telegram alerts, and provides interactive analytics through Power BI.

This project demonstrates modern data engineering, ETL development, data warehousing, automation, and business intelligence practices within a healthcare setting.

---

## Project Architecture

Healthcare Laboratory API
↓
Python ETL Pipeline
↓
Clinical Risk Classification Engine
↓
SQL Server Healthcare Warehouse
↓
Telegram Alert Automation
↓
Power BI Clinical Dashboard

---

## Business Problem

Healthcare organizations generate large volumes of laboratory results every day. Manual review of reports can delay identification of abnormal findings and critical patient conditions.

This project provides an automated workflow that:

- Monitors laboratory activity
- Identifies abnormal and critical results
- Prioritizes high-risk patients
- Supports departmental monitoring
- Delivers real-time operational insights

---

## Features

### Data Extraction

- Extracts laboratory data from a FastAPI healthcare API
- Retrieves patient demographics and laboratory information
- Processes structured JSON responses

### Data Transformation

- Validates laboratory values against reference ranges
- Identifies abnormal results
- Applies clinical risk classification rules
- Generates reporting metrics

### Data Storage

- Loads processed records into Microsoft SQL Server
- Uses a relational healthcare warehouse design
- Supports analytical reporting and dashboarding

### Automated Alerts

- Generates daily laboratory risk reports
- Sends notifications through Telegram Bot API
- Highlights critical and high-risk findings

### Analytics and Visualization

- Interactive Power BI dashboard
- Department-level analysis
- Risk-level monitoring
- Patient-level reporting
- Clinical trend analysis

---

## Technology Stack

| Category | Technology |
|-----------|------------|
| Programming | Python |
| API | FastAPI |
| Data Processing | Pandas |
| Database | Microsoft SQL Server |
| Database Connectivity | PyODBC |
| Business Intelligence | Power BI |
| Notifications | Telegram Bot API |
| Development Environment | VS Code |
| Version Control | Git & GitHub |

---

## ETL Workflow

### Extract

Retrieve healthcare laboratory data from the FastAPI endpoint.

### Transform

- Clean incoming records
- Validate laboratory values
- Assign result status
- Determine patient risk level
- Generate summary metrics

### Load

Store processed records within SQL Server warehouse tables.

---

## Database Design

### Database

HospitalLabDB

### Tables

#### patients

Stores patient demographic information.

| Column |
|----------|
| patient_id |
| age |
| sex |

#### diagnoses

Stores diagnosis reference information.

| Column |
|----------|
| diagnosis_code |
| diagnosis_name |

#### departments

Stores hospital department information.

| Column |
|----------|
| department_id |
| department_name |

#### providers

Stores provider information.

| Column |
|----------|
| provider_id |
| provider_name |

#### lab_tests

Stores laboratory reference values.

| Column |
|----------|
| lab_test_id |
| lab_test_name |
| unit |
| reference_low |
| reference_high |

#### encounters

Stores patient encounter information.

| Column |
|----------|
| encounter_id |
| patient_id |
| diagnosis_code |
| department_id |
| provider_id |
| encounter_date |

#### lab_results

Stores laboratory observations.

| Column |
|----------|
| result_id |
| encounter_id |
| lab_test_id |
| lab_value |
| result_status |
| risk_level |
| result_date |

---

## Data Model

patients
→ encounters
→ lab_results

diagnoses
→ encounters

departments
→ encounters

providers
→ encounters

lab_tests
→ lab_results

---

## Risk Classification

### Critical

Results that exceed predefined critical clinical thresholds.

### High Risk

Results outside normal reference ranges that require follow-up.

### Routine

Results within acceptable clinical limits.

---

## Power BI Dashboard

The dashboard provides:

- Total Lab Results
- Total Patients
- Critical Results
- High Risk Patients
- Abnormal Results Percentage
- Top Critical Lab Tests
- Risk Level Distribution
- Diagnosis Distribution
- Department Risk Heatmap
- Laboratory Trends
- High Risk Patient Monitoring

---

## Example Workflow

1. Extract healthcare data from REST API
2. Transform and validate laboratory values
3. Apply clinical risk rules
4. Load processed data into SQL Server
5. Generate daily laboratory report
6. Send Telegram alert
7. Visualize results in Power BI

---

## Project Outcome

This project demonstrates how healthcare organizations can transform raw laboratory data into actionable clinical intelligence through automated ETL processing, relational data warehousing, alert automation, and interactive business intelligence dashboards.

---

## Author

Kelvin Iyenoma

MSBA 692 – Pipelines to Insights

University of Louisville
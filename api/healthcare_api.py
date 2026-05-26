from fastapi import FastAPI
import random
from datetime import datetime, timedelta

app = FastAPI(title="LabRisk Healthcare API")

diagnoses = [
    ("E11.9", "Type 2 diabetes", "Endocrinology"),
    ("N18.4", "Chronic kidney disease", "Nephrology"),
    ("D64.9", "Anemia", "Internal Medicine"),
    ("I10", "Hypertension", "Cardiology"),
    ("J44.9", "COPD", "Pulmonology"),
    ("A41.9", "Sepsis", "Emergency"),
    ("K76.9", "Liver disease", "Hepatology"),
    ("I50.9", "Heart failure", "Cardiology"),
    ("N17.9", "Acute kidney injury", "ICU"),
    ("R50.9", "Fever", "Emergency")
]

lab_tests = [
    ("HbA1c", "%", 4.0, 5.6, 4.5, 11.5),
    ("Potassium", "mmol/L", 3.5, 5.1, 2.5, 6.8),
    ("Hemoglobin", "g/dL", 12.0, 16.0, 6.5, 17.5),
    ("Glucose", "mg/dL", 70, 140, 55, 420),
    ("Creatinine", "mg/dL", 0.6, 1.2, 0.4, 6.5),
    ("WBC", "10^9/L", 4.0, 11.0, 2.0, 28.0),
    ("ALT", "U/L", 7, 56, 5, 400),
    ("AST", "U/L", 10, 40, 8, 350),
    ("Sodium", "mmol/L", 135, 145, 118, 160),
    ("Lactate", "mmol/L", 0.5, 2.2, 0.4, 9.0),
    ("Troponin", "ng/L", 0, 14, 1, 120),
    ("Platelets", "10^9/L", 150, 450, 40, 650)
]

providers = [
    "Dr Adams",
    "Dr Lee",
    "Dr Patel",
    "Dr Jones",
    "Dr Smith",
    "Dr Brown",
    "Dr Wilson",
    "Dr Thomas"
]


def assign_result_status(value, reference_low, reference_high):
    if value < reference_low:
        return "Low"

    if value > reference_high:
        return "High"

    return "Normal"


def assign_risk_level(lab_test, value):
    if lab_test == "Potassium" and (value >= 6.0 or value <= 3.0):
        return "Critical"

    if lab_test == "Lactate" and value >= 4.0:
        return "Critical"

    if lab_test == "Troponin" and value >= 50:
        return "Critical"

    if lab_test == "Sodium" and (value <= 125 or value >= 155):
        return "Critical"

    if lab_test == "Hemoglobin" and value < 8.0:
        return "Critical"

    if lab_test == "HbA1c" and value >= 8.0:
        return "High Risk"

    if lab_test == "Glucose" and value >= 250:
        return "High Risk"

    if lab_test == "Creatinine" and value >= 2.0:
        return "High Risk"

    if lab_test == "WBC" and value >= 15:
        return "High Risk"

    if lab_test in ["ALT", "AST"] and value >= 150:
        return "High Risk"

    if lab_test == "Platelets" and (value < 100 or value > 500):
        return "High Risk"

    return "Routine"


def generate_lab_results(total_records=1000):
    records = []

    for i in range(1, total_records + 1):
        diagnosis_code, diagnosis, department = random.choice(diagnoses)
        lab_test, unit, reference_low, reference_high, min_value, max_value = random.choice(lab_tests)

        lab_value = round(random.uniform(min_value, max_value), 1)
        result_status = assign_result_status(lab_value, reference_low, reference_high)
        risk_level = assign_risk_level(lab_test, lab_value)

        result_date = datetime.today() - timedelta(days=random.randint(0, 30))

        record = {
            "patient_id": f"P{i:04d}",
            "encounter_id": f"E{i:04d}",
            "age": random.randint(18, 90),
            "sex": random.choice(["Male", "Female"]),
            "diagnosis_code": diagnosis_code,
            "diagnosis": diagnosis,
            "lab_test": lab_test,
            "lab_value": lab_value,
            "unit": unit,
            "reference_low": reference_low,
            "reference_high": reference_high,
            "result_status": result_status,
            "risk_level": risk_level,
            "department": department,
            "provider": random.choice(providers),
            "result_date": result_date.strftime("%Y-%m-%d")
        }

        records.append(record)

    return records


@app.get("/")
def home():
    return {
        "message": "LabRisk Healthcare API is running"
    }


@app.get("/lab-results")
def get_lab_results():
    return generate_lab_results(1000)
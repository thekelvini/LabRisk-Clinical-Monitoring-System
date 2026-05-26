def classify_result(row):
    value = row["lab_value"]
    low = row["reference_low"]
    high = row["reference_high"]

    if value < low:
        return "Low"

    elif value > high:
        return "High"

    return "Normal"


def classify_risk(row):
    test = row["lab_test"]
    value = row["lab_value"]

    if test == "Potassium" and (value >= 6.0 or value <= 3.0):
        return "Critical"

    elif test == "Hemoglobin" and value < 9.0:
        return "High Risk"

    elif test == "HbA1c" and value >= 8.0:
        return "High Risk"

    return "Routine"


def transform_lab_data(df):
    df["result_status"] = df.apply(classify_result, axis=1)
    df["risk_level"] = df.apply(classify_risk, axis=1)

    return df
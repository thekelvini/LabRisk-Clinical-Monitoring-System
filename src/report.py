def generate_daily_report(df):

    total_results = len(df)

    abnormal_results = len(
        df[df["result_status"] != "Normal"]
    )

    critical_results = len(
        df[df["risk_level"] == "Critical"]
    )

    high_risk_results = len(
        df[df["risk_level"] == "High Risk"]
    )

    message = "Daily Lab Risk Report\n\n"

    message += f"Total results: {total_results}\n"
    message += f"Abnormal results: {abnormal_results}\n"
    message += f"Critical results: {critical_results}\n"
    message += f"High-risk results: {high_risk_results}\n\n"

    message += "Top 10 patients needing follow-up:\n\n"

    high_risk_patients = df[
        df["risk_level"].isin(
            ["Critical", "High Risk"]
        )
    ].head(10)

    for _, row in high_risk_patients.iterrows():
        message += (
            f"{row['patient_id']} | "
            f"{row['lab_test']} | "
            f"{row['lab_value']} {row['unit']} | "
            f"{row['diagnosis']} | "
            f"{row['risk_level']}\n"
        )

    message += "\nFull dataset loaded into SQL Server."

    return message
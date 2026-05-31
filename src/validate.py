import logging


def validate_api_response(df):
    if df.empty:
        raise ValueError("Validation failed: API returned no records.")

    logging.info("API response validation passed.")


def validate_required_columns(df):
    required_columns = [
        "patient_id",
        "encounter_id",
        "age",
        "sex",
        "diagnosis_code",
        "diagnosis",
        "lab_test",
        "lab_value",
        "unit",
        "reference_low",
        "reference_high",
        "result_status",
        "risk_level",
        "department",
        "provider",
        "result_date"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Validation failed: Missing columns {missing_columns}"
        )

    logging.info("Schema validation passed.")


def validate_null_values(df):
    critical_columns = [
        "patient_id",
        "encounter_id",
        "lab_test",
        "lab_value",
        "risk_level",
        "result_date"
    ]

    null_counts = df[critical_columns].isnull().sum()

    failed_columns = null_counts[null_counts > 0]

    if not failed_columns.empty:
        raise ValueError(
            f"Validation failed: Null values found {failed_columns.to_dict()}"
        )

    logging.info("Null value validation passed.")


def validate_lab_value_range(df):
    invalid_values = df[
        (df["lab_value"] < 0) |
        (df["reference_low"] < 0) |
        (df["reference_high"] < 0) |
        (df["reference_low"] > df["reference_high"])
    ]

    if not invalid_values.empty:
        raise ValueError(
            "Validation failed: Invalid lab value or reference range detected."
        )

    logging.info("Range validation passed.")


def validate_duplicates(df):
    duplicate_encounters = df[df.duplicated(subset=["encounter_id"], keep=False)]

    if not duplicate_encounters.empty:
        logging.warning(
            "Duplicate encounter IDs detected. "
            "This may be acceptable if multiple lab results exist per encounter."
        )

    logging.info("Duplicate check completed.")


def run_validations(df):
    validate_api_response(df)
    validate_required_columns(df)
    validate_null_values(df)
    validate_lab_value_range(df)
    validate_duplicates(df)

    logging.info("All validation checks completed successfully.")
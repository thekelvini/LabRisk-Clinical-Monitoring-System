import pyodbc

SERVER = "DESKTOP-9IJ6R5C"
DATABASE = "HospitalLabDB"

connection_string = f"""
DRIVER={{ODBC Driver 17 for SQL Server}};
SERVER={SERVER};
DATABASE={DATABASE};
Trusted_Connection=yes;
"""


def load_to_database(df):

    connection = pyodbc.connect(connection_string)

    cursor = connection.cursor()

    # -----------------------------
    # Patients
    # -----------------------------

    patients_df = df[
        ["patient_id", "age", "sex"]
    ].drop_duplicates()

    for _, row in patients_df.iterrows():

        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1
                FROM patients
                WHERE patient_id = ?
            )
            INSERT INTO patients (
                patient_id,
                age,
                sex
            )
            VALUES (?, ?, ?)
        """,
        row["patient_id"],
        row["patient_id"],
        row["age"],
        row["sex"]
        )

    # -----------------------------
    # Diagnoses
    # -----------------------------

    diagnoses_df = df[
        ["diagnosis_code", "diagnosis"]
    ].drop_duplicates()

    for _, row in diagnoses_df.iterrows():

        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1
                FROM diagnoses
                WHERE diagnosis_code = ?
            )
            INSERT INTO diagnoses (
                diagnosis_code,
                diagnosis_name
            )
            VALUES (?, ?)
        """,
        row["diagnosis_code"],
        row["diagnosis_code"],
        row["diagnosis"]
        )

    # -----------------------------
    # Departments
    # -----------------------------

    departments_df = df[
        ["department"]
    ].drop_duplicates()

    for _, row in departments_df.iterrows():

        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1
                FROM departments
                WHERE department_name = ?
            )
            INSERT INTO departments (
                department_name
            )
            VALUES (?)
        """,
        row["department"],
        row["department"]
        )

    # -----------------------------
    # Providers
    # -----------------------------

    providers_df = df[
        ["provider"]
    ].drop_duplicates()

    for _, row in providers_df.iterrows():

        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1
                FROM providers
                WHERE provider_name = ?
            )
            INSERT INTO providers (
                provider_name
            )
            VALUES (?)
        """,
        row["provider"],
        row["provider"]
        )

    # -----------------------------
    # Lab Tests
    # -----------------------------

    lab_tests_df = df[
        [
            "lab_test",
            "unit",
            "reference_low",
            "reference_high"
        ]
    ].drop_duplicates()

    for _, row in lab_tests_df.iterrows():

        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1
                FROM lab_tests
                WHERE lab_test_name = ?
            )
            INSERT INTO lab_tests (
                lab_test_name,
                unit,
                reference_low,
                reference_high
            )
            VALUES (?, ?, ?, ?)
        """,
        row["lab_test"],
        row["lab_test"],
        row["unit"],
        row["reference_low"],
        row["reference_high"]
        )

    connection.commit()

    # -----------------------------
    # Lookup dictionaries
    # -----------------------------

    cursor.execute("""
        SELECT department_id, department_name
        FROM departments
    """)

    department_lookup = {
        row.department_name: row.department_id
        for row in cursor.fetchall()
    }

    cursor.execute("""
        SELECT provider_id, provider_name
        FROM providers
    """)

    provider_lookup = {
        row.provider_name: row.provider_id
        for row in cursor.fetchall()
    }

    cursor.execute("""
        SELECT lab_test_id, lab_test_name
        FROM lab_tests
    """)

    lab_test_lookup = {
        row.lab_test_name: row.lab_test_id
        for row in cursor.fetchall()
    }

    # -----------------------------
    # Encounters
    # -----------------------------

    encounters_df = df[
        [
            "encounter_id",
            "patient_id",
            "diagnosis_code",
            "department",
            "provider",
            "result_date"
        ]
    ].drop_duplicates()

    for _, row in encounters_df.iterrows():

        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1
                FROM encounters
                WHERE encounter_id = ?
            )
            INSERT INTO encounters (
                encounter_id,
                patient_id,
                diagnosis_code,
                department_id,
                provider_id,
                encounter_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        row["encounter_id"],
        row["encounter_id"],
        row["patient_id"],
        row["diagnosis_code"],
        department_lookup[row["department"]],
        provider_lookup[row["provider"]],
        row["result_date"]
        )

    # -----------------------------
    # Lab Results
    # -----------------------------

    for _, row in df.iterrows():

        cursor.execute("""
            INSERT INTO lab_results (
                encounter_id,
                lab_test_id,
                lab_value,
                result_status,
                risk_level,
                result_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        row["encounter_id"],
        lab_test_lookup[row["lab_test"]],
        row["lab_value"],
        row["result_status"],
        row["risk_level"],
        row["result_date"]
        )

    connection.commit()

    cursor.close()
    connection.close()

    print("Healthcare warehouse tables loaded successfully.")
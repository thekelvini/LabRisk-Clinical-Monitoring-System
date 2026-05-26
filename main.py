from src.extract import extract_lab_data
from src.transform import transform_lab_data
from src.report import generate_daily_report
from src.send_alert import send_telegram_alert
from src.load import load_to_database


PROCESSED_FILE = "data/processed/processed_lab_results.csv"
REPORT_FILE = "reports/daily_lab_report.txt"


def main():

    # Extract data from API
    df = extract_lab_data()

    # Transform and classify lab results
    transformed_df = transform_lab_data(df)

    # Save processed CSV
    transformed_df.to_csv(
        PROCESSED_FILE,
        index=False
    )

    # Load into SQL Server
    load_to_database(transformed_df)

    # Generate report
    report = generate_daily_report(transformed_df)

    # Save text report
    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    # Print report in terminal
    print(report)

    # Send Telegram alert
    send_telegram_alert(report)


if __name__ == "__main__":
    main()
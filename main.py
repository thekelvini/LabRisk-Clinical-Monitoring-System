import logging

from src.extract import extract_lab_data
from src.transform import transform_lab_data
from src.validate import run_validations
from src.report import generate_daily_report
from src.send_alert import send_telegram_alert
from src.load import load_to_database


PROCESSED_FILE = "data/processed/processed_lab_results.csv"
REPORT_FILE = "reports/daily_lab_report.txt"


logging.basicConfig(
    filename="reports/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    try:
        logging.info("Pipeline started.")

        df = extract_lab_data()
        logging.info("Data extraction completed.")

        transformed_df = transform_lab_data(df)
        logging.info("Data transformation completed.")

        run_validations(transformed_df)
        logging.info("Data validation completed.")

        transformed_df.to_csv(PROCESSED_FILE, index=False)
        logging.info("Processed CSV saved.")

        load_to_database(transformed_df)
        logging.info("Data loaded into SQL Server warehouse.")

        report = generate_daily_report(transformed_df)

        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            file.write(report)

        logging.info("Daily report generated.")

        print(report)

        send_telegram_alert(report)
        logging.info("Telegram alert sent.")

        logging.info("Pipeline completed successfully.")

    except Exception as error:
        logging.error(f"Pipeline failed: {error}")
        print(f"Pipeline failed: {error}")


if __name__ == "__main__":
    main()
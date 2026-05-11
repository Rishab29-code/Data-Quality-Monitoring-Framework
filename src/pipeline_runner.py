import subprocess
import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="../logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(message, level="info"):
    print(message)

    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)

log_and_print("=" * 60)
log_and_print("PIPELINE STARTED")
log_and_print("=" * 60)


steps = [
    ("API Ingestion", "python multi_source_ingestion.py"),
    ("Load to Snowflake", "python load_multi_source.py"),
    ("Validation", "python snowflake_validator.py"),
    ("dbt Transformation", 'dbt run --project-dir "c:/Users/RISHAB/data-quality-framework/dq_dbt" --profiles-dir "c:/Users/RISHAB/.dbt"'),
]

for step_name, command in steps:

    log_and_print(f"\nRunning: {step_name}")

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        log_and_print(f"FAILED at step: {step_name}", "error")
        break

    log_and_print(f"SUCCESS: {step_name}")

log_and_print("\nPIPELINE FINISHED")
logging.info("Pipeline execution completed")
# pipeline.py

from dagster import op, job
import subprocess
import sys
from pathlib import Path

@op
def scrape_telegram_data():
    """Run the telegram_scraper.py script."""
    subprocess.run([sys.executable, "scripts/telegram_scraper.py"], check=True)

@op
def load_raw_to_postgres():
    """Run the load_json_to_postgres.py script."""
    subprocess.run([sys.executable, "scripts/load_json_to_postgres.py"], check=True)

@op
def run_dbt_transformations():
    """Invoke `dbt run` inside the dbt folder."""
    subprocess.run(["dbt", "run"], cwd="dbt", check=True)

@op
def run_yolo_enrichment():
    """Run the image_processing.py script."""
    subprocess.run([sys.executable, "scripts/image_processing.py"], check=True)

@job
def etl_pipeline():
    """
    Full pipeline:
      1) scrape Telegram data
      2) load raw JSON → Postgres
      3) transform with dbt
      4) enrich images with YOLO
    """
    # chaining them as dependencies:
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

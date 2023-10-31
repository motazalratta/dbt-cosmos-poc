from airflow.datasets import Dataset
from pathlib import Path
import os

DBT_ROOT_PATH = os.path.join(Path(__file__).parent, "dbt")
SQL_ROOT_PATH = os.path.join(Path(__file__).parent, "sql")
DBT_FINANCE_PATH = os.path.join(DBT_ROOT_PATH, "finance")
GCP_DEFAULT_CONN ='default_gcp_conn'
GCP_BQ_PROJECT = os.getenv('GCP_BQ_PROJECT')
GCP_BQ_DATASET = os.getenv('GCP_BQ_DATASET')
GCP_GCS_BUCKET = os.getenv('GCP_GCS_BUCKET')
GCP_BQ_FACT_PRODUCTS_TABLE = os.getenv('GCP_BQ_FACT_PRODUCTS_TABLE')

FACT_FINANCE = Dataset("FACT://finance")
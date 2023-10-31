from datetime import timedelta
from airflow import AirflowException, DAG
import os
import defaults
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryExecuteQueryOperator,
    BigQueryDeleteTableOperator,
)

default_args = {
    'start_date': '2023-10-08',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'finance_reports_export_to_gsc',
    default_args=default_args,
    schedule=[defaults.FACT_FINANCE],
    catchup=False,
) as dag:

    sql_query_file = os.path.join(defaults.SQL_ROOT_PATH, 'finance_report.sql')
    gcs_final_destination = 'finance_report/finance_report_{{ ds_nodash }}.csv'
    temp_table = f"{defaults.GCP_BQ_PROJECT}.{defaults.GCP_BQ_DATASET}.temp_finance_report"
    source_table = f"{defaults.GCP_BQ_PROJECT}.{defaults.GCP_BQ_DATASET}.{defaults.GCP_BQ_FACT_PRODUCTS_TABLE}"

    try:
        # Read the SQL query from the file
        with open(sql_query_file, 'r') as file:
            sql_query = file.read()
    except Exception as e:
        raise AirflowException(f"Error reading SQL query file: {str(e)}")

    execute_query_task = BigQueryExecuteQueryOperator(
        task_id='export_report_to_temp_table',
        sql=sql_query,
        use_legacy_sql=False,
        destination_dataset_table=temp_table,
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
        gcp_conn_id=defaults.GCP_DEFAULT_CONN,
        params={"source_table_name": source_table},
    )

    export_to_gcs_task = BigQueryToGCSOperator(
        task_id='export_to_gcs',
        source_project_dataset_table=temp_table,
        destination_cloud_storage_uris=[f'gs://{defaults.GCP_GCS_BUCKET}/{gcs_final_destination}'],
        export_format='CSV',
        field_delimiter=',',
        print_header=True,
        force_rerun=True,
        gcp_conn_id=defaults.GCP_DEFAULT_CONN,
    )

    delete_temp_table_task = BigQueryDeleteTableOperator(
        task_id='delete_temp_table',
        deletion_dataset_table=temp_table,
        gcp_conn_id=defaults.GCP_DEFAULT_CONN,
    )

    execute_query_task >> export_to_gcs_task >> delete_temp_table_task
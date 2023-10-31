from datetime import datetime
from airflow.operators.empty import EmptyOperator
from airflow import DAG
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
from cosmos.profiles import GoogleCloudServiceAccountFileProfileMapping
import defaults

# Define the profile configuration
profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountFileProfileMapping(
        conn_id=defaults.GCP_DEFAULT_CONN,
        profile_args={"dataset": defaults.GCP_BQ_DATASET},
    ),
)

# Define the DAG
with DAG(
    dag_id="fact_dag",
    start_date=datetime(2023, 10, 8),
    doc_md=__doc__,
    catchup=False,
    schedule="@daily",
    max_active_runs=1,
) as dag:
    dbt_finance = DbtTaskGroup(
        project_config=ProjectConfig(defaults.DBT_FINANCE_PATH),
        profile_config=profile_config,
        operator_args={"install_deps": True}
    )

    # Create an EmptyOperator for post-dbt processing
    post_dbt = EmptyOperator(task_id="post_dbt", outlets=[defaults.FACT_FINANCE])

    # Set the task dependencies
    dbt_finance >> post_dbt
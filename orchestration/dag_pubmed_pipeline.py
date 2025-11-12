# ============================================================
# ⚙️ PubMed Pipeline Orchestration — Sprint 4 (INNVO-479)
# ------------------------------------------------------------
# Orchestrates Spark → dbt → Vector ETL flow
# ============================================================

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'sean',
    'start_date': datetime(2025, 11, 11),
    'retries': 0,
}

with DAG(
    dag_id='pubmed_pipeline_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['pubmed', 'etl', 'sprint4'],
) as dag:

    start = DummyOperator(task_id='start')

    # Step 1 — Spark Transform
    spark_transform = BashOperator(
        task_id='spark_transform',
        bash_command='bash -c "echo 🚀 Running Spark Producer... && python3 /home/seanthakur/DBA-DE_pubmed_pipeline/scripts/spark_producer.py && echo ✅ Spark Complete"'
    )

    # Step 2 — dbt Transform
    dbt_transform = BashOperator(
        task_id='dbt_transform',
        bash_command='bash -c "echo 🧩 Executing dbt models... && /home/seanthakur/DBA-DE_pubmed_pipeline/scripts/dbt_run.sh && echo ✅ dbt Complete"'
    )

    # Step 3 — Vector Load
    vector_load = BashOperator(
        task_id='vector_load',
        bash_command='bash -c "echo 🧠 Loading vectors into pgvector... && python3 /home/seanthakur/DBA-DE_pubmed_pipeline/scripts/vector_loader.py && echo ✅ Vector Load Complete"'
    )

    end = DummyOperator(task_id='end')

    start >> spark_transform >> dbt_transform >> vector_load >> end

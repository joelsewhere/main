from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator


with DAG(
    'test_connection',
    start_date=datetime(2022, 10, 23),
    schedule_interval=None,
) as dag:
    op = PostgresOperator(
        task_id='connection',
        postgres_conn_id='postgres',
        sql="create schema if not exists test;"
    )

op
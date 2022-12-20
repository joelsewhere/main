from src.utils.dag_factory import create_dag
from src.utils.main_data import MainData
from .src import download_transactions
from airflow.decorators import task
from airflow.operators.selenium_plugin import SeleniumChromeOperator
from datetime import datetime

CONFIG = MainData()
login = CONFIG.get('MintLogin')
password = CONFIG.get('MintPassword')

DAG_CONFIG = dict(
    dag_name="mint",
    schedule_interval="@daily",
    start_date=datetime(2022, 11, 25)
)

@create_dag(**DAG_CONFIG)
def mint():

    download = SeleniumChromeOperator(
        task_id="download_transactions",
        script=download_transactions,
        script_kwargs=dict(
            login=login,
            password=password
        )
    )

    # TODO: determine download location and parse dataset
    # TODO: Postgres operator

    



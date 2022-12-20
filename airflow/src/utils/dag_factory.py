import os
import inspect
from airflow import DAG
from datetime import datetime, timedelta
from typing import Union
from main_data import MainData


DEFAULT_ARGS = {
        "owner": "@joel",
        "depends_on_past": False,
        "email": ["joelsewhere+logs@gmail.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        "on_failure_callback": task_failure_handler,  # TODO: define
        "params": {
            "test_env": MainData.is_test()}}


# TODO: create_dag decorator

def create_dag(
    dag_name: str,
    schedule_interval: str,
    start_date: datetime,
    description: str='',
    template_searchpath: str=[],
    version: Union[str, int, None]=None,
    **kwargs
    ) -> DAG:

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    if len(template_searchpath) == 0:
        template_searchpath = [MainData.sql_templates_path(), sql_templates_path()]

    if version is None:
        version_str = ""
    else:
        version_str = f"__v{version}"

    return DAG(
        f"{dag_name}{version_str}",
        catchup=False,
        default_args=DEFAULT_ARGS,
        description=description,
        template_searchpath=template_searchpath,
        schedule_interval=schedule_interval,
        start_date=start_date,
        on_success_callback=dag_success_handler,  # TODO: define
        on_failure_callback=dag_failure_handler,  # TODO: define
        **kwargs
        ) 




def sql_templates_path():
    frame = inspect.stack()[2]  # 2 levels up the stack, the caller of create_dag
    module = inspect.getmodule(frame[0])
    return os.path.join(os.path.dirname(module.__file__), "sql")
from airflow import DAG
import os
from pathlib import Path
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from src.operators.selenium_operator import SeleniumChromeOperator


with DAG(
    'test_connection',
    start_date=datetime(2022, 12, 18),
    schedule_interval=None,
) as dag:
    op1 = PostgresOperator(
        task_id='connection',
        postgres_conn_id='postgres',
        sql="create schema if not exists tests;"
    )

    op1

with DAG(
    'test_selenium',
    start_date=datetime(2022, 12, 18),
    schedule_interval=None,
) as dag:
    
    def google(driver, **kwargs):
        driver.get('https://www.google.com')
        print(driver.page_source)

    op2 = SeleniumChromeOperator(
        task_id='google',
        script=google,
    )

    op2

    def download(driver, **kwargs):
        url = 'https://github.com/jupyter/nbgrader/releases/tag/v0.8.1'
        driver.get(url)
        button = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/jupyter/nbgrader/releases/download/v0.8.1/nbgrader-0.8.1.tgz"]')))
        button.click()

    def fetch_download(*ars, ti, **kwargs):
        start = datetime.now()
        files = []
        while (datetime.now() - start).seconds < 300 and (len(files) == 0):
            files = os.listdir('/opt/airflow/files/test/download')
        
        print(files)
        assert files
        ti.xcom_push(key='test_download', value='/opt/files/test/read/policies.csv')

 
    op3 = SeleniumChromeOperator(
        task_id='download',
        script=download,
        download_dir='test/download'
    )

    op4 = PythonOperator(
        task_id='fetch_download',
        python_callable=fetch_download
    )

    op5 = PostgresOperator(
        task_id='create_table',
        sql='policies.sql',
        postgres_conn_id='postgres',
    )


    op6 = PostgresOperator(
        task_id = "load_flat_file",
        postgres_conn_id='postgres',
        sql=f"""COPY tests.read_flat_file from '/Users/joel/Documents/joel/main-dashboard/airflow/files/test/read/policies.csv' csv;""")

    op3 >> op4 >> op5 >> op6

    


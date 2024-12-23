import os
import sys

# Ensure the Airflow directory is in PYTHONPATH
os.environ["PYTHONPATH"] = "/opt/airflow:" + os.environ.get("PYTHONPATH", "")
if "/opt/airflow" not in sys.path:
    sys.path.append("/opt/airflow")

import airflow
from handlers.dataframe import (
    read_and_combine_crime_data, read_offender_data, read_victim_data, 
    read_relationship_data
)
from airflow.decorators import dag, task

class FilePaths:
    airflow_path = "/opt/airflow"
    data_folder_path = airflow_path + "/data/"

    crimes_parquet_path = data_folder_path + "crimes.parquet"
    offender_parquet_path = data_folder_path + "offender.parquet"
    victim_parquet_path = data_folder_path + "victim.parquet"
    relationship_parquet_path = data_folder_path + "relationship.parquet"

@dag(
    schedule=None,
    start_date=airflow.utils.dates.days_ago(0),
    catchup=False
)
def crime_data_dag():

    @task(task_id="start")
    def _dummy_start():
        pass

    @task(task_id="create_and_save_crimes_parquet")
    def _create_and_save_crimes_parquet():
        dataframe = read_and_combine_crime_data()
        dataframe.to_parquet(FilePaths.crimes_parquet_path, index=False)

    @task(task_id="create_and_save_offender_parquet")
    def _create_and_save_offender_parquet():
        dataframe = read_offender_data()
        dataframe.to_parquet(FilePaths.offender_parquet_path, index=False)

    @task(task_id="create_and_save_victim_parquet")
    def _create_and_save_victim_parquet():
        dataframe = read_victim_data()
        dataframe.to_parquet(FilePaths.victim_parquet_path, index=False)

    @task(task_id="create_and_save_relationship_parquet")
    def _create_and_save_relationship_parquet():
        dataframe = read_relationship_data()
        dataframe.to_parquet(FilePaths.relationship_parquet_path, index=False)

    @task(task_id="end")
    def _dummy_end():
        pass

    start = _dummy_start()
    crimes_task = _create_and_save_crimes_parquet()
    offender_task = _create_and_save_offender_parquet()
    victim_task = _create_and_save_victim_parquet()
    relationship_task = _create_and_save_relationship_parquet()
    end = _dummy_end()

    start >> [crimes_task, offender_task, victim_task, relationship_task] >> end

crime_data_dag()

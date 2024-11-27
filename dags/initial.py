import sys
if "/opt/airflow" not in sys.path:
    sys.path.append("/opt/airflow")


import airflow
from handlers.dataframe import read_and_combine_data_to_single_dataframe, drop_duplicate_incidents
from airflow.decorators import dag, task


class FilePaths:
    airflow_path = "/opt/airflow"
    data_folder_path = airflow_path + "/data/"

    crime_parquet_path = data_folder_path + "crimes.parquet"
    crime_parquet_no_duplicates_path = data_folder_path + "crimes_no_duplicates.parquet"


@dag(
    schedule=None,
    start_date=airflow.utils.dates.days_ago(0),
    catchup=False
)
def crime_dag():

    @task(task_id="start")
    def _dummy_start():
        pass

    @task(task_id="create_and_save_crime_csv")
    def _create_and_save_crime_parquet():
        dataframe = read_and_combine_data_to_single_dataframe()
        dataframe.to_parquet(FilePaths.crime_parquet_path, index=False)

    @task(task_id="drop_duplicate_incidents")
    def _drop_duplicate_incidents(parquet_path):
        dataframe = drop_duplicate_incidents(parquet_path)
        dataframe.to_parquet(
            FilePaths.crime_parquet_no_duplicates_path, index=False)

    @task(task_id="end")
    def _dummy_end():
        pass

    start = _dummy_start()
    process = _create_and_save_crime_parquet()
    drop_duplicates = _drop_duplicate_incidents(FilePaths.crime_parquet_path)
    end = _dummy_end()

    start >> process >> drop_duplicates >> end


crime_dag()

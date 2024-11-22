import sys
if "/opt/airflow" not in sys.path:
    sys.path.append("/opt/airflow")


import airflow
from handlers.dataframe import read_and_combine_data_to_single_dataframe
from airflow.decorators import dag, task


class FilePaths:
    airflow_path = "/opt/airflow"
    data_folder_path = airflow_path + "/data/"

    crime_csv_path = data_folder_path + "crimes.csv"


@dag(
    schedule=None,
    start_date=airflow.utils.dates.days_ago(0),
    catchup=False
)
def crime_dag():

    @task()
    def dummy_start():
        pass

    @task()
    def create_and_save_crime_csv(file_paths):
        dataframe = read_and_combine_data_to_single_dataframe()
        dataframe.to_csv(file_paths.crime_csv_path, index=False)

    @task()
    def dummy_end():
        pass

    start = dummy_start()
    process = create_and_save_crime_csv(FilePaths)
    end = dummy_end()

    start >> process >> end


crime_dag()

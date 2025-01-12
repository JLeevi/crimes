import sys

if "/opt/airflow" not in sys.path:
    sys.path.append("/opt/airflow")


import airflow
import json
from handlers.dataframe import read_and_combine_data_to_single_dataframe, drop_duplicate_and_nan_incidents, drop_unnecessary_columns, get_crime_df
from handlers.fetchers import fetch_hate_crime_data, fetch_crime_csv
from airflow.decorators import dag, task
from constants.file_paths import FilePaths
from constants.drive_ids import GoogleDriveIds


@dag(
    schedule=None,
    start_date=airflow.utils.dates.days_ago(0),
    catchup=False
)
def ingest_crime_data():

    @task(task_id="start")
    def _dummy_start():
        pass

    @task(task_id="files_downloaded")
    def _files_downloaded():
        pass

    @task(task_id="create_and_save_crime_csv")
    def _create_and_save_crime_parquet():
        dataframe = read_and_combine_data_to_single_dataframe()
        dataframe.to_parquet(FilePaths.crime_parquet_path, index=False)

    @task(task_id="drop_duplicate_and_nan_incidents")
    def _drop_duplicate_and_nan_incidents(parquet_path):
        dataframe = drop_duplicate_and_nan_incidents(parquet_path)
        dataframe.to_parquet(
            FilePaths.crime_parquet_no_duplicates_path, index=False)

    @task(task_id="drop_unnecessary_columns")
    def _drop_unnecessary_columns(parquet_path):
        dataframe = drop_unnecessary_columns(parquet_path)
        dataframe.to_parquet(
            FilePaths.crime_parquet_columns_of_interest, index=False)

    @task(task_id="ingest_hate_crime_json")
    def _ingest_hate_crime_json():
        hate_crime_json = fetch_hate_crime_data()
        with open(FilePaths.hate_crime_json_path, "w") as f:
            json.dump(hate_crime_json, f, indent=4)

    @task(task_id="end")
    def _dummy_end():
        pass

    start = _dummy_start()
    files_downloaded = _files_downloaded()
    process = _create_and_save_crime_parquet()
    drop_duplicates = _drop_duplicate_and_nan_incidents(
        FilePaths.crime_parquet_path)
    drop_useless_columns = _drop_unnecessary_columns(
        FilePaths.crime_parquet_no_duplicates_path)
    ingest_hate_crime = _ingest_hate_crime_json()
    end = _dummy_end()

    for file_name, file_id in GoogleDriveIds.get_drive_files():
        @task(task_id=f"download_{file_name}")
        def _download_file(file_name, file_id):
            fetch_crime_csv(file_name, file_id)

        start >> _download_file(file_name, file_id) >> files_downloaded

    files_downloaded >> \
        process >> \
        drop_duplicates >> \
        drop_useless_columns >> \
        end

    start >> ingest_hate_crime >> end


ingest_crime_data()

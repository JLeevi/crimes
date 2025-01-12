import sys

if "/opt/airflow" not in sys.path:
    sys.path.append("/opt/airflow")


import airflow
import json
from handlers.fetchers import fetch_hate_crime_data, fetch_crime_csv
from airflow.decorators import dag, task
from constants.file_paths import FilePaths
from constants.drive_ids import GoogleDriveIds


@dag(
    schedule=None,
    start_date=airflow.utils.dates.days_ago(0),
    catchup=False
)
def ingest():

    @task(task_id="start")
    def _dummy_start():
        pass

    @task(task_id="ingest_hate_crime_json")
    def _ingest_hate_crime_json():
        hate_crime_json = fetch_hate_crime_data()
        with open(FilePaths.hate_crime_json_path, "w") as f:
            json.dump(hate_crime_json, f, indent=4)

    @task(task_id="end")
    def _dummy_end():
        pass

    start = _dummy_start()
    ingest_hate_crime = _ingest_hate_crime_json()
    end = _dummy_end()

    for file_name, file_id in GoogleDriveIds.get_drive_files():
        @task(task_id=f"download_{file_name}")
        def _download_file(file_name, file_id):
            fetch_crime_csv(file_name, file_id)

        start >> _download_file(file_name, file_id) >> end

    start >> ingest_hate_crime >> end


ingest()

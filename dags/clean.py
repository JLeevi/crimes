import sys

if "/opt/airflow" not in sys.path:
    sys.path.append("/opt/airflow")


import airflow
from airflow.decorators import dag, task
from handlers.database import insert_hate_crimes_to_mongo
from handlers.hate_crime import extract_offense_and_motive_counts
from constants.file_paths import FilePaths


@dag(
    schedule=None,
    start_date=airflow.utils.dates.days_ago(0),
    catchup=False
)
def clean_data():

    @task(task_id="start")
    def _dummy_start():
        pass

    @task(task_id="extract_hate_crime_statistics", multiple_outputs=True)
    def _extract_hate_crime_statistics():
        offense_counts, motive_counts = extract_offense_and_motive_counts(
            FilePaths.hate_crime_json_path)
        return {"offense_counts": offense_counts, "motive_counts": motive_counts}

    @task(task_id="upload_hate_crimes_to_mongo")
    def _upload_hate_crimes_to_mongo(offense_counts, motive_counts):
        insert_hate_crimes_to_mongo(offense_counts, motive_counts)

    @task(task_id="end")
    def _dummy_end():
        pass

    start = _dummy_start()
    hate_crime_stats = _extract_hate_crime_statistics()
    print(hate_crime_stats)
    hate_crimes_to_mongo = _upload_hate_crimes_to_mongo(
        hate_crime_stats["offense_counts"], hate_crime_stats["motive_counts"])
    end = _dummy_end()

    start >> hate_crime_stats >> hate_crimes_to_mongo >> end


clean_data()

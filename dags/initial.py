import sys

if "/opt/airflow" not in sys.path:
    sys.path.append("/opt/airflow")


import airflow
from handlers.database import insert_crimes_to_db
from handlers.dataframe import read_and_combine_data_to_single_dataframe, drop_duplicate_and_nan_incidents, drop_unnecessary_columns, get_crime_df
from airflow.decorators import dag, task
from utils.db_query import create_insert_crimes_sql_query
from constants.columns import map_original_column_to_target


class FilePaths:
    airflow_path = "/opt/airflow"
    data_folder_path = airflow_path + "/data/"

    crime_parquet_path = data_folder_path + "crimes.parquet"
    crime_parquet_no_duplicates_path = data_folder_path + "crimes_no_duplicates.parquet"
    crime_parquet_columns_of_interest = data_folder_path + \
        "crime_parquet_columns_of_interest.parquet"
    crime_sql_file_path = data_folder_path + "insert_crimes.sql"


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

    @task(task_id="create_insert_crimes_sql_query")
    def _create_insert_crimes_sql_query(parquet_path):
        df = get_crime_df(parquet_path)
        df = df.head(10)
        rows = df.values.tolist()
        columns = map_original_column_to_target.values()
        create_insert_crimes_sql_query(
            columns,
            rows,
            FilePaths.crime_sql_file_path
        )

    @task(task_id="push_crimes_to_postgres")
    def _push_crimes_to_postgres():
        insert_crimes_to_db(FilePaths.crime_sql_file_path)

    @task(task_id="end")
    def _dummy_end():
        pass

    start = _dummy_start()
    process = _create_and_save_crime_parquet()
    drop_duplicates = _drop_duplicate_and_nan_incidents(
        FilePaths.crime_parquet_path)
    drop_useless_columns = _drop_unnecessary_columns(
        FilePaths.crime_parquet_no_duplicates_path)
    create_insert_query = _create_insert_crimes_sql_query(
        FilePaths.crime_parquet_columns_of_interest)
    push_to_postgres = _push_crimes_to_postgres()
    end = _dummy_end()

    start >> process >> drop_duplicates >> drop_useless_columns >> create_insert_query >> push_to_postgres >> end


crime_dag()

import sys

if "/opt/airflow" not in sys.path:
    sys.path.append("/opt/airflow")


import airflow
import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.edgemodifier import Label
from io import BytesIO
from constants.file_paths import FilePaths
from handlers.transform import filter_empty_relationships, group_by_relationship_and_offense, remove_empty_offenders, get_damage_statistics, get_most_expensive_crimes, extract_offense_and_motive_counts
from handlers.database import insert_hate_crimes_to_mongo, insert_crime_relationship_statistics_to_mongo, insert_property_statistics_to_mongo
from handlers.dataframe import read_and_combine_data_to_single_dataframe, drop_duplicate_and_nan_incidents, drop_unnecessary_columns, get_crime_df, is_partial_sample_file
from handlers.redis import get_cached_file, set_cached_file


@dag(
    schedule=None,
    start_date=airflow.utils.dates.days_ago(0),
    catchup=False
)
def transform():

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

    @task(task_id="files_cleaned", trigger_rule="none_failed_min_one_success")
    def _files_cleaned():
        pass

    @task(task_id="extract_crime_relationship_statistics", multiple_outputs=True)
    def _extract_crime_relationship_statistics():
        df = get_crime_df(FilePaths.crime_parquet_columns_of_interest)
        df = filter_empty_relationships(df)
        statistics_dict = group_by_relationship_and_offense(df)
        return {"statistics_dict": statistics_dict}

    @task(task_id="upload_crime_relationship_statistics_to_mongo")
    def _upload_crime_relationship_statistics_to_mongo(statistics_dict):
        insert_crime_relationship_statistics_to_mongo(statistics_dict)

    @task(task_id="extract_hate_crime_statistics", multiple_outputs=True)
    def _extract_hate_crime_statistics():
        offense_counts, motive_counts = extract_offense_and_motive_counts(
            FilePaths.hate_crime_json_path)
        offense_counts = remove_empty_offenders(offense_counts)
        return {"offense_counts": offense_counts, "motive_counts": motive_counts}

    @task(task_id="upload_hate_crimes_to_mongo")
    def _upload_hate_crimes_to_mongo(offense_counts, motive_counts):
        insert_hate_crimes_to_mongo(offense_counts, motive_counts)

    @task(task_id="extract_property_value_statistics", multiple_outputs=True)
    def _get_property_value_statistics():
        df = get_crime_df(FilePaths.crime_parquet_columns_of_interest)
        property_statistics = get_damage_statistics(df)
        return {"property_statistics": property_statistics}

    @task(task_id="get_most_expensive_crimes", multiple_outputs=True)
    def _get_most_expensive_crimes():
        df = get_crime_df(FilePaths.crime_parquet_columns_of_interest)
        most_expensive_crimes = get_most_expensive_crimes(df)
        return {"most_expensive_crimes": most_expensive_crimes}

    @task(task_id="upload_property_statistics_to_mongo")
    def _upload_property_statistics_to_mongo(property_statistics, most_expensive_crimes):
        insert_property_statistics_to_mongo(
            property_statistics, most_expensive_crimes)

    @task(task_id="end")
    def _dummy_end():
        pass

    @task.branch(task_id="get_cleaned_file_from_cache")
    def _get_cleaned_file_from_cache():
        file_bytes = get_cached_file(FilePaths.final_file_name)
        if file_bytes:
            file_buffer = BytesIO(file_bytes)
            df = pd.read_parquet(file_buffer)
            df.to_parquet(
                FilePaths.crime_parquet_columns_of_interest, index=False)
            return "files_cleaned"
        return "create_and_save_crime_csv"

    @task(task_id="set_cleaned_file_to_cache")
    def _set_cleaned_file_to_cache():
        df = pd.read_parquet(FilePaths.crime_parquet_columns_of_interest)
        if not is_partial_sample_file(df):
            set_cached_file(FilePaths.final_file_name, df.to_parquet())

    start = _dummy_start()
    get_cleaned_file_from_cache = _get_cleaned_file_from_cache()
    files_cleaned = _files_cleaned()

    process = _create_and_save_crime_parquet()
    drop_duplicates = _drop_duplicate_and_nan_incidents(
        FilePaths.crime_parquet_path)
    drop_useless_columns = _drop_unnecessary_columns(
        FilePaths.crime_parquet_no_duplicates_path)
    cache_cleaned_file = _set_cleaned_file_to_cache()

    hate_crime_stats = _extract_hate_crime_statistics()
    hate_crimes_to_mongo = _upload_hate_crimes_to_mongo(
        hate_crime_stats["offense_counts"], hate_crime_stats["motive_counts"])

    relationship_stats = _extract_crime_relationship_statistics()
    relationship_stats_to_mongo = _upload_crime_relationship_statistics_to_mongo(
        relationship_stats["statistics_dict"])

    property_stats = _get_property_value_statistics()
    most_expensive_crimes = _get_most_expensive_crimes()
    property_stats_to_mongo = _upload_property_statistics_to_mongo(
        property_stats["property_statistics"], most_expensive_crimes["most_expensive_crimes"])

    end = _dummy_end()

    start >> get_cleaned_file_from_cache >> \
        Label("Found cached file") >> \
        files_cleaned

    start >> get_cleaned_file_from_cache >> \
        Label("Cached file not found") >> \
        process >> \
        drop_duplicates >> \
        drop_useless_columns >> \
        cache_cleaned_file >> \
        files_cleaned

    start >> hate_crime_stats >> hate_crimes_to_mongo >> end

    files_cleaned >> relationship_stats >> relationship_stats_to_mongo >> end
    files_cleaned >> [
        property_stats,
        most_expensive_crimes
    ] >> property_stats_to_mongo >> end


transform()

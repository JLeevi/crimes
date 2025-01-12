class FilePaths:
    airflow_path = "/opt/airflow"
    data_folder_path = airflow_path + "/data/"
    notebook_folder_path = airflow_path + "/notebooks/"

    crime_parquet_path = data_folder_path + "crimes.parquet"
    crime_parquet_no_duplicates_path = data_folder_path + "crimes_no_duplicates.parquet"
    crime_parquet_columns_of_interest = data_folder_path + \
        "crime_parquet_columns_of_interest.parquet"
    crime_sql_file_path = data_folder_path + "insert_crimes.sql"
    hate_crime_json_path = data_folder_path + "hate_crime.json"
    notebook_path = notebook_folder_path + "notebook.ipynb"
    notebook_output_path = notebook_folder_path + "notebook-prod.ipynb"

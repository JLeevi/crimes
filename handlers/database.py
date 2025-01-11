from airflow.providers.postgres.hooks.postgres import PostgresHook


def insert_crimes_to_db(insert_file_path):
    with open(insert_file_path, "r") as f:
        sql_query = f.read()
        postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
        postgres_hook.run(sql_query)

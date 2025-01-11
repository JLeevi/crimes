import os
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def insert_crimes_to_db(insert_file_path):
    with open(insert_file_path, "r") as f:
        sql_query = f.read()
        postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
        postgres_hook.run(sql_query)


def insert_hate_crimes_to_mongo(offense_counts, motive_counts):
    uri = os.getenv("MONGO_DB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["crimes"]
    collection = db["hate_crime"]
    collection.insert_one({
        "offense_counts": offense_counts,
        "motive_counts": motive_counts
    })


def insert_crime_relationship_statistics_to_mongo(statistics_dict):
    uri = os.getenv("MONGO_DB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["crimes"]
    collection = db["crime_relationship_statistics"]
    collection.insert_one(statistics_dict)

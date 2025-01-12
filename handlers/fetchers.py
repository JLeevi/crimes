import json
import os
import pickle
from redis import Redis
import requests

data_path = "./data"
sample_data_path = "./data-sample"
sample_hate_crime_path = sample_data_path + "/hate_crime.json"
sample_crime_folder_path = sample_data_path + "/crime-csvs"
crime_folder_path = data_path + "/crime-csvs"


def fetch_hate_crime_data():
    try:
        url = "https://api.usa.gov/crime/fbi/cde/hate-crime/state/CA"
        api_key = os.getenv("FBI_API_KEY")
        parameters = {
            "from": "01-2023",
            "to": "12-2023",
            "API_KEY": api_key,
            "type": "json"
        }

        response = requests.get(url, params=parameters)
        if response.status_code != 200:
            raise Exception("Failed to fetch hate crime data")
        data = response.json()
        return data
    except Exception as e:
        print("Failed to fetch hate crime data")
        print("Using offline sample file instead")
        return _get_offline_sample_hate_crime()


def ingest_crime_csv(file_name: str, file_id: str):
    redis_client = _get_redis_connection()
    cached_csv = redis_client.get(file_name)
    if cached_csv:
        print(f"Using cached file: {file_name}")
        content = pickle.loads(cached_csv)
        _save_csv(file_name, content)
    else:
        print(f"Downloading file: {file_name}")
        csv_data = _fetch_drive_file(file_name, file_id)
        redis_client.set(file_name, pickle.dumps(csv_data))
        _save_csv(file_name, csv_data)


def _fetch_drive_file(file_name: str, file_id: str):
    try:
        file_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        response = requests.get(file_url)
        if response.status_code != 200:
            raise Exception(f"Failed to download file: {file_name}")
        return response.content
    except Exception as e:
        print(f"Failed to download file: {file_name}")
        print(f"Using offline sample file instead")
        return _get_offline_sample_crime_file(file_name)


def _save_csv(file_name: str, content: bytes):
    os.makedirs(crime_folder_path, exist_ok=True)
    with open(f"{crime_folder_path}/{file_name}.csv", "wb") as file:
        file.write(content)


def _get_offline_sample_crime_file(file_name: str):
    with open(f"{sample_crime_folder_path}/{file_name}.csv", "rb") as file:
        return file.read()


def _get_offline_sample_hate_crime():
    with open(sample_hate_crime_path, "r") as file:
        return json.load(file)


def _get_redis_connection():
    redis_client = Redis(host='redis', port=6379,
                         db=0, decode_responses=False)
    return redis_client

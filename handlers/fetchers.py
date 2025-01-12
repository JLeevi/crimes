import os
import pickle
from redis import Redis
import requests


def fetch_hate_crime_data():
    url = "https://api.usa.gov/crime/fbi/cde/hate-crime/state/CA"
    api_key = os.getenv("FBI_API_KEY")
    parameters = {
        "from": "01-2023",
        "to": "12-2023",
        "API_KEY": api_key,
        "type": "json"
    }

    response = requests.get(url, params=parameters)
    data = response.json()
    return data


def ingest_crime_csv(file_name: str, file_id: str):
    redis_client = _get_redis_connection()
    cached_csv = redis_client.get(file_name)
    if cached_csv:
        print(f"Using cached file: {file_name}")
        content = pickle.loads(cached_csv)
        _save_csv(file_name, content)
    else:
        print(f"Downloading file: {file_name}")
        csv_data = _fetch_drive_file(file_id)
        redis_client.set(file_name, pickle.dumps(csv_data))
        _save_csv(file_name, csv_data)


def _fetch_drive_file(file_id: str):
    file_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    response = requests.get(file_url)
    return response.content


def _save_csv(file_name: str, content: bytes):
    os.makedirs("./data/crime-csvs", exist_ok=True)
    with open(f"./data/crime-csvs/{file_name}.csv", "wb") as file:
        file.write(content)


def _get_redis_connection():
    redis_client = Redis(host='redis', port=6379,
                         db=0, decode_responses=False)
    return redis_client

import os
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


def fetch_crime_csv(file_name: str, file_id: str):
    file_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    response = requests.get(file_url)
    os.makedirs("./data/crime-csvs", exist_ok=True)
    with open(f"./data/crime-csvs/{file_name}.csv", "wb") as file:
        file.write(response.content)

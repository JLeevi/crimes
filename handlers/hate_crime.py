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

import json
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


def extract_offense_and_motive_counts(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        offense_counts = data["bias_section"]["offender_race"]
        motive_counts = data["incident_section"]["bias"]
        return offense_counts, motive_counts

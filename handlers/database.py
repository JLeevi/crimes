import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


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


def insert_property_statistics_to_mongo(property_statistics, most_expensive_crimes):
    uri = os.getenv("MONGO_DB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["crimes"]
    collection = db["property_statistics"]
    collection.insert_one({
        "property_statistics": property_statistics,
        "most_expensive_crimes": most_expensive_crimes
    })


def get_crime_relationship_statistics_from_mongo():
    uri = os.getenv("MONGO_DB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["crimes"]
    collection = db["crime_relationship_statistics"]
    output = collection.find_one(sort=[('_id', -1)])
    output.pop("_id")
    return output


def get_hate_crime_statistics_from_mongo():
    uri = os.getenv("MONGO_DB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["crimes"]
    collection = db["hate_crime"]
    output = collection.find_one(sort=[('_id', -1)])
    output.pop("_id")
    return output


def get_property_statistics_from_mongo():
    uri = os.getenv("MONGO_DB_URI")
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["crimes"]
    collection = db["property_statistics"]
    output = collection.find_one(sort=[('_id', -1)])
    output.pop("_id")
    return output

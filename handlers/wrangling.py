import json
import pandas as pd


def filter_empty_relationships(dataframe):
    dataframe = dataframe[dataframe["relationship"] != "Relationship Unknown"]
    dataframe = dataframe[dataframe["relationship"] != "Victim Was Stranger"]
    dataframe = dataframe[dataframe["offense_category"] != "None/Unknown"]
    return dataframe


def group_by_relationship_and_offense(dataframe):
    dataframe_without_assaults = dataframe[dataframe["offense_category"]
                                           != "Assault Offenses"]

    assaults = _get_relationship_statistics(
        dataframe,
        normalize=False
    )
    assaults_normalized = _get_relationship_statistics(
        dataframe,
        normalize=True
    )
    without_assaults = _get_relationship_statistics(
        dataframe_without_assaults,
        normalize=False
    )
    without_assaults_normalized = _get_relationship_statistics(
        dataframe_without_assaults,
        normalize=True
    )

    return {
        "statistics": {
            "assaults": assaults,
            "assaults_normalized": assaults_normalized,
            "without_assaults": without_assaults,
            "without_assaults_normalized": without_assaults_normalized
        }
    }


def _get_relationship_statistics(dataframe, normalize):
    seven_largest_categories = dataframe["offense_category"].value_counts(
    ).nlargest(7).index
    dataframe = dataframe[dataframe["offense_category"].isin(
        seven_largest_categories)]
    dataframe = dataframe.groupby("relationship")[
        "offense_category"].value_counts(
        normalize=normalize).unstack()
    dataframe = dataframe.fillna(0)
    dataframe = dataframe.to_dict()
    return dataframe


def extract_offense_and_motive_counts(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        offense_counts = data["bias_section"]["offender_race"]
        motive_counts = data["incident_section"]["bias"]
        return offense_counts, motive_counts


def remove_empty_offenders(offender_statistics):
    return {k: v for k, v in offender_statistics.items() if k not in ["Not Specified", "Unknown"]}


def get_damage_statistics(dataframe):
    dataframe = dataframe.dropna(subset=["property_value"])
    property_grouped = dataframe.groupby("property_description")[
        "property_value"]
    top_5 = property_grouped.mean().sort_values(ascending=False).head(5).index
    property_grouped_df = dataframe[dataframe["property_description"].isin(
        top_5)]
    property_grouped = property_grouped_df.groupby(
        "property_description")["property_value"]
    property_statistics = pd.DataFrame({
        "mean": property_grouped.mean(),
        "median": property_grouped.median()
    }).sort_values(by="mean", ascending=True).to_dict()
    return property_statistics


def get_most_expensive_crimes(dataframe):
    dataframe = dataframe.dropna(subset=["property_value"])
    dataframe = dataframe[dataframe["property_description"] != "Other"]
    dataframe = dataframe.sort_values(
        by="property_value", ascending=False).head(5)
    dataframe = dataframe[["property_value", "property_description",
                           "property_loss_description", "crime_against", "location"]]
    dataframe = dataframe.to_dict(orient="records")
    return dataframe

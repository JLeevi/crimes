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


def remove_empty_offenders(offender_statistics):
    return {k: v for k, v in offender_statistics.items() if k not in ["Not Specified", "Unknown"]}

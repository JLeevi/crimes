def filter_empty_relationships(dataframe):
    dataframe = dataframe[dataframe["relationship"] != "Relationship Unknown"]
    dataframe = dataframe[dataframe["relationship"] != "Victim Was Stranger"]
    dataframe = dataframe[dataframe["offense_category"] != "None/Unknown"]
    return dataframe


def group_by_relationship_and_offense(dataframe):
    dataframe = dataframe.groupby("relationship")[
        "offense_category"].value_counts(normalize=True).unstack()
    dataframe = dataframe.fillna(0)
    return dataframe.to_dict()

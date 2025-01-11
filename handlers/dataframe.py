import pandas as pd
from file_readers.RelationshipFileReader import RelationshipFileReader
from file_readers.PropertyFileReader import PropertyFileReader
from file_readers.OffenseFileReader import OffenseFileReader
from file_readers.LocationFileReader import LocationFileReader
from file_readers.CriminalActFileReader import CriminalActFileReader
from file_readers.OffenderFileReader import OffenderFileReader
from constants.columns import columns_to_keep, map_original_column_to_target


def read_and_combine_data_to_single_dataframe():
    property_file_reader = PropertyFileReader()
    offense_file_reader = OffenseFileReader()
    location_file_reader = LocationFileReader()
    criminal_act_file_reader = CriminalActFileReader()
    offender_file_reader = OffenderFileReader()
    relationship_file_reader = RelationshipFileReader()

    dataframe = property_file_reader.get_property_df()
    dataframe = offense_file_reader.merge_offense_to_df(dataframe)
    dataframe = location_file_reader.merge_location_to_df(dataframe)
    dataframe = criminal_act_file_reader.merge_criminal_act_to_df(dataframe)
    dataframe = offender_file_reader.merge_offender_to_df(dataframe)
    dataframe = relationship_file_reader.merge_relationship_to_df(dataframe)
    dataframe = dataframe.sort_values(by="property_value", ascending=False)

    return dataframe


def drop_duplicate_and_nan_incidents(parquet_path):
    dataframe = pd.read_parquet(parquet_path)
    dataframe = dataframe.drop_duplicates(subset=["incident_id"])
    dataframe = dataframe.dropna(subset=["incident_id"])
    return dataframe


def drop_unnecessary_columns(parquet_path):
    dataframe = pd.read_parquet(parquet_path)
    return dataframe[columns_to_keep].rename(columns=map_original_column_to_target)


def get_crime_df(parquet_path):
    return pd.read_parquet(parquet_path)

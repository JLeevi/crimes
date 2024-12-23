import pandas as pd
from file_readers.PropertyFileReader import PropertyFileReader
from file_readers.OffenseFileReader import OffenseFileReader
from file_readers.LocationFileReader import LocationFileReader
from file_readers.CriminalActFileReader import CriminalActFileReader
from file_readers.OffenderFileReader import OffenderFileReader
from file_readers.VictimFileReader import VictimFileReader
from file_readers.RelationshipFileReader import RelationshipFileReader

def read_and_combine_crime_data():
    property_file_reader = PropertyFileReader()
    offense_file_reader = OffenseFileReader()
    location_file_reader = LocationFileReader()
    criminal_act_file_reader = CriminalActFileReader()
    offender_file_reader = OffenderFileReader()

    dataframe = property_file_reader.get_property_df()
    dataframe = offense_file_reader.merge_offense_to_df(dataframe)
    dataframe = location_file_reader.merge_location_to_df(dataframe)
    dataframe = criminal_act_file_reader.merge_criminal_act_to_df(dataframe)
    dataframe = offender_file_reader.merge_offender_to_df(dataframe)
    dataframe = dataframe.sort_values(by="property_value", ascending=False)

    return dataframe

def read_offender_data():
    offender_file_reader = OffenderFileReader()
    dataframe = offender_file_reader.get_offender_df()
    dataframe = dataframe.sort_values(by="offender_id", ascending=True)
    return dataframe

def read_victim_data():
    victim_file_reader = VictimFileReader()
    dataframe = victim_file_reader.get_victim_df()
    dataframe = dataframe.sort_values(by="victim_id", ascending=True)
    return dataframe

def read_relationship_data():
    relationship_file_reader = RelationshipFileReader()
    dataframe = relationship_file_reader.get_victim_offender_rel_df()
    dataframe = dataframe.sort_values(by="relationship_id", ascending=True)
    return dataframe

def drop_duplicate_and_nan_incidents(parquet_path):
    dataframe = pd.read_parquet(parquet_path)
    dataframe = dataframe.drop_duplicates(subset=["incident_id"])
    dataframe = dataframe.dropna(subset=["incident_id"])
    return dataframe


from file_readers.PropertyFileReader import PropertyFileReader
from file_readers.OffenseFileReader import OffenseFileReader
from file_readers.LocationFileReader import LocationFileReader
from file_readers.CriminalActFileReader import CriminalActFileReader
from file_readers.OffenderFileReader import OffenderFileReader


def read_and_combine_data_to_single_dataframe():
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

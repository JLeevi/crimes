import pandas as pd
from file_readers.BaseFileReader import BaseFileReader


class LocationFileReader(BaseFileReader):
    def __init__(self):
        super().__init__()

        self.__location_file = "NIBRS_LOCATION_TYPE.csv"

        self.__location_id_column = "location_id"

    def merge_location_to_df(self, to_df):
        assert self.__location_id_column in to_df.columns
        location_df = self.__get_location_df()
        return self.merge_dfs(to_df, location_df, self.__location_id_column)

    def __get_location_df(self):
        location_df = self.read_as_dataframe(self.__location_file)
        return location_df

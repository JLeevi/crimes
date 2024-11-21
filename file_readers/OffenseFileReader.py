import pandas as pd
from file_readers.BaseFileReader import BaseFileReader


class OffenseFileReader(BaseFileReader):
    def __init__(self):
        super().__init__()

        self.__offense_file = "NIBRS_OFFENSE.csv"
        self.__offense_type_file = "NIBRS_OFFENSE_TYPE.csv"

        self.__offense_code_column = "offense_code"
        self__offense_name_column = "offense_name"

        self.__columns_to_keep = [
            self.incident_id_column,
            self__offense_name_column
        ]

    def merge_offense_name_to_df(self, to_df):
        offense_df = self.__get_offense_name_df()
        return self.merge_dfs(to_df, offense_df, self.incident_id_column)

    def __get_offense_name_df(self):
        offense_df = self.read_as_dataframe(self.__offense_file)
        offense_type_df = self.read_as_dataframe(self.__offense_type_file)
        merged_df = self.merge_dfs(
            offense_df, offense_type_df, self.__offense_code_column)
        merged_df = self.only_keep_columns(merged_df, self.__columns_to_keep)
        return merged_df

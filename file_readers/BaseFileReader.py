import pandas as pd
import os


class BaseFileReader:
    def __init__(self):
        self.incident_id_column = "incident_id"
        self.__folder_path = os.path.join(
            os.path.dirname(__file__), "../data/CA/")

    def read_as_dataframe(self, file_name):
        return pd.read_csv(self.__to_full_path(file_name))

    def merge_dfs(self, first_df, second_df, on_column):
        return pd.merge(first_df, second_df, on=on_column)

    def __to_full_path(self, file):
        return self.__folder_path + file

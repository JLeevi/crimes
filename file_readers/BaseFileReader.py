import pandas as pd
import os


class BaseFileReader:
    def __init__(self):
        self.incident_id_column = "incident_id"
        self.__folder_path = os.path.join(
            os.path.dirname(__file__), "../data/CA/")

    def read_as_dataframe(self, file_name: str):
        df = pd.read_csv(self.__to_full_path(file_name))
        df = self.__convert_id_columns_to_integers(df)
        return df

    def merge_dfs(self, first_df: pd.DataFrame, second_df: pd.DataFrame, on_column: str):
        columns_without_duplicates = self.__get_columns_without_duplicates(
            first_df, second_df, on_column)
        second_df_without_duplicate_columns = second_df[columns_without_duplicates]
        merged_df = pd.merge(
            first_df, second_df_without_duplicate_columns, on=on_column, how="outer")
        merged_df = self.__convert_id_columns_to_integers(merged_df)
        return merged_df

    def __convert_id_columns_to_integers(self, df: pd.DataFrame):
        float_columns = df.select_dtypes(include=["float"]).columns
        df[float_columns] = df[float_columns].astype("Int64")
        df.head()
        return df

    def __to_full_path(self, file):
        return self.__folder_path + file

    def __get_columns_without_duplicates(self, first_df: pd.DataFrame, second_df: pd.DataFrame, on_column: str = None):
        columns_without_duplicates = second_df.columns.difference(
            first_df.columns)
        if on_column:
            columns_without_duplicates = columns_without_duplicates.insert(
                0, on_column)
        return columns_without_duplicates

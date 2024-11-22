import pandas as pd
from .BaseFileReader import BaseFileReader


class PropertyFileReader(BaseFileReader):
    def __init__(self):
        super().__init__()

        self.__property_mapping_file = "NIBRS_PROPERTY.csv"
        self.__property_file = "NIBRS_PROPERTY_DESC.csv"
        self.__property_type_file = "NIBRS_PROP_DESC_TYPE.csv"
        self.__property_loss_file = "NIBRS_PROP_LOSS_TYPE.csv"

        self.__property_id_column = "property_id"
        self.__property_type_id_column = "prop_desc_id"
        self.__property_value_column = "property_value"
        self.__property_loss_id = "prop_loss_id"

    def get_property_df(self):
        property_mapping_df = self.__get_property_mapping_df()
        property_data_df = self.__get_property_data_df()
        property_type_df = self.__get_property_type_df()
        property_loss_df = self.__get_property_loss_df()
        merged_df = self.merge_dfs(
            property_mapping_df, property_data_df, self.__property_id_column)
        merged_df = self.merge_dfs(
            merged_df, property_type_df, self.__property_type_id_column)
        merged_df = self.merge_dfs(
            merged_df, property_loss_df, self.__property_loss_id)
        merged_df = self.__clear_unset_property_values(merged_df)
        return merged_df

    def __get_property_mapping_df(self):
        return self.read_as_dataframe(self.__property_mapping_file)

    def __get_property_data_df(self):
        return self.read_as_dataframe(self.__property_file)

    def __get_property_type_df(self):
        return self.read_as_dataframe(self.__property_type_file)

    def __get_property_loss_df(self):
        return self.read_as_dataframe(self.__property_loss_file)

    def __clear_unset_property_values(self, df):
        return df[~df.apply(self.__is_property_value_unset, axis=1)]

    def __is_property_value_unset(self, row):
        property_value = row[self.__property_value_column]
        return pd.isnull(property_value) or property_value <= 1.0

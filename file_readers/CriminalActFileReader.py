import pandas as pd
from file_readers.BaseFileReader import BaseFileReader


class CriminalActFileReader(BaseFileReader):
    def __init__(self):
        super().__init__()

        self.__criminal_act_file = "NIBRS_CRIMINAL_ACT.csv"
        self.__criminal_act_type_file = "NIBRS_CRIMINAL_ACT_TYPE.csv"

        self.__offense_id_column = "offense_id"
        self.__criminal_act_id_column = "criminal_act_id"

    def merge_criminal_act_to_df(self, to_df):
        assert self.__offense_id_column in to_df.columns
        criminal_act_df = self.__get_criminal_act_df()
        return self.merge_dfs(to_df, criminal_act_df, self.__offense_id_column)

    def __get_criminal_act_df(self):
        df_with_id = self.read_as_dataframe(self.__criminal_act_file)
        df_with_name = self.read_as_dataframe(self.__criminal_act_type_file)
        criminal_act_df = pd.merge(
            df_with_id, df_with_name, on=self.__criminal_act_id_column)
        return criminal_act_df

import pandas as pd
from file_readers.BaseFileReader import BaseFileReader


class OffenderFileReader(BaseFileReader):
    def __init__(self):
        super().__init__()

        self.__offender_file = "NIBRS_OFFENDER.csv"
        self.__race_file = "REF_RACE.csv"

        self.__race_id_column = "race_id"

    def merge_offender_to_df(self, to_df):
        assert self.incident_id_column in to_df.columns
        offender_df = self.__get_offender_df()
        return self.merge_dfs(to_df, offender_df, self.incident_id_column)

    def __get_offender_df(self):
        offender_df = self.read_as_dataframe(self.__offender_file)
        df_with_race = self.read_as_dataframe(self.__race_file)
        offender_df = pd.merge(
            offender_df, df_with_race, on=self.__race_id_column)
        return offender_df

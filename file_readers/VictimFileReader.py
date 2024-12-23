import pandas as pd
from file_readers.BaseFileReader import BaseFileReader

class VictimFileReader(BaseFileReader):
    def __init__(self):
        super().__init__()

        self.__victim_file = "NIBRS_VICTIM.csv"
        self.__victim_type_file = "NIBRS_VICTIM_TYPE.csv"

        self.__victim_type_id_column = "victim_type_id"
        self.__columns_to_keep = [
            "victim_id","data_year", "incident_id", "victim_seq_num", "victim_type_id",
            "assignment_type_id", "activity_type_id", "age_id", "age_num",
            "sex_code", "race_id", "ethnicity_id"
        ]

    def merge_victim_to_df(self, to_df):
        assert self.incident_id_column in to_df.columns
        victim_df = self.get_victim_df()
        return self.merge_dfs(to_df, victim_df, self.incident_id_column)

    def get_victim_df(self):
        victim_df = self.read_as_dataframe(self.__victim_file)
        victim_df = victim_df[self.__columns_to_keep]
        victim_df = victim_df.drop_duplicates()

        victim_type_df = self.read_as_dataframe(self.__victim_type_file)
        merged_df = self.merge_dfs(
            victim_df, victim_type_df, self.__victim_type_id_column)
        
        return merged_df
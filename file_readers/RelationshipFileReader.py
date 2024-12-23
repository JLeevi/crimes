import pandas as pd
from file_readers.BaseFileReader import BaseFileReader

class RelationshipFileReader(BaseFileReader):
    def __init__(self):
        super().__init__()

        self.__victim_offender_rel_file = "NIBRS_VICTIM_OFFENDER_REL.csv"
        self.__relationship_file = "NIBRS_RELATIONSHIP.csv"

        self.__relationship_id_column = "relationship_id"
        self.__columns_to_keep = [
            "data_year", "victim_id", "offender_id", "relationship_id", "nibrs_victim_offender_id"
        ]

    def merge_victim_offender_rel_to_df(self, to_df):
        assert self.incident_id_column in to_df.columns
        victim_offender_rel_df = self.get_victim_offender_rel_df()
        return self.merge_dfs(to_df, victim_offender_rel_df, self.incident_id_column)

    def get_victim_offender_rel_df(self):
        victim_offender_rel_df = self.read_as_dataframe(self.__victim_offender_rel_file)
        victim_offender_rel_df = victim_offender_rel_df[self.__columns_to_keep]
        victim_offender_rel_df = victim_offender_rel_df.drop_duplicates()

        relationship_df = self.read_as_dataframe(self.__relationship_file)
        merged_df = self.merge_dfs(
            victim_offender_rel_df, relationship_df, self.__relationship_id_column)
        
        return merged_df

from file_readers.BaseFileReader import BaseFileReader


class RelationshipFileReader(BaseFileReader):
    def __init__(self):
        super().__init__()
        self.__victim_file = "NIBRS_VICTIM.csv"
        self.__victim_type_file = "NIBRS_VICTIM_TYPE.csv"
        self.__relationship_file = "NIBRS_VICTIM_OFFENDER_REL.csv"
        self.__relationship_type_file = "NIBRS_RELATIONSHIP.csv"
        self.__victim_id_column = "victim_id"
        self.__victim_type_column = "victim_type_id"
        self.__relationship_id_column = "relationship_id"

    def merge_relationship_to_df(self, to_df):
        assert self.incident_id_column in to_df.columns
        victim_df = self.__get_victim_df()
        relationship_df = self.__get_relationship_df()
        victim_df = self.merge_dfs(
            victim_df, relationship_df, self.__victim_id_column)
        return self.merge_dfs(to_df, victim_df, self.incident_id_column)

    def __get_victim_df(self):
        victim_df = self.read_as_dataframe(self.__victim_file)
        victim_type_df = self.read_as_dataframe(self.__victim_type_file)
        merged_df = self.merge_dfs(
            victim_df, victim_type_df, self.__victim_type_column)
        return merged_df

    def __get_relationship_df(self):
        relationship_df = self.read_as_dataframe(self.__relationship_file)
        relationship_type_df = self.read_as_dataframe(
            self.__relationship_type_file)
        merged_df = self.merge_dfs(
            relationship_df, relationship_type_df, self.__relationship_id_column)
        return merged_df

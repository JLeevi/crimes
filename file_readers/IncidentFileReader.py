import pandas as pd
from file_readers.BaseFileReader import BaseFileReader


class IncidentFileReader(BaseFileReader):
    def __init__(self):
        super().__init__()
        self.__incident_file = "NIBRS_incident.csv"

    def get_incident_df(self):
        return self.read_as_dataframe(self.__incident_file)

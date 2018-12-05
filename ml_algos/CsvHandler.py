import sys
import os.path
import pandas as pd
import numpy as np
from config.config import env

class CsvHandler():
    def __init__(self, name, df):
        self.name = name
        self.df = df

    def df_to_csv(self):
        path = os.path.join(env['UPLOADS_DIR'] + '/csv_files_keywords', self.name)
        return self.df.to_csv(path)
    
    def format_name(self):
        pass

        
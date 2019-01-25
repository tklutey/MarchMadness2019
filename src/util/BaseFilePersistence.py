# -*- coding: utf-8 -*-
import pandas as pd

class BaseFilePersistence:
    def __init__(self, filepath):
        self.filepath = filepath;
        
    def read_from_csv(self):
        return pd.read_csv(self.filepath)
    
    def write_to_csv(self, df):
        df.to_csv(self.filepath)
# -*- coding: utf-8 -*-
class BaseFileWriter:
    def __init__(self, filepath):
        self.filepath = filepath;
        
    def write_to_csv(self, df):
        df.to_csv(self.filepath)
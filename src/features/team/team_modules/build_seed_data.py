# -*- coding: utf-8 -*-

from data import make_dataset
from features.utils import feature_utils 

def make():
    df = make_dataset.load_seed_data()
    df['TeamSeasonId'] = feature_utils.create_key_from_fields(df['TeamID'], df['Season'])
    df = df.drop('TeamID', axis=1)
    return df

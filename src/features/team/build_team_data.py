#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 23:58:09 2019

@author: kluteytk
"""
import pandas as pd
from features.utils import feature_utils 
from features.team.team_modules import build_season_data  
from features.team.team_modules import build_team_metadata  
import re

from util.IntermediateFileWriter import IntermediateFileWriter

def groom_spellings(df):
    for col, series in df.iteritems():
        if col == 'School':
            for i in series:
                if ' NCAA' in i:
                    x = re.sub(' NCAA', '', i)
                    series.replace(i, x, inplace=True)

    return df

def merge_season_team_metadata(df_team_metadata, df_regular_season_aggregated):
    df_regular_season_data = pd.merge(left=df_team_metadata, right=df_regular_season_aggregated, how='inner', right_on='School', left_on='TeamName').drop('School', axis=1)
    df_regular_season_data['TeamSeasonId'] = feature_utils.create_key_from_fields(df_regular_season_data['TeamID'], df_regular_season_data['Year'])
    return df_regular_season_data

def main():
    df_team_metadata = build_team_metadata.main()
    df_regular_season_aggregated = build_season_data.main()
    df_regular_season_aggregated = groom_spellings(df_regular_season_aggregated)
    df = merge_season_team_metadata(df_team_metadata, df_regular_season_aggregated)
    a = IntermediateFileWriter('TeamData.csv')
    a.write_to_csv(df)
    
    return df

if __name__ == '__main__':
    df = main()
    
    print(df.head())

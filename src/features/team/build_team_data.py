#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 23:58:09 2019

@author: kluteytk
"""
import pandas as pd
from features.utils import feature_utils 
from features.team.team_modules import build_season_data  
from features.team.team_modules import build_season_ratings
from features.team.team_modules import parse_team_names 
from features.team.team_modules import build_seed_data 
from data import make_dataset


from util.IntermediateFilePersistence import IntermediateFilePersistence

def __merge_season_team_metadata(df_team_sp, df_regular_season_aggregated):
    df_team_sp['TeamNameSpelling'] = df_team_sp['TeamNameSpelling'].str.lower()
    df_regular_season_aggregated['School'] = df_regular_season_aggregated['School'].str.lower()
    
    __find_mismatched_schools(df_team_sp, df_regular_season_aggregated)

    df_regular_season_data = pd.merge(left=df_team_sp, right=df_regular_season_aggregated, how='inner', right_on='School', left_on='TeamNameSpelling').drop('TeamNameSpelling', axis=1)
    df_regular_season_data['TeamName'] = df_regular_season_data['School'].str.upper()
    df_regular_season_data = df_regular_season_data.drop('School', axis=1)
    
    df_regular_season_data['TeamSeasonId'] = feature_utils.create_key_from_fields(df_regular_season_data['TeamID'], df_regular_season_data['Year'])
    return df_regular_season_data

def __merge_reference_data(df_a, df_b):
    df_a = df_a.drop(['TeamID', 'SOS', 'SRS', 'Year', 'TeamName'], axis=1)

    df = pd.merge(left=df_a, right=df_b, how='inner', on='TeamSeasonId')
    return df

def __merge_seed_team_data(df_seeds, df_team):
    df = pd.merge(left=df_seeds, right=df_team, how='inner', on='TeamSeasonId').drop(labels=['Season'], axis=1)
    return df

def __find_mismatched_schools(df_team_sp, df_regular_season_aggregated):
    
    df_regular_season_data = pd.merge(left=df_team_sp, right=df_regular_season_aggregated, how='right', right_on='School', left_on='TeamNameSpelling').drop('TeamNameSpelling', axis=1)
    df_regular_season_data = df_regular_season_data[df_regular_season_data['TeamID'].isnull()]
    df_duplicate = df_regular_season_data['School']
    df_duplicate = df_duplicate.drop_duplicates(keep='first')
    print("Mismatched team names = " + str(df_duplicate.size))

def make():
    df_team_sp = make_dataset.load_spellings()
    df_regular_season_aggregated = build_season_data.main()
    df_ratings_aggregated = build_season_ratings.main()
    
    df_regular_season_aggregated = parse_team_names.groom_spellings(df_regular_season_aggregated)
    df_ratings_aggregated = parse_team_names.groom_spellings(df_ratings_aggregated)

    df_season = __merge_season_team_metadata(df_team_sp, df_regular_season_aggregated)
    df_ratings = __merge_season_team_metadata(df_team_sp, df_ratings_aggregated)
    
    df = __merge_reference_data(df_season, df_ratings)
    
    df = __merge_seed_team_data(df, build_seed_data.make())
    return df
    
def persist(df):
    fp = IntermediateFilePersistence('TeamData.csv')
    fp.write_to_csv(df)
    
if __name__ == '__main__':
    df = make()
    print(df.head())
    persist(df)

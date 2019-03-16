#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 23:58:09 2019

@author: kluteytk
"""
import pandas as pd
from features.utils import feature_utils 
from data import make_dataset


from util.IntermediateFilePersistence import IntermediateFilePersistence

def __merge_season_team_metadata(df_team_sp, df_regular_season_aggregated):
    df_team_sp['TeamNameSpelling'] = df_team_sp['TeamNameSpelling'].str.lower()
    df_regular_season_aggregated['School'] = df_regular_season_aggregated['School'].str.lower()
    
    __find_mismatched_schools(df_team_sp, df_regular_season_aggregated)

    df_regular_season_data = pd.merge(left=df_team_sp, right=df_regular_season_aggregated, how='inner', right_on='School', left_on='TeamNameSpelling').drop('TeamNameSpelling', axis=1)
    df_regular_season_data['TeamName'] = df_regular_season_data['School'].str.upper()
    df_regular_season_data = df_regular_season_data.drop('School', axis=1)
    
    df_regular_season_data['TeamSeasonId'] = feature_utils.create_key_from_season_team(df_regular_season_data['Year'], df_regular_season_data['TeamID'])
    return df_regular_season_data

def __merge_reference_data(df_a, df_b):
    df_a = df_a.drop(['TeamID', 'Year', 'TeamName'], axis=1)

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
    df_regular_season_aggregated = make_dataset.load_season_team_data();
    df_ratings_aggregated = make_dataset.load_ratings_team_data();
    df_advanced_aggregated = make_dataset.load_advanced_team_data();

    df_season = __merge_season_team_metadata(df_team_sp, df_regular_season_aggregated)
    df_ratings = __merge_season_team_metadata(df_team_sp, df_ratings_aggregated)
    df_advanced_aggregated = __merge_season_team_metadata(df_team_sp, df_advanced_aggregated)
    
    df = __merge_reference_data(df_season, df_ratings)
    df = __merge_reference_data(df_advanced_aggregated, df)
    
    df = __merge_seed_team_data(df, make_dataset.load_seed_data())
    df.drop(labels=['TeamID', 'Year'], inplace=True, axis=1)
    return df
    
def persist(df):
    fp = IntermediateFilePersistence('TeamData.csv')
    fp.write_to_csv(df)
    
if __name__ == '__main__':
    df = make()
    print(df.head())
    print(df.keys())
    persist(df)

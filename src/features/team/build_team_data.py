#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 23:58:09 2019

@author: kluteytk
"""
import sys
sys.path.append('/Users/kluteytk/development/projects/MarchMadness2019/src')
import pandas as pd
from features.utils import feature_utils 
from features.team.team_modules import build_season_data  
from features.team.team_modules import build_season_ratings
from features.team.team_modules import parse_team_names 
from data import make_dataset


from util.IntermediateFileWriter import IntermediateFileWriter

def merge_season_team_metadata(df_team_sp, df_regular_season_aggregated):
    df_team_sp['TeamNameSpelling'] = df_team_sp['TeamNameSpelling'].str.lower()
    df_regular_season_aggregated['School'] = df_regular_season_aggregated['School'].str.lower()
    
    find_mismatched_schools(df_team_sp, df_regular_season_aggregated)

    df_regular_season_data = pd.merge(left=df_team_sp, right=df_regular_season_aggregated, how='inner', right_on='School', left_on='TeamNameSpelling').drop('TeamNameSpelling', axis=1)
    df_regular_season_data['TeamName'] = df_regular_season_data['School'].str.upper()
    df_regular_season_data = df_regular_season_data.drop('School', axis=1)
    
    df_regular_season_data['TeamSeasonId'] = feature_utils.create_key_from_fields(df_regular_season_data['TeamID'], df_regular_season_data['Year'])
    return df_regular_season_data

def merge_reference_data(df_a, df_b):
    df_a = df_a.drop(['TeamID', 'SOS', 'SRS', 'Year', 'TeamName'], axis=1)

    df = pd.merge(left=df_a, right=df_b, how='inner', on='TeamSeasonId')
    return df


def find_mismatched_schools(df_team_sp, df_regular_season_aggregated):
    
    df_regular_season_data = pd.merge(left=df_team_sp, right=df_regular_season_aggregated, how='right', right_on='School', left_on='TeamNameSpelling').drop('TeamNameSpelling', axis=1)
    df_regular_season_data = df_regular_season_data[df_regular_season_data['TeamID'].isnull()]
    df_duplicate = df_regular_season_data['School']
    df_duplicate = df_duplicate.drop_duplicates(keep='first')
    print("Mismatched team names = " + str(df_duplicate.size))

def main():
    df_team_sp = make_dataset.load_spellings()
    df_regular_season_aggregated = build_season_data.main()
    df_ratings_aggregated = build_season_ratings.main()
    
    df_regular_season_aggregated = parse_team_names.groom_spellings(df_regular_season_aggregated)
    df_ratings_aggregated = parse_team_names.groom_spellings(df_ratings_aggregated)

    df_season = merge_season_team_metadata(df_team_sp, df_regular_season_aggregated)
    df_ratings = merge_season_team_metadata(df_team_sp, df_ratings_aggregated)
    
    df = merge_reference_data(df_season, df_ratings)
    
    a = IntermediateFileWriter('TeamData.csv')
    a.write_to_csv(df)
    
    return df

if __name__ == '__main__':
    df = main()
    
    print(df.head())
    print(df.shape)

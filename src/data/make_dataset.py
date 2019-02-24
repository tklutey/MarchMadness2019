# -*- coding: utf-8 -*-
import pandas as pd
from data.bball_reference import helper
from util.IntermediateFilePersistence import IntermediateFilePersistence
from features.utils import feature_utils

base_dir = '/Users/kluteytk/development/projects/MarchMadness2019/data/'
tourney_results_csv = base_dir + '/raw/NCAATourneyCompactResults.csv'
tourney_seeds_csv = base_dir + '/raw/NCAATourneySeeds.csv'
tourney_rounds_csv = base_dir + '/raw/NCAATourneySeedRoundSlots.csv'
spellings_csv = base_dir + '/raw/TeamSpellings.csv'

START_YEAR = 1993
END_YEAR = 2018


def load_season_team_data(start=START_YEAR, end=END_YEAR):
    bball_ref_dir = base_dir + '/external/bball_reference/'
    df_regular_season_aggregated = pd.DataFrame()
    for year in range(start, end + 1):
        regular_season_csv = bball_ref_dir + str(year) + '_season.csv'
        df_regular_season = pd.read_csv(regular_season_csv, header=1)
        df_regular_season['Year'] = year
        df_regular_season_aggregated = df_regular_season_aggregated.append(df_regular_season)

    df = helper.parse_single_season_team_data(df_regular_season_aggregated)
    fr = IntermediateFilePersistence('transformed/SeasonRawStats.csv')
    fr.write_to_csv(df)
    return df_regular_season_aggregated


def load_ratings_team_data(start=START_YEAR, end=END_YEAR):
    bball_ref_dir = base_dir + 'external/bball_reference/ratings/'
    df_regular_season_aggregated_ratings = pd.DataFrame()
    for year in range(start, end + 1):
        ratings_csv = bball_ref_dir + str(year) + 'SchoolRatings.csv'
        df_ratings = pd.read_csv(ratings_csv, header=1)
        df_ratings['Year'] = year
        df_regular_season_aggregated_ratings = df_regular_season_aggregated_ratings.append(df_ratings)

    df = helper.parse_ratings(df_regular_season_aggregated_ratings)
    df = df.dropna(1)
    fr = IntermediateFilePersistence('transformed/SeasonRatings.csv')
    fr.write_to_csv(df)
    return df


def load_tournament_game_results():
    return pd.read_csv(tourney_results_csv)

def load_seed_data():
    df = pd.read_csv(tourney_seeds_csv)
    df['TeamSeasonId'] = feature_utils.create_key_from_fields(df['TeamID'], df['Season'])
    df = df.drop('TeamID', axis=1)
    fr = IntermediateFilePersistence('transformed/SeedData.csv')
    fr.write_to_csv(df)
    return df

def load_spellings():
    return pd.read_csv(spellings_csv, encoding='iso8859_16')

if __name__ == '__main__':
    df = load_seed_data()
    print(df.head())
    print(df.keys())

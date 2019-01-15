# -*- coding: utf-8 -*-
import pandas as pd
import logging

base_dir = '/Users/kluteytk/development/projects/MarchMadness2019/data/'
tourney_results_csv = base_dir + '/raw/NCAATourneyCompactResults.csv'
tourney_seeds_csv = base_dir + '/raw/NCAATourneySeeds.csv'
tourney_rounds_csv = base_dir + '/raw/NCAATourneySeedRoundSlots.csv'
teams_csv = base_dir + '/raw/Teams.csv'
    
def load_season_team_data(start, end):
    bball_ref_dir = base_dir + '/external/bball_reference/'
    df_regular_season_aggregated = pd.DataFrame()
    for year in range(start, end + 1):
        regular_season_csv = bball_ref_dir + str(year) + '_season.csv'
        df_regular_season = pd.read_csv(regular_season_csv, header=1)
        df_regular_season['Year'] = year
        df_regular_season_aggregated = df_regular_season_aggregated.append(df_regular_season)        
        
    return df_regular_season_aggregated

def load_team_metadata():
    return pd.read_csv(teams_csv)

def load_tournament_game_results():
    return pd.read_csv(tourney_results_csv)

def load_round_data():
    return pd.read_csv(tourney_rounds_csv)

def load_seed_data():
    return pd.read_csv(tourney_seeds_csv)


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    main()
    df = load_season_team_data(2000, 2002)
    print(df.head())



import pandas as pd
from features.team import build_team_data
from features.game import build_game_data
from util.IntermediateFilePersistence import IntermediateFilePersistence
from features.utils import feature_utils

def __merge_game_with_team_data(df_game_results, df_regular_season_data):
    
    df_team_a = pd.merge(left=df_game_results, right=df_regular_season_data, how='inner', left_on=['TeamA_ID'], right_on=['TeamSeasonId'])
    df_team_a.drop(labels=['TeamSeasonId', 'Year', 'Season'], inplace=True, axis=1)

    df_team_b = pd.merge(left=df_game_results, right=df_regular_season_data, how='inner', left_on=['TeamB_ID'], right_on=['TeamSeasonId'])
    df_team_b.drop(labels=['TeamSeasonId', 'Year', 'ScoreDiff', 'TeamA_ID', 'TeamB_ID'], inplace=True, axis=1)
    
    df_dataset = pd.merge(left=df_team_a, right=df_team_b, how='inner', on='GameID')

    return df_dataset


def make():
    build_team_data.make()
    team_fp = IntermediateFilePersistence('TeamData.csv')
    df_team = team_fp.read_from_csv()
    df = __merge_game_with_team_data(build_game_data.main(), df_team)
    df['Round'] = df.apply(feature_utils.__get_round, axis=1)
    return df
    
def persist(df):
    fr = IntermediateFilePersistence('CanonicalFeatureData.csv')
    fr.write_to_csv(df)
    
if __name__ == '__main__':
    df = make()
    print(df.head())
    persist(df)
import pandas as pd
from features.team import build_team_data
from features.game import build_game_data
from util.IntermediateFilePersistence import IntermediateFilePersistence
from features.utils import feature_utils

drop_duplicates = ['TeamSeasonId', 'TeamA_ID', 'TeamB_ID', 'Season']

def __merge_game_with_team_data(df_game_results, df_regular_season_data):
    df_team_a = pd.merge(left=df_game_results, right=df_regular_season_data, how='inner', left_on=['TeamA_ID'], right_on=['TeamSeasonId']).drop('TeamSeasonId', axis=1)

    df_team_b = pd.merge(left=df_game_results, right=df_regular_season_data, how='inner', left_on=['TeamB_ID'], right_on=['TeamSeasonId'])
    df_team_b.drop(labels=drop_duplicates, inplace=True, axis=1)

    df_dataset = pd.merge(left=df_team_a, right=df_team_b, how='inner', on='GameID')

    return df_dataset


def make(game_data=None):
    build_team_data.persist(build_team_data.make())
    team_fp = IntermediateFilePersistence('TeamData.csv')
    df_team = team_fp.read_from_csv()
    if game_data is None:
        game_data = build_game_data.create_labeled_game_data()
        df = __merge_game_with_team_data(game_data, df_team)
        df.drop(labels=['ScoreDiff_y'], inplace=True, axis=1)
        df = df.rename(columns={"ScoreDiff_x": "ScoreDiff", "LTeamID": "TeamB_ID"})
    else:
        df = __merge_game_with_team_data(game_data, df_team)
    df['Round'] = df.apply(feature_utils.__get_round, axis=1)
    return df
    
def persist(df):
    fr = IntermediateFilePersistence('CanonicalFeatureData.csv')
    fr.write_to_csv(df)
    
if __name__ == '__main__':
    df = make()
    persist(df)
import pandas as pd

import sys
sys.path.append('/Users/kluteytk/development/projects/march_madness/MarchMadness2019/src/')

from features.team import build_team_data
from features.game import build_game_data
from features.normalize import normalize_features
from util.IntermediateFileWriter import IntermediateFileWriter

def merge_game_with_team_data(df_game_results, df_regular_season_data):

    df_team_a = pd.merge(left=df_game_results, right=df_regular_season_data, how='inner', left_on=['TeamA_ID'], right_on=['TeamSeasonId'])
    df_team_a.drop(labels=['TeamSeasonId', 'Year'], inplace=True, axis=1)


    df_team_b = pd.merge(left=df_game_results, right=df_regular_season_data, how='inner', left_on=['TeamB_ID'], right_on=['TeamSeasonId'])
    df_team_b.drop(labels=['TeamSeasonId', 'Year', 'Season', 'ScoreDiff', 'TeamA_ID', 'TeamB_ID'], inplace=True, axis=1)
    
    df_dataset = pd.merge(left=df_team_a, right=df_team_b, how='inner', on='GameID')
    
    return df_dataset

def groom_normalize(df):
    df = normalize_features.groom(df)
    df = normalize_features.normalize(df)
    return df

def split_training_data(df_dataset):
    train_dataset = df_dataset.sample(frac=0.8,random_state=0)
    test_dataset = df_dataset.drop(train_dataset.index)
    
    train_labels = train_dataset.pop('ScoreDiff')
    test_labels = test_dataset.pop('ScoreDiff')
    
    return (train_dataset, train_labels), (test_dataset, test_labels)
    
    
def create_dataset():
    df = merge_game_with_team_data(build_game_data.main(), build_team_data.main())
    fr = IntermediateFileWriter('CanonicalFeatureData.csv')
    fr.write_to_csv(df)
    df = groom_normalize(df)
    return split_training_data(df)

if __name__ == '__main__':
#    print(create_dataset())
    create_dataset()
# -*- coding: utf-8 -*-

import pandas as pd
from data import make_dataset
from features.utils import feature_utils

def create_mirrored_results(df_game_results, column_name_a='', column_name_b=''):
    # Create mirror of score
    df_mirror = pd.DataFrame()
    for col, series in df_game_results.iteritems():
        if col == 'ScoreDiff':
            df_mirror[col] = -series
        else:
            df_mirror[col] = series
        df_mirror[column_name_a] = df_game_results[column_name_b]
        df_mirror[column_name_b] = df_game_results[column_name_a]
    return df_mirror


def create_labels():
    df_game_results = make_dataset.load_tournament_game_results()
    df_game_results['GameID'] = feature_utils.create_game_key(df_game_results['Season'], df_game_results['WTeamID'], df_game_results['LTeamID'])
    df_game_results['ScoreDiff'] = df_game_results.WScore - df_game_results.LScore
    df_game_results.drop(labels=['DayNum', 'WScore', 'LScore', 'WLoc',
                                 'NumOT', 'WTeamID', 'LTeamID', 'Season'], inplace=True, axis=1)
    return df_game_results


def create_features():
    df_game_results = make_dataset.load_tournament_game_results();

    df_game_results['GameID'] = feature_utils.create_game_key(df_game_results['Season'], df_game_results['WTeamID'], df_game_results['LTeamID'])
    df_game_results['WTeamID'] = feature_utils.create_key_from_season_team(df_game_results['Season'], df_game_results['WTeamID'])
    df_game_results['LTeamID'] = feature_utils.create_key_from_season_team(df_game_results['Season'], df_game_results['LTeamID'])

    df_game_results.drop(labels=['DayNum', 'WScore', 'LScore', 'WLoc',
                                 'NumOT'], inplace=True, axis=1)

    return df_game_results


def create_labeled_game_data():
    df = pd.merge(left=create_labels(), right=create_features(), on='GameID')
    df_mirror = create_mirrored_results(df, 'WTeamID', 'LTeamID')
    df['GameID'] = df['GameID'] + '_a'
    df_mirror['GameID'] = df_mirror['GameID'] + '_b'
    df = df.append(df_mirror, sort=False)
    df = df.rename(columns={"WTeamID": "TeamA_ID", "LTeamID": "TeamB_ID"})
    return df

    
if __name__ == '__main__':
    print(create_labels())
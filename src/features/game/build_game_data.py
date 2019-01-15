# -*- coding: utf-8 -*-

import pandas as pd
from data import make_dataset
from features.utils import feature_utils

def mirror_results(df_game_results):
    # Create mirror of score
    df_mirror = pd.DataFrame()
    for col, series in df_game_results.iteritems():
        if col == 'ScoreDiff':
            df_mirror[col] = -series
        else:
            df_mirror[col] = series
        df_mirror['TeamA_ID'] = df_game_results['TeamB_ID']
        df_mirror['TeamB_ID'] = df_game_results['TeamA_ID']

    
    return df_mirror

def main():
    df_game_results = make_dataset.load_tournament_game_results();
    df_game_results.drop(labels=['WLoc', 'NumOT'], inplace=True, axis=1)
    df_game_results['GameID'] = feature_utils.create_key_from_fields(df_game_results['Season'], df_game_results['WTeamID'], df_game_results['LTeamID'])
    df_game_results['TeamA_ID'] = feature_utils.create_key_from_fields(df_game_results['WTeamID'], df_game_results['Season'])
    df_game_results['TeamB_ID'] = feature_utils.create_key_from_fields(df_game_results['LTeamID'], df_game_results['Season'])
    df_game_results.drop(labels=['WTeamID', 'LTeamID'], inplace=True, axis=1)
    
    # Create difference in score
    df_game_results['ScoreDiff'] = df_game_results.WScore - df_game_results.LScore
    df_game_results.drop(labels=['WScore', 'LScore'], inplace=True, axis=1)
    
    df_mirror = mirror_results(df_game_results)
    df_game_results['GameID'] = df_game_results['GameID'] + '_a'
    df_mirror['GameID'] = df_mirror['GameID'] + '_b'
    
    df_game_results = df_game_results.append(df_mirror, sort=False)
    
    return df_game_results

    
if __name__ == '__main__':
    import sys
    sys.path.append('/Users/kluteytk/development/projects/march_madness/MarchMadness2019/src/')
    print(main().head())
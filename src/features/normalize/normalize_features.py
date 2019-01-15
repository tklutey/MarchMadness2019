# -*- coding: utf-8 -*-

def groom(df_dataset):
    df_dataset.drop(labels=['DayNum_x', 'DayNum_y', 'TeamA_ID', 'TeamB_ID', 'GameID', 'TeamName_x', 'TeamName_y'], inplace=True, axis=1)
    return df_dataset

def norm(x, train_stats):
    df_label = x.pop('ScoreDiff')
    x = (x - train_stats['mean']) / train_stats['std']
    x['ScoreDiff'] = df_label
    return x
    

def normalize(df_dataset):
    df_stats = df_dataset.describe()
    df_stats = df_stats.transpose()
    df_dataset = norm(df_dataset, df_stats)
    return df_dataset
# -*- coding: utf-8 -*-
import pandas as pd

def groom(df_dataset):
    
    # Drop non-numerical
    df_dataset.drop(labels=['DayNum_x', 'DayNum_y', 'TeamA_ID', 'TeamB_ID', 'GameID', 'TeamName_x', 'TeamName_y', 'TeamID_x', 'TeamID_y'], inplace=True, axis=1)
    
    # Drop experimental
#    df_dataset.drop(labels=['G_x', 'W_x', 'L_x', 'G_y', 'W_y', 'L_y'], inplace=True, axis=1)

    return df_dataset

def norm(x, train_stats):
    df_label = x.pop('ScoreDiff')
    x = (x - train_stats['mean']) / train_stats['std']
    x['ScoreDiff'] = df_label
    return x
    

def normalize(df_dataset):
    
    # Normalize grouping by each season
    df_normed_dataset = pd.DataFrame()
    for i in range(df_dataset['Season'].min(), df_dataset['Season'].max()):
        df = df_dataset.loc[df_dataset['Season'] == i]
        df_stats = df.describe()
        df_stats = df_stats.transpose()
        df = norm(df, df_stats)
        df_normed_dataset = df_normed_dataset.append(df)
        
    df_normed_dataset.drop(labels=['Season'], inplace=True, axis=1)
    return df_normed_dataset

    

# -*- coding: utf-8 -*-
import pandas as pd
from util.IntermediateFileWriter import IntermediateFileWriter


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
    
    df_conf_x = df_dataset.pop('Conf_x')
    df_conf_y = df_dataset.pop('Conf_y')

    dummies_x = pd.get_dummies(df_conf_x)
    dummies_x = dummies_x.add_suffix('_x')
    dummies_y = pd.get_dummies(df_conf_y)   
    dummies_y = dummies_y.add_suffix('_y')


    
    # Normalize grouping by each season
    df_normed_dataset = pd.DataFrame()
    for i in range(df_dataset['Season'].min(), df_dataset['Season'].max() + 1):
        df = df_dataset.loc[df_dataset['Season'] == i]
        df_stats = df.describe()
        df_stats = df_stats.transpose()
        df = norm(df, df_stats)
        df_normed_dataset = df_normed_dataset.append(df)
        
    df_normed_dataset.drop(labels=['Season'], inplace=True, axis=1)
    df_normed_dataset = pd.concat([df_normed_dataset, dummies_x], axis=1)
    df_normed_dataset = pd.concat([df_normed_dataset, dummies_y], axis=1)
    
    fr = IntermediateFileWriter('NormalizedFeatureData.csv')
    fr.write_to_csv(df_normed_dataset)

    return df_normed_dataset

    

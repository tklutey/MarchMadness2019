# -*- coding: utf-8 -*-
import pandas as pd
from util.IntermediateFilePersistence import IntermediateFilePersistence


def __parse_seed(df, orig_label, dest_label):
    df_seeds = df.copy()
    df_seeds[orig_label] = df_seeds[orig_label].str[1:3]
    df_seeds[dest_label] = df_seeds[orig_label].apply(pd.to_numeric)
    df_seeds.drop(labels=[orig_label], inplace=True, axis=1)
    return df_seeds

def __groom(df_dataset):
    groomed_features = ['Season', 'G_x', 'W_x',
                    'L_x', 'W-L%_x', 'Points for_x', 'FG_x', 'FGA_x', 'FG%_x', '3P_x',
                    '3PA_x', '3P%_x', 'FT_x', 'FTA_x', 'FT%_x', 'AST_x', 'STL_x', 'BLK_x',
                    'Rk_x', 'Conf_x', 'Pts_x', 'SOS_x', 'OSRS_x', 'DSRS_x', 'SRS_x',
                    'Seed_x', 'G_y', 'W_y', 'L_y', 'W-L%_y',
                    'Points for_y', 'FG_y', 'FGA_y', 'FG%_y', '3P_y', '3PA_y', '3P%_y',
                    'FT_y', 'FTA_y', 'FT%_y', 'AST_y', 'STL_y', 'BLK_y', 'Rk_y', 'Conf_y',
                    'Pts_y', 'SOS_y', 'OSRS_y', 'DSRS_y', 'SRS_y', 'Seed_y',
                    'Round']

    if 'ScoreDiff' in df_dataset.keys():
        groomed_features.append('ScoreDiff')
        print("Normalizing with labeled data...")
    else:
        print("Normalizing without labeled data...")
    
    df_dataset = df_dataset[groomed_features]
    df_dataset = __parse_seed(df_dataset, 'Seed_x', 'Seed_int_x')
    df_dataset = __parse_seed(df_dataset, 'Seed_y', 'Seed_int_y')

    return df_dataset


def __norm(x, train_stats):
    x = (x - train_stats['mean']) / train_stats['std']
    return x


def __standardize(df_dataset):
    # Normalize grouping by each season
    df_normed_dataset = pd.DataFrame()
    df_label = None
    if 'ScoreDiff' in df_dataset.keys():
        df_label = df_dataset.pop('ScoreDiff')
    for i in range(df_dataset['Season'].min(), df_dataset['Season'].max() + 1):
        df = df_dataset.loc[df_dataset['Season'] == i]
        df_stats = df.describe()
        df_stats = df_stats.transpose()
        df = __norm(df, df_stats)
        df_normed_dataset = df_normed_dataset.append(df)
    if df_label is not None:
        df_normed_dataset['ScoreDiff'] = df_label

    return df_normed_dataset


def __normalize(df_dataset):
    df_conf_x = df_dataset.pop('Conf_x')
    df_conf_y = df_dataset.pop('Conf_y')

    dummies_x = pd.get_dummies(df_conf_x)
    dummies_x = dummies_x.add_suffix('_x')
    dummies_y = pd.get_dummies(df_conf_y)
    dummies_y = dummies_y.add_suffix('_y')

    df_normed_dataset = __standardize(df_dataset)

    df_normed_dataset.drop(labels=['Season'], inplace=True, axis=1)
    df_normed_dataset = pd.concat([df_normed_dataset, dummies_x], axis=1)
    df_normed_dataset = pd.concat([df_normed_dataset, dummies_y], axis=1)

    return df_normed_dataset


def make(df=None):
    if df is None:
        fp = IntermediateFilePersistence('CanonicalFeatureData.csv')
        df = fp.read_from_csv()
    df = __groom(df)
    df = __normalize(df)
    return df


def persist(df):
    fr = IntermediateFilePersistence('NormalizedFeatureData.csv')
    fr.write_to_csv(df)


if __name__ == '__main__':
    df = make()
    print(df.head())
    persist(df)

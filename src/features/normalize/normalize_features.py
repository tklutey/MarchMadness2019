# -*- coding: utf-8 -*-
import pandas as pd
from util.IntermediateFilePersistence import IntermediateFilePersistence


def __parse_seed(df, orig_label, dest_label):
    df_seeds = df.copy()
    df_seeds[orig_label] = df_seeds[orig_label].str[1:3]
    df_seeds[dest_label] = df_seeds[orig_label].apply(pd.to_numeric)
    df_seeds.drop(labels=[orig_label], inplace=True, axis=1)
    return df_seeds

def __groomed_team_features():
    groomed_features = ['G', 'W',
                        'L', 'W-L%', 'Points for', 'Points against', 'FG', 'FGA', 'FG%', '3P',
                        '3PA', '3P%', 'FT', 'FTA', 'FT%', 'AST', 'STL', 'BLK',
                        'Rk', 'Conf', 'Pts', 'SOS', 'OSRS', 'DSRS', 'SRS',
                        'Seed', 'FTr', '3PAr', 'TS%', 'AST%', 'eFG%', 'TRB%', 'TOV%']

    x_list = []
    y_list = []
    for feature in groomed_features:
        x_list.append(feature + '_x')
        y_list.append(feature + '_y')

    return x_list + y_list

def __groom(df_dataset):
    game_features = ['Season', 'Round']

    groomed_features = __groomed_team_features()
    for feature in game_features:
        groomed_features.append(feature)

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

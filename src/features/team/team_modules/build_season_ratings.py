# -*- coding: utf-8 -*-
from data import make_dataset

def parse_columns(dataframe):
    dataframe.drop(labels=['Unnamed: 3', 'W', 'L', 'Unnamed: 9', 'Unnamed: 11'], inplace=True, axis=1)
    dataframe.drop(labels=['Conf'], inplace=True, axis=1)


    return dataframe

def main():
    df = make_dataset.load_ratings_team_data(1993, 2018)
    df = parse_columns(df)
    df = df.dropna(0, subset=['MOV'])
    df = df.dropna(1)

    return df

if __name__ == '__main__':
    df = main()
    print(df.keys())

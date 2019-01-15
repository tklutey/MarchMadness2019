#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 00:18:12 2019

@author: kluteytk
"""
from data import make_dataset

def parse_single_season_team_data(dataframe):
    dataframe.rename(
        index=str,
        columns={
            'W.1': 'Conf. wins', 'L.1': 'Conf. losses',
            'W.2': 'Home wins', 'L.2': 'Home losses',
            'W.3': 'Away wins', 'L.3': 'Away losses',
            'Tm.': 'Points for', 'Opp.': 'Points against'
        },
        inplace=True
    )
    # Drop columns that have known null values for multiple rows
    dataframe.drop(labels=['Conf. wins', 'Conf. losses', 'MP', 'ORB', 'Rk', 'Unnamed: 16',
                           
                          'Home wins', 'Home losses', 'Away wins', 'Away losses',
                           'Points against', 'TRB', 'TOV', 'PF'
                           
                          ], inplace=True, axis=1)
    
    # Experiment w/ columns to drop
#     dataframe.drop(labels=['G', 'W', 'L', 'Points for', 'FG', 'FGA', '3P', '3PA', 'FT', 'FTA'], inplace=True, axis=1)

    return dataframe

def main():
    df = make_dataset.load_season_team_data(1993, 2017)
    df = parse_single_season_team_data(df)
    return df

if __name__ == '__main__':
    print(main())
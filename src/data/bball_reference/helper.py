from util import parse_team_names


def parse_single_season_team_data(dataframe):
    dataframe.rename(index=str,
                     columns={
                         'W.1': 'Conf. wins', 'L.1': 'Conf. losses',
                         'W.2': 'Home wins', 'L.2': 'Home losses',
                         'W.3': 'Away wins', 'L.3': 'Away losses',
                         'Tm.': 'Points for', 'Opp.': 'Points against'
                     }, inplace=True)
    # Drop columns that have known null values for multiple rows
    dataframe.drop(
        labels=['Conf. wins', 'Conf. losses', 'MP', 'ORB', 'Rk', 'Unnamed: 16', 'Home wins', 'Home losses', 'Away wins',
                'Away losses', 'TRB', 'TOV', 'PF', 'SOS', 'SRS'], inplace=True, axis=1)

    dataframe = parse_team_names.groom_spellings(dataframe)

    return dataframe


def parse_ratings(dataframe):
    dataframe.drop(labels=['Unnamed: 3', 'W', 'L', 'Unnamed: 9', 'Unnamed: 11'], inplace=True, axis=1)
    dataframe = parse_team_names.groom_spellings(dataframe)

    return dataframe

def parse_advanced(dataframe):
    groomed_features = ['Year', 'School', 'FTr', '3PAr', 'TS%',
       'AST%', 'eFG%', 'TRB%', 'TOV%']
    dataframe = parse_team_names.groom_spellings(dataframe)
    df = dataframe[groomed_features]
    return df


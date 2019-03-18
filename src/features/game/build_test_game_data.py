from data import make_dataset
from features.utils import feature_utils
from util.IntermediateFilePersistence import IntermediateFilePersistence


def make():
    fr = IntermediateFilePersistence('transformed/2019GeneratedMatchups.csv')

    print("Generating test matchups...")
    df_test = make_dataset.load_test_data()

    df_a = df_test
    df_b = df_test.drop('Season', axis=1)

    df = df_a.assign(key=1).merge(df_b.assign(key=1), on='key').drop('key', 1)
    df = df[df['TeamID_x'] != df['TeamID_y']]

    df['GameID'] = feature_utils.create_game_key(df['Season'], df['TeamID_x'], df['TeamID_y'])
    df['TeamA_ID'] = feature_utils.create_key_from_season_team(df['Season'], df['TeamID_x'])
    df['TeamB_ID'] = feature_utils.create_key_from_season_team(df['Season'], df['TeamID_y'])

    df.drop(labels=['TeamID_x', 'TeamID_y'], inplace=True, axis=1)

    print("Writing test values to disk...")

    fr.write_to_csv(df)

    return df


if __name__ == '__main__':
    make()

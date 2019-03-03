def add_dummies(df_less, df_more):
    x = df_less.keys()
    y = df_more.keys()
    z = y.difference(x)
    for col in z:
        df_less[col] = 0
    return df_less
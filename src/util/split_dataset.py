# -*- coding: utf-8 -*-


def split_training_data_randomly_with_seed(df_dataset, seed=0):
    train_dataset = df_dataset.sample(frac=0.8,random_state=seed)
    test_dataset = df_dataset.drop(train_dataset.index)
    
    return pop_label(train_dataset), pop_label(test_dataset)


def pop_label(df, label='ScoreDiff'):
    label = df.pop(label)
    return df, label

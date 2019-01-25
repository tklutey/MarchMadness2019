# -*- coding: utf-8 -*-

def split_training_data(df_dataset):
    train_dataset = df_dataset.sample(frac=0.8,random_state=0)
    test_dataset = df_dataset.drop(train_dataset.index)
    
    train_labels = train_dataset.pop('ScoreDiff')
    test_labels = test_dataset.pop('ScoreDiff')
    
    return (train_dataset, train_labels), (test_dataset, test_labels)

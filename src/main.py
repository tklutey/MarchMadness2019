#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 17:24:10 2019

@author: kluteytk
"""

# -*- coding: utf-8 -*-
from features import build_features
from features.game import build_test_game_data
from models.build_output import build_historical_output, build_test_output
from util import split_dataset
from features.normalize import normalize_features
from models import predict_model
from models import train_model
from util.ProcessedFilePersistence import ProcessedFilePersistence
from util.build_bracket_output import build_bracket_output

from util.conference_utils import add_dummies


def full_workflow(historical=True):
    # Create dataset
    df_canonical = build_features.make()
    build_features.persist(df_canonical)

    # Normalize dataset
    df_normalized = normalize_features.make()
    normalize_features.persist(df_normalized)

    if historical is True:
        (train_dataset, train_labels), (test_dataset, test_labels) = split_dataset.split_training_data_randomly_with_seed(df_normalized)

        # Train model
        model = train_model.make("dev")
        train_model.persist(model)

        # Create predictions
        predictions = predict_model.predict()
        # Evaluate predictions
        predict_model.evaluate_predictions(predictions, test_labels)

    else:
        train_dataset, train_labels = split_dataset.pop_label(df_normalized)

        test_dataset = build_features.make(build_test_game_data.make())

        normalized_test_dataset = normalize_features.make(test_dataset)
        normalized_test_dataset = add_dummies(normalized_test_dataset, train_dataset)

        # Train model
        model = train_model.make("test", train_dataset, train_labels)
        train_model.persist(model)

        # Create predictions                  
        predictions = predict_model.predict(normalized_test_dataset)
        df_predictions = build_test_output(test_dataset, predictions)
        fr = ProcessedFilePersistence('2019Predictions.csv')
        fr.write_to_csv(df_predictions)
        build_bracket_output()

if __name__ == '__main__':    
    full_workflow(False)

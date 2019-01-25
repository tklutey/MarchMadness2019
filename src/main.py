#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 17:24:10 2019

@author: kluteytk
"""

# -*- coding: utf-8 -*-
from features import build_features
from util import split_dataset
from features.normalize import normalize_features
from models import predict_model
from models import train_model
      
def full_workflow():
    # Create dataset
    df_canonical = build_features.make()
    build_features.persist(df_canonical)
    
    # Normalize dataset
    df_normalized = normalize_features.make()
    normalize_features.persist(df_normalized)
    
    (train_dataset, train_labels), (test_dataset, test_labels) = split_dataset.split_training_data(df_normalized)
    
    # Train model
    model = train_model.make()
    train_model.persist(model)
    
    # Create predictions
    predictions = predict_model.predict()
    # Evaluate predictions
    predict_model.evaluate_predictions(predictions, test_labels)
    
if __name__ == '__main__':    
    full_workflow()
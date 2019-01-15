#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 17:24:10 2019

@author: kluteytk
"""

# -*- coding: utf-8 -*-
from features import build_features
from models import predict_model
from models import train_model

def main():
    # Create dataset
    (train_dataset, train_labels), (test_dataset, test_labels) = build_features.create_dataset()
    
    # Train model
    model = train_model.create_train_model()
    
    # Create predictions
    predictions = predict_model.predict(model, test_dataset)
    
    # Evaluate predictions
    predict_model.evaluate_predictions(predictions, test_labels)
    
if __name__ == '__main__':    
    main()
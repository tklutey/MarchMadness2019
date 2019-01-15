#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 00:18:55 2019

@author: kluteytk

@TODO: Migrate this over to not using converted names
"""

from data import make_dataset

def main():
    df = make_dataset.load_team_metadata()
    df.drop(labels=['FirstD1Season', 'LastD1Season'], inplace=True, axis=1)
    return df


    
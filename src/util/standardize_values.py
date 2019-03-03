# -*- coding: utf-8 -*-

def standardize_values(series, new_max = 1, new_min = 0):
    return (series - series.min()) / (series.max() - series.min()) * (new_max - new_min) + new_min

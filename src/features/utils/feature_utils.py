# -*- coding: utf-8 -*-

def create_key_from_fields(*a):
    first = True
    key = ''
    for i in a:
        if first is True:
            key = i.astype(str)
            first = False
        else:
            key = key + '_' + i.astype(str)
    return key
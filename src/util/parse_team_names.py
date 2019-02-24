# -*- coding: utf-8 -*-
import re

def groom_spellings(df):
    for col, series in df.iteritems():
        if col == 'School':
            for i in series:
                if ' NCAA' in i:
                    x = re.sub(' NCAA', '', i)
                    series.replace(i, x, inplace=True)

    return df
# -*- coding: utf-8 -*-

from util.BaseFilePersistence import BaseFilePersistence


class ProcessedFilePersistence(BaseFilePersistence):

    def __init__(self, filename):
        filepath = '/Users/kluteytk/development/projects/MarchMadness2019/data/processed/' + filename
        BaseFilePersistence.__init__(self, filepath);


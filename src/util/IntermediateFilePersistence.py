# -*- coding: utf-8 -*-

from util.BaseFilePersistence import BaseFilePersistence

class IntermediateFilePersistence(BaseFilePersistence):
        
    def __init__(self, filename):
        filepath = '/Users/kluteytk/development/projects/MarchMadness2019/data/interim/' + filename
        BaseFilePersistence.__init__(self, filepath);
        
    
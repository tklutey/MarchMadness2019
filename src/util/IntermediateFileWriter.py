# -*- coding: utf-8 -*-

from util.BaseFileWriter import BaseFileWriter

class IntermediateFileWriter(BaseFileWriter):
        
    def __init__(self, filename):
        filepath = '/Users/kluteytk/development/projects/march_madness/MarchMadness2019/data/interim/' + filename
        BaseFileWriter.__init__(self, filepath);
        
    
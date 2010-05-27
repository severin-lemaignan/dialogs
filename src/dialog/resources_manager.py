# -*- coding: utf-8 -*-

import os.path

#This value is overridden in dialog.py. Only useful to test parser.py alone.
DATA_DIR = 'share/dialog'

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
 
@singleton
class ResourcePool:
    
    def __init__(self, data_path = DATA_DIR):
        
        self.adjectives = []
        self.irregular_verbs = []
        self.preposition_verbs = []
        self.sentence_starts = []
        
        #lecture de la liste des adjectifs
        for line in open (os.path.join(data_path, "adjectives")):
            for word in line.split():
                self.adjectives += [word]
        
        self.irregular_verbs = [tuple(line.split()) 
                                for line 
                                in open (os.path.join(data_path, "irregular_verbs"))]
        
        self.preposition_verbs = [tuple(line.split()) 
                                for line 
                                in open (os.path.join(data_path, "preposition_verbs"))]
                                
        # lire les mots avec lesquels on peut commencer une phrase
        self.sentence_starts = [tuple(line.split()) 
                                for line 
                                in open (os.path.join(data_path, "sentence_starts"))]        


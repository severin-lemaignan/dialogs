#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path

from dialog_exceptions import UnknownVerb

#This value is overridden in dialog.py. Only useful to test parser.py alone.
DATA_DIR = 'share/dialog'

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class ThematicRole:
    def __init__(self, desc):        
        if desc.startswith('['): #optional role
            self.optional = True
            desc = desc[1:-1] #remove square brackets
        else:
            self.optional = False
        
        tokens = desc.strip().split()
        self.id = tokens[0]
        
        if tokens[1].startswith('['): #preposition
            self.preposition = tokens[1][1:-1]
            self.actors_classes = tokens[2].split(',')
        else:
            self.preposition = None
            self.actors_classes = tokens[1].split(',')
    
    def __str__(self):
        res = " (optional)" if self.optional else ""
        res += " " + self.id
        if self.preposition:
            res += " (introduced by \"" + self.preposition + "\")"
        res += " that expects " + str(self.actors_classes)
        return res

class VerbEntry:
    def __init__(self, name, ref, roles):        
        self.name = name
        self.ref = ref
        self.subject = roles[0]
        self.roles = roles[1:]
        
        self._role_pointer = 0
    
    def next_role(self):
        self._role_pointer += 1
        try:
            role = self.roles[self._role_pointer - 1]
            
            if role.preposition: #if next role is supposed to be introduced by a preposition, skip it
                return self.next_role()
            else:
                return role
            
        except IndexError:
            return None
    
    def get_role_for_preposition(self, prep):
        
        for role in self.roles:
            if role.preposition == prep:
                self.roles.remove(role)
                return role
        return None
            
    def __str__(self):
        res = "verb \"" + self.name + "\""
        
        if self.ref != self.name:
            res += " (syn. of " + self.ref + ")"
            
        res += " that has roles:\n"
        for role in self.roles:
            res += str(role) + "\n"
        return res

@singleton
class ThematicRolesDict:
    """This class contains all the verbs with their associated thematic roles
    as listed in the data/dialog/thematic_roles file. Refer to this file for 
    details regarding syntax.
    """
    def __init__(self):
        self.verbs = {}
    
    def add_verb(self, desc):
        lines = desc.split("\n")
        verb_desc = lines[0].strip().split()
        
        roles = [ThematicRole(desc) for desc in lines[1:-2]] #lines[0] is verb desc, line[n] is '}'
        
        verbs = [VerbEntry(verb_desc[0],verb_desc[0], roles)]
        if verb_desc[1].startswith('('): #synonyms
            for syn in verb_desc[1][1:-1].split(','):
                verbs.append(VerbEntry(syn,verb_desc[0], roles))
        
        for verb in verbs:
            self.verbs[verb.name] = verb
            
    def get_subject_role(self, verb, with_spaces = False):
        try:
            res = self.verbs[verb.lower()].subject.id
        except KeyError:
            raise UnknownVerb('Verb ' + verb + ' has no thematic role defined')
        return (" " + res + " ") if with_spaces else res
        
    def get_next_cmplt_role(self, verb, with_spaces = False):
        try:
            res = self.verbs[verb.lower()].next_role().id
        except KeyError:
            raise UnknownVerb('Verb ' + verb + ' has no thematic role defined')
        return (" " + res + " ") if with_spaces else res
    
    def get_cmplt_role_for_preposition(self, verb, preposition, with_spaces = False):
        try:
            res = self.verbs[verb.lower()].get_role_for_preposition(preposition).id
        except KeyError:
            raise UnknownVerb('Verb ' + verb + ' has no thematic role defined')
        return (" " + res + " ") if with_spaces else res
    
        
    def __str__(self):
        res = ""
        for name, verb in self.verbs.items():
            res += str(verb) + "\n"
        return res
    
@singleton
class ResourcePool:
    
    def __init__(self, data_path = DATA_DIR):
        
        self.adjectives = {}
        self.irregular_verbs = []
        self.preposition_verbs = []

        """list of tokens that can start a sentence"""
        self.sentence_starts = []
        
        """
        list of verbs that express a goal - ie, that would translate to a
        [S desires O] statement.
        """
        self.goal_verbs = []
        
        """
        dictionnary of all verbs for which thematic roles are known.
        """
        self.thematic_roles = ThematicRolesDict()
        
        for line in open (os.path.join(data_path, "adjectives")):
            if line.startswith("#") or not line.strip():
                continue
            try:
                adj, cat = line.split()
            except ValueError: #for adjectives without category, set a generic "Feature" category
                adj = line.split()[0]
                cat = "Feature"
            self.adjectives[adj] = cat
        
        self.irregular_verbs = [tuple(line.split()) 
                                for line 
                                in open (os.path.join(data_path, "irregular_verbs"))]
        
        self.preposition_verbs = [tuple(line.split()) 
                                for line 
                                in open (os.path.join(data_path, "preposition_verbs"))]
                                
        self.sentence_starts = [tuple(line.split()) 
                                for line 
                                in open (os.path.join(data_path, "sentence_starts"))]        
        
        self.goal_verbs = [line.strip()
                            for line 
                            in open (os.path.join(data_path, "goal_verbs"))]
        
        
        desc = ""
        for line in open (os.path.join(data_path, "thematic_roles")):
            if line.startswith("#") or not line.strip():
                continue
            
            desc += line
            
            if line.startswith("}"): #end of block
                self.thematic_roles.add_verb(desc)
                desc = ""


if __name__ == '__main__':
    
    resources = ResourcePool()
    
    print("*** DIALOG Resource manager ***")
    print
    print("List of loaded resources:")
    
    print
    print("Adjectives:")
    print(str(resources.adjectives))
    
    print
    print("Irregular verbs:")
    print(str(resources.irregular_verbs))
    
    print
    print("Preposition verbs:")
    print(str(resources.preposition_verbs))
    
    print
    print("Sentence starts:")
    print(str(resources.sentence_starts))
    
    print
    print("Goal verbs:")
    print(str(resources.goal_verbs))
    
    
    print
    print("Thematic roles:")
    print(str(resources.thematic_roles))


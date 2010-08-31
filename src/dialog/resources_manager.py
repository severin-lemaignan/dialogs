#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger("dialog")

import os.path

from pyoro import Oro, OroServerError

from dialog_exceptions import UnknownVerb

#These values are overridden in dialog.py. Only useful for unittesting alone.
DATA_DIR = os.path.dirname(__file__).split('lib')[0].split('src')[0] + '/share/dialog/' #tries to find out the current prefix and then the data directory
ORO_HOST = 'localhost'
ORO_PORT = 6969

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
    
    def get_ref(self, verb):
        """If the verb is the synonym of a known verb, as stated in the
        thematic_roles file, return the known verb.
        """
        try:
            return self.verbs[verb].ref
        except KeyError:
            raise UnknownVerb('Verb ' + verb + ' doesn\'t exist in the thematic role list.')
            
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
            #raise UnknownVerb('Verb ' + verb + ' has no thematic role defined')
            res = "performedBy" #for now, return by default a generic "performedBy" predicate when no specific thematic role for the subject is defined.
        return (" " + res + " ") if with_spaces else res
        
    def get_next_cmplt_role(self, verb, with_spaces = False):
        res = "involves" #for now, return by default a generic "involve" predicate when no specific thematic role is defined.
        try:
            res = self.verbs[verb.lower()].next_role().id
        except KeyError:
            #raise UnknownVerb('Verb ' + verb + ' has no thematic role defined')
            pass 
        except AttributeError:
            #TODO: case "get me the bottle" -> "get" expects only one cmplt -> warn the user that the grammatical structure is wrong
            pass
        return (" " + res + " ") if with_spaces else res
    
    def get_cmplt_role_for_preposition(self, verb, preposition, with_spaces = False):
        try:
            role = self.verbs[verb.lower()].get_role_for_preposition(preposition)
        except KeyError:
            #raise UnknownVerb('Verb ' + verb + ' has no thematic role defined')
            return None
        
        if not role:
            return None
            
        return (" " + role.id + " ") if with_spaces else role.id
    
    def get_all_verbs(self):
        return self.verbs.keys()
        
    def __str__(self):
        res = ""
        for name, verb in self.verbs.items():
            res += str(verb) + "\n"
        return res


        
            
@singleton
class ResourcePool:
    
    def split_list(self, word_list):
                
        #init
        flag=0
        list_list_word=our_list=[]
        for i in word_list:
            if i!=[]:
                if i[0].startswith('#'):
                    if flag==0:
                        flag=1
                        if our_list!=[]:
                            list_list_word=list_list_word+[our_list]
                            our_list=[]
                    else:
                        flag=0
                else:
                    if flag==0:
                        our_list=our_list+[i]
                            
        list_list_word=list_list_word+[our_list]
        return list_list_word

    def __init__(self, data_path = DATA_DIR, oro_host = ORO_HOST, oro_port = ORO_PORT):
        
        self.ontology_server = None
        
        try:
            if oro_host:
                self.ontology_server = Oro(oro_host, oro_port)
            else:
                logger.warning("Starting without ontology server. Resolution won't work")
        except OroServerError:
            logger.error("Error while trying to connect to ORO on " + oro_host + ":" + str(oro_port) + \
            ". Continuing without the ontology server. Amongst others, resolution won't work.")
        
        self.adjectives = {}
        self.irregular_verbs_past = []
        self.irregular_verbs_present = []
        self.preposition_verbs = []
        self.modal = []
        self.adjective_verb = []
        self.special_nouns = []
        self.pronouns = []
        self.numbers = []
        self.demonstrative_det = []
        self.adverbs = []
        self.proposals = []
        self.preposition_rdf_object_property = {}
        self.compelement_proposals = []
        self.capital_letters = []
        self.determinants = []
        self.nouns_end_s = []
        self.relatives = []
        self.subsentences = []
        self.det_quantifiers = []
        self.adjective_rules = []
        self.composed_nouns = []
        self.plural_nouns = []
        self.auxiliary = []
        self.direct_transitive = []
        self.indirect_transitive = []
        self.state = []
        self.complement_pronouns = []
        self.concatenate_proposals = []
        self.change_tuples = []
        self.adjective_numbers = []
        self.be_pronoun = []
        self.noun_not_composed = []
        self.adj_quantifiers = []
        self.verb_need_to = []
        self.prep_change_place = []
        self.replace_tuples = []
        self.adjective_numbers_digit = []
        self.days_list = []
        self.months_list = [] 
        self.time_adverbs = []
        self.unusable_words = []
        self.time_proposals = []
        self.action_verb_with_passive_behaviour = []


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
        
        
        
        verbs = [list(line.split()) 
                                for line 
                                in open (os.path.join(data_path, "verbs"))]
        verbs = self.split_list(verbs)
        self.irregular_verbs_past=verbs[0]
        self.irregular_verbs_present=verbs[1]
        self.preposition_verbs=verbs[2]
        self.modal=[k[0] for k in verbs[3]]
        self.adjective_verb=[k[0] for k in verbs[4]]
        self.auxiliary=[k[0] for k in verbs[5]]
        self.direct_transitive=[k[0] for k in verbs[6]]
        self.indirect_transitive=[k[0] for k in verbs[7]]
        self.state=[k[0] for k in verbs[8]]
        self.verb_need_to=[k[0] for k in verbs[9]]
        self.action_verb_with_passive_behaviour = [k[0] for k in verbs[10]]
                                
        self.sentence_starts = [tuple(line.split()) 
                                for line 
                                in open (os.path.join(data_path, "sentence_starts"))]       
        
        
        nouns = [list(line.split()) 
                    for line 
                    in open (os.path.join(data_path, "nouns"))]
        nouns = self.split_list(nouns)
        self.special_nouns=[k[0] for k in nouns[0]]
        self.pronouns=[k[0] for k in nouns[1]]
        for i in nouns[1]:
            if i[1]=='1':
                self.complement_pronouns=self.complement_pronouns+[i[0]]
        self.demonstrative_det=[k[0] for k in nouns[2]]
        self.determinants=[k[0] for k in nouns[3]]
        self.nouns_end_s=[k[0] for k in nouns[4]]
        self.relatives=[k[0] for k in nouns[5]]
        self.composed_nouns=[k[0] for k in nouns[6]]
        self.plural_nouns=nouns[7]
        self.noun_not_composed=[k[0] for k in nouns[8]]
        self.days_list=nouns[9]
        self.months_list=nouns[10]
        self.unusable_words=[k[0] for k in nouns[11]]
        
        
        adverbials = [list(line.split()) 
                    for line 
                    in open (os.path.join(data_path, "adverbial"))]   
        adverbials = self.split_list(adverbials)
        self.adverbs=[k[0] for k in adverbials[0]]
        self.time_adverbs=adverbials[0]
        for k in adverbials[1]:
            if k[1]=='1':
                self.compelement_proposals=self.compelement_proposals+[k[0]]
        self.proposals=[k[0] for k in adverbials[1]]
        self.preposition_rdf_object_property = dict([(k[0],k[3:]) for k in adverbials[1]])
        self.time_proposals=adverbials[1]
        self.subsentences=[k[0] for k in adverbials[2]]
        self.prep_change_place=[k[0] for k in adverbials[3]]
        
        
        grammatical_rules = [list(line.split()) 
                    for line 
                    in open (os.path.join(data_path, "grammatical_rules"))]   
        grammatical_rules = self.split_list(grammatical_rules)
        self.numbers=grammatical_rules[0]
        self.det_quantifiers=grammatical_rules[1]
        self.capital_letters=[k[0] for k in grammatical_rules[2]]
        self.adjective_rules=[k[0] for k in grammatical_rules[3]]
        self.concatenate_proposals=grammatical_rules[4]
        self.change_tuples=grammatical_rules[5]
        self.adjective_numbers_digit=grammatical_rules[6]
        self.adjective_numbers=[k[0] for k in grammatical_rules[6]]
        self.be_pronoun=[k[0] for k in grammatical_rules[7]]
        self.adj_quantifiers=[k[0] for k in grammatical_rules[8]]
        for k in grammatical_rules[9]:
            self.replace_tuples=self.replace_tuples+[[k[0],k[1:]]]
        
        
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
    print("special nouns:")
    print(str(ResourcePool().special_nouns))
    
    print
    print("pronouns:")
    print(str(ResourcePool().pronouns))
    
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
    

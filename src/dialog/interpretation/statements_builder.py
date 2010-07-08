#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import random
import inspect
from pyoro import Oro
from resources_manager import ResourcePool

from dialog_exceptions import DialogError
from dialog_exceptions import GrammaticalError


from sentence import *

"""This module implements ...

"""

class StatementBuilder:
    
    def __init__(self,current_speaker = None):
        self._sentence = None
        self._current_speaker = current_speaker
        self._statements = []
        

    def clear_statements(self):
        self._statements = []
    
    def set_current_speaker(self, current_speaker):
        self._current_speaker = current_speaker
    
    def process_sentence(self, sentence):
        if not sentence.resolved():
            raise DialogError("Trying to process an unresolved sentence!")
            
        self._sentence = sentence
        
        #self._sentence = dump_resolved(sentence, self._current_speaker, 'myself')#TODO: dumped_resolved is only for the test of statement builder. Need to be replaced as commented above
        if sentence.sn:
            self.process_nominal_groups(self._sentence.sn)
        if sentence.sv:
            self.process_verbal_groups(self._sentence)
            
        return self._statements
    
    
    def process_nominal_groups(self, nominal_groups):
        ng_stmt_builder = NominalGroupStatementBuilder(nominal_groups, self._current_speaker) 
        self._statements.extend(ng_stmt_builder.get_statements())
        
        
    def process_verbal_groups(self, sentence):
        vg_stmt_builder = VerbalGroupStatementBuilder(sentence.sv, self._current_speaker)
        #Case: an imperative sentence does not contain an sn attribute,
        #      we will assume that it is implicitly an order from the current speaker.
        #      performed by the recipient of the order.
        #      Therefore, the sn.id holds the value 'myself'
        if sentence.data_type == 'imperative':
            subject_id = 'myself'
            vg_stmt_builder._processing_order = True
            self._statements.extend(vg_stmt_builder.get_statements(subject_id))        
        else:
            for sn in sentence.sn:
                if sn.id:
                    subject_id = sn.id
                else:
                    subject_id = generate_id()                  
                
                self._statements.extend(vg_stmt_builder.get_statements(subject_id))
    

class NominalGroupStatementBuilder:
    def __init__(self, nominal_groups, current_speaker = None):
        self._nominal_groups = nominal_groups
        self._current_speaker = current_speaker
        self._statements = []
    
    def clear_statements(self):
        self._statements = []
        
        
    def get_statements(self):
        """ The following function builds a list of statement from a list of nominal group
        A NominalGroupStatementBuilder needs to have been instantiated before"""
        for ng in self._nominal_groups:
            if ng.id:
                ng_id = ng.id
            else:
                ng_id = generate_id()            
                
            self.process_nominal_group(ng, ng_id)                    
        return self._statements
    
    
    def process_nominal_group(self, ng, ng_id):
        """ The following function processes a single nominal_group"""    
        if ng.det:
            self.process_determiners(ng, ng_id)
        if ng.noun:
            self.process_noun_phrases(ng, ng_id)
        if ng.adj:
            self.process_adjectives(ng, ng_id)
        if ng.noun_cmpl:
            self.process_noun_cmpl(ng, ng_id)
        if ng.relative:
            self.process_relative(ng, ng_id)
            

    def process_determiners(self, nominal_group, ng_id):
        for det in nominal_group.det:
            logging.debug("Found determiner:\"" + det + "\"")
            # Case 1: definite article : the"""
            # Case 2: demonstratives : this, that, these, those"""
            # Case 3: possessives : my, your, his, her, its, our, their """
            if det == "my":
                self._statements.append(ng_id + " belongsTo " + self._current_speaker)
            elif det == "your":
                self._statements.append(ng_id + " belongsTo myself")
            # Case 4: general determiners: See http://www.learnenglish.de/grammar/determinertext.htm"""
            
    
    def process_noun_phrases(self, nominal_group, ng_id):
        for noun in nominal_group.noun:
            logging.debug("Found a noun phrase:\"" + noun + "\"")
                        
            # Case : existing ID
            oro = Oro("localhost", 6969) #TODO: remove connection. Use a variable that will be set up for a single connection to ORO
            onto = oro.lookup(noun)
            oro.close()
            
            if onto and [noun,"INSTANCE"] in onto:
                pass #Just to be checked. The Id has already been resolved
                
            # Case : common noun
            elif nominal_group.det:
                self._statements.append(ng_id + " rdf:type " + noun.capitalize())            
                
            #Case : proper noun or personal pronoun
            else:
                #TODO: the list ["I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "their"] needs to be inserted in ResourcePool
                """
                if not noun in ResourcePool().personal_determiner
                """
                if not noun in ["I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "their"]:
                    self._statements.append(ng_id + " rdfs:label \"" + noun + "\"")
                
                    
    
    def process_adjectives(self, nominal_group, ng_id):
        """For any adjectives, we add it in the ontology with the objectProperty 
        'hasFeature' except if a specific category has been specified in the 
        adjectives list.
        """
        for adj in nominal_group.adj:
            logging.debug("Found adjective:\"" + adj + "\"")
            try:
                self._statements.append(ng_id + " has" + ResourcePool().adjectives[adj] + " " + adj)
            except KeyError:
                self._statements.append(ng_id + " hasFeature " + adj)
    
    
    def process_noun_cmpl(self, nominal_group, ng_id):
        logging.debug("processing noun complement:")
        for noun_cmpl in nominal_group.noun_cmpl:
            if noun_cmpl._resolved:
                noun_cmpl_id = noun_cmpl.id
            else:
                noun_cmpl_id = generate_id()
                
            self.process_nominal_group(noun_cmpl, noun_cmpl_id)
            self._statements.append(ng_id + " belongsTo " + noun_cmpl_id)
    
    def process_relative(self, nominal_group, ng_id):
        """ The following processes the relative clause of the subject of a sentence.           
           case 1: the subject of the sentence is complement of the relative clause
                    e.g. the man that you heard from is my boss
                          => the man is my boss + you heard from the man
                          => sn != []
            
           case 2: the subject of the sentence is subject of the relative clause.
                   we process only the verbal group of the relative.
                    e.g. the man who is talking, is tall
                         => the man is tall and is talking
                         => sn == []
        """
        for rel in nominal_group.relative:
            logging.debug("processing relative:")    
            #case 1   
            if rel.sn:
                logging.warning("Don't know how to resolve a relative clause in this situation yet")
                """
                for ng in rel.sn:
                    if ng._resolved:
                        ng_rel_id = ng.id
                    else:
                        ng_rel_id = "Blagnac_Aircraft"                    
                    self.process_nominal_group(ng, ng_rel_id)
                
                if rel.sv:
                    rel_vg_stmt_builder = VerbalGroupStatementBuilder(rel.sv)    
                    rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng_rel_id, ng_id)
                    self._statements.append(rel_vg_stmt_builder._statements)
                    rel_vg_stmt_builder.clear_statements()
                """
            #case 2        
            else:
                if rel.sv:
                    rel_vg_stmt_builder = VerbalGroupStatementBuilder(rel.sv, self._current_speaker)
                    rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng_id)
                    self._statements.extend(rel_vg_stmt_builder._statements)
            
                    

class VerbalGroupStatementBuilder:
    def __init__(self, verbal_groups, current_speaker = None):
        self._verbal_groups = verbal_groups
        self._current_speaker = current_speaker
        self._statements = []
        #the following attribute holds the value True when an imperative sentence or an order is processed
        self._processing_order = False
        
        
    def clear_statements(self):
        self._statements = [] 
    
    def get_statements(self, subject_id):
        self.process_verbal_groups(self._verbal_groups  , subject_id)                
        return self._statements
   
   
    def process_verbal_groups(self, verbal_groups, subject_id, subject_rel_id = None):
        
        for vg in verbal_groups:          
            self.process_state(vg)
            if vg.vrb_main:
                self.process_verb(vg, subject_id)
            
            if vg.advrb:
                self.process_adverbial_sentence(vg)
            if vg.vrb_adv:
                self.process_adverb(vg)
            if vg.vrb_sub_sentence:
                self.process_adverb(vg)   

    #TODO:   
    def process_state(self, state):
        """For A != B, Shall we use owl:complementOf => see Negation in http://www.co-ode.org/resources/tutorials/intro/slides/OWLFoundationsSlides.pdf """
        pass
    
    def process_verb(self, verbal_group, subject_id):
        for verb in verbal_group.vrb_main:
         
            logging.debug("Found verb:\"" + verb + "\"")
            #TODO: modal verbs e.g can+go
            
            #Case 1:  the linking verb 'to be'/"""
            #Case 2:  actions or stative verbs with a specified 'goal' role:
            #                          see '../../share/dialog/thematic_roles'
            #Case 3:  other action or stative verbs
            
            goal_verbs = ResourcePool().goal_verbs 
            
            #Case 1:
            if verb == "be":
                sit_id = subject_id
                
            else:
                sit_id = generate_id()#TODO: does a situation ID involves a unique situation?
                #Case 2:                
                if verb in goal_verbs:
                    self._statements.append(subject_id + " desires " + sit_id)
                    
                    if verbal_group.verb_sec:
                        self.process_vrb_sec(verbal_group)                      
                #Case 3:   
                else:
                    self._statements.append(sit_id + " rdf:type " + verb.capitalize())
                    self._statements.append(sit_id + " performedBy " + subject_id)
                    
            
            
            if self._processing_order:
                self._statements.append(self._current_speaker + " desires " + sit_id)
            
            
            if verbal_group.d_obj:
                self.process_direct_object(verbal_group.d_obj, verb, sit_id)
            
            if verbal_group.i_cmpl:
                self.process_indirect_complement(verbal_group.i_cmpl, verb, sit_id)
            
                    
                    
                
            
    def process_vrb_sec(self, verbal_group):
        for verb in verbal_group.vrb_sec:
            logging.debug("Found verb:\"" + verb + "\"")
            
    def process_direct_object(self, d_objects, verb, id):
        logging.debug("Processing direct object d_obj:")
        d_obj_stmt_builder = NominalGroupStatementBuilder(d_objects, self._current_speaker)
        
        for d_obj in d_objects:
            #Case 1: The direct object follows the verb 'to be'.
            #        We process the d_obj with the same id as the subject of the sentence
            if verb == "be":
                d_obj_id = id
            
            
            #Case 2: The direct object follows another stative or action verb.
            #        we process the d_obj as involved by the situation
            else:
                if d_obj.id:
                    d_obj_id = d_obj.id
                else:
                    d_obj_id = generate_id()    
                    
                self._statements.append(id + " involves " + d_obj_id)
            
            d_obj_stmt_builder.process_nominal_group(d_obj, d_obj_id)
        
        self._statements.extend(d_obj_stmt_builder._statements)
        
        
            
            
            
    def process_indirect_complement(self, indirect_cmpls, verb, sit_id):
             
        thematic_roles = ResourcePool().thematic_roles
        try:
            role = thematic_roles.get_next_cmplt_role(verb, True)
        except:
            role = None
        
        #TODO: Uncomment the line below For test only
        #role = "hasGoal"
        
        for ic in indirect_cmpls:
            logging.debug("Processing indirect complement i_cmpl:")
            
            # Case 1: if there is no preposition, the indirect complement is obviously an indirect object.
            #        Therefore, it receives the action
            #            e.g. I gave you a ball also means I gave a ball 'to' you
            #        see http://www.englishlanguageguide.com/english/grammar/indirect-object.asp
            
            #Case 2: if there is a preposition, the indirect complement is either an indirect object or an adverbial
            #        if the main verb is specified as a thematic role, we extract the matching object_property to the preposition.
            #            e.g I moved the bottle 'to' the table. The object_property takes the value "hasGoal"
            # 
            #        if the preposition is 'to' , by default we assume the indirect complement is an indirect object
            #            e.g. I gave a ball to Jido. The object_property takes the value "receivedBy"
            #        otherwise, the default processing is to create an object_property by concatenating is and the preposition
            #            e.g. I bought a ball for Jido. The object_property takes the value "isFor"
            
            
            i_stmt_builder = NominalGroupStatementBuilder(ic.nominal_group, self._current_speaker)
            for ic_noun  in ic.nominal_group:
                if ic_noun.id:
                    ic_noun_id = ic_noun.id
                else:
                    ic_noun_id = generate_id()
                    
                if not ic.prep:
                    self._statements.append(sit_id + " receivedBy " + ic_noun_id)
                    
                elif role:
                    self._statements.append(sit_id + "" + role + "" + ic_noun_id)
                else:
                    self._statements.append(sit_id + " is" + ic.prep[0]+ " " + ic_noun_id)
                
                
                i_stmt_builder.process_nominal_group(ic_noun, ic_noun_id)
                
            self._statements.extend(i_stmt_builder._statements)
                
         
                
                
    #TODO:      
    def process_adverbial_sentence(self, advrb):
        for adv in advrb:
            logging.debug("Found adverbial phrase:\"" + adv + "\"")
            
    #TODO:       
    def process_adverb(self, advrb):
        for adv in advrb:
            logging.debug("Found adverb:\"" + adv + "\"")
            
    #TODO:
    def vrb_subsentence(self, vrb_sub_sentence):
        for sub in vrb_sub_sentence:
            logging.debug("Processing adverbial clauses:")
            
            
               
            

def generate_id():
    sequence = "0123456789abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sample = random.sample(sequence, 5)
    return "".join(sample)



"""
    Please write your test below using the following template
    then , in the functio
"""
"""
def my_unittest():
    print "**** Test My unit test  *** "
    print "Danny drives a car"  
    sentence = Sentence("statement", "", 
                         [Nominal_Group([],
                                        ['Danny'],
                                        [],
                                        [],
                                        [])],                                         
                         [Verbal_Group(['drive'],
                                       [],
                                       'present_simple',
                                       [Nominal_Group(['a'],['car'],[],[],[])],
                                       [],
                                       [],
                                       [],
                                       'affirmative',
                                       [])])    
    
    expected_result = ['* rdfs:label "Danny"',
                       '* rdf:type Drive',
                       '* performedBy *',
                       '* involves *',
                       '* rdf:type Car']
    return test(sentence, expected_result)
    
    #in order to print the statements resulted from the test, uncomment the line below:
    #return test(sentence, display_statement_result = True)
    #
    #otherwise, use the following if you want to hide the statements 
    #return test(sentence)
    #
    #You may like to compare the expected result. Then use either of the line below
    #return test(sentence, expected_result, display_statement_result = True)
    #    or
    #return test(sentence, expected_result, display_statement_result = False)
    #    or
    #return test(sentence, expected_result)
    #
                    
"""
def test_1():
    print "**** Test 1  *** "
    print "Danny drives a blue car"  
    sentence = Sentence("statement", "", 
                         [Nominal_Group([],
                                        ['Danny'],
                                        [],
                                        [],
                                        [])],                                         
                         [Verbal_Group(['drive'],
                                       [],
                                       'present_simple',
                                       [Nominal_Group(['a'],['car'],['blue'],[],[])],
                                       [],
                                       [],
                                       [],
                                       'affirmative',
                                       [])])    
    
    expected_result = ['* rdfs:label "Danny"',
                       '* rdf:type Drive',
                       '* performedBy *',
                       '* involves *',
                       '* rdf:type Car',
                       '* hasColor blue']
    
    return test(sentence, expected_result, display_statement_result = True)

    

def test_2():
    print "**** Test 2  *** "
    print "my car is blue"
    sentence = Sentence("statement", "", 
                         [Nominal_Group(['my'],
                                        ['car'],
                                        ['blue'],
                                        [],
                                        [])],                                         
                         [Verbal_Group(['be'],
                                       [],
                                       'present_simple',
                                       [],
                                       [],
                                       [],
                                       [],
                                       'affirmative',
                                       [])])
    expected_result = ['* rdf:type Car',
                       '* hasColor blue',
                       '* belongsTo SPEAKER']   
    return test(sentence, expected_result, display_statement_result = True)
    
    
def test_3():
    print "**** Test 3  *** "
    print "Jido is a robot"
    sentence = Sentence("statement", "", 
                         [Nominal_Group([],
                                        ['Jido'],
                                        [],
                                        [],
                                        [])],                                         
                         [Verbal_Group(['be'],
                                       None,
                                       'present_simple',
                                       [Nominal_Group(['a'],['robot'],[],[],[])],
                                       [],
                                       [],
                                       [],
                                       'affirmative',
                                      [])])  
    expected_result = ['* rdfs:label "Jido"',
                       '* rdf:type Robot']   
    return test(sentence, expected_result, display_statement_result = True)
    

def test_4():
    print "**** Test 4  *** "
    print "the man that I saw , has a small car"
    relative4 = Sentence("statement", "", 
                         [Nominal_Group([],
                                        ['I'],
                                        [],
                                        [],
                                        [])], 
                        [Verbal_Group(['see'],
                                      [],
                                      'past_simple',
                                      [],
                                      [],
                                      [],
                                      [],
                                      'affirmative',
                                      [])])
     
    sentence = Sentence("statement", "", 
                         [Nominal_Group(['the'],
                                        ['man'],
                                        [],
                                        [],
                                        [relative4])],                                         
                         [Verbal_Group(['have'],
                                       [],
                                       'present_simple',
                                       [Nominal_Group(
                                                      ['a'],
                                                      ['car'],
                                                      ['small'],
                                                      [],
                                                      [])],
                                       [],
                                       [],
                                       [],
                                       'affirmative',
                                       [])]) 
    expected_resut = ['* rdf:type Man',
                      '* performedBy SPEAKER',
                      '* rdf:type See',
                      '* involves *',
                      '* rdf:type Have',
                      '* performedBy *',
                      '* rdf:type Car *',
                      '* hasSize small *']
    return test(sentence, expected_resut, display_statement_result = True)
    
    
def test_5():
    print "**** Test 5  *** "
    print "the man that talks , has a small car"
    relative5 = Sentence("statement", "", 
                        [], 
                        [Verbal_Group(['talk'],
                                      [],
                                      'past_simple',
                                      [],
                                      [],
                                      [],
                                      [],
                                      'affirmative',
                                      [])]) 
    sentence = Sentence("statement", "", 
                         [Nominal_Group(['the'],
                                        ['man'],
                                        [],
                                        [],
                                        [relative5])],                                         
                         [Verbal_Group(['have'],
                                       [],
                                       'present_simple',
                                       [Nominal_Group(
                                                      ['a'],
                                                      ['car'],
                                                      ['small'],
                                                      [],
                                                      [])],
                                       [],
                                       [],
                                       [],
                                       'affirmative',
                                       [])])    
    
    expected_resut = ['* rdf:type Man',
                      '* rdf:type Talk',
                      '* performedBy *',
                      '* rdf:type Have',
                      '* involves *',
                      '* rdf:type Car *',
                      '* hasSize small *']
    return test(sentence, expected_resut, display_statement_result = True)
    



def test_6():
    
    print "**** Test 6  *** "
    print "I gave you the car of the brother of Danny"   
    sentence = Sentence("statement", 
                         "",
                         [Nominal_Group([],
                                        ['I'],
                                        [],
                                        [],
                                        [])], 
                          [Verbal_Group(['give'],
                                        [],
                                        'past_simple',
                                        [Nominal_Group(['the'],
                                                       ['car'],
                                                       [],
                                                       [Nominal_Group(
                                                                      ['the'],
                                                                      ['brother'],
                                                                      [],
                                                                      [Nominal_Group([],
                                                                                     ['Danny'],
                                                                                     [],
                                                                                     [],
                                                                                     [])],
                                                                      [])],
                                                        [])] , 
                                        [Indirect_Complement([],
                                                             [Nominal_Group([],
                                                                            ['you'],
                                                                            [],
                                                                            [],
                                                                            [])])], 
                                        [],
                                        [],
                                        'affirmative', 
                                        [])])
    expected_resut = ['* rdf:type Give',
                      '* performedBy SPEAKER',
                      '* involves *',
                      '* rdf:type Car',
                      '* belongsTo *',
                      '* rdf:type Brother',
                      '* belongsTo *',
                      '* rdfs:label "Danny"',
                      '* receivedBy myself']
    
    return test(sentence, expected_resut, display_statement_result = True)
    

def test_7():
    
    print "**** Test 7  *** "
    print "I went to Toulouse"
    sentence = Sentence("statement", "", 
                         [Nominal_Group([],
                                        ['I'],
                                        [],
                                        [],
                                        [])],                                         
                         [Verbal_Group(['go'],
                                       [],
                                       'present_simple',
                                       [],
                                       [Indirect_Complement(['to'], [Nominal_Group([],['Toulouse'],[],[],[])])],
                                       [],
                                       [],
                                       'affirmative',
                                       [])])
    expected_resut = ['* rdf:type Go',
                      '* performedBy SPEAKER',
                      '* actsOnObject *',
                      '* rdfs:label "Toulouse"']
    return test(sentence, expected_resut, display_statement_result = True)
    

def test_8():
    print "**** Test 8  *** "
    print "put the bottle in the cardbox"
    sentence = Sentence("imperative", "", 
                         [],                                         
                         [Verbal_Group(['put'],
                                       [],
                                       'present_simple',
                                       [Nominal_Group(['the'],['bottle'],[],[],[])],
                                       [Indirect_Complement(['in'],
                                                            [Nominal_Group(['the'],['cardbox'],[],[],[])]) ],
                                       [],
                                       [],
                                       'affirmative',
                                       [])])
    expected_resut = ['SPEAKER desires *',
                      '* rdf:type Put',
                      '* performedBy myself',
                      '* involves *',
                      '* rdf:type Bottle',
                      '* actsOnObject *',
                      '* rdf:type Cardbox']  
    return test(sentence, expected_resut, display_statement_result = True)
    
    
    
    
"""
    The following functions are implemented for test purpose only
"""
def dump_resolved(sentence, current_speaker, current_listener):
    def resolve_ng(ngs):
        #TODO: remove connection. Use a variable that will be set up for a single connection to ORO
        oro = Oro("localhost", 6969) 
        
           
        for ng in ngs:
            
            onto = oro.lookup(ng.noun[0])
            #  : Make sure the following is resolved in Resolution
            if onto and [ng.noun[0],"INSTANCE"] in onto:
                ng.id = ng.noun[0]
            elif ng.noun[0] in ['me', 'Me','I']:
                ng.id = current_speaker
            elif ng.noun[0] in ['you', 'You']:
                ng.id = current_listener
            else:
                ng.id = generate_id()
                
            if ng.noun_cmpl:
                ng.noun_cmpl = resolve_ng(ng.noun_cmpl)
                
            if ng.relative:
                for rel in ng.relative:
                    rel = dump_resolved(rel, current_speaker, current_listener)                    
        oro.close()
        return ngs
    
    if sentence.sn:
        sentence.sn = resolve_ng(sentence.sn)
    
    
    if sentence.sv:
        for sv in sentence.sv:
            if sv.d_obj:
                sv.d_obj = resolve_ng(sv.d_obj)
    
            if sv.i_cmpl:
                for i_cmpl in sv.i_cmpl:
                    i_cmpl = resolve_ng(i_cmpl.nominal_group)
        
    return sentence



def test(sentence, expected_result = None, display_statement_result = False):
    stmt = StatementBuilder("SPEAKER")
    collect_checkup = []
    try:
        res = stmt.process_sentence(sentence)
    except RuntimeError:
        collect_checkup.extend([inspect.stack()[1][3], "ERROR PROCESSING"])
    
    if display_statement_result:
        print "*** result " + inspect.stack()[1][3] + " ****"
        str(res)
    
    
    if expected_result:
        if check_results(res, expected_result):
            collect_checkup.extend([inspect.stack()[1][3], "OK"])
        else:
            collect_checkup.extend([inspect.stack()[1][3], "NOT RESOLVED"])
    else:
        collect_checkup.extend([inspect.stack()[1][3], "EXPECTED_RESULT not stated"])
        
    
    return collect_checkup


def check_results(res, expected):
    def check_triplets(tr , te):
        tr_split = tr.split()
        te_split = te.split()
        
        return (tr_split[0] == te_split[0] or te_split[0] == '*') and\
                (tr_split[1] == te_split[1]) and\
                (tr_split[2] == te_split[2] or te_split[2] == '*') 
       
    while res:
        r = res.pop()
        for e in expected:
            if check_triplets(r, e):
                expected.remove(e)
    if expected:
        print "**** Missing assertion from result:   "
        print expected
        print "FAIL"
           
    return expected == res
        
    

def str(list):
    for l in list:
        print l
    
        
def unit_tests():
    """This function tests the main features of the class StatementBuilder"""
    #logging.basicConfig(level=logging.DEBUG,format="%(message)s")
    
    #The following parameter is the check-list of the unit test stated below.
    _check_list = []
    
    print("This is a test...")
    #call your unit test below"""
    #_check_list.append(my_test())
    _check_list.append(test_1())
    _check_list.append(test_2())
    _check_list.append(test_3())
    _check_list.append(test_4())
    _check_list.append(test_5())
    _check_list.append(test_6())
    _check_list.append(test_7())
    _check_list.append(test_8())
        
    #Comment the line bellow to hide check-list of the unit test
    print "********* CHECK-LIST******************"
    str(_check_list)
    
if __name__ == '__main__':
    unit_tests()
    


"""Further test
#I gave you the car of Martin
objectInteraction = ObjectInteraction(Sentence("statement", "", [Nominal_Group([],['I'],[],[],None)], Verbal_Group(['give'],None,'past_simple',[Nominal_Group(['the'],['car'],[],[Nominal_Group([],['Martin'],[],[],None)],None)] , [Indirect_Complement([], [Nominal_Group([],  ['you'],[],[], None)])], [], [], 'affirmative', None )),"human_xyz", "myself", "2011-02-04", "12:11:34")
responseList = server.dialog(objectInteraction)
for response in responseList:
    response.sentence.getString()



#what did I give you?
objectInteraction = ObjectInteraction(Sentence("w_question", "thing", [Nominal_Group([],['I'],[],[],None)], Verbal_Group(['give'],None,'past_simple',[] , [Indirect_Complement([], [Nominal_Group([],  ['you'],[],[], None)])], [], [], 'affirmative', None )),"human_xyz", "myself", "2011-02-04", "12:11:34")
responseList = server.dialog(objectInteraction)
for response in responseList:
    response.sentence.getString()

#who has a small car?
objectInteraction = ObjectInteraction(Sentence("w_question", "person", [], Verbal_Group(['have'],None,'past_simple',[Nominal_Group(['a'],  ['car'],['small'],[], None)] , [], [], [], 'affirmative', None )),"human_xyz", "myself", "2011-02-04", "12:11:34")
responseList = server.dialog(objectInteraction)
for response in responseList:
    response.sentence.getString()

#how is my bottle?
objectInteraction = ObjectInteraction(Sentence("w_question", "manner", [Nominal_Group(['my'],['bottle'],[],[],None)], Verbal_Group(['be'],None,'past_simple',[],[],[], [], 'affirmative', None)) ,"human_xyz", "myself", "2011-02-04", "12:11:34")
responseList = server.dialog(objectInteraction)
for response in responseList:
    response.sentence.getString()

#what does Danny drive?
objectInteraction = ObjectInteraction(Sentence("w_question", "thing", [Nominal_Group([],['Danny'],[],[],None)], Verbal_Group(['drive'],None,'past_simple',[] , [], [], [], 'affirmative', None )),"human_xyz", "myself", "2011-02-04", "12:11:34")
responseList = server.dialog(objectInteraction)
for response in responseList:
    response.sentence.getString()
"""
    


# -*- coding: utf-8 -*-

import logging

from sentence_types import *

from helpers.sentence_atoms import *
from helpers.printers import pprint, level_marker
from helpers.helpers import colored_print
from resources_manager import ResourcePool

class Sentence:
    """
    A sentence is formed from:
    data_type: the type of a sentence whether it is a question, an imperative, ...
    sn : a nominal structure typed into a Nominal_group
    sv : a verbal structure typed into a Verbal_Group
    aim : is used for retrieveing the aim of a question
    """
    def __init__(
        self,
        data_type,
        aim,
        sn,
        sv,
        ):
        self.data_type = data_type
        self.aim = aim
        self.sn = sn
        self.sv = sv
    
    def isvalid(self):
       """ Checks a sentence is grammatically valid
       """
       return  reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x.isvalid(), self.sn), 
                        True) \
                and \
                reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x.isvalid(), self.sv), 
                        True)

    def resolved(self):
        """returns True when the whole sentence is completely resolved
        to concepts known by the robot.
        """
        return  reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.sn), 
                        True) \
                and \
                reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.sv), 
                        True)

    
    def __str__(self):
        res = level_marker() + pprint(self.data_type, SENTENCE_TYPE)
        res += pprint(self.aim, SENTENCE_AIM) # 'aim' may be None
        
        if self.sn:
            sn = ""
            for s in self.sn:
                sn = str(s).replace("\n", "\n\t") + "\n"
            res += pprint(sn, SUBJECT)
        if self.sv:
            for s in self.sv:
                res += str(s).replace("\n", "\n\t") + "\n"
        
        #res += "This sentence is " + ("fully resolved." if self.resolved() else "not fully resolved.")

        if self.isvalid():
            res = pprint(res, SENTENCE)
        else:
            res = pprint(res, AGRAMMATICAL_SENTENCE)
        return res
    
    def flatten(self):
        return [self.data_type,
                self.aim,
                map(lambda x: x.flatten(), self.sn),
                map(lambda x: x.flatten(), self.sv)]
    
    def isaborting(self):
        #Forget it
        if self.data_type == IMPERATIVE \
            and "forget" in [verb for sv in self.sv for verb in sv.vrb_main]\
            and "affirmative" in [sv.state for sv in self.sv]:
            return True
            
        #[it] doesn't matter'
        if self.data_type == STATEMENT  \
            and "matter" in [verb for sv in self.sv for verb in sv.vrb_main]\
            and "negative" in [sv.state for sv in self.sv]:
            return True
            
        return False
    
    def islearning(self):
        #Learn that
        if  self.data_type == IMPERATIVE\
            and "learn" in [verb for sv in self.sv for verb in sv.vrb_main]\
            and "affirmative" in [sv.state for sv in self.sv]:
            return True
        return False
    
    def append_sub_sentence(self, sub_sentence):
        """This append a subsentence to the current sentence """
        self.sv[0].d_obj = []
        self.sv[0].i_cmpl = []
        self.sv[0].vrb_sub_sentence.append(sub_sentence)
                

class Nominal_Group:
    """
    Nominal group class declaration
    det : determinant
    noun: a simple noun
    adj: a list of adjectives describing the noun, the form is ['adjective',['list', 'of', 'quantifiers']]
    noun_cmpl: a list of noun complements
    relative : is a relative sentence typed into Sentence
    """

    def __init__(   self,
                    det,
                    noun,
                    adj,
                    noun_cmpl,
                    relative,
                    ):
        self.det = det
        self.noun = noun
        self.adj = adj
        self.noun_cmpl = noun_cmpl
        self.relative = relative
                
        """This field is True when this nominal group is resolved to a concept
        known by the robot."""
        self._resolved = False
        
        """This field hold the ID of the concept represented by this group.
        When the group is resolved, id must be different from None
        """
        self.id = None
        
        self._conjunction = 'AND' #could be 'AND' or 'OR'... TODO: use constants!
        self._quantifier = 'ONE'  #could be 'ONE' or 'SOME'... TODO: use constants!

    def isvalid(self):
        """ Check this nominal group is valid.

        This currently means:
            - it has either non-null adjective or non-null nouns or both 
        """
        return True if (self.noun or self.adj) else False

    def __str__(self):
        
        res = level_marker()
        
        if self._conjunction != 'AND':
            res += pprint(self._conjunction, CONJUNCTION)
        
        if self._quantifier != 'ONE':
            res += pprint(self._quantifier, QUANTIFIER)
            
        if self._resolved:
            res += pprint(self.id, ID)
            res = pprint(res, RESOLVED)
            
        else:
            
            
            if self.det:
                res +=   pprint(" ".join(self.det), DETERMINER) 
            
            
            for k in self.adj:
                if k[1]:
                    res +=  pprint(" ".join(k[1]), ADJECTIVE_QUALIFIER) 
                res +=  pprint(k[0], ADJECTIVE)
            
            if self.noun:
                res +=   pprint(" ".join(self.noun), NOUN)
            
            
            if self.noun_cmpl:
                for s in self.noun_cmpl:
                    res += pprint(str(s).replace("\n", "\n\t"), NOUN_CMPLT)
            
            if self.relative:
                for rel in self.relative:
                    res += pprint(str(rel).replace("\n", "\n\t"), RELATIVE_GRP)
        
        return pprint(res, NOMINAL_GROUP)
    
    
    def flatten(self):
        return [self.det,
                self.noun,
                self.adj,
                map(lambda x: x.flatten(), self.noun_cmpl),
                map(lambda x: x.flatten(), self.relative)]
        
        
    def adjectives_only(self):
        """This method returns True when this nominal group holds only a set of adjectives.
        E.g: the banana is yellow. The parser provides an object sentence with two nominal groups:
        - Nominal_Group(['the'], ['banana'], [], [],[]) and adjectives_only returns False
        - Nominal_Group([], [], ['yellow'], [],[]) and adjectives_only returns True
        """
        if self.adj and \
                not self.noun and \
                not self.noun_cmpl and \
                not self.relative:
            return True
        else:
            return False
        
    
class Indirect_Complement:
    """
    Indirect complement class declaration
    gn : nominal group
    prep : preposition
    """
    
    def __init__(self, prep, nominal_group):
        self.prep = prep
        self.gn = nominal_group
        
    def resolved(self):
        return  reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.gn), 
                        True)
        
    def __str__(self):
        res = pprint(" ".join(self.prep), PREPOSITION)
        
        if self.gn:
            for s in self.gn:
                res += pprint(str(s).replace("\n", "\n\t"), INDIRECT_OBJECT)
        
        return res

    def isvalid(self):
        """ Check this indirect group is valid.
        
        This currently means:
            - its nominal group is valid
        """
        return  self.gn \
                and \
                reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x.isvalid(), self.gn), 
                        True)
 

   
    def flatten(self):
        return [self.prep,
                map(lambda x: x.flatten(), self.gn)]

class Verbal_Group:
    """
    Verbal_group class declaration
    vrb_main: the main verb of a sentence
    vrb_sec : an accompanying verb of the main verb
    vrb_tense: the main verb tense
    d_obj : the  direct object referred by the main verb
    i_cmpl : the indirect object referred by the main verb or an adverbial formed from a nominal group
    vrb_adv : an adverb describing the verb
    advrb : an adverb used as an adverbial of the whole sentence
    """
    
    #List of verb state
    affirmative = "affirmative"
    negative = "negative"
    
    def __init__(
            self,
            vrb_main,
            sv_sec,
            vrb_tense,
            d_obj,
            i_cmpl,
            vrb_adv,
            advrb,
            state,
            vrb_sub_sentence,
            ):
        self.vrb_main = vrb_main
        self.sv_sec = sv_sec
        self.vrb_tense = vrb_tense
        self.d_obj = d_obj
        self.i_cmpl = i_cmpl
        self.advrb = advrb
        self.vrb_adv = vrb_adv
        self.state = state
        self.vrb_sub_sentence = vrb_sub_sentence
        
        """This field is True when this verbal group is resolved to a concept
        known by the robot."""
        self._resolved = False
        
        self.comparator = [] #To process comparison like stronger than you
        
        
    def isvalid(self):
        """ Check this verbal group is valid.

        This currently means:
            - it has a verb
            - its direct and indirect complements, if they exists, are valid
            - the sub sentence, if it exists, is valid 
        """
        return  (True if self.vrb_main else False) \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x.isvalid(), self.d_obj), True) \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x.isvalid(), self.i_cmpl), True) \
                and \
                reduce(lambda c1,c2: c1 and c2 , map(lambda x: x.isvalid(), self.sv_sec), True)\
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x.isvalid(), self.vrb_sub_sentence), True)
 

    def resolved(self):
        return  self._resolved \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x._resolved, self.d_obj), True) \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x.resolved(), self.i_cmpl), True) \
                and \
                reduce(lambda c1,c2: c1 and c2 , map(lambda x: x.resolved(), self.sv_sec), True)\
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x.resolved(), self.vrb_sub_sentence), True)
    
    def __str__(self):
        res =  pprint(" ".join(self.vrb_main), VERB) + pprint(self.vrb_tense, TENSE)
        if self.advrb:
            res += pprint(" ".join(self.advrb), ADVERBIAL)
        if self.vrb_adv:
            res += pprint(" ".join(self.vrb_adv), VERBAL_ADVERBIAL)
                
        if self.d_obj:
            for cmpl in self.d_obj:
                res += '\t' + pprint(str(cmpl).replace("\n", "\n\t"), DIRECT_OBJECT) + "\n"
        
        if self.i_cmpl:
            for cmpl in self.i_cmpl:
                res += '\t' + str(cmpl).replace("\n", "\n\t") + "\n"
        
        if self.vrb_sub_sentence:
            for vrb_sub_s in self.vrb_sub_sentence:
                res += '\t' + pprint(str(vrb_sub_s).replace("\n", "\n\t"), SUB_SENTENCE) + "\n"
        
        if self.sv_sec:
            for vrb_sec_s in self.sv_sec:
                res += '\t' + pprint(str(vrb_sec_s).replace("\n", "\n\t"), SECONDARY_VERBAL_GROUP) + "\n"
        
        res = pprint(res, AFFIRMATIVE if self.state == Verbal_Group.affirmative else NEGATIVE) 
        res = pprint(res, RESOLVED) if self.resolved() else pprint(res, NOT_RESOLVED)
        
        return pprint(res, VERBAL_GROUP)


    def flatten(self):
        return [self.vrb_main,
                map(lambda x: x.flatten(), self.sv_sec),
                self.vrb_tense,
                map(lambda x: x.flatten(), self.d_obj),
                map(lambda x: x.flatten(), self.i_cmpl),
                self.vrb_adv,
                self.advrb,
                self.state,
                map(lambda x: x.flatten(), self.vrb_sub_sentence)]



class Comparator():
    """
    This class holds a single method that compares two objects and return True or False.
    The objects should hold a method 'flatten', turning it into a list
    
    """    
    def __init__(self):
        pass
    
    def compare(self, obj1, obj2):
        return obj1.__class__ == obj2.__class__ and \
                obj1.flatten() == obj2.flatten()

def ispronoun(word):
    if word in ResourcePool().pronouns:
        return True
    return False

def concat_gn(nominal_group_structure, new_class, flag):      
    """
    concatenates 2 nominal groups
    Input=2 nominal groups and the flag
    Output= nominal group
    """
    
    #If failure we need to change information else we add 
    if nominal_group_structure.adj!=new_class.adj:
        if flag=='FAILURE':
            nominal_group_structure.adj=new_class.adj
        elif flag=='SUCCESS':
            nominal_group_structure.adj=nominal_group_structure.adj+new_class.adj
    
    #If there is a difference may be it can from 'a' to  'the' or 'this'        
    if new_class.det!= [] and nominal_group_structure.det!=new_class.det:
        nominal_group_structure.det=new_class.det
    
    #We make change if there is 'one' or difference
    if new_class.noun!=[] and nominal_group_structure.noun!=new_class.noun and new_class.noun!=['one']:
        nominal_group_structure.noun=new_class.noun
    
    #If failure we need to change information else we add 
    if flag=='FAILURE' :
        nominal_group_structure.relative=new_class.relative
    else:
        nominal_group_structure.relative=nominal_group_structure.relative+new_class.relative
    
    #If failure we need to change information else we add 
    if flag=='FAILURE':    
        nominal_group_structure.noun_cmpl=new_class.noun_cmpl
    else:
        nominal_group_structure.noun_cmpl=nominal_group_structure.noun_cmpl+new_class.noun_cmpl



def process_verbal_group_part(verbal_group,nominal_group_structure, flag):  
    """
    process merge in the verbal part
    Input=nominal groups, the verbal part and the flag
    Output= nominal group
    """
    
    #The direct complement is a nominal group
    for object in verbal_group.d_obj:
        concat_gn(nominal_group_structure, object, flag)
    
    ind_cmpl=i_cmpl(verbal_group.i_cmpl)
    #For indirect complement
    for i in ind_cmpl:
        if i.prep[0] in ResourcePool().compelement_proposals and verbal_group.vrb_main[0]!='talk':
            #If it is an adverbial related to the noun, we have to add it like a relative
            rltv=Sentence('relative', 'which',[],[verbal_group])
            nominal_group_structure.relative=nominal_group_structure.relative+[rltv] 
        else:
            #Else we process the concatenate with the nominal part of the indirect complement   
            for k in i.gn:
                concat_gn(nominal_group_structure, k, flag)
    
    for i in verbal_group.sv_sec:
        process_verbal_group_part(i,nominal_group_structure, flag)
    
    #For the subsentences
    nominal_group_remerge(verbal_group.vrb_sub_sentence, flag , nominal_group_structure)
    
    return nominal_group_structure



def process_verbal_group_nega_part(verbal_group,nominal_group_structure, flag):  
    """
    process merge in the verbal part when we have negative sentence
    Input=nominal groups, the verbal part and the flag
    Output= nominal group
    """
    
    #The direct complement is a nominal group
    for object in verbal_group.d_obj:
        if object._conjunction=='BUT':
            concat_gn(nominal_group_structure, object, flag)
    
    ind_cmpl=i_cmpl(verbal_group.i_cmpl)
    #For indirect complement
    for i in ind_cmpl:
        
        if i.prep[0] in ResourcePool().compelement_proposals and i.gn[0]._conjunction=='BUT' and verbal_group.vrb_main[0]!='talk':
            #If it is an adverbial related to the noun, we have to add it like a relative
            i.gn[0]._conjunction='AND'
            #We delete the nominal groups before this one 
            verbal_group.i_cmpl=verbal_group.i_cmpl[verbal_group.i_cmpl.index(i):]
            verbal_group.state='affirmative'
            #We continue processing
            rltv=Sentence('relative', 'which',[],[verbal_group])
            if flag=='FAILURE' and nominal_group_structure.relative!=[]:
                nominal_group_structure.relative=[rltv]
            else :
                nominal_group_structure.relative=nominal_group_structure.relative+[rltv]
  
        else:
            #Else we process the concatenate with the nominal part of the indirect complement  
            for k in i.gn:
                if k._conjunction=='BUT':
                    concat_gn(nominal_group_structure, k, flag)
    
    for i in verbal_group.sv_sec:
        process_verbal_group_part(i,nominal_group_structure, flag)
    
    #For the subsentences
    nominal_group_remerge(verbal_group.vrb_sub_sentence, flag , nominal_group_structure)
    
    return nominal_group_structure



def refine_nominal_group_relative_sv (verbal_structure,nominal_group):
    """
    replaces one by the noun in verbal part of relative
    Input=nominal groups and verbal part
    Output= nominal group
    """
    
    #For direct complement
    for object in verbal_structure.d_obj:
        if object.noun==['one']:
            object.noun=nominal_group.noun
        refine_nominal_group_relative(object)
    
    #For indirect complement
    for i_object in verbal_structure.i_cmpl:
        for ng in i_object.gn:
            if ng.noun==['one']:
                ng.noun=nominal_group.noun
            refine_nominal_group_relative(ng)
    
    for second_vrb in verbal_structure.sv_sec:
            refine_nominal_group_relative_sv(second_vrb,nominal_group)



def refine_nominal_group_relative(nominal_group):
    """
    replaces one by the noun in relative
    Input=nominal groups
    Output= nominal group
    """
    
    for i in nominal_group.relative:
        for ns in i.sn:
            if ns.noun==['one']:
                ns.noun=nominal_group.noun
            refine_nominal_group_relative(ns)
        for verbal_structure in i.sv:
            refine_nominal_group_relative_sv(verbal_structure,nominal_group)

def i_cmpl(indirect_complement):
    """
    separates indirect complements when they have same preposition
    Input=indirect complement
    Output=indirect complement
    """

    #init
    i=0

    while i<len(indirect_complement):
        if len(indirect_complement[i].gn)>1:
            list_nominal_group=indirect_complement[i].gn[1:]
            indirect_complement[i].gn=[indirect_complement[i].gn[1]]
            for k in list_nominal_group:
                indirect_complement=indirect_complement+[Indirect_Complement(indirect_complement[i].prep,[k])]
        i=i+1
    return indirect_complement

def nominal_group_remerge(utterance, flag , nominal_group_structure):
    """
    process merge
    Input=nominal groups, the use utterance and the flag      Output= nominal group
    """

    for i in utterance:
        if i.data_type==IMPERATIVE:
            i.data_type=STATEMENT
            i.sn=[Nominal_Group(['the'],i.sv[0].vrb_main,[],[],[])]

        if i.data_type==STATEMENT or i.data_type.startswith(SUBSENTENCE) :
            if i.sv[0].state==Verbal_Group.affirmative:

                #We can have just the subject
                if i.sv[0].d_obj==[] and i.sv[0].i_cmpl==[] and i.sv[0].sv_sec==[] and i.sv[0].vrb_sub_sentence==[]:
                    for k in i.sn:
                        concat_gn(nominal_group_structure, k, flag)
                    refine_nominal_group_relative(nominal_group_structure)
                    return nominal_group_structure

                for k in i.sn:
                    if not ispronoun(k.noun[0]):
                        concat_gn(nominal_group_structure, k, flag)
                #We finish the process with the verbal part
                for v in i.sv:
                    nominal_group_structure=process_verbal_group_part(v,nominal_group_structure, flag)

            elif i.sv[0].state==Verbal_Group.negative:
                #For all other sentences flag will be FAILURE
                flag='FAILURE'

                for k in i.sn:
                    if not ispronoun(k.noun[0]):
                        concat_gn(nominal_group_structure, k, flag)
                #We finish the process with the verbal par
                for v in i.sv:
                    nominal_group_structure=process_verbal_group_nega_part(v,nominal_group_structure, flag)

    refine_nominal_group_relative(nominal_group_structure)
    return nominal_group_structure

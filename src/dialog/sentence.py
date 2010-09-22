# -*- coding: utf-8 -*-

import logging

from helpers import colored_print, level_marker
from resources_manager import ResourcePool


    
class Sentence:
    """
    A sentence is formed from:
    data_type: the type of a sentence whether it is a question, an imperative, ...
    sn : a nominal structure typed into a Nominal_group
    sv : a verbal structure typed into a Verbal_Group
    aim : is used for retrieveing the aim of a question
    """
    
    #List of data types
    statement = "statement"
    imperative = "imperative"
    interjection = "interjection"
    gratulation = "gratulation"
    agree = "agree"
    disagree = "disagree"
    exclamation = "exclamation"
    w_question = "w_question"
    yes_no_question = "yes_no_question"
    subsentence = "subsentence"
    relative = "relative"
    start = "start"
    end = "end"
    

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
            
    def resolved(self):
        """returns True when the whole sentence is completely resolved
        to concepts known by the robot."""
        return  reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.sn), 
                        True) \
                and \
                reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.sv), 
                        True)

    
    def __str__(self):
        res = level_marker() + colored_print(">> " + self.data_type.upper(), 'bold')
        if self.aim:
            res += " (aim: " + self.aim + ')'
        res += '\n'
        
        if self.sn:
            for s in self.sn:
                res += level_marker() + colored_print('nominal grp', 'bold') + ':\n\t' + str(s).replace("\n", "\n\t") +  level_marker() + "\n"
        if self.sv:
            for s in self.sv:
                res += level_marker() + colored_print('verbal grp', 'bold') + ':\n\t' + str(s).replace("\n", "\n\t") + level_marker() + "\n"
        
        #res += "This sentence is " + ("fully resolved." if self.resolved() else "not fully resolved.")
        return res
    
    def flatten(self):
        return [self.data_type,
                self.aim,
                map(lambda x: x.flatten(), self.sn),
                map(lambda x: x.flatten(), self.sv)]
    
    def quit_loop(self):
        #Forget it
        if self.data_type == "imperative" \
            and "forget" in [verb for sv in self.sv for verb in sv.vrb_main]\
            and "affirmative" in [sv.state for sv in self.sv]:
            return True
            
        #[it] doesn't matter'
        if self.data_type == "statement"  \
            and "matter" in [verb for sv in self.sv for verb in sv.vrb_main]\
            and "negative" in [sv.state for sv in self.sv]:
            return True
            
        return False
    
    def learn_it(self):
        #Learn that
        if  self.data_type == "imperative"\
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

    def __str__(self):
        
        res = level_marker()
        
        if self._conjunction != 'AND':
            res += colored_print('[' + self._conjunction + "] ", 'bold')
        
        if self._quantifier != 'ONE':
            res += colored_print('[' + self._quantifier + "] ", 'bold')
            
        if self._resolved:
            res += colored_print(self.id, 'white', 'blue') + '\n' + level_marker() + colored_print('>resolved<', 'green')
            
        else:
            
            
            if self.det:
                res +=   colored_print(self.det, 'yellow') + " " 
            
            
            for k in self.adj:
                res +=  colored_print(k[1], 'red') + " " 
                res +=  colored_print([k[0]], 'green') + " " 
            
            if self.noun:
                res +=   colored_print(self.noun, 'blue') + '\n'
            
            
            if self.noun_cmpl:
                for s in self.noun_cmpl:
                    res += level_marker() + '[OF] \n\t' + str(s).replace("\n", "\n\t") + "\n"
            
            if self.relative:
                for rel in self.relative:
                    res += level_marker() + 'relative:\n\t' + str(rel).replace("\n", "\n\t") + "\n"
        
        return res
    
    
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
        self.nominal_group = nominal_group
        
    def resolved(self):
        return  reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.nominal_group), 
                        True)
        
    def __str__(self):
        res = colored_print(self.prep, 'yellow') + "..."
        
        if self.nominal_group:
            for s in self.nominal_group:
                res += level_marker() + '\n\t' + str(s).replace("\n", "\n\t") + "\n"
        
        return res

    
    def flatten(self):
        return [self.prep,
                map(lambda x: x.flatten(), self.nominal_group)]

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
        res =   level_marker() + colored_print(self.vrb_main, 'magenta') + " (" + str(self.vrb_tense) + ")\n"
        if self.advrb:
            res += level_marker() + 'adverb: ' + colored_print(self.advrb, 'yellow') + "\n"
        if self.vrb_adv:
            res += level_marker() + 'vrb adv: ' + colored_print(self.vrb_adv, 'green') + "\n"
                
        if self.d_obj:
            res += level_marker() + 'direct objects:\n'
            for cmpl in self.d_obj:
                res += '\t' + str(cmpl).replace("\n", "\n\t") + "\n"
        
        if self.i_cmpl:
            res += level_marker() + 'indirect objects:\n'
            for cmpl in self.i_cmpl:
                res += '\t' + str(cmpl).replace("\n", "\n\t") + "\n"
        
        if self.vrb_sub_sentence:
            for vrb_sub_s in self.vrb_sub_sentence:
                res += level_marker() + 'vrb_sub_sentence:\n\t' + str(vrb_sub_s).replace("\n", "\n\t") + "\n"
        
        if self.sv_sec:
            for vrb_sec_s in self.sv_sec:
                res += level_marker() + 'secondary verbal grp:\n\t' + str(vrb_sec_s).replace("\n", "\n\t") + "\n"
        
        res += colored_print(">resolved<", 'green') if self.resolved() else colored_print(">not resolved<", 'red')
        
        return res


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
      
        

def it_is_pronoun(word):
    if word in ResourcePool().pronouns:
        return 1
    return 0
                    
                           
def concat_gn(nominal_group_structure, new_class, flag):      
    """
    concatenates 2 nominal groups                                      
    Input=2 nominal groups and the flag           Output= nominal group                   
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
    Input=nominal groups, the verbal part and the flag      Output= nominal group                   
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
            for k in i.nominal_group:
                concat_gn(nominal_group_structure, k, flag)
    
    for i in verbal_group.sv_sec:
        process_verbal_group_part(i,nominal_group_structure, flag)
    
    #For the subsentences
    nominal_group_remerge(verbal_group.vrb_sub_sentence, flag , nominal_group_structure)
    
    return nominal_group_structure



def process_verbal_group_nega_part(verbal_group,nominal_group_structure, flag):  
    """
    process merge in the verbal part when we have negative sentence                                    
    Input=nominal groups, the verbal part and the flag      Output= nominal group                   
    """
    
    #The direct complement is a nominal group
    for object in verbal_group.d_obj:
        if object._conjunction=='BUT':
            concat_gn(nominal_group_structure, object, flag)
    
    ind_cmpl=i_cmpl(verbal_group.i_cmpl)
    #For indirect complement
    for i in ind_cmpl:
        
        if i.prep[0] in ResourcePool().compelement_proposals and i.nominal_group[0]._conjunction=='BUT' and verbal_group.vrb_main[0]!='talk':
            #If it is an adverbial related to the noun, we have to add it like a relative
            i.nominal_group[0]._conjunction='AND'
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
            for k in i.nominal_group:
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
    Input=nominal groups and verbal part          Output= nominal group                   
    """
    
    #For direct complement
    for object in verbal_structure.d_obj:
        if object.noun==['one']:
            object.noun=nominal_group.noun
        refine_nominal_group_relative(object)
    
    #For indirect complement
    for i_object in verbal_structure.i_cmpl:
        for ng in i_object.nominal_group:
            if ng.noun==['one']:
                ng.noun=nominal_group.noun
            refine_nominal_group_relative(ng)
    
    for second_vrb in verbal_structure.sv_sec:
            refine_nominal_group_relative_sv(second_vrb,nominal_group)



def refine_nominal_group_relative(nominal_group):
    """
    replaces one by the noun in relative                                      
    Input=nominal groups                      Output= nominal group                   
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
    Input=indirect complement                  Output=indirect complement                   
    """
    
    #init
    i=0
    
    while i<len(indirect_complement):
        if len(indirect_complement[i].nominal_group)>1:
            list_nominal_group=indirect_complement[i].nominal_group[1:]
            indirect_complement[i].nominal_group=[indirect_complement[i].nominal_group[1]]
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
        if i.data_type==Sentence.imperative:
            i.data_type=Sentence.statement
            i.sn=[Nominal_Group(['the'],i.sv[0].vrb_main,[],[],[])]
      
        if i.data_type==Sentence.statement or i.data_type.startswith(Sentence.subsentence) :
            if i.sv[0].state==Verbal_Group.affirmative:
            
                #We can have just the subject
                if i.sv[0].d_obj==[] and i.sv[0].i_cmpl==[] and i.sv[0].sv_sec==[] and i.sv[0].vrb_sub_sentence==[]:
                    for k in i.sn:
                        concat_gn(nominal_group_structure, k, flag)
                    refine_nominal_group_relative(nominal_group_structure)
                    return nominal_group_structure
                
                for k in i.sn:
                    if it_is_pronoun(k.noun[0])==0:
                        concat_gn(nominal_group_structure, k, flag)                    
                #We finish the process with the verbal part
                for v in i.sv:
                    nominal_group_structure=process_verbal_group_part(v,nominal_group_structure, flag)        
            
            elif i.sv[0].state==Verbal_Group.negative:
                #For all other sentences flag will be FAILURE
                flag='FAILURE'
                
                for k in i.sn:
                    if it_is_pronoun(k.noun[0])==0:
                        concat_gn(nominal_group_structure, k, flag)
                #We finish the process with the verbal par
                for v in i.sv:
                    nominal_group_structure=process_verbal_group_nega_part(v,nominal_group_structure, flag)   
                
    refine_nominal_group_relative(nominal_group_structure)
    return nominal_group_structure

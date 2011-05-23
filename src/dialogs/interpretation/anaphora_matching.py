#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi
 06/08/2010
 The package contains functions perform the anaphora processing
 Functions:
    delete_redon_nominal_group : to delete the redundancy in the list of nominal groups
    delete_unuse_nominal_group : to delete the pronoun from the list of the nominal groups
    recover_nominal_group_list : to return the list of the nominal groups used by anaphora processing
    first_replacement : to perform the first replacement (before the loop)
"""
import logging
logger = logging.getLogger("dialogs")

from dialogs.sentence import *
from pyoro import OroServerError

class AnaphoraMatcher:
    
    def match_first_object(self, sentences, c_gr):
        list_gr=recover_nominal_group_list(sentences)
        gr = first_replacement(list_gr, c_gr)
            
        return [gr, list_gr]
        


def find_cap_lettre(word):
    """
    return 1 if the word starts with upper case letter                       
    Input=word               Output=flag(0 if no upper case or 1 if upper case)        
    """
    if word==[]:
        return 0
    
    for i in ResourcePool().capital_letters:
        if word[0][0]==i:
            return 1
    return 0



def delete_redon_nominal_group(nominal_group_list):
    """
    delete the redundancy in the list of nominal groups                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    i=0
    j=0
    
    #We have to loop the list twice
    while i < len(nominal_group_list):
        j=i+1
        while j < len(nominal_group_list):
            #If same id => same nominal group
            if nominal_group_list[j].id==nominal_group_list[i].id:
                nominal_group_list=nominal_group_list[:j]+nominal_group_list[j+1:]
                #When we delete => we increment j
                j=j-1
            j=j+1
        i=i+1 
    
    return nominal_group_list



def delete_unuse_nominal_group(nominal_group_list):
    """
    delete the pronoun from the list of the nominal groups                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    i=0
    
    while i < len(nominal_group_list):
        #if a nominal group is an agent's proper noun, we remove it 
        onto_class = []
        try:
            onto_class = ResourcePool().ontology_server.getDirectClassesOf(nominal_group_list[i].id)
        except AttributeError:
            pass
        except OroServerError:
            logger.debug("Nominal group with no ID. pass")
            pass
        
        if onto_class and "Agent" in onto_class.keys():
            nominal_group_list=nominal_group_list[:i]+nominal_group_list[i+1:]
            #When we delete => we increment i
            i=i-1
                
        
        for j in ResourcePool().pronouns:
            #If the nominal group is a pronoun
            if ([j]==nominal_group_list[i].noun and nominal_group_list[i].det==[]):# or find_cap_lettre(nominal_group_list[i].noun)==1:
                nominal_group_list=nominal_group_list[:i]+nominal_group_list[i+1:]
                #When we delete => we increment i
                i=i-1
                break
        
        #We can have a nominal group with just a determinant or adjective
        if i>-1 and nominal_group_list[i].noun==[]:
            nominal_group_list=nominal_group_list[:i]+nominal_group_list[i+1:]
            #When we delete => we increment i
            i=i-1
        
            
        i=i+1
    return nominal_group_list



def recover_nominal_group_list(sentences):
    """
    return the list of the nominal groups used by anaphora processing                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    nominal_group_list=[]

    #We recover all nominal groups of the sentences
    for i in sentences:
        nominal_group_list=nominal_group_list+i.sn
        for j in i.sv:
            nominal_group_list=nominal_group_list+j.d_obj
            
            for x in j.i_cmpl:
                nominal_group_list=nominal_group_list+x.gn
            nominal_group_list=nominal_group_list+recover_nominal_group_list(j.vrb_sub_sentence)
    
    
    #We perform deletions
    nominal_group_list=delete_redon_nominal_group(nominal_group_list)
    nominal_group_list=delete_unuse_nominal_group(nominal_group_list)
    
    #If sentence is empty, we return an empty list      
    return nominal_group_list



def recover_nominal_group_list_without_id(sentences):
    """
    return the list of the nominal groups used by anaphora processing                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    nominal_group_list=[]

    #We recover all nominal groups of the sentences
    for i in sentences:
        nominal_group_list=nominal_group_list+i.sn
        for j in i.sv:
            nominal_group_list=nominal_group_list+j.d_obj
            
            for x in j.i_cmpl:
                nominal_group_list=nominal_group_list+x.gn
            nominal_group_list=nominal_group_list+recover_nominal_group_list(j.vrb_sub_sentence)
    
    #We perform deletions
    nominal_group_list=delete_unuse_nominal_group(nominal_group_list)
    
    #If sentence is empty, we return an empty list      
    return nominal_group_list


def first_replacement(nominal_group_list, current_nominal_group):
    """
    perform the first replacement (before the loop)                          
    Input=nominal group list and the current one       Output=a nominal group or NONE         
    """
    
    #init
    flg=0
    
    if nominal_group_list==[]:
        return None
    
    if current_nominal_group.noun==['it'] or (current_nominal_group.det==['this'] and current_nominal_group.noun==[]):
        return nominal_group_list[0]
    
    #We have to change only the noun
    elif current_nominal_group.noun==['one']:
        if current_nominal_group.det==['this']:
            current_nominal_group.det=nominal_group_list[0].det
        current_nominal_group.noun=nominal_group_list[0].noun
        
        #We add adjectives and delete the redundancy
        for i in nominal_group_list[0].adj:
            for j in current_nominal_group.adj:
                if i==j:
                    flg=1
            if flg==1:
                flg=0
            else:
                current_nominal_group.adj=current_nominal_group.adj+[i]
        
        #For all other information, we perform an addition
        current_nominal_group.noun_cmpl=current_nominal_group.noun_cmpl+nominal_group_list[0].noun_cmpl
        current_nominal_group.relative=current_nominal_group.relative+nominal_group_list[0].relative 
        
        #We affect the if
        current_nominal_group.id=nominal_group_list[0].id
        
        return current_nominal_group
    return None
    


def replacement(utterance, nominal_group, list_nominal_group, last_nominal_group):
    """
    perform the first replacement (before the loop)                          
    Input=nominal group list and the current one       Output=a nominal group or NONE         
    """
    
    #Usually if it is OK the first sentence is agree
    if utterance[0].data_type=='agree':
        return [last_nominal_group,True]
    
    #There is no nominal group to make change (same with first replacement)
    if recover_nominal_group_list_without_id(utterance)==[]:
        nominal_group = first_replacement(list_nominal_group, nominal_group)
        return [nominal_group,False]
    
    #We will use remerge of nominal group to perform anaphora
    nominal_group=nominal_group_remerge(utterance, 'FAILURE' , nominal_group)
    return [nominal_group,True]
    

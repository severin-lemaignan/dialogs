#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi                                                       
 06/08/2010                                                                       
 The package contains functions perform the anaphora processing
 Functions:   
    delete_redon_nom_group : to delete the redundancy in the list of nominal groups                                                                     
    delete_unuse_nom_gr : to delete the pronoun from the list of the nominal groups          
    recover_nom_gr_list : to return the list of the nominal groups used by anaphora processing 
    first_replacement : to perform the first replacement (before the loop)
"""
import logging
logger = logging.getLogger("dialog")

from dialog.sentence import *
from pyoro import OroServerError

class AnaphoraMatcher:
    
    def match_first_object(self, sentences, c_gr):
        list_gr=recover_nom_gr_list(sentences)
        gr = first_replacement(list_gr, c_gr)
            
        return [gr, list_gr]
        
"""
Statement of lists
"""
cap_let_list = ResourcePool().capital_letters
pronoun_list = ResourcePool().pronouns



def find_cap_lettre(word):
    """
    Function return 1 if the word starts with upper case letter                       
    Input=word               Output=flag(0 if no upper case or 1 if upper case)        
    """
    if word==[]:
        return 0
    
    for i in cap_let_list:
        if word[0][0]==i:
            return 1
    return 0



def delete_redon_nom_group(nom_gr_list):
    """
    This function delete the redundancy in the list of nominal groups                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    i=0
    j=0
    
    #We have to loop the list twice
    while i < len(nom_gr_list):
        j=i+1
        while j < len(nom_gr_list):
            #If same id => same nominal group
            if nom_gr_list[j].id==nom_gr_list[i].id:
                nom_gr_list=nom_gr_list[:j]+nom_gr_list[j+1:]
                #When we delete => we increment j
                j=j-1
            j=j+1
        i=i+1 
    
    return nom_gr_list



def delete_unuse_nom_gr(nom_gr_list):
    """
    This function delete the pronoun from the list of the nominal groups                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    i=0
    
    while i < len(nom_gr_list):
        #if a nominal group is an agent's proper noun, we remove it 
        onto_class = []
        try:
            onto_class = ResourcePool().ontology_server.getDirectClassesOf(nom_gr_list[i].id)
        except AttributeError:
            pass
        except OroServerError:
            logger.debug("Nominal group with no ID. pass")
            pass
        
        if onto_class and "Agent" in onto_class.keys():
            nom_gr_list=nom_gr_list[:i]+nom_gr_list[i+1:]
            #When we delete => we increment i
            i=i-1
                
        
        for j in pronoun_list:
            #If the nominal group is a pronoun
            if ([j]==nom_gr_list[i].noun and nom_gr_list[i].det==[]):# or find_cap_lettre(nom_gr_list[i].noun)==1:
                nom_gr_list=nom_gr_list[:i]+nom_gr_list[i+1:]
                #When we delete => we increment i
                i=i-1
                break
        
        #We can have a nominal group with just a determinant or adjective
        if i>-1 and nom_gr_list[i].noun==[]:
            nom_gr_list=nom_gr_list[:i]+nom_gr_list[i+1:]
            #When we delete => we increment i
            i=i-1
        
            
        i=i+1
    return nom_gr_list



def recover_nom_gr_list(sentences):
    """
    This function return the list of the nominal groups used by anaphora processing                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    nom_gr_list=[]

    #We recover all nominal groups of the sentences
    for i in sentences:
        nom_gr_list=nom_gr_list+i.sn
        for j in i.sv:
            nom_gr_list=nom_gr_list+j.d_obj
            
            for x in j.i_cmpl:
                nom_gr_list=nom_gr_list+x.nominal_group
            nom_gr_list=nom_gr_list+recover_nom_gr_list(j.vrb_sub_sentence)
    
    
    #We perform deletions
    nom_gr_list=delete_redon_nom_group(nom_gr_list)
    nom_gr_list=delete_unuse_nom_gr(nom_gr_list)
    
    #If sentence is empty, we return an empty list      
    return nom_gr_list



def recover_nom_gr_list_without_id(sentences):
    """
    This function return the list of the nominal groups used by anaphora processing                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    nom_gr_list=[]

    #We recover all nominal groups of the sentences
    for i in sentences:
        nom_gr_list=nom_gr_list+i.sn
        for j in i.sv:
            nom_gr_list=nom_gr_list+j.d_obj
            
            for x in j.i_cmpl:
                nom_gr_list=nom_gr_list+x.nominal_group
            nom_gr_list=nom_gr_list+recover_nom_gr_list(j.vrb_sub_sentence)
    
    #We perform deletions
    nom_gr_list=delete_unuse_nom_gr(nom_gr_list)
    
    #If sentence is empty, we return an empty list      
    return nom_gr_list


def first_replacement(nom_gr_list, current_nom_gr):
    """
    This function perform the first replacement (before the loop)                          
    Input=nominal group list and the current one       Output=a nominal group or NONE         
    """
    
    #init
    flg=0
    
    if nom_gr_list==[]:
        return None
    
    if current_nom_gr.noun==['it'] or (current_nom_gr.det==['this'] and current_nom_gr.noun==[]):
        return nom_gr_list[0]
    
    #We have to change only the noun
    elif current_nom_gr.noun==['one']:
        if current_nom_gr.det==['this']:
            current_nom_gr.det=nom_gr_list[0].det
        current_nom_gr.noun=nom_gr_list[0].noun
        
        #We add adjectives and delete the redundancy
        for i in nom_gr_list[0].adj:
            for j in current_nom_gr.adj:
                if i==j:
                    flg=1
            if flg==1:
                flg=0
            else:
                current_nom_gr.adj=current_nom_gr.adj+[i]
        
        #For all other information, we perform an addition
        current_nom_gr.noun_cmpl=current_nom_gr.noun_cmpl+nom_gr_list[0].noun_cmpl
        current_nom_gr.relative=current_nom_gr.relative+nom_gr_list[0].relative 
        
        #We affect the if
        current_nom_gr.id=nom_gr_list[0].id
        
        return current_nom_gr
    
    return None
    


def replacement(utterance, nom_gr, list_gr, last_nom_gr):
    """
    This function perform the first replacement (before the loop)                          
    Input=nominal group list and the current one       Output=a nominal group or NONE         
    """
    
    #Usually if it is OK the first sentence is agree
    if utterance[0].data_type=='agree':
        return [last_nom_gr,True]
    
    #There is no nominal group to make change (same with first replacement)
    if recover_nom_gr_list_without_id(utterance)==[]:
        nom_gr = first_replacement(list_gr, nom_gr)
        return [nom_gr,False]
    
    #We will use remerge of nominal group to perform anaphora
    nom_gr=nominal_group_remerge(utterance, 'FAILURE' , nom_gr)
    return [nom_gr,True]




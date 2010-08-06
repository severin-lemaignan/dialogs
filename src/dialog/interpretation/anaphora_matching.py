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
"""
from sentence import *


"""
Statement of lists
"""
pronoun_list=['you', 'I', 'we', 'he', 'she', 'me', 'it', 'he', 'they', 'yours', 'mine', 'him']


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
        for j in pronoun_list:
            #If the nominal group is a pronoun
            if [j]==nom_gr_list[i].noun and nom_gr_list[i].det==[]:
                nom_gr_list=nom_gr_list[:i]+nom_gr_list[i+1:]
                #When we delete => we increment i
                i=i-1
                break
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



def unit_tests():
    

if __name__ == '__main__':
    unit_tests()
    
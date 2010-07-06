#!/usr/bin/python
# -*- coding: utf-8 -*-
#SVN:rev202


"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 21/06/2010                                                                       ##
## The package contains functions that affect the analysis of nominal groups        ##
## We return all elements of a nominal group                                        ##
## Functions:                                                                       ##
##    adjective_pos : to return the postion of the noun in the sentence             ##
##    find_sn_pos : to return the nom_group in a given position with adjective_pos  ##
##    find_sn : to return the first nominal group found in the sentence             ##
##    refine_nom_gr : to refine the nominal group if there is a mistake             ##
##    return_det : to recover the determinant of the nominal group                  ##
##    return_adj : to recover the adjectives of the nominal group                   ##
##    return_noun : to recover the noun of the nominal group                        ##
##    find_nom_gr_compl : to recover the complement noun of the nominal group       ##
##    take_off_nom_gr : to take off a nominal group from the sentence               ##
##    find_relative : to find the position of the relative                          ##
######################################################################################
"""
from resources_manager import ResourcePool
import other_functions


"""
############################## Statement of lists ####################################
"""
pronoun_list=['you', 'I', 'we', 'he', 'she', 'me', 'it', 'he', 'they', 'yours', 'mine', 'him']
det_list=['the', 'a', 'an', 'your', 'his', 'my', 'this', 'her', 'their', 'these', 'that', 'every']


"""
######################################################################################
## We have to read all irregular adjectives before the treatment                    ##
######################################################################################
"""
adjective_list = ResourcePool().adjectives.keys()


"""
######################################################################################
## We have to read all nouns which have a confusion with regular adjectives         ##
######################################################################################
"""
noun_list = ResourcePool().adjectives.keys()


"""
######################################################################################
## This function return the position of the end of the nominal group                ##
## We have to use the list of irregular adjectives                                  ##
## Input=the sentence (list of strings) and the position of the first adjective    ##
## Output=the position of the last word of the nominal group                        ##
######################################################################################
"""
def adjective_pos(phrase, word_pos):

    #If it is the end of the phrase
    if len(phrase)-1==word_pos:
        return 1

    #It is a noun so we have to return 1
    for j in noun_list:
        if phrase[word_pos]==j:
            return 1

    #For the regular adjectives
    if phrase[word_pos].endswith('al'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('est'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('ous'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('ing'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('y'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('less'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('ble'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('ed'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('ful'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('ish'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('ive'):
        return 1+adjective_pos(phrase, word_pos+1)
    if phrase[word_pos].endswith('ic'):
        return 1+adjective_pos(phrase, word_pos+1)

    #We use the irregular adjectives list to find it
    for i in adjective_list:
        if phrase[word_pos]==i:
            adjective_pos(phrase, word_pos+1)
            return 1+ adjective_pos(phrase, word_pos+1)

    #Default case
    return 1


"""
######################################################################################
## We will find the nominal group which is in a known position                      ##
## We have to use adjective_pos to return the end position of nominal group         ##
## Input=the sentence (list of strings) and the position of the nominal group       ##
## Output=the nominal group                                                         ##
######################################################################################
"""
def find_sn_pos (phrase, begin_pos):

    end_pos = 1

    #If it is a pronoun
    for i in pronoun_list:
        if phrase[begin_pos]==i:
            return [phrase[begin_pos]]

    #If there is a nominal group with determinant
    for j in det_list:
        if phrase[begin_pos]==j:
            end_pos= end_pos + adjective_pos(phrase, begin_pos+1)
            return phrase[begin_pos : end_pos+begin_pos]

    #If it is a proper name
    counter=begin_pos
    while (counter<len(phrase) and other_functions.find_cap_lettre(phrase[counter])==1):
        counter=counter+1

    #Cases like 'next week'
    if phrase[begin_pos]=='next' or phrase[begin_pos]=='last':
        end_pos= end_pos + adjective_pos(phrase, begin_pos+1)
        return phrase[begin_pos-1 : end_pos+begin_pos]

    #Default case return [] => ok if counter=begin_pos
    return phrase[begin_pos : counter]


"""
######################################################################################
## We will find the nominal group without the position                              ##
## Input=the sentence (list of strings)                                             ##
## Output=the nominal group                                                         ##
######################################################################################
"""
def find_sn (phrase):
    nb_position=1

    #If phrase is empty
    if phrase ==[]:
        return []

    for x in phrase:
        #If there is a pronoun
        for y in pronoun_list:
            if x==y:
                return [phrase[phrase.index(x)]]

        #If there is a nominal group with determinant
        for j in det_list:
            if x==j:
                nb_position= nb_position + adjective_pos(phrase, phrase.index(x)+1)
                return phrase[phrase.index(x) : phrase.index(x)+nb_position]

        #If there is a proper name
        counter=phrase.index(x)
        while (counter<len(phrase) and other_functions.find_cap_lettre(phrase[counter])==1):
            counter=counter+1
        #Not equal => there is a proper name
        if counter!=phrase.index(x):
            return phrase[phrase.index(x) : counter]

        #Cases like 'next week'
        if x=='last' or x=='next':
            #We replace x by the to have nominal group
            phrase[phrase.index(x)]='the'
            ng= [x]+find_sn_pos(phrase, phrase.index('the'))[1:]
            phrase[phrase.index('the')]=x
            #We take off the proposal
            return ng[1:]

    #Default case
    return []


"""
######################################################################################
## This function refine the nominal group if there is a mistake                     ##
## Input=nominal group                              Output=nominal group            ##
######################################################################################
"""
def refine_nom_gr(nom_gr):

    if nom_gr[len(nom_gr)-1]=='?' or nom_gr[len(nom_gr)-1]=='!' or nom_gr[len(nom_gr)-1]=='.':
        return nom_gr[:len(nom_gr)-1]

    return nom_gr


"""
######################################################################################
## This function returns the determinant of the nominal group                       ##
## Input=nominal group                              Output=the determinant          ##
######################################################################################
"""
def return_det (nom_gr):

    #nom_gr is empty
    if nom_gr==[]:
        return []
    for j in det_list:
        #We return the first element of the list
        if nom_gr[0]==j:
            return [j]
    #Default case
    return []


"""
######################################################################################
## This function returns adjectives of the nominal group                            ##
## Input=nominal group                              Output=the adjective            ##
######################################################################################
"""
def return_adj (nom_gr):

    #If nom_gr is empty
    if nom_gr==[]:
        return []

    #We assumed that the noun represented by 1 element at the end
    for j in det_list:
        if nom_gr[0]==j:
            return nom_gr[1:len(nom_gr)-1]

    #Default case
    return []


"""
######################################################################################
## This function returns the noun of the nominal group                              ##
## Input=nominal group, the determinant and the adjecvtive        Output=the noun   ##
######################################################################################
"""
def return_noun (nom_gr, adjective, determinant):

    #If nom_gr is empty
    if nom_gr==[]:
        return []
    
    return nom_gr[len(determinant)+len(adjective):]


"""
######################################################################################
## We will find the complement of the nominal group which is a nominal group also   ##
## We know the position of the complement so we use find_sn_pos                     ##
## Input=nominal group, his position and the sentence                               ##
## Output=nominal group complement                                                  ##
######################################################################################
"""
def find_nom_gr_compl (nom_gr, phrase, position):

    #If the nom_gr or phrase is empty
    if nom_gr==[]:
        return []

    else:
        #This condition include the case when we have 'of' at the end of the sentence
        if len(phrase)<=len(nom_gr)+position or len(phrase)==len(nom_gr)+position+1:
            return []

        else:
            #We have a complement when there is 'of' before
            if phrase[position+len(nom_gr)]=='of':
                return find_sn_pos(phrase, position+len(nom_gr)+1)

    #Default case
    return []


"""
######################################################################################
## Function to delete the nominal group form the sentence                           ##
## Input=sentence, nominal group and his position               Output=sentence     ##
######################################################################################
"""
def take_off_nom_gr(phrase, nom_gr, nom_gr_pos):

    if nom_gr!=[]:
        
        #If we have to remove the complement
        if phrase[nom_gr_pos-1]=='of' :
            phrase = phrase[:nom_gr_pos-1]+phrase[nom_gr_pos+len(nom_gr):]
        else :
            phrase = phrase[:nom_gr_pos]+phrase[nom_gr_pos+len(nom_gr):]

        #If there is a nominal complement
        while len(phrase)>nom_gr_pos and phrase[nom_gr_pos]=='of' :
            nom_gr=find_sn_pos(phrase, nom_gr_pos+1)
            phrase=take_off_nom_gr(phrase, nom_gr, phrase.index(nom_gr[0]))
           
    return phrase


"""
######################################################################################
## Function to find the position of the relative                                    ##
## Input=sentence, nominal group and his position and the relative's proposal's list##
## Output=the position of the relative                                              ##
######################################################################################
"""
def find_relative (nom_gr, phrase, position, propo_rel_list):

    #Nominal group or phrase is empty
    if nom_gr==[] or phrase ==[]:
        return -1
        
    else:
        #Relative motion is obtained after a proposal
        for i in propo_rel_list:

            #We deleted all nominal groups and their complements => we have not nom_gr+relative but relative only
            if phrase[0:len(nom_gr)]!=nom_gr and phrase[0]==i:
                return 0

            #The proposal is after the nominal group
            if len(phrase)>len(nom_gr)+position+1 and i == phrase[position+len(nom_gr)]:
                return position+len(nom_gr)
    
    return -1

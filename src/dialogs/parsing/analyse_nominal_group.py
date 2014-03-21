#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi
 21/06/2010
 The package contains functions that affect the analysis of nominal groups
 We return all elements of a nominal group
 Functions:
    is_an_adj : to know if a word is an adjective
    adjective_pos : to return the position of the noun in the sentence
    find_sn_pos : to return the nom_group in a given position with adjective_pos
    find_sn : to return the first nominal group found in the sentence
    find_the_plural : to find if there is a plural and add 'a'
    find_plural : to add 'a' for plural
    refine_nom_gr : to refine the nominal group if there is a mistake             
    return_det : to recover the determinant of the nominal group                  
    return_adj : to recover the adjectives of the nominal group
    convert_adj_to_digit : to return the list of adjectives after change number to digit
    process_adj_quantifier : to return adjectives of the nominal group organized with quantifier
    return_noun : to recover the noun of the nominal group                        
    find_nom_gr_compl : to recover the complement noun of the nominal group       
    take_off_nom_gr : to take off a nominal group from the sentence               
    find_relative : to find the position of the relative                          
    complete_relative : to complete the relative with her object 
"""
from dialogs.resources_manager import ResourcePool
import other_functions

def is_an_adj(word):
    """Determines if a word is an adjective

    :param string word: a word

    :return: True if the word is recognized as an adjective, False else. 
    """

    #It is a noun verb pronoun or determinant so we have to return False
    if word in ResourcePool().special_nouns + ResourcePool().special_verbs + ResourcePool().pronouns + ResourcePool().determinants:
        return False

    #For the regular adjectives
    for k in ResourcePool().adjective_rules:
        if word.endswith(k):
            return True

    #For adjectives created from numbers
    if word.endswith('th') and other_functions.number(word) == 2:
        return True

    #We use the irregular adjectives list to find it
    if word in ResourcePool().adjectives.keys()+ResourcePool().adjective_numbers+ResourcePool().adj_quantifiers:
        return True

    return False

def adjective_pos(sentence, word_pos):
    """
    Returns the position of the end of the nominal group                
    We have to use the list of irregular adjectives                                  
    
    :param list sentence: the sentence (list of strings)
    :param word_pos: the position of the first adjective    
    :return: the position of the last word of the nominal group                       
    """
    
    #If it is the end of the sentence
    if len(sentence)-1<=word_pos:
        return 1
    
    #The case of '2 of them'
    if sentence[word_pos]=='of':
        return 0
    
    #It is a noun so we have to return 1
    if sentence[word_pos] in ResourcePool().special_nouns:
        return 1
    
    #For the regular adjectives
    for k in ResourcePool().adjective_rules:
        if sentence[word_pos].endswith(k):
            return 1+adjective_pos(sentence, word_pos+1)
    
    #For adjectives created from numbers
    if sentence[word_pos].endswith('th') and other_functions.number(sentence[word_pos])==2:
        return 1+adjective_pos(sentence, word_pos+1)
    
    #We use the irregular adjectives list to find it
    if sentence[word_pos] in ResourcePool().adjectives.keys()+ResourcePool().adjective_numbers+ResourcePool().adj_quantifiers:
        return 1+ adjective_pos(sentence, word_pos+1)

    #Default case
    return 1



def find_sn_pos (sentence, begin_pos):
    """
    We will find the nominal group which is in a known position                      
    We have to use adjective_pos to return the end position of nominal group         

    :param list sentence: the sentence (list of strings)
    :param begin_pos:the position of the nominal group       
    :return: the nominal group (as a list of words)
    """
    
    if begin_pos>=len(sentence):
        return []
    
    end_pos = 1
    
    #If it is a pronoun
    if sentence[begin_pos] in ResourcePool().pronouns:
        return [sentence[begin_pos]]

    #If there is a nominal group with determinant
    if sentence[begin_pos] in ResourcePool().determinants:
        end_pos += adjective_pos(sentence, begin_pos + 1)
        return sentence[begin_pos : end_pos+begin_pos]
    
    #If we have 'something'
    for k in ResourcePool().composed_nouns:
        if sentence[begin_pos].startswith(k):
            if sentence[begin_pos] in ResourcePool().noun_not_composed:
                return []
            return [sentence[begin_pos]]    
       
    #If there is a number, it will be the same with determinant
    if other_functions.number(sentence[begin_pos])==1:
        end_pos += adjective_pos(sentence, begin_pos + 1)
        return sentence[begin_pos : end_pos+begin_pos]

    #If it is a proper name
    counter=begin_pos
    while (counter<len(sentence) and other_functions.find_cap_lettre(sentence[counter])==1):
        counter += 1
    
    #Default case return [] => ok if counter=begin_pos
    return sentence[begin_pos : counter]



def find_sn (sentence):
    """
    Returns the first nominal group found in the sentence.                              
    
    :param list sentence: the sentence as a list of words                                             
    :return: the nominal group                                                        
    """

    nb_position=1

    #If sentence is empty
    if sentence ==[]:
        return []

    for x in sentence:
        #If there is a pronoun
        if x in ResourcePool().pronouns:
            return [sentence[sentence.index(x)]]

        #If there is a nominal group with determinant
        if x in ResourcePool().determinants:
            nb_position += adjective_pos(sentence, sentence.index(x) + 1)
            return sentence[sentence.index(x) : sentence.index(x)+nb_position]
        
        #If we have 'something'
        for k in ResourcePool().composed_nouns:
            if x.startswith(k):
                if x in ResourcePool().noun_not_composed:
                    return []
                return [sentence[sentence.index(x)]]
        
        #If there is a number, it will be the same with determinant
        if other_functions.number(x)==1:
            nb_position += adjective_pos(sentence, sentence.index(x) + 1)
            return sentence[sentence.index(x) : sentence.index(x)+nb_position]

        #If there is a proper name
        counter=sentence.index(x)
        while (counter<len(sentence) and other_functions.find_cap_lettre(sentence[counter])==1):
            counter += 1
        #Not equal => there is a proper name
        if counter!=sentence.index(x):
            return sentence[sentence.index(x) : counter]
   
    #Default case
    return []



def find_the_plural(sentence, position):
    """ Finds if there is a plural and add 'a'

    :param sentence and position of nominal group
    :return: the position of plural or -1
    """ 
    
    if len(sentence) - position - 1 < 0:
        return -1
    
    #It is a number the word is not a plural
    if other_functions.number(sentence[position]) == 1:
        return -1
    
    #If it is proposal we continue
    if sentence[position] in ResourcePool().proposals:
        return find_the_plural(sentence, position+1)
    
    if sentence[position] in ResourcePool().nouns_end_s:
        return -1
    
    #If it is adjective we continue
    if is_an_adj(sentence[position]):
        if find_the_plural(sentence, position+1)!=-1:
            return position
    
    #If it is an  adjective ends with 's'
    if sentence[0].endswith("'s") or sentence[position].endswith("ous"):
        return -1
    
    #we have plural if the noun ends with 's'
    if find_sn_pos(sentence, position) == [] and sentence[position].endswith('s'):
        return position

    return -1



def find_plural(sentence):
    """Adds 'a' for plural

    :param list sentence: sentence
    :return: sentence
    """

    #We find the position of the plural in the sentence
    position=find_the_plural(sentence,0)
    if position != -1:
        #If not -1 we have plural without determinant
        sentence = sentence[:position] + ['a'] + sentence[position:]
    return sentence



def refine_nom_gr(nominal_group):
    """This function refine the nominal group if there is a mistake

    :param nominal_group: nominal group
    :return: nominal group
    """

    idx = len(nominal_group)-1
    
    #Case of the end of the sentence
    if nominal_group[idx] in ['?','!','.']:
        return nominal_group[:idx]
    
    #Case of after we have a indirect complement
    if nominal_group[idx] in ResourcePool().proposals:
        return nominal_group[:idx]
    
    #Case of after we have an adverb
    if nominal_group[idx] in ResourcePool().adverbs:
        return nominal_group[:idx]
    return nominal_group


def return_det (nominal_group):
    """
    This function returns the determinant of the nominal group                       
    :param nominal group                           
    :return: the determinant          
    """

    #nominal_group is empty
    if nominal_group==[]:
        return []
    
    #We return the first element of the list
    if nominal_group[0] in ResourcePool().determinants:
        return [nominal_group[0]]
    
    #If there is a number
    if other_functions.number(nominal_group[0])==1:
        return [nominal_group[0]]
     
    #Default case
    return []



def return_adj (nominal_group):
    """Returns adjectives of the nominal group

    :param Nominal_Group nominal_group: a nominal group

    :return: a list of adjectives
    """
    
    #init
    k=1
    adj_list=[]
    
    #If nominal_group is empty
    if nominal_group==[]:
        return []

    #We assumed that the noun represented by 1 element at the end
    if nominal_group[0] in ResourcePool().determinants:
        while k < len(nominal_group):
            if is_an_adj(nominal_group[k]):
                adj_list = adj_list + [nominal_group[k]]
            k += 1
    return adj_list



def convert_adj_to_digit(adj_list):
    """
    returns the list of adjectives after change number to digit                           
    :param the adjective                            
    :return: the adjective            
    """
    
    for i in adj_list:
        if i.endswith('th') and other_functions.number(i)==2:
            adj_list[adj_list.index(i)]=other_functions.convert_to_digit(i)+'th'
    
    return adj_list



def process_adj_quantifier(adj_list):    
    """
    returns adjectives of the nominal group organized with quantifier                           
    :param the adjective                            
    :return: the adjective            
    """
    
    #init
    adjective_list=[]   
    
    #Now, we will put quantifier (if it exist) with the adjective
    z=len(adj_list)-1
    if z==0:
        adjective_list=[[adj_list[z],[]]]+adjective_list
    else:
        while z >= 0:
            if adj_list[z] in ResourcePool().adj_quantifiers:
                #We can't have quantifier if there is no adjective
                adjective_list[0][1]=[adj_list[z]]+adjective_list[0][1]
            else:
                adjective_list=[[adj_list[z],[]]]+adjective_list

            z -= 1
    return adjective_list



def return_noun (nominal_group, adjective, determinant):
    """
    returns the noun of the nominal group
    :param nominal group, the determinant and the adjecvtive     
    :return: the noun   
    """

    #If nominal_group is empty
    if nominal_group==[] or nominal_group[len(determinant)+len(adjective):]==[]:
        return []
    return [" ".join(nominal_group[len(determinant)+len(adjective):])]



def find_nom_gr_compl (nominal_group, sentence, position):
    """
    We will find the complement of the nominal group which is also a nominal group
    We know the position of the complement so we use find_sn_pos                     

    :param nominal_group: the nominal group we look the complement for
    :param sentence: the complete sentence as a list of words
    :param position: the position of the nominal group in the sentence
    :return: nominal group complement                                                 
    """

    #If the nominal_group or sentence is empty
    if nominal_group==[]:
        return []
    else:
        #This condition include the case when we have 'of' at the end of the sentence
        if len(sentence)<=len(nominal_group)+position or len(sentence)==len(nominal_group)+position+1:
            return []
        else:
            #We have a complement when there is 'of' before
            if sentence[position+len(nominal_group)]=='of':
                return find_sn_pos(sentence, position+len(nominal_group)+1)
    #Default case
    return []



def take_off_nom_gr(sentence, nominal_group, nominal_group_pos):
    """
    Function to delete the nominal group form the sentence                           
    
    :param sentence: the original sentence
    :param nomianl_group: the nominal group to wipe off
    :param nominal_group_pos: the position of the nominal group in the sentence            
    :return: the modified sentence     
    """

    if nominal_group:
        
        #If we have to remove the complement
        if sentence[nominal_group_pos-1] == 'of' :
            sentence = sentence[:nominal_group_pos-1]+sentence[nominal_group_pos+len(nominal_group):]
        else :
            sentence = sentence[:nominal_group_pos]+sentence[nominal_group_pos+len(nominal_group):]

        #If there is a nominal complement
        while len(sentence)>nominal_group_pos and sentence[nominal_group_pos]=='of' :
            nominal_group=find_sn_pos(sentence, nominal_group_pos+1)
            sentence=take_off_nom_gr(sentence, nominal_group, sentence.index(nominal_group[0]))
           
    return sentence



def find_relative (nominal_group, sentence, position, propo_rel_list):
    """
    Function to find the position of the relative                                    

    :param nominal_group: the object of the relative 
    :param sentence: the sentence to search in 
    :param position: the nominal group position
    :param propo_rel_list: the relative's proposal's list
    :return: the position of the relative or -1 if there is no relative                                        
    """

    # Nominal group or sentence is empty
    if not nominal_group or not sentence:
        return -1

    # Relative motion is obtained after a proposal

    # We deleted all nominal groups and their complements 
    # => we have not nominal_group+relative but relative only
    if sentence[0:len(nominal_group)] != nominal_group \
       and sentence[0] in propo_rel_list:
        return 0
    #The proposal is after the nominal group
    if len(sentence) > len(nominal_group) + position + 1 \
       and sentence[position + len(nominal_group)] in propo_rel_list:
        return position+len(nominal_group)
    
    return -1



def complete_relative(sentence, object):
    """
    Completes the relative with her object                                    
    
    :param sentence: the relative
    :param object: the object of the relative (its nominal group)
    :return: relative concatenated to the nominal group                                        
    """
    
    #init
    i=0
    
    #If there is a subject, the relative proposal refer to direct or indirect complement
    if find_sn_pos(sentence, 0)!=[]:
        
        while i < len(sentence):
            if sentence[i] in ResourcePool().proposals and find_sn_pos(sentence, i+1)==[]:
                #It is an indirect complement
                sentence=sentence[:i+1]+object+sentence[i+1:]
                return sentence
            
            elif sentence[i] in ResourcePool().proposals:
                #We don't have an indirect object
                i += len(find_sn_pos(sentence, i + 1))

            i += 1
        #It is a direct complement
        sentence=sentence+object
   
    #Default case
    return sentence               

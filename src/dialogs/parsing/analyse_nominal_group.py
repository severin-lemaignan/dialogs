#!/usr/bin/python
# -*- coding: utf-8 -*-
#SVN:rev202


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

def adjective_pos(phrase, word_pos):
    """
    returns the position of the end of the nominal group                
    We have to use the list of irregular adjectives                                  
    Input=the sentence (list of strings) and the position of the first adjective    
    Output=the position of the last word of the nominal group                       
    """
    
    #If it is the end of the phrase
    if len(phrase)-1<=word_pos:
        return 1
    
    #The case of '2 of them'
    if phrase[word_pos]=='of':
        return 0
    
    #It is a noun so we have to return 1
    if phrase[word_pos] in ResourcePool().special_nouns:
        return 1
    
    #For the regular adjectives
    for k in ResourcePool().adjective_rules:
        if phrase[word_pos].endswith(k):
            return 1+adjective_pos(phrase, word_pos+1)
    
    #For adjectives created from numbers
    if phrase[word_pos].endswith('th') and other_functions.number(phrase[word_pos])==2:
        return 1+adjective_pos(phrase, word_pos+1)
    
    #We use the irregular adjectives list to find it
    if phrase[word_pos] in ResourcePool().adjectives.keys()+ResourcePool().adjective_numbers+ResourcePool().adj_quantifiers:
        return 1+ adjective_pos(phrase, word_pos+1)

    #Default case
    return 1



def find_sn_pos (phrase, begin_pos):
    """
    We will find the nominal group which is in a known position                      
    We have to use adjective_pos to return the end position of nominal group         
    Input=the sentence (list of strings) and the position of the nominal group       
    Output=the nominal group                                                         
    """
    
    if begin_pos>=len(phrase):
        return []
    
    end_pos = 1
    
    #If it is a pronoun
    if phrase[begin_pos] in ResourcePool().pronouns:
        return [phrase[begin_pos]]

    #If there is a nominal group with determinant
    if phrase[begin_pos] in ResourcePool().determinants:
        end_pos= end_pos + adjective_pos(phrase, begin_pos+1)
        return phrase[begin_pos : end_pos+begin_pos]
    
    #If we have 'something'
    for k in ResourcePool().composed_nouns:
        if phrase[begin_pos].startswith(k):
            if phrase[begin_pos] in ResourcePool().noun_not_composed:
                return []
            return [phrase[begin_pos]]    
       
    #If there is a number, it will be the same with determinant
    if other_functions.number(phrase[begin_pos])==1:
        end_pos= end_pos + adjective_pos(phrase, begin_pos+1)
        return phrase[begin_pos : end_pos+begin_pos]

    #If it is a proper name
    counter=begin_pos
    while (counter<len(phrase) and other_functions.find_cap_lettre(phrase[counter])==1):
        counter=counter+1
    
    #Default case return [] => ok if counter=begin_pos
    return phrase[begin_pos : counter]



def find_sn (phrase):
    """
    We will find the nominal group without the position                              
    Input=the sentence (list of strings)                                             
    Output=the nominal group                                                        
    """

    nb_position=1

    #If phrase is empty
    if phrase ==[]:
        return []

    for x in phrase:
        #If there is a pronoun
        if x in ResourcePool().pronouns:
            return [phrase[phrase.index(x)]]

        #If there is a nominal group with determinant
        if x in ResourcePool().determinants:
            nb_position= nb_position + adjective_pos(phrase, phrase.index(x)+1)
            return phrase[phrase.index(x) : phrase.index(x)+nb_position]
        
        #If we have 'something'
        for k in ResourcePool().composed_nouns:
            if x.startswith(k):
                if x in ResourcePool().noun_not_composed:
                    return []
                return [phrase[phrase.index(x)]]
        
        #If there is a number, it will be the same with determinant
        if other_functions.number(x)==1:
            nb_position= nb_position + adjective_pos(phrase, phrase.index(x)+1)
            return phrase[phrase.index(x) : phrase.index(x)+nb_position]

        #If there is a proper name
        counter=phrase.index(x)
        while (counter<len(phrase) and other_functions.find_cap_lettre(phrase[counter])==1):
            counter=counter+1
        #Not equal => there is a proper name
        if counter!=phrase.index(x):
            return phrase[phrase.index(x) : counter]
   
    #Default case
    return []



def find_the_plural(phrase, position):
    """ Finds if there is a plural and add 'a'

    Input=sentence and position of nominal group   Output=the position of plural or -1
    """ 
    
    if len(phrase) - position - 1 < 0:
        return -1
    
    #It is a number the word is not a plural
    if other_functions.number(phrase[position]) == 1:
        return -1
    
    #If it is proposal we continue
    if phrase[position] in ResourcePool().proposals:
        return find_the_plural(phrase, position+1)
    
    if phrase[position] in ResourcePool().nouns_end_s:
        return -1
    
    #If it is adjective we continue
    if is_an_adj(phrase[position]):
        if find_the_plural(phrase, position+1)!=-1:
            return position
    
    #If it is an  adjective ends with 's'
    if phrase[0].endswith("'s") or phrase[position].endswith("ous"):
        return -1
    
    #we have plural if the noun ends with 's'
    if find_sn_pos(phrase, position) == [] and phrase[position].endswith('s'):
        return position

    return -1



def find_plural(phrase):
    """Adds 'a' for plural

    :param list phrase: sentence
    :return: sentence
    """

    #We find the position of the plural in the phrase
    position=find_the_plural(phrase,0)
    if position != -1:
        #If not -1 we have plural without determinant
        phrase = phrase[:position] + ['a'] + phrase[position:]
    return phrase



def refine_nom_gr(nom_gr):
    """This function refine the nominal group if there is a mistake

    :param nom_gr: nominal group
    :return: nominal group
    """

    #Case of the end of the sentence
    if nom_gr[len(nom_gr)-1]=='?' or nom_gr[len(nom_gr)-1]=='!' or nom_gr[len(nom_gr)-1]=='.':
        return nom_gr[:len(nom_gr)-1]
    
    #Case of after we have a indirect complement
    if nom_gr[len(nom_gr)-1] in ResourcePool().proposals:
        return nom_gr[:len(nom_gr)-1]
    
    #Case of after we have an adverb
    if nom_gr[len(nom_gr)-1] in ResourcePool().adverbs:
        return nom_gr[:len(nom_gr)-1]
    return nom_gr



def return_det (nom_gr):
    """
    This function returns the determinant of the nominal group                       
    Input=nominal group                              Output=the determinant          
    """

    #nom_gr is empty
    if nom_gr==[]:
        return []
    
    #We return the first element of the list
    if nom_gr[0] in ResourcePool().determinants:
        return [nom_gr[0]]
    
    #If there is a number
    if other_functions.number(nom_gr[0])==1:
        return [nom_gr[0]]
     
    #Default case
    return []



def return_adj (nom_gr):
    """Returns adjectives of the nominal group

    :param Nominal_Group nom_gr: a nominal group

    :return: a list of adjectives
    """
    
    #init
    k=1
    adj_list=[]
    
    #If nom_gr is empty
    if nom_gr==[]:
        return []

    #We assumed that the noun represented by 1 element at the end
    if nom_gr[0] in ResourcePool().determinants:
        while k < len(nom_gr):
            if is_an_adj(nom_gr[k]):
                adj_list = adj_list + [nom_gr[k]]
            k = k + 1
    return adj_list



def convert_adj_to_digit(adj_list):
    """
    returns the list of adjectives after change number to digit                           
    Input=the adjective                               Output=the adjective            
    """
    
    for i in adj_list:
        if i.endswith('th') and other_functions.number(i)==2:
            adj_list[adj_list.index(i)]=other_functions.convert_to_digit(i)+'th'
    
    return adj_list



def process_adj_quantifier(adj_list):    
    """
    returns adjectives of the nominal group organized with quantifier                           
    Input=the adjective                               Output=the adjective            
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
            
            z=z-1     
    return adjective_list



def return_noun (nom_gr, adjective, determinant):
    """
    returns the noun of the nominal group
    Input=nominal group, the determinant and the adjecvtive        Output=the noun   
    """

    #If nom_gr is empty
    if nom_gr==[] or nom_gr[len(determinant)+len(adjective):]==[]:
        return []
    return [" ".join(nom_gr[len(determinant)+len(adjective):])]



def find_nom_gr_compl (nom_gr, phrase, position):
    """
    We will find the complement of the nominal group which is a nominal group also   
    We know the position of the complement so we use find_sn_pos                     
    Input=nominal group, his position and the sentence                               
    Output=nominal group complement                                                 
    """

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



def take_off_nom_gr(phrase, nom_gr, nom_gr_pos):
    """
    Function to delete the nominal group form the sentence                           
    Input=sentence, nominal group and his position               Output=sentence     
    """

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



def find_relative (nom_gr, phrase, position, propo_rel_list):
    """
    Function to find the position of the relative                                    
    Input=sentence, nominal group and his position and the relative's proposal's list
    Output=the position of the relative or -1 if there is no relative                                        
    """

    #Nominal group or phrase is empty
    if nom_gr==[] or phrase ==[]:
        return -1

    #Relative motion is obtained after a proposal
    else:
        #We deleted all nominal groups and their complements => we have not nom_gr+relative but relative only
        if phrase[0:len(nom_gr)]!=nom_gr and phrase[0] in propo_rel_list:
            return 0
        #The proposal is after the nominal group
        if len(phrase)>len(nom_gr)+position+1 and phrase[position+len(nom_gr)] in propo_rel_list:
            return position+len(nom_gr)
    
    return -1



def complete_relative(phrase, sbj):
    """
    completes the relative with her object                                    
    Input=relative, the object of the relative (his nominal group)
    Output=relative concatenated to the nominal group                                        
    """
    
    #init
    i=0
    
    #If there is a subject, the relative proposal refer to direct or indirect complement
    if find_sn_pos(phrase, 0)!=[]:
        
        while i < len(phrase):
            if phrase[i] in ResourcePool().proposals and find_sn_pos(phrase, i+1)==[]:
                #It is an indirect complement
                phrase=phrase[:i+1]+sbj+phrase[i+1:]
                return phrase
            
            elif phrase[i] in ResourcePool().proposals:
                #We don't have an indirect object
                i=i+len(find_sn_pos(phrase, i+1))
            
            i=i+1
        #It is a direct complement
        phrase=phrase+sbj
   
    #Default case
    return phrase               

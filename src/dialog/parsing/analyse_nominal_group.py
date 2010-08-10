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
    find_plural : to find if there is a plural and add 'a'    
    refine_nom_gr : to refine the nominal group if there is a mistake             
    return_det : to recover the determinant of the nominal group                  
    return_adj : to recover the adjectives of the nominal group                   
    return_noun : to recover the noun of the nominal group                        
    find_nom_gr_compl : to recover the complement noun of the nominal group       
    take_off_nom_gr : to take off a nominal group from the sentence               
    find_relative : to find the position of the relative                          
    complete_relative : to complete the relative with her object 
"""
from resources_manager import ResourcePool
import other_functions


"""
Statement of lists
"""
pronoun_list=['you', 'I', 'we', 'he', 'she', 'me', 'it', 'he', 'they', 'yours', 'mine', 'him']
det_list=['that','the', 'a', 'an', 'your', 'his', 'my', 'this', 'her', 'their', 'these', 
          'every', 'there', 'some', 'any', 'those','all','no','more','less', 'another']
proposal_list=['in', 'on', 'at', 'from', 'to', 'about', 'for', 'next', 'last', 'ago', 
               'with', 'by', 'behind','behind+to','next+to','in+front+of','as', 'into']
adv_list=['here','tonight', 'yesterday', 'tomorrow', 'today', 'now']
adj_rules=['al','ous','est','ing','y','less','ble','ed','ful','ish','ive','ic']
composed_noun=['some', 'any', 'no']
end_s_list=['is', 'this']
word_list=['now']
superlative_number=['first','second','third','fifth','ninth']



"""
We have to read all irregular adjectives before the processing                    
"""
adjective_list = ResourcePool().adjectives.keys()


"""
We have to read all nouns which have a confusion with regular adjectives        
"""
noun_list = ResourcePool().special_nouns



def is_an_adj(word):
    """
    This function to know if a word is an adjective                                  
    Input=word                Output=1 if it is an adjective and 0 if not                     
    """
    
    #It is a noun so we have to return 1
    for j in noun_list:
        if word==j[0]:
            return 0
    
    #For the regular adjectives
    for k in adj_rules:
        if word.endswith(k):
            return 1
    
    #For adjectives created from numbers
    if word.endswith('th') and other_functions.number(word)==2:
        return 1
        
    #We use the irregular adjectives list to find it
    for i in adjective_list+superlative_number:
        if word==i:
            return 1
    
    return 0

    
    
def adjective_pos(phrase, word_pos):
    """
    This function return the position of the end of the nominal group                
    We have to use the list of irregular adjectives                                  
    Input=the sentence (list of strings) and the position of the first adjective    
    Output=the position of the last word of the nominal group                       
    """

    #If it is the end of the phrase
    if len(phrase)-1==word_pos:
        return 1

    #It is a noun so we have to return 1
    for j in noun_list:
        if phrase[word_pos]==j[0]:
            return 1
    
    #For the regular adjectives
    for k in adj_rules:
        if phrase[word_pos].endswith(k):
            return 1+adjective_pos(phrase, word_pos+1)
    
    #For adjectives created from numbers
    if phrase[word_pos].endswith('th') and other_functions.number(phrase[word_pos])==2:
        return 1+adjective_pos(phrase, word_pos+1)
    
    #We use the irregular adjectives list to find it
    for i in adjective_list+superlative_number:
        if phrase[word_pos]==i:
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
    for i in pronoun_list:
        if phrase[begin_pos]==i:
            return [phrase[begin_pos]]

    #If there is a nominal group with determinant
    for j in det_list:
        if phrase[begin_pos]==j:
            end_pos= end_pos + adjective_pos(phrase, begin_pos+1)
            return phrase[begin_pos : end_pos+begin_pos]
    
    #If we have 'something'
    for k in composed_noun:
        if phrase[begin_pos].startswith(k):
            for l in word_list:
                if l==phrase[begin_pos]:
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

    #Cases like 'next week'
    if phrase[begin_pos]=='next' or phrase[begin_pos]=='last':
        end_pos= end_pos + adjective_pos(phrase, begin_pos+1)
        return phrase[begin_pos-1 : end_pos+begin_pos]

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
        for y in pronoun_list:
            if x==y:
                return [phrase[phrase.index(x)]]

        #If there is a nominal group with determinant
        for j in det_list:
            if x==j:
                nb_position= nb_position + adjective_pos(phrase, phrase.index(x)+1)
                return phrase[phrase.index(x) : phrase.index(x)+nb_position]
        
        #If we have 'something'
        for k in composed_noun:
            if x.startswith(k):
                for l in word_list:
                    if l==x:
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



def find_plural(phrase, position):
    """
    This function find if there is a plural and add 'a'                     
    Input=sentence and position of nominal group         Output=sentence            
    """ 
    if position>len(phrase)-1:
        return phrase
    
    for i in end_s_list:
        if i==phrase[position]:
            return phrase
    
    if phrase[position].endswith("'s") or phrase[position].endswith("ous"):
        return phrase
    
    if find_sn_pos(phrase, position)==[] and phrase[position].endswith('s'):
        #It can not be a verb
        phrase=['a']+phrase
    return phrase



def refine_nom_gr(nom_gr):
    """
    This function refine the nominal group if there is a mistake                     
    Input=nominal group                              Output=nominal group            
    """

    #Case of the end of the sentence
    if nom_gr[len(nom_gr)-1]=='?' or nom_gr[len(nom_gr)-1]=='!' or nom_gr[len(nom_gr)-1]=='.':
        return nom_gr[:len(nom_gr)-1]
    
    #Case of after we have a indirect complement
    for i in proposal_list:
        if nom_gr[len(nom_gr)-1]==i:
            return nom_gr[:len(nom_gr)-1]
    
    #Case of after we have an adverb
    for i in adv_list:
        if nom_gr[len(nom_gr)-1]==i:
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
    for j in det_list:
        #We return the first element of the list
        if nom_gr[0]==j:
            return [j]
    
    #If there is a number
    if other_functions.number(nom_gr[0])==1:
        return [nom_gr[0]]
     
    #Default case
    return []



def return_adj (nom_gr):
    """
    This function returns adjectives of the nominal group                            
    Input=nominal group                              Output=the adjective            
    """
    
    #init
    k=1
    adj_list=[]
    
    #If nom_gr is empty
    if nom_gr==[]:
        return []

    #We assumed that the noun represented by 1 element at the end
    for j in det_list:
        if nom_gr[0]==j:
            while k < len(nom_gr):
                if is_an_adj(nom_gr[k])==1:
                    adj_list=adj_list+[nom_gr[k]]
                k=k+1
    return adj_list



def return_noun (nom_gr, adjective, determinant):
    """
    This function returns the noun of the nominal group
    Input=nominal group, the determinant and the adjecvtive        Output=the noun   
    """

    #If nom_gr is empty
    if nom_gr==[]:
        return []
    
    return nom_gr[len(determinant)+len(adjective):]



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



def complete_relative(phrase, sbj):
    """
    Function to complete the relative with her object                                    
    Input=relative, the object of the relative (his nominal group)
    Output=relative concatenated to the nominal group                                        
    """
    
    #init
    i=0
    
    #If there is a subject, the relative proposal refer to direct or indirect complement
    if find_sn_pos(phrase, 0)!=[]:
        
        while i < len(phrase):
            for j in proposal_list:
                if j==phrase[i] and find_sn_pos(phrase, i+1)==[]:
                    #It is an indirect complement
                    phrase=phrase[:i+1]+sbj+phrase[i+1:]
                    return phrase
                elif j==phrase[i]:
                    i=i+len(find_sn_pos(phrase, i+1))
            i=i+1
        
        #It is a direct complement
        phrase=phrase+sbj
   
    #Default case
    return phrase               
    
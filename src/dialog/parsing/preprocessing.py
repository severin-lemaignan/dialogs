#!/usr/bin/python
# -*- coding: utf-8 -*-
# SVN:rev202 + PythonTidy

"""
 Created by Chouayakh Mahdi                                                       
 22/06/2010                                                                       
 The package contains functions which are important for the pre-parsing
 We return a list of all sentence in the utterance to do processing                    
 Functions:                                                                       
    delete_and_from_number : to delete 'and' between two numbers
    concat_number : to concatenate numbers with '+'
    upper_to_lower : to process the upper case at the beginning of the sentence        
    concatenate_pos : to concatenate an element in a position given               
    case_apostrophe_s_to_is : to know if there is this kind of "'s"               
    expand_contractions : to perform expand contraction using concatenate_pos     
    determination_nom_gr : to return the nominal group with his complement
    and_nom_group : to process the case when there is a comma between nominal groups                                               
    find_nom_gr_list : take off noun chain linked by 'of'                         
    create_possession_claus : to transform a noun chain to string's list with 'of'
    possesion_form : to exchange the "'s" to 'of' by using 2 latest functions    
    other_processing : to perform other processing                                 
    move_prep : to put the preposition before the nominal group
    or_processing : to create a nominal group before and after the 'or'
    reorganize_adj : to delete ',' and 'and' if it is between adjectives*
    subsentence_comma : to delete ',' or changed on ';'
    delete_empty : to delete '' from sentence
    remerge_sentences : to transform some sentences of the remerge part
    processing : is used by process_sentence
    process_sentence : to split utterance into many sentences using all other functions 
"""
from resources_manager import ResourcePool
from resources_manager import ThematicRolesDict
import analyse_nominal_group
import other_functions


"""
Statement of lists
"""
apostrophe_s_to_is_list=["he's", "she's", "it's", "that's", "what's", "who's", "how's"]
replacement_tuples=[("won't",['will', 'not']),("wanna",['want', 'to']),("gonna",['going', 'to'])]
insertion_tuples=[(";", ';', 1),(",", ',', 1),("'m", 'am', 2),("'ve", 'have', 3),
                  ("'re", 'are', 3),("'ll", 'will', 3),("'d", 'would', 2),("n't", 'not', 3)]
prep_list=['ago']
prep_concat_list=[['next','to'],['behind','to'],['in','front','of']]
rel_list=['which', 'who','that']
sub_list=['while', 'but','where', 'when']
adverbial_list=['in', 'on', 'at', 'from', 'for', 'next', 'last', 'behind','behind+to','next+to','in+front+of']



"""
We have to read all words that sentence can begin with                           
"""
frt_wd = ResourcePool().sentence_starts


"""
We have to read action verbs known by the robot                                  
"""
action_verb = ThematicRolesDict().get_all_verbs()



def delete_and_from_number(sentence):
    """
    This function delete 'and' between two numbers                                 
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    while i < len(sentence):
        if sentence[i]=='and' and other_functions.number(sentence[i-1])==1 and other_functions.number(sentence[i+1])==1:
            sentence=sentence[:i]+sentence[i+1:]
        i=i+1
    return sentence


            
def concat_number(sentence):
    """
    This function concatenate numbers with '+'                                 
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    sentence = delete_and_from_number(sentence)
    
    while i < len(sentence):
        #There is a number
        if other_functions.number(sentence[i])==1:
            begin_pos=i
                
            while i<len(sentence) and other_functions.number(sentence[i])==1:
                i=i+1
            end_pos=i
            
            sentence=sentence[:begin_pos]+[other_functions.convert_to_string(sentence[begin_pos:end_pos])]+sentence[end_pos:]
            
        i=i+1    
    return sentence
        
        
def upper_to_lower(sentence):
    """
    This function converts the upper case to lower case
    Input=sentence, beginning sentence list                  Output=sentence         
    """
    
    #If the sentence begins with upper case
    if other_functions.find_cap_lettre(sentence[0]):

        #We convert upper case to lower case if it is not 'I'
        if sentence[0]=='I':
            return sentence
        else:
            sentence[0]=sentence[0][0].lower()+sentence[0][1:]
        
        #We find an action verb => it is an imperative sentence        
        for i in action_verb:
            if sentence[0]==i:
                return sentence
            
        #If we find the word in the Beginning_sentence list
        for v in frt_wd:
            if sentence[0]==v[0]:
                return sentence
            
        #We find a number
        if other_functions.number(sentence[0])==1:
            return sentence
        
        #If there is a nominal group
        if analyse_nominal_group.find_sn_pos (sentence, 0)!=[]:
            return sentence

        #It a proper name, we convert lower case to upper case
        sentence[0]=sentence[0][0].upper()+sentence[0][1:]
        return sentence

    #If the sentence begins with lower case
    return sentence



def concatenate_pos(sentence, position, element, pos_rem):
    """
    Function to concatenate an element in sentence at a position                     
    Input=sentence, position+element to concatenate, letter's number to remove        
    Output=sentence                                                                  
    """

    #We perform concatenation
    sentence = sentence[:position+1] + element + sentence[position+1:]

    #We remove the superfusion part
    sentence[position] = sentence[position][:len(sentence[position])-pos_rem]
    return sentence



def case_apostrophe_s_to_is(word):
    """
    Function to know if we have to expand contraction 's to is (return 1)            
    Input=word                      Output=flag(0 if no or 1 if yes)                 
    """
    
    word=word[0].lower()+word[1:]
    for i in apostrophe_s_to_is_list:
        if i == word:
            return 1
    return 0



def expand_contractions(sentence):
    """
    Replaces the contractions by the equivalent meaning, but without contraction
    Input=sentence                       Output=sentence
    """
    
    #init
    i=0
    
    while i < len(sentence):

        if case_apostrophe_s_to_is(sentence[i])==1:
            sentence = concatenate_pos(sentence, i, ['is'], 2)
            i=i+1
        
        for j in replacement_tuples:
            if sentence[i].endswith(j[0]):
                sentence = sentence[:i] + j[1] + sentence[i+1:]
                i=i+1
                break
            
        for j in insertion_tuples:
            if sentence[i].endswith(j[0]):
                sentence = concatenate_pos(sentence, i, [j[1]], j[2])
                i=i+1
                break
        i=i+1
        
    return sentence



def prep_concat(sentence):
    """
    This function to concatenate some words to have a preposition 
    Input=sentence                                     Output=sentence               
    """    
    
    #init
    i=0
    
    #For the case of whom
    if sentence[0:2]==['To', 'whom']:
        sentence=['To+whom']+sentence[2:]
    
    #For all other prepositions
    while i < len(sentence):
        
        for j in prep_concat_list:
            if i+len(j) < len(sentence) and sentence[i:i+len(j)]==j:
                sentence=sentence[:i]+[other_functions.convert_to_string(j)]+sentence[i+len(j):]
                break
                
        i=i+1
    return sentence
    
    
    
def determination_nom_gr(sentence, position):
    """
    This function return the nominal group with his complement                             
    Input=sentence                             Output=nominal group               
    """
    
    nom_gr=analyse_nominal_group.find_sn_pos(sentence, position)
    list_nom_gr=nom_gr
    
    while position+len(nom_gr)<len(sentence) and sentence[position+len(nom_gr)] == 'of':
        position=position+len(nom_gr)+1
        nom_gr=analyse_nominal_group.find_sn_pos(sentence, position)
        list_nom_gr=list_nom_gr+['of']+nom_gr
        
    return list_nom_gr
        
        

def and_nom_group(sentence):
    """
    This function process the case when there is a comma between nominal groups                             
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    flag=2
    list_nom_gr=[]
    
    #If we find ','
    while i < len(sentence):
        if sentence[i]==',':
            nom_gr=determination_nom_gr(sentence, i+1)
            end_pos=len(nom_gr)+i+1
            
            #First we recover the all nominal groups preceded by ','
            while nom_gr!=[] and sentence[end_pos]==',':
                list_nom_gr=['and']+nom_gr
                nom_gr=determination_nom_gr(sentence, end_pos+1)
                end_pos=len(nom_gr)+end_pos+1
                #Flag still 2 because this stage is not compulsory
                flag=2
            
            #We will find the last nominal group of this phrase
            if nom_gr!=[] and sentence[end_pos]=='and':
                list_nom_gr=list_nom_gr+['and']+nom_gr
                nom_gr=determination_nom_gr(sentence, end_pos+1)
                end_pos=len(nom_gr)+end_pos+1
                list_nom_gr=list_nom_gr+['and']+nom_gr
                #Flag will be 1 because this stage is compulsory
                flag=flag-1
            
            #If flag=1 => we can have the and_nom_group case
            if flag==1:
                #We have to find the first nominal group
                begin_pos=i-1
                nom_gr=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
                while nom_gr==[] and begin_pos>0:
                    begin_pos=begin_pos-1
                    nom_gr=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
                #If this nominal group preceded the first ',' => OK
                if nom_gr!=[] and begin_pos+len(nom_gr)==i:
                    flag=flag-1
                    list_nom_gr=nom_gr+list_nom_gr
                    
            #We have an and_nom_group case 
            if flag==0:
                sentence=sentence[:begin_pos]+list_nom_gr+sentence[end_pos:]
        
        i=i+1
    
    return sentence

       

def find_nom_gr_list(phrase):
    """
    This function break phrase into nominal groups with ('s)                         
    And return also the elements number of the end of this list in the sentence       
    Input=sentence                    Output=list of nominal group                   
    """
    
    #init
    list=[]
    nb_element=0
    
    nom_gr=analyse_nominal_group.find_sn_pos(phrase, 0)
    #We use the length of the nominal group because it will be different with len(nom_gr)
    nom_gr_lent=len(nom_gr)

    #We loop until there is no more nominal group
    while nom_gr!=[] and (nom_gr[len(nom_gr)-1].endswith("'s") or nom_gr[len(nom_gr)-1].endswith("s'"):

        list=[nom_gr]+list
        nb_element=nb_element+nom_gr_lent

        #re-init phrase and nominal group
        phrase=phrase[nom_gr_lent:]
        nom_gr=analyse_nominal_group.find_sn_pos(phrase, 0)
        nom_gr_lent=len(nom_gr)

        #We need to have a nominal group so we forced it
        if nom_gr == []:
            nom_gr=analyse_nominal_group.find_sn_pos(['the']+phrase, 0)
            nom_gr_lent=len(nom_gr)-1

    list=[nom_gr]+list
    nb_element=nb_element+nom_gr_lent

    #We put the elments number at the end of the list
    list=list+[nb_element]
    
    return list



def create_possession_claus(list):
    """
    This function create phrase with 'of'                                            
    Input=list of nominal group                 Output=phrase of nominal group       
    """
    
    #init
    i=1
    #To take the first element
    phrase=list[i-1]

    #We concatenate
    while i < len(list):
        phrase=phrase+['of']+list[i]
        i=i+1

    #We delete the 's
    for j in phrase:
        if j.endswith("'s"):
            word= phrase[phrase.index(j)]
            phrase[phrase.index(j)]= word[:len(word)-2]
        if j.endswith("s'"):
            word= phrase[phrase.index(j)]
            phrase[phrase.index(j)]= word[:len(word)-1]

    return phrase



def possesion_form(sentence): 
    """
    This function convert 's to possession form 'of'                                 
    Input=sentence                                     Output=sentence               
    """

    #init
    begin_pos=0
    flag=0

    #We will find the possession case
    while (begin_pos<len(sentence)):

        #We found a posssession case
        if sentence[begin_pos].endswith("'s") or sentence[begin_pos].endswith("s'"):

            #We have to find the first nominal group
            nom_gr=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
            
            #In the case of a propre name
            while nom_gr!=[] and begin_pos!=0 and other_functions.find_cap_lettre(nom_gr[0])==1:
                begin_pos=begin_pos-1

                nom_gr=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
                flag=1

            #If flag=1 => there is a propre name so we haven't decrement the begin_pos
            if flag==0:
                while nom_gr == []:
                    begin_pos=begin_pos-1
                    nom_gr=analyse_nominal_group.find_sn_pos(sentence, begin_pos)

            else:
                #If there is a propre name, begin_pos is wrong, we have to increment
                begin_pos=begin_pos+1
                flag=0

            #We recover the list of nominal groups
            nom_gr_list=find_nom_gr_list(sentence[begin_pos:])
            #We create the final phrase
            end_pos=nom_gr_list[len(nom_gr_list)-1]+begin_pos
            sentence=sentence[:begin_pos]+create_possession_claus(nom_gr_list[:len(nom_gr_list)-1])+sentence[end_pos:]

            #We continue processing from the end's position
            begin_pos=end_pos
            
        else:
            begin_pos=begin_pos+1

    return sentence



def other_processing(sentence):
    """
    This function performs processing to facilitate the analysis that comes after    
    Input=sentence                              Output=sentence                      
    """
    
    #Question with which starts with nominal group without determinant
    if sentence[0]=='which':
        sentence=[sentence[0]]+['the']+sentence[1:]

    return sentence
 
 
 
def move_prep(sentence):
    """ 
    This function to put the preposition before the nominal group                     
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i < len(sentence):
        for p in prep_list:
            
            #If there is a preposal
            if sentence[i]==p:
                position=i
                
                #We have to find the nominal group just before
                while analyse_nominal_group.find_sn_pos(sentence, position)==[]:
                    position=position-1
                    
                sentence=sentence[:position]+[p]+sentence[position:i]+sentence[i+1:]
        i=i+1
        
    return sentence 

                

def or_processing(sentence):
    """ 
    This function creates a nominal group before and after the 'or'                  
    Input=sentence                              Output=sentence                      
    """ 
    #init
    i=0
    
    while i < len(sentence):
        
        if sentence[i]=='or':
            #We have to find the first and the second nominal group in the sentence
            position=i
            fst_nom_gr=analyse_nominal_group.find_sn_pos(sentence, position)
            
            #Until we find the first nominal group
            while fst_nom_gr==[]:
                position=position-1
                fst_nom_gr=analyse_nominal_group.find_sn_pos(sentence, position)
        
            #We will find the second nominal group
            scd_nom_gr=analyse_nominal_group.find_sn_pos(sentence, i+1)
            
            if fst_nom_gr[len(fst_nom_gr)-1]=='or' and scd_nom_gr==[]:
                #We have to know the second nominal group
                sentence=sentence[:i+1]+[fst_nom_gr[0]]+sentence[i+1:]
                scd_nom_gr=analyse_nominal_group.find_sn_pos(sentence, i+1)
                
                #We insert word to have 2 nominal groups in the sentence
                sentence=sentence[:position]+fst_nom_gr[:len(fst_nom_gr)-1]+[scd_nom_gr[len(scd_nom_gr)-1]]+['or']+sentence[i+1:]
            
            elif fst_nom_gr[len(fst_nom_gr)-1]=='or':
                #We insert word to have 1 nominal group in the sentence
                sentence=sentence[:position]+fst_nom_gr[:len(fst_nom_gr)-1]+[scd_nom_gr[len(scd_nom_gr)-1]]+sentence[i:]
    
        i=i+1
    
    return sentence


def reorganize_adj(sentence):
    """ 
    This function delete ',' and 'and' if it is between adjectives                  
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i < len(sentence)-1:
        if sentence[i] ==',' or sentence[i] =='and':
            if analyse_nominal_group.is_an_adj(sentence[i+1]) and analyse_nominal_group.is_an_adj(sentence[i-1]):
                sentence=sentence[:i]+sentence[i+1:]
        
        i=i+1
    return sentence
    
    
    
def subsentence_comma(sentence):
    """ 
    This function delete ',' or changed on ';'                  
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i < len(sentence):
        if sentence[i]==',':
            sentence[i]=';'
            if i==len(sentence)-1:
                sentence=sentence[:i]
            elif sentence[i+1]=='?' or sentence[i+1]=='!' or sentence[i+1]=='.':
                sentence=sentence[:i]+sentence[i+1:]
            else:
                for j in rel_list+sub_list:
                    if  j==sentence[i+1]:
                        sentence=sentence[:i]+sentence[i+1:]
                        break
        i=i+1
    return sentence
    
    
    
def delete_empty(sentence):
    """ 
    This function delete '' from sentence                  
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i < len(sentence):
        if sentence[i]=='':
            sentence=sentence[:i]+sentence[i+1:]
        i=i+1
        
    return sentence   
    
    
    
def remerge_sentences(sentence):
    """ 
    This function transform some sentences of the remerge part                  
    Input=sentence                              Output=sentence                      
    """ 
    
    gr=determination_nom_gr(sentence, 0)
    if gr!=[] and len(gr)<len(sentence):
        
        #Case of 'the bottle on the table'
        for i in adverbial_list:
            if i==sentence[len(gr)]:
                if analyse_nominal_group.find_sn_pos(sentence, len(gr)+1)!=[]:
                    sentence=gr+['is']+sentence[sentence.index(i):]
                    
    return sentence    
    
    
    
def processing(sentence):
    """ 
    This function is used by process_sentence                  
    Input=sentence                              Output=sentence                      
    """ 

    sentence = expand_contractions(sentence)
    sentence = delete_empty(sentence)
    sentence = prep_concat(sentence)
    sentence = upper_to_lower(sentence)
    sentence = concat_number(sentence)
    sentence = other_processing(sentence)
    sentence = reorganize_adj(sentence)
    sentence = possesion_form(sentence)
    sentence = and_nom_group(sentence)
    sentence = move_prep(sentence)
    sentence = or_processing(sentence)
    sentence = subsentence_comma(sentence)
    sentence = remerge_sentences(sentence)        
    return sentence



def process_sentence(utterance):
    """
    This function breaks the utterance (as a list) into sentences                        
    And does the processing of punctuation                                            
    Input=utterance and beginning sentence list         Output=list of sentence          
    """

    #init
    sentence=[]
    sentence_list=[]
    utterance = utterance.split()
   
    for j in utterance:

        #If user put space between the last word and the punctuation
        if j=='.' or j=='?' or j=='!':
            sentence = sentence+[j]
            sentence = processing(sentence)
            sentence_list=sentence_list+[sentence]
            sentence=[]

        elif j.endswith('.') or j.endswith('?') or j.endswith('!'):
            sentence = sentence+[j[:len(j)-1]] + [j[len(j)-1]]
            sentence = processing(sentence)
            sentence_list=sentence_list+[sentence]
            sentence=[]

        else:
            sentence=sentence+[j]
            
    #If the user forget the punctuation at the end
    if sentence!=[]:
        sentence = processing(sentence)
        sentence_list=sentence_list+[sentence]

    return sentence_list

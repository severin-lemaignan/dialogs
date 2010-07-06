#!/usr/bin/python
# -*- coding: utf-8 -*-
# SVN:rev202 + PythonTidy


"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 22/06/2010                                                                       ##
## The package contains functions which are important for the pre-parsing           ##
## We return a list of all sentence in the reply to do traitment                    ##
## Functions:                                                                       ##
##    upper_to_lower : to treat the uppcase at the baginning of the sentence        ##
##    concatenate_pos : to concatenate an element in a position given               ##
##    case_apostrophe_s_to_is : to know if there is this kind of "'s"               ##
##    expand_contractions : to perform expand contraction using concatenate_pos     ##
##    comma : to replace ',' by 'and'                                               ##
##    find_nom_gr_list : take off noun chain linked by 'of'                         ##
##    create_possession_claus : to transform a noun chain to string's list with 'of'##
##    possesion_form : to exchange the "'s" to 'of' by using 2 lastest functions    ##
##    other_treatment : to perform other treatments                                 ##
##    treat_sentence : to split reply into many sentences using all other functions ##
######################################################################################
"""
from resources_manager import ResourcePool
import analyse_nominal_group
import other_functions


"""
############################## Statement of lists ####################################
"""
apostrophe_s_to_is_list=["he's", "she's", "it's", "that's", "what's", "who's", "how's"]


"""
######################################################################################
## We have to read all irregular adjectives before the treatment                    ##
######################################################################################
"""
act_vbr_list = ResourcePool().sentence_starts.keys()


"""
######################################################################################
## We have to read all words that sentence can begin with                           ##
######################################################################################
"""
frt_wd = ResourcePool().sentence_starts.keys()


"""
######################################################################################
## This function converts the uppercase to lowercase                                ##
## Input=sentence, beginning sentence list                  Output=sentence         ##
######################################################################################
"""
def upper_to_lower(sentence):

    #If the sentence begins with uppercase
    if other_functions.find_cap_lettre(sentence[0]):

        #We convert uppercase to lowercase if it is not 'I'
        if sentence[0]=='I':
            return sentence
        else:
            sentence[0]=sentence[0][0].lower()+sentence[0][1:]

        #If we find the word in the Beginning_sentence list
        for v in frt_wd:
            if sentence[0]==v[0]:
                return sentence

        #If there is a nominal group
        if analyse_nominal_group.find_sn_pos (sentence, 0)!=[]:
            return sentence

        #If there is an action verb
        for x in act_vbr_list:
            if x==sentence[0]:
                return sentence

        #It a propre name, we convert lowercase to uppercase
        sentence[0]=sentence[0][0].upper()+sentence[0][1:]
        return sentence

    #If the sentence begins with lowercase
    return sentence


"""
######################################################################################
## Function to concatenate an element in sentence at a position                     ##
## Input=sentece, position+element to concatenate, letter's number to remove        ##
## Output=sentence                                                                  ##
######################################################################################
"""
def concatenate_pos(sentence, position, element, pos_rem):

    #We perform concatenation
    sentence = sentence[:position+1] + element + sentence[position+1:]

    #We remove the superfusion part
    sentence[position] = sentence[position][:len(sentence[position])-pos_rem]
    return sentence


"""
######################################################################################
## Function to know if we have to expand contraction 's to is (return 1)            ##
## Input=word                      Output=flag(0 if no or 1 if yes)                 ##
######################################################################################
"""
def case_apostrophe_s_to_is(word):
    word=word[0].lower()+word[1:]
    for i in apostrophe_s_to_is_list:
        if i == word:
            return 1
    return 0


"""
######################################################################################
## Replaces the contractions by the equivalent meaning, but without contraction     ##
## Input=sentence                       Output=sentence                             ##
######################################################################################
"""
def expand_contractions(sentence):

    for i in sentence:

        if case_apostrophe_s_to_is(i)==1:
            sentence = concatenate_pos(sentence, sentence.index(i), ['is'], 2)

        #For 'will not'
        elif i == "won't":
            sentence= sentence = sentence[:sentence.index(i)] + ['will', 'not'] + sentence[sentence.index(i)+1:]

        #For 'am'
        elif i.endswith("'m"):
            sentence = concatenate_pos(sentence, sentence.index(i), ['am'], 2)

        #For 'are'
        elif i.endswith("'re"):
            sentence = concatenate_pos(sentence, sentence.index(i), ['are'], 3)

        #For 'have'
        elif i.endswith("'ve"):
            sentence = concatenate_pos(sentence, sentence.index(i), ['have'], 3)

        #For 'will'
        elif i.endswith("'ll"):
            sentence = concatenate_pos(sentence, sentence.index(i), ['will'], 3)

        #For 'would'
        elif i.endswith("'d"):
            sentence = concatenate_pos(sentence, sentence.index(i), ['would'], 2)

        #For 'not'
        elif i.endswith("n't"):
            sentence = concatenate_pos(sentence, sentence.index(i), ['not'], 3)

        #For 'want to'
        elif i.endswith("wanna"):
            sentence = sentence[:sentence.index(i)] + ['want', 'to'] + sentence[sentence.index(i)+1:]

        #For 'going to'
        elif i.endswith("gonna"):
            sentence = sentence[:sentence.index(i)] + ['going', 'to'] + sentence[sentence.index(i)+1:]
        
    return sentence


"""
######################################################################################
## This function treats the case when there is a comma                              ##
## Input=sentence                                     Output=sentence               ##
######################################################################################
"""
def comma(sentence):

    #Replace ',' by 'and'
    for i in sentence:
        if i==',':
            sentence = sentence[:sentence.index(i)] + ['and'] + sentence[sentence.index(i)+1:]
        elif i.endswith(','):
            sentence = concatenate_pos(sentence, sentence.index(i), ['and'], 1)
    return sentence


"""
######################################################################################
## This function break phrase into nominal groups with ('s)                         ##
## And return also the elments number of the end of this list in the sentence       ##
## Input=sentence                    Output=list of nominal group                   ##
######################################################################################
"""
def find_nom_gr_list(phrase):
    
    #init
    list=[]
    nb_element=0
    nom_gr=analyse_nominal_group.find_sn_pos(phrase, 0)
    #We use the length of the nominal group because it will be different with len(nom_gr)
    nom_gr_lent=len(nom_gr)

    #We loop until there is no more nominal group
    while nom_gr!=[] and nom_gr[len(nom_gr)-1].endswith("'s"):

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


"""
######################################################################################
## This function create phrase with 'of'                                            ##
## Input=list of nominal group                 Output=phrase of nominal group       ##
######################################################################################
"""
def create_possession_claus(list):

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

    return phrase


"""
######################################################################################
## This function convert 's to possession form 'of'                                 ##
## Input=sentence                                     Output=sentence               ##
######################################################################################
"""
def possesion_form(sentence):

    #init
    begin_pos=0
    flag=0

    #We will find the possession case
    while (begin_pos<len(sentence)):

        #We found a posssession case
        if sentence[begin_pos].endswith("'s"):

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

            #We continue treatment from the end's position
            begin_pos=end_pos
            
        else:
            begin_pos=begin_pos+1

    return sentence


"""
######################################################################################
## This function performs treatments to facilitate the analysis that comes after    ##
## Input=sentence                              Output=sentence                      ##
######################################################################################
"""
def other_treatment(sentence):

    #Question with which starts with nominal group without determinant
    if sentence[0]=='which':
        sentence=[sentence[0]]+['the']+sentence[1:]

    return sentence

"""
######################################################################################
## This function breaks the reply (as a list) into sentences                        ##
## And does the treatment of punctuation                                            ##
## Input=reply and beginning sentence list         Output=list of sentence          ##
######################################################################################
"""
def treat_sentence(reply):

    #init
    sentence=[]
    sentence_list=[]
    reply = reply.split()
   
    for j in reply:

        #If user put space between the last word and the punctuation
        if j=='.' or j=='?' or j=='!':
            sentence = sentence+[j]
            sentence = expand_contractions(sentence)
            sentence = upper_to_lower(sentence)
            sentence = other_treatment(sentence)
            sentence = possesion_form(sentence)
            sentence = comma(sentence)
            sentence_list=sentence_list+[sentence]
            sentence=[]

        elif j.endswith('.') or j.endswith('?') or j.endswith('!'):
            sentence = sentence+[j[:len(j)-1]] + [j[len(j)-1]]
            sentence = expand_contractions(sentence)
            sentence = upper_to_lower(sentence)
            sentence = other_treatment(sentence)
            sentence = possesion_form(sentence)
            sentence = comma(sentence)
            sentence_list=sentence_list+[sentence]
            sentence=[]

        else:
            sentence=sentence+[j]
            
    #If the user forget the punctuation at the end
    if sentence!=[]:
        sentence = expand_contractions(sentence)
        sentence = upper_to_lower(sentence)
        sentence = other_treatment(sentence)
        sentence = possesion_form(sentence)
        sentence = comma(sentence)
        sentence_list=sentence_list+[sentence]

    return sentence_list

#!/usr/bin/python
# -*- coding: utf-8 -*-
#SVN:rev202


"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 23/06/2010                                                                       ##
## The package contains functions that affect the analysis of verbs                 ##
## We return the tense of the sentence and the verb corresponding to                ##
## Functions:                                                                       ##
##    find_tense_statement : to return the tense of a statement                     ##
##    find_verb_statement : to recover the verb of a statement                      ##
##    find_tense_question : to return the tense of a question                       ##
##    find_verb_question : to recover the verb of a question                        ##
##    infinitive : to return the infinitive form of the verb                        ##
##    return_verb : to return the verb (with proposal)                              ##
######################################################################################
"""
from resources_manager import ResourcePool


"""
######################################################################################
## We have to read all past irregular verb forms                                    ##
######################################################################################
"""
past_irreg_vrb = ResourcePool().past_irregular_verbs


"""
######################################################################################
## We have to read all past irregular verb forms                                    ##
######################################################################################
"""
present_irreg_vrb = ResourcePool().present_irregular_verbs


"""
######################################################################################
## We have to read all past irregular verb forms                                    ##
######################################################################################
"""
phrasal_vrb = ResourcePool().preposition_verbs


"""
######################################################################################
## This function returns the time of conjugation of the verb in a statement         ##
## We have to know the list of adverbs before the verb                              ##
## Input=sentence and the adverb bound to the verb           Output=tense           ##
######################################################################################
"""
def find_tense_statement (phrase, adverb):

    #Treatment for the simple past
    if phrase[len(adverb)].endswith('ed'):
        return 'past simple'
    
    #Traitment for the future simple
    if phrase[0]=='will':
        return 'future simple'

    #Treatment for the present perfect
    if phrase[0]=='have' or phrase[0]=='has':
        #For regular forms
        if phrase[1+len(adverb)].endswith('ed'):
            return 'present perfect'
        #For irregular forms
        for i in past_irreg_vrb:
            if phrase[1+len(adverb)]==i[2]:
                return 'present perfect'
    
    #Treatment for the past perfect
    if phrase[0]=='had':
        #For regular forms
        if phrase[1+len(adverb)].endswith('ed'):
            return 'past perfect'
        #For irregular forms
        for i in past_irreg_vrb:
            if phrase[1+len(adverb)]==i[2]:
                return 'past perfect'
    
    #Treatment for the progressive form and passive form (in present)
    if phrase[0]=='is' or phrase[0]=='are' or phrase[0]=='am':
        #Progressive form in the present
        if len(phrase)!=1 and phrase[1+len(adverb)].endswith('ing'):
            return 'present progressive'
        #Passive form in the present
        elif find_tense_statement(['have']+phrase[1:], adverb)=='present perfect':
            return 'present passive'
    
    #Treatment for the progressive form and passive form (in past)
    if phrase[0]=='was' or phrase[0]=='were':
        #Progressive form in the past
        if len(phrase)!=1 and phrase[1+len(adverb)].endswith('ing'):
            return 'past progressive'
        elif find_tense_statement(['have']+phrase[1:], adverb)=='present perfect':
            return 'past passive'

    #Treatment for the conditionnal form
    if phrase[0]=='would':
        if find_tense_statement(phrase[1:], adverb)=='present simple':
            return 'present conditionnal'
        else:
            return 'past conditionnal'

    #For the irregular forms
    for i in past_irreg_vrb:
        if phrase[len(adverb)]==i[1]:
            #Default case : if past form = present form we choose present simple
            if i[1]==i[0]:
                return 'present simple'
            else:
                return 'past simple'

    #Default case
    return 'present simple'


"""
######################################################################################
## This function find the verb in a statement                                       ##
## Input=sentence, tense and the adverb bound to the verb      Output=main verb     ##
######################################################################################
"""
def find_verb_statement (phrase, adv, tense):

    #If phrase is empty
    if len(phrase)==0:
        return []

    elif tense=='present simple' or tense=='past simple':
        return [phrase[0+len(adv)]]

    elif tense=='present perfect' or tense=='past perfect' or tense=='future simple':
        return [phrase[1+len(adv)]]

    elif tense=='present progressive' or tense=='past progressive':
        return [phrase[1+len(adv)]]

    elif tense=='present passive' or tense=='past passive':
        return [phrase[1+len(adv)]]

    elif tense=='present conditionnal' or tense=='past conditionnal':
        return [phrase[1+len(adv)]]

    #Default case
    return []


"""
######################################################################################
## This function returns the time of conjugation of the verb in a question          ##
## We have to know the list of adverbs before the verb                              ##
## Input=sentence, auxilary and the adverb bound to the verb       Output=tense     ##
######################################################################################
"""
def find_tense_question (phrase, aux, adverb):

    #Traitment for the future simple
    if aux=='will':
        return 'future simple'

    #Duality between prgrossive, passive and present simple
    elif aux=='is' or aux=='are' or aux=='am':
  
        if phrase[len(adverb)].endswith('ing'):
            return 'present progressive'
        elif phrase[len(adverb)].endswith('ed'):
            return 'present passive'
        for i in past_irreg_vrb:
            if phrase[len(adverb)]==i[2]:
                return 'present passive'
        else:
            return 'present simple'

    #Duality between prgrossive, passive and past simple
    elif aux=='was' or aux=='were':
        if phrase[len(adverb)].endswith('ing'):
            return 'past progressive'
        elif phrase[len(adverb)].endswith('ed'):
            return 'past passive'
        for i in past_irreg_vrb:
            if phrase[len(adverb)]==i[2]:
                return 'past passive'
            else:
                return 'past simple'

    #Traitment for the present perfect
    elif aux=='have' or aux=='has':
        if phrase[len(adverb)].endswith('ed'):
            return 'present perfect'
        for i in past_irreg_vrb:
            if phrase[len(adverb)]==i[2]:
                return 'present perfect'

    #Traitment for the past perfect
    elif aux=='had':
        if phrase[len(adverb)].endswith('ed'):
            return 'past perfect'
        for i in past_irreg_vrb:
            if phrase[len(adverb)]==i[2]:
                return 'past perfect'

    #Traitment for the past perfect
    elif aux=='would':
        return find_tense_statement(['would']+phrase, adverb)

    elif aux=='should' or aux=='might' or aux=='could':
        return 'present conditionnal'

    #Default case
    else:
        return find_tense_statement([aux], [])


"""
######################################################################################
## This function find the verb in a question                                        ##
## Input=sentence, tense, auxilary and the adverb bound to the verb                 ##
## Output=main verb                                                                 ##
######################################################################################
"""
def find_verb_question (phrase, adv, aux, tense):

    #Phrase is empty
    if len(phrase)==0:
        return []

    #If it is in the present with a verb state
    if aux=='is' or aux=='are' or aux=='am':
        if tense=='present simple':
            return [aux]

    #If it is in the past with a verb state
    if aux=='was' or aux=='were':
        if tense=='past simple':
            return [aux]

    #When others
    return [phrase[0+len(adv)]]


"""
######################################################################################
## This function return the infinitive form of the verb                             ##
## 'verb' is the base so it is just the first element of Verb (list of one element) ##
## Input=main verb and the tense           Output=main verb in infinitive form      ##
######################################################################################
"""
def infinitive (verb, tense):

    #Treatment for the future simple
    if tense=='future simple':
        return verb

    #Treatment for the present simple
    elif tense=='present simple':
        for i in present_irreg_vrb:
            if i[1] == verb[0]:
                return [i[0]]
        if verb[0].endswith('s'):
            return [verb[0][0:len(verb[0])-1]]

    #Treatment for the past simple, present perfect, past perfect, present passive and past passive
    elif tense=='present perfect' or tense=='past perfect' or tense=='present passive' or tense=='past passive':
        for i in past_irreg_vrb:
            if i[2]==verb[0]:
                return [i[0]]
        if verb[0].endswith('ed'):
            return [verb[0][0:len(verb[0])-2]]

    #Treatment for the past simple, present perfect, past perfect, present passive and past passive
    elif tense=='past simple':
        for i in past_irreg_vrb:
            if i[1]==verb[0]:
                return [i[0]]
        if verb[0].endswith('ed'):
            return [verb[0][0:len(verb[0])-2]]

    #Treatment for the progressive forms
    elif tense=='present progressive' or tense=='past progressive':
        for i in present_irreg_vrb:
            if i[2]==verb[0]:
                return [i[0]]
        if verb[0].endswith('ing'):
            return [verb[0][0:len(verb[0])-3]]

    #Treatment for the conditionnal forms
    elif tense=='present conditionnal':
        return infinitive (verb, 'present simple')
    elif tense=='past conditionnal':
        return infinitive (verb, 'past simple')

    #Default case
    return verb


"""
######################################################################################
## This function return the final form of the verb => a list with one element       ##
## Input=sentence, main verb and the tense                Output=verb               ##
######################################################################################
"""
def return_verb (phrase, main_verb, tense):

    #To have the infinitive form
    verb=infinitive(main_verb, tense)
    
    #If the main verb is not on the end of the sentence
    if phrase[len(phrase)-1]!=main_verb[0]:
    
        #We will recover the proposal of the verb
        for i in phrasal_vrb:
            if verb[0]==i[0] and phrase[phrase.index(main_verb[0])+1]==i[1]:
                return verb+[phrase[phrase.index(main_verb[0])+1]]
    
    #Default case : we return the main verb in infinitive form
    return verb

#!/usr/bin/python
# -*- coding: utf-8 -*-
#SVN:rev202


"""
 Created by Chouayakh Mahdi                                                       
 23/06/2010                                                                       
 The package contains functions that affect the analysis of verbs                 
 We return the tense of the sentence and the verb corresponding to                
 Functions:                                                                       
    find_tense_statement : to return the tense of a statement                     
    find_verb_statement : to recover the verb of a statement                      
    find_tense_question : to return the tense of a question                       
    find_verb_question : to recover the verb of a question                        
    infinitive : to return the infinitive form of the verb                        
    return_verb : to return the verb (with proposal)                              
"""
from dialogs.resources_manager import ResourcePool


def find_tense_statement(phrase):
    """
    returns the time of conjugation of the verb in a statement         
    We have to know the list of adverbs before the verb                              
    Input=sentence and the adverb bound to the verb           Output=tense           
    """

    #processing for the simple past
    if phrase[0].endswith('ed') and phrase[0] != 'need':
        return 'past simple'

    #processing for the future simple
    if phrase[0] == 'will':
        return 'future simple'

    #processing for the present perfect
    if phrase[0] == 'have' or phrase[0] == 'has':
        #For regular forms
        if phrase[1].endswith('ed'):
            return 'present perfect'
            #For irregular forms
        for i in ResourcePool().irregular_verbs_past:
            if phrase[1] == i[2]:
                return 'present perfect'

    #processing for the past perfect
    if phrase[0] == 'had':
        #For regular forms
        if phrase[1].endswith('ed'):
            return 'past perfect'
            #For irregular forms
        for i in ResourcePool().irregular_verbs_past:
            if phrase[1] == i[2]:
                return 'past perfect'

    #processing for the progressive form and passive form (in present)
    if phrase[0] == 'is' or phrase[0] == 'are' or phrase[0] == 'am' or phrase[0] == 'be':
        #Progressive form in the present
        if len(phrase) != 1 and phrase[1].endswith('ing') and not (phrase[1].endswith('thing')):
            return 'present progressive'
        #Passive form in the present
        elif find_tense_statement(['have'] + phrase[1:]) == 'present perfect':
            #If there is an adjective and not a verb
            if phrase[1] in ResourcePool().adjective_verb:
                return 'present simple'
            return 'present passive'

    #processing for the progressive form and passive form (in past)
    if phrase[0] == 'was' or phrase[0] == 'were':
        #Progressive form in the past
        if len(phrase) != 1 and phrase[1].endswith('ing') and not (phrase[1].endswith('thing')):
            return 'past progressive'
        elif find_tense_statement(['have'] + phrase[1:]) == 'present perfect':
            #If there is an adjective and not a verb
            if phrase[1] in ResourcePool().adjective_verb:
                return 'past simple'
            return 'past passive'

    #For using modal
    elif phrase[0] == 'should' or phrase[0] == 'might' or phrase[0] == 'could':
        if find_tense_statement(phrase[1:]) == 'present perfect' or find_tense_statement(
                phrase[1:]) == 'present passive':
            return 'passive conditional'
        return 'present conditional'

    #processing for the conditional form
    if phrase[0] == 'would':
        if find_tense_statement(phrase[1:]) == 'present passive':
            return 'passive conditional'
        elif find_tense_statement(phrase[1:]) == 'present simple':
            return 'present conditional'
        else:
            return 'past conditional'

    #For the irregular forms
    for i in ResourcePool().irregular_verbs_past:
        if phrase[0] == i[1]:
            #Default case : if past form = present form we choose present simple
            if i[1] == i[0]:
                return 'present simple'
            else:
                return 'past simple'

    #Default case
    return 'present simple'


def find_verb_statement(phrase, tense):
    """
    find the verb in a statement
    Input=sentence, tense and the adverb bound to the verb      Output=main verb     
    """

    #If phrase is empty
    if len(phrase) == 0:
        return []

    elif tense == 'present simple' or tense == 'past simple':
        return [phrase[0]]

    elif tense == 'present perfect' or tense == 'past perfect' or tense == 'future simple':
        return [phrase[1]]

    elif tense == 'present progressive' or tense == 'past progressive':
        return [phrase[1]]

    elif tense == 'present passive' or tense == 'past passive':
        return [phrase[1]]

    elif tense == 'present conditional':
        return [phrase[1]]

    elif tense == 'past conditional' or 'passive conditional':
        return [phrase[2]]

    #Default case
    return []


def find_tense_question(phrase, aux):
    """
    returns the time of conjugation of the verb in a question          
    We have to know the list of adverbs before the verb                              
    Input=sentence, auxiliary and the adverb bound to the verb       Output=tense     
    """

    if phrase[0] == 'be':
        if find_tense_statement(phrase) == 'present passive':
            #For using modal
            if aux == 'should' or aux == 'might' or aux == 'could':
                return 'passive conditional'
            else:
                return 'present passive'

    #Processing for the future simple
    if aux == 'will':
        return 'future simple'

    #Duality between progressive, passive and present simple
    elif aux == 'is' or aux == 'are' or aux == 'am':

        if phrase[0].endswith('ing') and not (phrase[0].endswith('thing')):
            return 'present progressive'
        elif phrase[0].endswith('ed'):
            #If there is an adjective and not a verb
            if phrase[1] in ResourcePool().adjective_verb:
                return 'present simple'
            return 'present passive'
        for i in ResourcePool().irregular_verbs_past:
            if phrase[0] == i[2]:
                return 'present passive'
        else:
            return 'present simple'

    #Duality between progressive, passive and past simple
    elif aux == 'was' or aux == 'were':
        if phrase[0].endswith('ing') and not (phrase[0].endswith('thing')):
            return 'past progressive'
        elif phrase[0].endswith('ed'):
            #If there is an adjective and not a verb
            if phrase[1] in ResourcePool().adjective_verb:
                return 'past simple'
            return 'past passive'
        for i in ResourcePool().irregular_verbs_past:
            if phrase[0] == i[2]:
                return 'past passive'
            else:
                return 'past simple'

    #Processing for the present perfect
    elif aux == 'have' or aux == 'has':
        if phrase[0].endswith('ed'):
            return 'present perfect'
        for i in ResourcePool().irregular_verbs_past:
            if phrase[0] == i[2]:
                return 'present perfect'

    #Processing for the past perfect
    elif aux == 'had':
        if phrase[0].endswith('ed'):
            return 'past perfect'
        for i in ResourcePool().irregular_verbs_past:
            if phrase[0] == i[2]:
                return 'past perfect'

    #Processing for the past perfect
    elif aux == 'would':
        return find_tense_statement(['would'] + phrase)

    #For using modal
    elif aux == 'should' or aux == 'might' or aux == 'could':
        return 'present conditional'

    #Default case
    else:
        return find_tense_statement([aux])


def find_verb_question(phrase, aux, tense):
    """
    find the verb in a question                                        
    Input=sentence, tense, auxiliary and the adverb bound to the verb                 
    Output=main verb                                                                
    """

    #Phrase is empty
    if len(phrase) == 0:
        return []

    #If it is in the present with a verb state
    if aux == 'is' or aux == 'are' or aux == 'am':
        if tense == 'present simple':
            return [aux]

    #If it is in the past with a verb state
    if aux == 'was' or aux == 'were':
        if tense == 'past simple':
            return [aux]

    if tense == 'past conditional' or tense == 'passive conditional':
        return [phrase[1]]

    if tense == 'present passive' and phrase[0] == 'be':
        return [phrase[1]]

    #When others
    return [phrase[0]]


def infinitive(verb, tense):
    """
    returns the infinitive form of the verb                             
    'verb' is the base so it is just the first element of Verb (list of one element) 
    Input=main verb and the tense           Output=main verb in infinitive form      
    """

    #processing for the future simple
    if tense == 'future simple':
        return verb

    #processing for the present simple
    elif tense == 'present simple':
        for i in ResourcePool().irregular_verbs_present:
            if i[1] == verb[0] or i[0] == verb[0]:
                return [i[0]]

        if verb[0].endswith('s'):
            return [verb[0][0:len(verb[0]) - 1]]

    #processing for the past simple, present perfect, past perfect, present passive and past passive
    elif tense == 'present perfect' or tense == 'past perfect' or tense == 'present passive' or tense == 'past passive' or tense == 'passive conditional':
        for i in ResourcePool().irregular_verbs_past:
            if i[2] == verb[0]:
                return [i[0]]
        if verb[0].endswith('ed'):
            return [verb[0][0:len(verb[0]) - 2]]

    #processing for the past simple, present perfect, past perfect, present passive and past passive
    elif tense == 'past simple':
        for i in ResourcePool().irregular_verbs_past:
            if i[1] == verb[0]:
                return [i[0]]
        if verb[0].endswith('ed'):
            return [verb[0][0:len(verb[0]) - 2]]

    #processing for the progressive forms
    elif tense == 'present progressive' or tense == 'past progressive':
        for i in ResourcePool().irregular_verbs_present:
            if i[2] == verb[0]:
                return [i[0]]
        if verb[0].endswith('ing'):
            return [verb[0][0:len(verb[0]) - 3]]

    #processing for the conditional forms
    elif tense == 'present conditional':
        return infinitive(verb, 'present simple')
    elif tense == 'past conditional':
        return infinitive(verb, 'present perfect')

    #Default case
    return verb


def return_verb(phrase, main_verb, tense):
    """
    returns the final form of the verb => a list with one element       
    Input=sentence, main verb and the tense                Output=verb               
    """

    #To have the infinitive form
    verb = infinitive(main_verb, tense)

    #If the main verb is not on the end of the sentence
    if phrase[len(phrase) - 1] != main_verb[0]:

        #We will recover the proposal of the verb
        for i in ResourcePool().preposition_verbs:
            if verb[0] == i[0] and phrase[phrase.index(main_verb[0]) + 1] == i[1]:
                return verb + [phrase[phrase.index(main_verb[0]) + 1]]

    #Default case : we return the main verb in infinitive form
    return verb

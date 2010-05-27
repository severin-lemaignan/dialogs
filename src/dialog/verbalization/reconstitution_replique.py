#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN rev.203 + Python Tidy + removed convert_string + ...

from dialog_exceptions import UnrecognizedSentenceType

import reconstitution_phrase

def eliminer_redond(liste):
    phrase = []
    if liste != []:
        phrase = [liste[0]]
        for i in range(1, len(liste)):
            if liste[i] != liste[i - 1]:
                phrase = phrase + [liste[i]]
    return phrase


def recon_replique(analyse):
    
    if analyse.data_type == 'w_question':
        if analyse.aim == 'date':
            result = ' '.join(eliminer_redond(['when']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'place':
            result = ' '.join(eliminer_redond(['where']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'origine':
            result = ' '.join(eliminer_redond(['where']
                                  + reconstitution_phrase.y_o_question(analyse)
                                  + ['from']))
        elif analyse.aim == 'time':
            result = ' '.join(eliminer_redond(['what', 'time']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'color':
            result = ' '.join(eliminer_redond(['what', 'color']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'size':
            result = ' '.join(eliminer_redond(['what', 'size']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'situation':
            result = ' '.join(eliminer_redond(reconstitution_phrase.w_question_situation(analyse)))
        elif analyse.aim == 'problem':
            result = ' '.join(eliminer_redond(reconstitution_phrase.w_question_problem(analyse)))
        elif analyse.aim.startswith('classification'):
            result = ' '.join(eliminer_redond(reconstitution_phrase.w_question_classi(analyse)))
        elif analyse.aim == 'opinion' or analyse.aim == 'descrition' \
            or analyse.aim == 'thing' or analyse.aim == 'object' \
            or analyse.aim == 'explication':
            result = ' '.join(eliminer_redond(reconstitution_phrase.w_question_what(analyse)))
        elif analyse.aim == 'age':
            result = ' '.join(eliminer_redond(['how', 'old']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'duration':
            result = ' '.join(eliminer_redond(['how', 'long']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'frequency':
            result = ' '.join(eliminer_redond(['how', 'often']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'distance':
            result = ' '.join(eliminer_redond(['how', 'far']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'manner':
            result = ' '.join(eliminer_redond(['how']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'quantity':
            result = ' '.join(eliminer_redond(reconstitution_phrase.w_question_quantity(analyse)))
        elif analyse.aim == 'invitation':
            result = ' '.join(eliminer_redond(reconstitution_phrase.w_question_invitation(analyse)))
        elif analyse.aim == 'reason':
            result = ' '.join(eliminer_redond(['why']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'possession':
            result = ' '.join(eliminer_redond(reconstitution_phrase.w_question_possession(analyse)))
        elif analyse.aim == 'people':
            result = ' '.join(eliminer_redond(['who']
                                  + reconstitution_phrase.y_o_question(analyse)))
        elif analyse.aim == 'choice':
            result = ' '.join(eliminer_redond(reconstitution_phrase.w_question_choice(analyse)))
        else:
            raise UnrecognizedSentenceType("Don't know question type: " + analyse.aim)
        
        result += '?'
        
    elif analyse.data_type == 'yes_no_question':
        result = ' '.join(eliminer_redond(reconstitution_phrase.y_o_question(analyse)))
        result += '?'
        
    elif analyse.data_type == 'statement':
        result = ' '.join(eliminer_redond(reconstitution_phrase.statement_sentence(analyse)))
    elif analyse.data_type == 'imperative':
        result = ' '.join(eliminer_redond(reconstitution_phrase.imperative_sentence(analyse)))
    elif analyse.data_type == 'amorce':
        result = 'hello'
    elif analyse.data_type == 'agree':
        result = 'ok'
    elif analyse.data_type == 'disagree':
        result = 'no'
    else:
        raise UnrecognizedSentenceType("Don't know type: " + analyse.data_type)
    
    return result


def reconsti_replique(analyse):
    replique = ''
    for i in analyse:
        replique = replique + recon_replique(i)
    return replique



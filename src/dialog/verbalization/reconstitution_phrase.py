#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN rev.203 + Python Tidy + ...various fixes (syntax, exceptions...)

from dialog_exceptions import EmptyGrammaticalGroup

import recuperation_element


def recup_string(chaine):
    for i in chaine:
        if i == '+':
            return [chaine[:chaine.index(i)]] \
                + recup_string(chaine[chaine.index(i) + 1:])
    return [chaine]


def relative_sentence(class_relative):
    phrase = statement_sentence(class_relative)
    return ['that'] + phrase


def traite_sub(sub):
    res = []
    for i in sub:
        if i.data_type == 'condition':
            res += ['if'] + statement_sentence(i)
    return res

def statement_sentence(analyse):
    if not analyse:
        raise EmptyGrammaticalGroup("Encountered an empty sentence while " + \
                                    "creating the NL version of the sentence.")
    phrase = recuperation_element.gr_nominal(analyse.sn)
    verbe = recup_string(analyse.sv.vrb_main[0])
    phrase = phrase \
        + recuperation_element.conjuguer_verbe_sent(analyse.sv.vrb_tense,
            verbe, analyse.sv.vrb_adv, analyse.sn, analyse.sv.state)
    phrase += recuperation_element.gr_nominal(analyse.sv.d_obj)
    phrase = phrase \
        + recuperation_element.reconsitu_indirect_compl(analyse.sv.i_cmpl)
    phrase += analyse.sv.advrb
    if analyse.sv.sv_sec != None:
        phrase += ['to'] + analyse.sv.sv_sec.vrb_adv \
            + recup_string(analyse.sv.sv_sec.vrb_main[0])
        phrase = phrase \
            + recuperation_element.gr_nominal(analyse.sv.sv_sec.d_obj)
        phrase = phrase \
            + recuperation_element.reconsitu_indirect_compl(analyse.sv.sv_sec.i_cmpl)
        phrase += analyse.sv.sv_sec.advrb
    if analyse.sv.vrb_sub_sentence:
        phrase += traite_sub(analyse.sv.vrb_sub_sentence)
    return phrase


def imperative_sentence(analyse):
    verbe = recup_string(analyse.sv.vrb_main[0])
    phrase = \
        recuperation_element.conjuguer_verbe_sent(analyse.sv.vrb_tense,
            verbe, analyse.sv.vrb_adv, analyse.sn, analyse.sv.state)
    phrase += recuperation_element.gr_nominal(analyse.sv.d_obj)
    phrase = phrase \
        + recuperation_element.reconsitu_indirect_compl(analyse.sv.i_cmpl)
    phrase += analyse.sv.advrb
    if analyse.sv.sv_sec != None:
        phrase += ['to'] + analyse.sv.sv_sec.vrb_adv \
            + recup_string(analyse.sv.sv_sec.vrb_main[0])
        phrase = phrase \
            + recuperation_element.gr_nominal(analyse.sv.sv_sec.d_obj)
        phrase = phrase \
            + recuperation_element.reconsitu_indirect_compl(analyse.sv.sv_sec.i_cmpl)
        phrase += analyse.sv.sv_sec.advrb
    if analyse.sv.vrb_sub_sentence != []:
        phrase += traite_sub(analyse.sv.vrb_sub_sentence)
    return phrase


def y_o_question(analyse):
    phrase = recuperation_element.gr_nominal(analyse.sn)
    verbe = recup_string(analyse.sv.vrb_main[0])
    phrase = recuperation_element.conjuguer_verbe_ques(analyse.sn,
            analyse.sv.vrb_tense, verbe, phrase, analyse.sv.vrb_adv)

    if analyse.sv.state == 'negative':
        phrase = [phrase[0]] + ['not'] + phrase[1:]
        
    phrase += recuperation_element.gr_nominal(analyse.sv.d_obj)
    phrase += recuperation_element.reconsitu_indirect_compl(analyse.sv.i_cmpl)
    phrase += (analyse.sv.advrb if analyse.sv.advrb else [])

    if analyse.sv.sv_sec:
        phrase += ['to'] + analyse.sv.sv_sec.vrb_adv \
                  + recup_string(analyse.sv.sv_sec.vrb_main[0])
        phrase += recuperation_element.gr_nominal(analyse.sv.sv_sec.d_obj)
        phrase += recuperation_element.reconsitu_indirect_compl(analyse.sv.sv_sec.i_cmpl)
        phrase += analyse.sv.sv_sec.advrb
        
    if analyse.sv.vrb_sub_sentence:
        phrase += traite_sub(analyse.sv.vrb_sub_sentence)
    
    return phrase


def w_question_situation(analyse):
    phrase = []
    verbe = recup_string(analyse.sv.vrb_main[0])
    if len(verbe) > 1:
        verbe[len(verbe) - 1] = 'be'
        phrase = recuperation_element.conjuguer_verbe_ques(analyse.sn,
                analyse.sv.vrb_tense, verbe, phrase, analyse.sv.vrb_adv)
    phrase += ['happened']
    phrase = phrase \
        + recuperation_element.reconsitu_indirect_compl(analyse.sv.i_cmpl)
    phrase += analyse.sv.advrb
    if analyse.sv.vrb_sub_sentence != []:
        phrase += traite_sub(analyse.sv.vrb_sub_sentence)
    return ['what'] + phrase


def w_question_problem(analyse):
    phrase = ['what']
    verbe = recup_string(analyse.sv.vrb_main[0])
    phrase = phrase \
        + recuperation_element.conjuguer_verbe_sent(analyse.sv.vrb_tense,
            verbe, analyse.sv.vrb_adv, analyse.sn, analyse.sv.state)
    phrase += ['wrong', 'with']
    phrase += recuperation_element.gr_nominal(analyse.sv.d_obj)
    phrase = phrase \
        + recuperation_element.reconsitu_indirect_compl(analyse.sv.i_cmpl)
    if analyse.sv.vrb_sub_sentence != []:
        phrase += traite_sub(analyse.sv.vrb_sub_sentence)
    return phrase


def w_question_classi(analyse):
    phrase = ['what', 'kind', 'of'] + [analyse.aim[15:]]
    if analyse.aim[15:] == analyse.sn[0].noun[0]:
        phrase = statement_sentence(analyse)
        return ['what', 'kind', 'of'] + phrase[1:]
    else:
        phrase = y_o_question(analyse)
        return ['what', 'kind', 'of'] + [analyse.aim[15:]] + phrase


def w_question_what(analyse):
    phrase = y_o_question(analyse)
    verbe = recup_string(analyse.sv.vrb_main[0])
    if analyse.aim == 'opinion':
        if len(verbe) > 1 and verbe[1] == 'like' or verbe[0] == 'like':
            return ['how'] + phrase
    if analyse.aim == 'descrition' and analyse.sv.vrb_tense \
        != 'futur simple':
        return ['what'] \
            + recuperation_element.conjug_verb(analyse.sv.vrb_tense,
                ['be'], analyse.sn) + phrase[1:]
    return ['what'] + phrase


def w_question_quantity(analyse):
    verbe = recup_string(analyse.sv.vrb_main[0])
    if analyse.sv.d_obj == [] and (verbe[0] == 'be' or len(verbe) > 1
                                   and verbe[1] == 'be'):
        phrase = statement_sentence(analyse)
        return ['how', 'much'] + phrase[1:]
    elif analyse.sv.d_obj == []:
        return ['how', 'much'] + y_o_question(analyse)
    else:
        phrase = recuperation_element.gr_nominal(analyse.sn)
        verbe = recup_string(analyse.sv.vrb_main[0])
        phrase = recuperation_element.conjuguer_verbe_ques(analyse.sn,
                analyse.sv.vrb_tense, verbe, phrase, analyse.sv.vrb_adv)
        if analyse.sv.state == 'negative':
            phrase = [phrase[0]] + ['not'] + phrase[1:]
        phrase = phrase \
            + recuperation_element.reconsitu_indirect_compl(analyse.sv.i_cmpl)
        phrase += analyse.sv.advrb
        if analyse.sv.sv_sec != None:
            phrase += ['to'] + analyse.sv.sv_sec.vrb_adv \
                + recup_string(analyse.sv.sv_sec.vrb_main[0])
            phrase = phrase \
                + recuperation_element.gr_nominal(analyse.sv.sv_sec.d_obj)
            phrase = phrase \
                + recuperation_element.reconsitu_indirect_compl(analyse.sv.sv_sec.i_cmpl)
            phrase += analyse.sv.sv_sec.advrb
        if analyse.sv.vrb_sub_sentence != []:
            phrase += traite_sub(analyse.sv.vrb_sub_sentence)
        return ['how', 'much'] + analyse.sv.d_obj[0].noun + phrase


def w_question_invitation(analyse):
    phrase = y_o_question(analyse)
    return ['how', 'about'] + phrase[1:]


def w_question_possession(analyse):
    verbe = recup_string(analyse.sv.vrb_main[0])
    phrase = recuperation_element.gr_nominal(analyse.sn)
    phrase = phrase \
        + recuperation_element.conjuguer_verbe_sent(analyse.sv.vrb_tense,
            verbe, analyse.sv.vrb_adv, analyse.sn, analyse.sv.state)
    phrase[0] = 'whose'
    if analyse.sn[0].noun[0].endswith('s') or len(analyse.sn) > 1:
        phrase += ['these']
    else:
        phrase += ['this']
    phrase = phrase \
        + recuperation_element.reconsitu_indirect_compl(analyse.sv.i_cmpl)
    phrase += analyse.sv.advrb
    if analyse.sv.vrb_sub_sentence != []:
        phrase += traite_sub(analyse.sv.vrb_sub_sentence)
    return phrase


def w_question_choice(analyse):
    phrase = statement_sentence(analyse)
    phrase[0] = 'which'
    return phrase



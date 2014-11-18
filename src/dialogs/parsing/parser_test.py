#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi
 06/07/2010
 The package contains the parser unit tests + functions to perform test
 It is more used for the subject
 Functions:
    compare_nominal_group : to compare 2 nominal groups
    compare_icompl : to compare 2 indirect complements
    compare_vs : to compare 2 verbal structures
    compare_sentence : to compare 2 sentences
    compare_utterance : to compare 2 replies
    display_ng : to display nominal group
    display : to display class Sentence
"""

import unittest
import logging
from difflib import unified_diff

from dialogs.sentence import *
import preprocessing
import analyse_sentence


def compare_nominal_group(ng, rslt_ng):
    """
    Function to compare 2 nominal groups
    """

    # init
    i = 0
    j = 0

    if len(ng) != len(rslt_ng):
        return 1
    else:
        while i < len(rslt_ng):
            if rslt_ng[i].det != ng[i].det or rslt_ng[i].adj != ng[i].adj or rslt_ng[i].noun != ng[i].noun:
                return 1

            # We compare the noun complement
            if compare_nominal_group(rslt_ng[i].noun_cmpl, ng[i].noun_cmpl) == 1:
                return 1

            # We compare the relative
            if len(rslt_ng[i].relative) != len(ng[i].relative):
                return 1
            else:
                while j < len(rslt_ng[i].relative):
                    if compare_sentence(rslt_ng[i].relative[j], ng[i].relative[j]) == 1:
                        return 1
                    j += 1

                # reinit
                j = 0

            # We compare the flag (if there is an 'or' or an 'and')
            if rslt_ng[i]._conjunction != ng[i]._conjunction:
                return 1
            if rslt_ng[i]._quantifier != ng[i]._quantifier:
                return 1
            i += 1
        return 0


def compare_icompl(icompl, rslt_icompl):
    """
    Function to compare 2 indirect complements
    """

    # init
    i = 0

    if len(icompl) != len(rslt_icompl):
        return 1
    else:
        while i < len(rslt_icompl):
            if rslt_icompl[i].prep != icompl[i].prep:
                return 1
            if compare_nominal_group(rslt_icompl[i].gn, icompl[i].gn) == 1:
                return 1
            i += 1
        return 0


def compare_vs(vs, rslt_vs):
    """
    Function to compare 2 verbal structures
    """

    # init
    i = 0
    j = 0

    if len(vs) != len(rslt_vs):
        return 1

    else:
        while i < len(rslt_vs):
            if vs[i].vrb_main != rslt_vs[i].vrb_main or \
                            vs[i].vrb_tense != rslt_vs[i].vrb_tense or \
                            vs[i].state != rslt_vs[i].state:
                return 1
            if vs[i].advrb != rslt_vs[i].advrb or vs[i].vrb_adv != rslt_vs[i].vrb_adv:
                return 1

            # We compare the d_obj
            if compare_nominal_group(vs[i].d_obj, rslt_vs[i].d_obj) == 1:
                return 1

            # We compare the i_cmpl
            if compare_icompl(vs[i].i_cmpl, rslt_vs[i].i_cmpl) == 1:
                return 1
            if compare_vs(vs[i].sv_sec, rslt_vs[i].sv_sec) == 1:
                return 1

            # We compare the vrb_sub_sentence
            if len(rslt_vs[i].vrb_sub_sentence) != len(vs[i].vrb_sub_sentence):
                return 1
            else:
                while j < len(rslt_vs[i].vrb_sub_sentence):
                    if compare_sentence(vs[i].vrb_sub_sentence[j], rslt_vs[i].vrb_sub_sentence[j]) == 1:
                        return 1
                    j += 1

            i += 1

        return 0


def compare_sentence(stc, stc_rslt):
    """
    Function to compare 2 sentences
    """
    if stc.data_type != stc_rslt.data_type or stc.aim != stc_rslt.aim:
        return False
    if compare_nominal_group(stc.sn, stc_rslt.sn) == 1:
        return False
    if compare_vs(stc.sv, stc_rslt.sv) == 1:
        return False

    return True


def compare_utterance(utterance, rslt_utterance, sentence_list):
    """
    Function to compare 2 replies
    """

    # init
    i = 0

    if len(utterance) != len(rslt_utterance):
        print('There is a problem with the analyse utterance : length(utterance)!=length(result)')
    else:
        while i < len(rslt_utterance):

            print("The sentence after the analyse utterance is :")
            if i < len(sentence_list):
                print(sentence_list[i])

            print(str(utterance[i]))

            for a in utterance[i].sv:
                for z in a.comparator:
                    print("The comparison in the sentence is : ")
                    print(z['object'])
                    print(str(z['nom_gr'][0]))

            # ok = compare_sentence(utterance[i], rslt_utterance[i])
            ok = (str(utterance[i]) == str(rslt_utterance[i]))
            if not ok:
                print("Parsing result for this sentence is not what was expected.")
                print("Expected result:")
                print(str(rslt_utterance[i]))
                print("Diff:")
                diff = unified_diff(str(utterance[i]).splitlines(),
                                    str(rslt_utterance[i]).splitlines(),
                                    fromfile="what I got",
                                    tofile="what I expected",
                                    n=1)
                print(''.join(diff) + "\033[0m")  # reset the ANSI colors, if any
                return 1
            else:
                print("############### Parsing is OK ###############")
                print('')

            i += 1
    return 0


class TestParsing(unittest.TestCase):
    """
    Function to perform unit tests                                                   
    """

    def test_01(self):
        print('')
        print('######################## test 1.1 ##############################')
        utterance = "The bottle is on the table. The bottle is blue. the bottle is Blue"
        print("Object of this test : To use different cases with a state's verb")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['blue', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], ['Blue'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_02(self):
        print('')
        print('######################## test 1.2 ##############################')
        utterance = "Jido's blue bottle is on the table. I'll play a guitar, a piano and a violon."
        print("Object of this test : To use the complement of the noun and the duplication with 'and'")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [['blue', []]], [NominalGroup([], ['Jido'], [], [], [])],
                             [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'future simple',
                                       [NominalGroup(['a'], ['guitar'], [], [], []),
                                        NominalGroup(['a'], ['piano'], [], [], []),
                                        NominalGroup(['a'], ['violon'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[1].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[1].sv[0].d_obj[1]._quantifier = "SOME"
        rslt[1].sv[0].d_obj[2]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_03(self):
        print('')
        print('######################## test 1.3 ##############################')
        utterance = "It's on the table. I give it to you. give me the bottle. I don't give the bottle to you."
        print("Object of this test : Present the duality between the direct and indirect complement")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup([], ['it'], [], [], [])],
                                       [IndirectComplement(['to'], [NominalGroup([], ['you'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                    [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [], [], [])],
                                       [IndirectComplement(['to'], [NominalGroup([], ['you'], [], [], [])])],
                             [], [], VerbalGroup.negative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_04(self):
        print('')
        print('######################## test 1.4 ##############################')
        utterance = "you aren't preparing the car and my father's moto at the same time. is the bottle of my brother in your right?"
        print("Object of this test : To have more information in sentence and trying the yes or no question")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['prepare'], [], 'present progressive',
                                       [NominalGroup(['the'], ['car'], [], [], []),
                                        NominalGroup(['the'], ['moto'], [],
                                                      [NominalGroup(['my'], ['father'], [], [], [])], [])],
                                       [IndirectComplement(['at'], [
                                           NominalGroup(['the'], ['time'], [['same', []]], [], [])])],
                             [], [], VerbalGroup.negative, [])]),
                Sentence(YES_NO_QUESTION, '',
                         [NominalGroup(['the'], ['bottle'], [], [NominalGroup(['my'], ['brother'], [], [], [])], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['in'], [NominalGroup(['your'], ['right'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_05(self):
        print('')
        print('######################## test 1.5 ##############################')
        utterance = "You shouldn't drive his poorest uncle's wife's big new car. Should I give you the bottle? shall I go"
        print("Object of this test : Using different case of modal")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['should+drive'], [], 'present conditional',
                                       [NominalGroup(['the'], ['car'], [['big', []], ['new', []]],
                                                      [NominalGroup(['the'], ['wife'], [],
                                                                     [NominalGroup(['his'], ['uncle'],
                                                                                    [['poorest', []]], [], [])], [])],
                                           [])],
                             [],
                             [], [], VerbalGroup.negative, [])]),
                Sentence(YES_NO_QUESTION, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['should+give'], [], 'present conditional',
                                       [NominalGroup(['the'], ['bottle'], [], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['you'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(YES_NO_QUESTION, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['shall+go'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_06(self):
        print('')
        print('######################## test 1.6 ##############################')
        utterance = "Isn't he doing his homework and his game now? Can't he take this bottle. good afternoon"
        print("Object of this test : Using different case of modal and start dialogue")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(YES_NO_QUESTION, '',
                         [NominalGroup([], ['he'], [], [], [])],
                         [VerbalGroup(['do'], [], 'present progressive',
                                       [NominalGroup(['his'], ['homework'], [], [], []),
                                        NominalGroup(['his'], ['game'], [], [], [])],
                             [],
                             [], ['now'], VerbalGroup.negative, [])]),
                Sentence(YES_NO_QUESTION, '',
                         [NominalGroup([], ['he'], [], [], [])],
                         [VerbalGroup(['can+take'], [], 'present simple',
                                       [NominalGroup(['this'], ['bottle'], [], [], [])],
                             [],
                             [], [], VerbalGroup.negative, [])]),
                Sentence(START, 'good afternoon.', [], [])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_07(self):
        print('')
        print('######################## test 1.7 ##############################')
        utterance = "Don't quickly give me the blue bottle. I wanna play with my guitar. I'd like to go to the cinema."
        print("Object of this test : Using the second verb of the sentence")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(IMPERATIVE, '',
            [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [['blue', []]], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                                       ['quickly'], [], VerbalGroup.negative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['want'], [VerbalGroup(['play'],
                             [], '',
                             [],
                                                               [IndirectComplement(['with'], [
                                                                   NominalGroup(['my'], ['guitar'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])],
                                       'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['like'], [VerbalGroup(['go'],
                             [], '',
                             [],
                                                               [IndirectComplement(['to'], [
                                                                   NominalGroup(['the'], ['cinema'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])],
                                       'present conditional',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_08(self):
        print('')
        print('######################## test 1.8 ##############################')
        utterance = "the man, who talks, has a new car. I play the guitar, that I bought yesterday,."
        print("Object of this test : Using relative with subject and object")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)
        print(sentence_list)
        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['man'], [], [], [Sentence(RELATIVE, 'who',
                             [],
                                                                            [VerbalGroup(['talk'], [],
                                                                                          'present simple',
                                                                                [],
                                                                                [],
                                                                                [], [], VerbalGroup.affirmative,
                                                                                [])])])],
                         [VerbalGroup(['have'], [], 'present simple',
                                       [NominalGroup(['a'], ['car'], [['new', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'present simple',
                                       [NominalGroup(['the'], ['guitar'], [], [], [Sentence(RELATIVE, 'that',
                                                                                             [NominalGroup([], ['I'],
                                                                                                 [], [], [])],
                                                                                             [VerbalGroup(['buy'], [],
                                                                                                           'past simple',
                                                                                                           [
                                                                                                               NominalGroup(
                                                                                                                   [
                                                                                                                       'the'],
                                                                                                                   [
                                                                                                                       'guitar'],
                                                                                                                   [],
                                                                                                                   [],
                                                                                                                   [])],
                                                                                                 [],
                                                                                                 [], ['yesterday'],
                                                                                                           VerbalGroup.affirmative,
                                                                                                 [])])])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_11(self):
        print('')
        print('######################## test 2.1 ##############################')
        utterance = "don't quickly give me the bottle which is on the table, and the glass which I cleaned yesterday, at my left"
        print("Object of this test : Using nested relative with he duplication with 'and'")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(IMPERATIVE, '',
            [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [], [], [Sentence(RELATIVE, 'which',
                                           [],
                                                                                             [VerbalGroup(['be'], [],
                                                                                                           'present simple',
                                                                                                 [],
                                                                                                           [
                                                                                                               IndirectComplement(
                                                                                                                   [
                                                                                                                       'on'],
                                                                                                                   [
                                                                                                                       NominalGroup(
                                                                                                                           [
                                                                                                                               'the'],
                                                                                                                           [
                                                                                                                               'table'],
                                                                                                                           [],
                                                                                                                           [],
                                                                                                                           [])])],
                                                                                                 [], [],
                                                                                                           VerbalGroup.affirmative,
                                                                                                 [])])]),
                                        NominalGroup(['the'], ['glass'], [], [], [Sentence(RELATIVE, 'which',
                                                                                            [NominalGroup([], ['I'],
                                                                                                [], [], [])],
                                                                                            [VerbalGroup(['clean'], [],
                                                                                                          'past simple',
                                                                                                          [
                                                                                                              NominalGroup(
                                                                                                                  [
                                                                                                                      'the'],
                                                                                                                  [
                                                                                                                      'glass'],
                                                                                                                  [],
                                                                                                                  [],
                                                                                                                  [])],
                                                                                                [],
                                                                                                [], ['yesterday'],
                                                                                                          VerbalGroup.affirmative,
                                                                                                [])])])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])]),
                                        IndirectComplement(['at'], [NominalGroup(['my'], ['left'], [], [], [])])],
                                       ['quickly'], [], VerbalGroup.negative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_12(self):
        print('')
        print('######################## test 2.2 ##############################')
        utterance = "The bottle that I bought from the store which is in the shopping center, , is yours."
        print("Object of this test : Using relative")
        print(utterance)
        print('#################################################################')
        print('')
        print()
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [Sentence(RELATIVE, 'that',
                                                                               [NominalGroup([], ['I'], [], [], [])],
                                                                               [VerbalGroup(['buy'], [], 'past simple',
                                                                                             [NominalGroup(['the'],
                                                                                                            ['bottle'],
                                                                                                 [], [], [])],
                                                                                             [IndirectComplement(
                                                                                                 ['from'], [
                                                                                                     NominalGroup(
                                                                                                         ['the'],
                                                                                                         ['store'], [],
                                                                                                         [], [Sentence(
                                                                                                             RELATIVE,
                                                                                                             'which',
                                                                                                             [],
                                                                                                             [
                                                                                                                 VerbalGroup(
                                                                                                                     [
                                                                                                                         'be'],
                                                                                                                     [],
                                                                                                                     'present simple',
                                                                                                                     [],
                                                                                                                     [
                                                                                                                         IndirectComplement(
                                                                                                                             [
                                                                                                                                 'in'],
                                                                                                                             [
                                                                                                                                 NominalGroup(
                                                                                                                                     [
                                                                                                                                         'the'],
                                                                                                                                     [
                                                                                                                                         'center'],
                                                                                                                                     [
                                                                                                                                         [
                                                                                                                                             'shopping',
                                                                                                                                             []]],
                                                                                                                                     [],
                                                                                                                                     [])])],
                                                                                                                     [],
                                                                                                                     [],
                                                                                                                     VerbalGroup.affirmative,
                                                                                                                     [])])])])],
                                                                                   [], [], VerbalGroup.affirmative,
                                                                                   [])])])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], ['yours'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_13(self):
        print('')
        print('######################## test 2.3 ##############################')
        utterance = "When won't the planning session take place? when must you take the bus"
        print("Object of this test : Using different cases of when questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'date',
                         [NominalGroup(['the'], ['session'], [['planning', []]], [], [])],
                         [VerbalGroup(['take+place'], [], 'future simple',
                             [],
                             [],
                             [], [], VerbalGroup.negative, [])]),
                Sentence(W_QUESTION, 'date',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['must+take'], [], 'present simple',
                                       [NominalGroup(['the'], ['bus'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_14(self):
        print('')
        print('######################## test 2.4 ##############################')
        utterance = "Where is Broyen ? where are you going. Where must Jido and you be from?"
        print("Object of this test : Using different cases of where questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'place',
                         [NominalGroup([], ['Broyen'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'place',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['go'], [], 'present progressive',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'origin',
                         [NominalGroup([], ['Jido'], [], [], []), NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['must+be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_15(self):
        print('')
        print('######################## test 2.5 ##############################')
        utterance = "What time is the news on TV? What size do you wear? the code is written by me. Mahdi is gonna the Laas?"
        print("Object of this test : Using different cases of what questions and forced yes no question")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'time',
                         [NominalGroup(['the'], ['news'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup([], ['TV'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'size',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['wear'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['code'], [], [], [])],
                         [VerbalGroup(['write'], [], 'present passive',
                             [],
                                       [IndirectComplement(['by'], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(YES_NO_QUESTION, '',
                         [NominalGroup([], ['Mahdi'], [], [], [])],
                         [VerbalGroup(['go'], [], 'present progressive',
                             [],
                                       [IndirectComplement(['to'], [NominalGroup(['the'], ['Laas'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_16(self):
        print('')
        print('######################## test 2.6 ##############################')
        utterance = "what is the weather like in the winter here? what were you doing? What isn't Jido going to do tomorrow"
        print("Object of this test : Using different cases of what questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'description',
                         [NominalGroup(['the'], ['weather'], [], [], [])],
                         [VerbalGroup(['like'], [], 'present simple',
                             [],
                                       [IndirectComplement(['in'], [NominalGroup(['the'], ['winter'], [], [], [])])],
                             [], ['here'], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'thing',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['do'], [], 'past progressive',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'thing',
                         [NominalGroup([], ['Jido'], [], [], [])],
                         [VerbalGroup(['go'], [VerbalGroup(['do'],
                             [], '',
                             [],
                             [],
                             [], ['tomorrow'], VerbalGroup.affirmative, [])],
                                       'present progressive',
                             [],
                             [],
                             [], [], VerbalGroup.negative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_17(self):
        print('')
        print('######################## test 2.7 ##############################')
        utterance = "What's happening. What must happen in the company today? What didn't happen here. no. Sorry."
        print("Object of this test : Using different cases of what questions and disagree")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'situation',
            [],
                         [VerbalGroup(['happen'], [], 'present progressive',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'situation',
                    [],
                         [VerbalGroup(['must+happen'], [], 'present simple',
                             [],
                                       [IndirectComplement(['in'], [NominalGroup(['the'], ['company'], [], [], [])])],
                             [], ['today'], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'situation',
                    [],
                         [VerbalGroup(['happen'], [], 'past simple',
                             [],
                             [],
                             [], ['here'], VerbalGroup.negative, [])]),
                Sentence('disagree', 'no.', [], []),
                Sentence('disagree', 'sorry.', [], [])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_18(self):
        print('')
        print('######################## test 2.8 ##############################')
        utterance = "What is the biggest bottle's color on your left. What does your brother do for a living?"
        print("Object of this test : Using different cases of what questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'thing',
                         [NominalGroup(['the'], ['color'], [],
                                        [NominalGroup(['the'], ['bottle'], [['biggest', []]], [], [])], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['your'], ['left'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'explication',
                         [NominalGroup(['your'], ['brother'], [], [], [])],
                         [VerbalGroup(['do'], [], 'present simple',
                             [],
                                       [IndirectComplement(['for'],
                                                            [NominalGroup(['a'], [], [['living', []]], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[1].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_21(self):
        print('')
        print('######################## test 3.1 ##############################')
        utterance = "What type of people don't read this magazine? what kind of music must he listen to everyday"
        print("Object of this test : Using different cases of what questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'classification+people',
            [],
                         [VerbalGroup(['read'], [], 'present simple',
                                       [NominalGroup(['this'], ['magazine'], [], [], [])],
                             [],
                             [], [], VerbalGroup.negative, [])]),
                Sentence(W_QUESTION, 'classification+music',
                         [NominalGroup([], ['he'], [], [], [])],
                         [VerbalGroup(['must+listen+to'], [], 'present simple',
                             [],
                                       [IndirectComplement([], [NominalGroup([], ['everyday'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_22(self):
        print('')
        print('######################## test 3.2 ##############################')
        utterance = "What kind of sport is your favorite? what is the problem with him? what is the matter with this person"
        print("Object of this test : Using different cases of what questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'classification+sport',
                         [NominalGroup(['your'], [], [['favorite', []]], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'thing',
                         [NominalGroup(['the'], ['problem'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['with'], [NominalGroup([], ['him'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'thing',
                         [NominalGroup(['the'], ['matter'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['with'],
                                                            [NominalGroup(['this'], ['person'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_23(self):
        print('')
        print('######################## test 3.3 ##############################')
        utterance = "How old are you? how long is your uncle's store opened tonight? how long is your uncle's store open tonight?"
        print("Object of this test : Using different cases of how questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'old',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'long',
                         [NominalGroup(['the'], ['store'], [], [NominalGroup(['your'], ['uncle'], [], [], [])], [])],
                         [VerbalGroup(['open'], [], 'present passive',
                             [],
                             [],
                             [], ['tonight'], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'long',
                         [NominalGroup(['the'], ['store'], [], [NominalGroup(['your'], ['uncle'], [], [], [])], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['open', []]], [], [])],
                             [],
                             [], ['tonight'], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_24(self):
        print('')
        print('######################## test 3.4 ##############################')
        utterance = "how far is it from the hotel to the restaurant? how soon can you be here? How often does Jido go skiing?"
        print("Object of this test : Using different cases of how questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'far',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['from'], [NominalGroup(['the'], ['hotel'], [], [], [])]),
                                        IndirectComplement(['to'],
                                                            [NominalGroup(['the'], ['restaurant'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'soon',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['can+be'], [], 'present simple',
                             [],
                             [],
                             [], ['here'], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'often',
                         [NominalGroup([], ['Jido'], [], [], [])],
                         [VerbalGroup(['go+skiing'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_25(self):
        print('')
        print('######################## test 3.5 ##############################')
        utterance = "how much water should they transport? how many guests weren't at the party? how much does the motocycle cost"
        print("Object of this test : Using different cases of how questions of quantity")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'quantity',
                         [NominalGroup([], ['they'], [], [], [])],
                         [VerbalGroup(['should+transport'], [], 'present conditional',
                                       [NominalGroup(['a'], ['water'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'quantity',
                         [NominalGroup(['a'], ['guests'], [], [], [])],
                         [VerbalGroup(['be'], [], 'past simple',
                             [],
                                       [IndirectComplement(['at'], [NominalGroup(['the'], ['party'], [], [], [])])],
                             [], [], VerbalGroup.negative, [])]),
                Sentence(W_QUESTION, 'quantity',
                         [NominalGroup(['the'], ['motocycle'], [], [], [])],
                         [VerbalGroup(['cost'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_26(self):
        print('')
        print('######################## test 3.6 ##############################')
        utterance = "How about going to the cinema? how have not they gotten a loan for their business? OK"
        print("Object of this test : Using different cases of how questions and agree")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'invitation',
            [],
                         [VerbalGroup(['go'], [], 'present progressive',
                             [],
                                       [IndirectComplement(['to'], [NominalGroup(['the'], ['cinema'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'manner',
                         [NominalGroup([], ['they'], [], [], [])],
                         [VerbalGroup(['get'], [], 'present perfect',
                                       [NominalGroup(['a'], ['loan'], [], [], [])],
                                       [IndirectComplement(['for'],
                                                            [NominalGroup(['their'], ['business'], [], [], [])])],
                             [], [], VerbalGroup.negative, [])]),
                Sentence('agree', 'OK.', [], [])]

        rslt[1].sv[0].d_obj[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_27(self):
        print('')
        print('######################## test 3.7 ##############################')
        utterance = "How did you like Steven Spilburg's new movie. how could I get to the restaurant from here"
        print("Object of this test : Using different cases of how questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'opinion',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['like'], [], 'past simple',
                                       [NominalGroup(['the'], ['movie'], [['new', []]],
                                                      [NominalGroup([], ['Steven Spilburg'], [], [], [])], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'manner',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['could+get+to'], [], 'present conditional',
                                       [NominalGroup(['the'], ['restaurant'], [], [], [])],
                                       [IndirectComplement(['from'], [NominalGroup([], ['here'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_28(self):
        print('')
        print('######################## test 3.8 ##############################')
        utterance = "Why should she go to Toulouse? who could you talk to on the phone. Whose blue bottle and red glass are these."
        print("Object of this test : Using different cases of why, who and Whose questions")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'reason',
                         [NominalGroup([], ['she'], [], [], [])],
                         [VerbalGroup(['should+go'], [], 'present conditional',
                             [],
                                       [IndirectComplement(['to'], [NominalGroup([], ['Toulouse'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'people',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['could+talk'], [], 'present conditional',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['phone'], [], [], [])]),
                                        IndirectComplement(['to'], [NominalGroup([], ['it'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'owner',
                         [NominalGroup(['that'], ['bottle'], [['blue', []]], [], []),
                          NominalGroup(['that'], ['glass'], [['red', []]], [], [])],
                         [VerbalGroup(['be'], [], '',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_31(self):
        print('')
        print('######################## test 4.1 ##############################')
        utterance = "What are you thinking about the idea that I present you? what color is the bottle that you bought,"
        print("Object of this test : Using different cases of what question with relative" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'opinion',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['think+about'], [], 'present progressive',
                                       [NominalGroup(['the'], ['idea'], [], [], [Sentence(RELATIVE, 'that',
                                                                                           [NominalGroup([], ['I'], [],
                                                                                               [], [])],
                                                                                           [VerbalGroup(['present'],
                                                                                               [], 'present simple',
                                                                                                         [NominalGroup(
                                                                                                             ['the'],
                                                                                                             ['idea'],
                                                                                                             [], [],
                                                                                                             [])],
                                                                                                         [
                                                                                                             IndirectComplement(
                                                                                                                 [], [
                                                                                                                     NominalGroup(
                                                                                                                         [],
                                                                                                                           [
                                                                                                                               'you'],
                                                                                                                         [],
                                                                                                                         [],
                                                                                                                         [])])],
                                                                                               [], [],
                                                                                                         VerbalGroup.affirmative,
                                                                                               [])])])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'color',
                         [NominalGroup(['the'], ['bottle'], [], [], [Sentence(RELATIVE, 'that',
                                                                               [NominalGroup([], ['you'], [], [], [])],
                                                                               [VerbalGroup(['buy'], [], 'past simple',
                                                                                             [NominalGroup(['the'],
                                                                                                            ['bottle'],
                                                                                                 [], [], [])],
                                                                                   [],
                                                                                   [], [], VerbalGroup.affirmative,
                                                                                   [])])])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_32(self):
        print('')
        print('######################## test 4.2 ##############################')
        utterance = "Which salesperson's competition won the award which we won in the last years"
        print("Object of this test : Using different cases of what question with relative" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'choice',
                         [NominalGroup(['the'], ['competition'], [],
                                        [NominalGroup(['the'], ['salesperson'], [], [], [])], [])],
                         [VerbalGroup(['win'], [], 'past simple',
                                       [NominalGroup(['the'], ['award'], [], [], [Sentence(RELATIVE, 'which',
                                                                                            [NominalGroup([], ['we'],
                                                                                                [], [], [])],
                                                                                            [VerbalGroup(['win'], [],
                                                                                                          'past simple',
                                                                                                          [
                                                                                                              NominalGroup(
                                                                                                                  [
                                                                                                                      'the'],
                                                                                                                  [
                                                                                                                      'award'],
                                                                                                                  [],
                                                                                                                  [],
                                                                                                                  [])],
                                                                                                          [
                                                                                                              IndirectComplement(
                                                                                                                  [
                                                                                                                      'in'],
                                                                                                                  [
                                                                                                                      NominalGroup(
                                                                                                                          [
                                                                                                                              'the'],
                                                                                                                          [
                                                                                                                              'year'],
                                                                                                                          [
                                                                                                                              [
                                                                                                                                  'last',
                                                                                                                                  []]],
                                                                                                                          [],
                                                                                                                          [])])],
                                                                                                [], [],
                                                                                                          VerbalGroup.affirmative,
                                                                                                [])])])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[0].relative[0].sv[0].i_cmpl[0].gn[0]._quantifier = "ALL"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_33(self):
        print('')
        print('######################## test 4.3 ##############################')
        utterance = "what'll your house look like? what do you think of the latest novel which Jido wrote"
        print("Object of this test : Using different cases of what question with relative")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'description',
                         [NominalGroup(['your'], ['house'], [], [], [])],
                         [VerbalGroup(['look+like'], [], 'future simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'opinion',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['think+of'], [], 'present simple',
                                       [NominalGroup(['the'], ['novel'], [['latest', []]], [],
                                                      [Sentence(RELATIVE, 'which',
                                                                [NominalGroup([], ['Jido'], [], [], [])],
                                                                [VerbalGroup(['write'], [], 'past simple',
                                                                              [NominalGroup(['the'], ['novel'],
                                                                                             [['latest', []]], [], [])],
                                                                    [],
                                                                    [], [], VerbalGroup.affirmative, [])])])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_34(self):
        print('')
        print('######################## test 4.4 ##############################')
        utterance = "learn that I want you to give me the blue bottle,. If you do your job, you will be happy."
        print("Object of this test : Using different cases of what question with relative" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(IMPERATIVE, '',
            [],
                         [VerbalGroup(['learn'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'that',
                                                                         [NominalGroup([], ['I'], [], [], [])],
                                                                         [VerbalGroup(['want'],
                                                                                       [VerbalGroup(['give'], [], '',
                                                                                                     [NominalGroup(
                                                                                                         ['the'],
                                                                                                         ['bottle'],
                                                                                                         [['blue', []]],
                                                                                                         [], [])],
                                                                                                     [
                                                                                                         IndirectComplement(
                                                                                                             [], [
                                                                                                                 NominalGroup(
                                                                                                                     [],
                                                                                                                       [
                                                                                                                           'me'],
                                                                                                                     [],
                                                                                                                     [],
                                                                                                                     [])])],
                                                                                           [], [],
                                                                                                     VerbalGroup.affirmative,
                                                                                           [])], 'present simple',
                                                                                       [NominalGroup([], ['you'], [],
                                                                                           [], [])],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['be'], [], 'future simple',
                                       [NominalGroup([], [], [['happy', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'if',
                                                                         [NominalGroup([], ['you'], [], [], [])],
                                                                         [VerbalGroup(['do'], [], 'present simple',
                                                                                       [NominalGroup(['your'], ['job'],
                                                                                           [], [], [])],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_35(self):
        print('')
        print('######################## test 4.5 ##############################')
        utterance = "what is wrong with him? I'll play a guitar or a piano and a violon. I played a guitar a year ago."
        print(
            "Object of this test : Using wrong in the what questions, using the 'or' and moving preposition like 'ago'")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'thing',
                         [NominalGroup([], [], ['wrong'], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['with'], [NominalGroup([], ['him'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'future simple',
                                       [NominalGroup(['a'], ['guitar'], [], [], []),
                                        NominalGroup(['a'], ['piano'], [], [], []),
                                        NominalGroup(['a'], ['violon'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'past simple',
                                       [NominalGroup(['a'], ['guitar'], [], [], [])],
                                       [IndirectComplement(['ago'], [NominalGroup(['a'], ['year'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[1].sv[0].d_obj[1]._conjunction = "OR"
        rslt[1].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[1].sv[0].d_obj[1]._quantifier = "SOME"
        rslt[1].sv[0].d_obj[2]._quantifier = "SOME"
        rslt[2].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[2].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_36(self):
        print('')
        print('######################## test 4.6 ##############################')
        utterance = "this is a bottle. There is a bottle on the table"
        print("Object of this test : To use different demonstrative determinant" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['this'], [], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup(['a'], ['bottle'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['a'], ['bottle'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[1].sn[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_37(self):
        print('')
        print('######################## test 4.7 ##############################')

        utterance = "What do you do for a living in this building? What does your brother do for a living here"
        print("Object of this test : Correct duality between nominal group with and without noun" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'explication',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['do'], [], 'present simple',
                             [],
                                       [IndirectComplement(['for'],
                                                            [NominalGroup(['a'], [], [['living', []]], [], [])]),
                                        IndirectComplement(['in'],
                                                            [NominalGroup(['this'], ['building'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'explication',
                         [NominalGroup(['your'], ['brother'], [], [], [])],
                         [VerbalGroup(['do'], [], 'present simple',
                             [],
                                       [IndirectComplement(['for'],
                                                            [NominalGroup(['a'], [], [['living', []]], [], [])])],
                             [], ['here'], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"
        rslt[1].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_38(self):
        print('')
        print('######################## test 4.8 ##############################')
        utterance = "To whom are you talking? you should have the bottle. would you have played a guitar. you would have played a guitar"
        print("Object of this test : Using 'to whom' and passive conditional")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'people',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['talk+to'], [], 'present progressive',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['should+have'], [], 'present conditional',
                                       [NominalGroup(['the'], ['bottle'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(YES_NO_QUESTION, '',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['play'], [], 'past conditional',
                                       [NominalGroup(['a'], ['guitar'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['play'], [], 'past conditional',
                                       [NominalGroup(['a'], ['guitar'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[2].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[3].sv[0].d_obj[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_41(self):
        print('')
        print('######################## test 5.1 ##############################')
        utterance = "you'd like the blue bottle or the glass? the green or blue bottle is on the table. the green or the blue glass is mine?"
        print("Object of this test : Process 'OR'")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(YES_NO_QUESTION, '',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['like'], [], 'present conditional',
                                       [NominalGroup(['the'], ['bottle'], [['blue', []]], [], []),
                                        NominalGroup(['the'], ['glass'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [['green', []]], [], []),
                          NominalGroup(['the'], ['bottle'], [['blue', []]], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(YES_NO_QUESTION, '',
                         [NominalGroup(['the'], ['glass'], [['green', []]], [], []),
                          NominalGroup(['the'], ['glass'], [['blue', []]], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], ['mine'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[1]._conjunction = "OR"
        rslt[1].sn[1]._conjunction = "OR"
        rslt[2].sn[1]._conjunction = "OR"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_42(self):
        print('')
        print('######################## test 5.2 ##############################')

        utterance = "learn that I want you to give me the blue bottle that is blue."
        print("Object of this test : Duality between 'that' derminant and 'that' of adverbial")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(IMPERATIVE, '',
            [],
                         [VerbalGroup(['learn'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'that',
                                                                         [NominalGroup([], ['I'], [], [], [])],
                                                                         [VerbalGroup(['want'],
                                                                                       [VerbalGroup(['give'], [], '',
                                                                                                     [NominalGroup(
                                                                                                         ['the'],
                                                                                                         ['bottle'],
                                                                                                         [['blue', []]],
                                                                                                         [], [Sentence(
                                                                                                             RELATIVE,
                                                                                                             'that',
                                                                                                             [],
                                                                                                             [
                                                                                                                 VerbalGroup(
                                                                                                                     [
                                                                                                                         'be'],
                                                                                                                     [],
                                                                                                                     'present simple',
                                                                                                                     [
                                                                                                                         NominalGroup(
                                                                                                                             [],
                                                                                                                             [],
                                                                                                                               [
                                                                                                                                   [
                                                                                                                                       'blue',
                                                                                                                                       []]],
                                                                                                                             [],
                                                                                                                             [])],
                                                                                                                     [],
                                                                                                                     [],
                                                                                                                     [],
                                                                                                                     VerbalGroup.affirmative,
                                                                                                                     [])])])],
                                                                                                     [
                                                                                                         IndirectComplement(
                                                                                                             [], [
                                                                                                                 NominalGroup(
                                                                                                                     [],
                                                                                                                       [
                                                                                                                           'me'],
                                                                                                                     [],
                                                                                                                     [],
                                                                                                                     [])])],
                                                                                           [], [],
                                                                                                     VerbalGroup.affirmative,
                                                                                           [])], 'present simple',
                                                                                       [NominalGroup([], ['you'], [],
                                                                                           [], [])],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_43(self):
        print('')
        print('######################## test 5.3 ##############################')
        utterance = "The bottle is behind to me. The bottle is next to the table in front of the kitchen."
        print("Object of this test : Using preposition with more than one word")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['behind+to'], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['next+to'],
                                                            [NominalGroup(['the'], ['table'], [], [], [])]),
                                        IndirectComplement(['in+front+of'],
                                                            [NominalGroup(['the'], ['kitchen'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_44(self):
        print('')
        print('######################## test 5.4 ##############################')
        utterance = "Take the bottle carefully. I take that bottle that I drink in. I take twenty two bottles."
        print("Object of this test : Find adverb after verb, duplicate information in relative and include numbers")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(IMPERATIVE, '',
            [],
                         [VerbalGroup(['take'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [], [], [])],
                             [],
                                       ['carefully'], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['take'], [], 'present simple',
                                       [NominalGroup(['that'], ['bottle'], [], [], [Sentence(RELATIVE, 'that',
                                                                                              [NominalGroup([], ['I'],
                                                                                                  [], [], [])],
                                                                                              [VerbalGroup(['drink'],
                                                                                                  [], 'present simple',
                                                                                                  [],
                                                                                                            [
                                                                                                                IndirectComplement(
                                                                                                                    [
                                                                                                                        'in'],
                                                                                                                    [
                                                                                                                        NominalGroup(
                                                                                                                            [
                                                                                                                                'that'],
                                                                                                                            [
                                                                                                                                'bottle'],
                                                                                                                            [],
                                                                                                                            [],
                                                                                                                            [])])],
                                                                                                  [], [],
                                                                                                            VerbalGroup.affirmative,
                                                                                                  [])])])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['take'], [], 'present simple',
                                       [NominalGroup(['22'], ['bottle'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[2].sv[0].d_obj[0]._quantifier = "DIGIT"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_45(self):
        print('')
        print('######################## test 5.5 ##############################')
        utterance = "I'll play Jido's guitar, a saxophone, a piano of the wife of my oncle and Patrick's violon."
        print("Object of this test : Process with many 'of' and 'and'")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'future simple',
                                       [NominalGroup(['the'], ['guitar'], [],
                                                      [NominalGroup([], ['Jido'], [], [], [])], []),
                                        NominalGroup(['a'], ['saxophone'], [], [], []),
                                        NominalGroup(['a'], ['piano'], [], [NominalGroup(['the'], ['wife'], [], [
                                            NominalGroup(['my'], ['oncle'], [], [], [])], [])], []),
                                        NominalGroup(['the'], ['violon'], [],
                                                      [NominalGroup([], ['Patrick'], [], [], [])], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[1]._quantifier = "SOME"
        rslt[0].sv[0].d_obj[2]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_46(self):
        print('')
        print('######################## test 5.6 ##############################')
        utterance = "Give me two or three bottles. the bottle is blue, big and fanny. give me the bottle on the table"
        print("Object of this test : Using numbers, many adjectives and transform indirect complement into relative")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(IMPERATIVE, '',
            [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['2'], ['bottle'], [], [], []),
                                        NominalGroup(['3'], ['bottle'], [], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['blue', []], ['big', []], ['fanny', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                    [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [], [], [Sentence(RELATIVE, 'which',
                                           [],
                                                                                             [VerbalGroup(['be'], [],
                                                                                                           'present simple',
                                                                                                 [],
                                                                                                           [
                                                                                                               IndirectComplement(
                                                                                                                   [
                                                                                                                       'on'],
                                                                                                                   [
                                                                                                                       NominalGroup(
                                                                                                                           [
                                                                                                                               'the'],
                                                                                                                           [
                                                                                                                               'table'],
                                                                                                                           [],
                                                                                                                           [],
                                                                                                                           [])])],
                                                                                                 [], [],
                                                                                                           VerbalGroup.affirmative,
                                                                                                 [])])])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[1]._conjunction = "OR"
        rslt[0].sv[0].d_obj[0]._quantifier = "DIGIT"
        rslt[0].sv[0].d_obj[1]._quantifier = "DIGIT"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_47(self):
        print('')
        print('######################## test 5.7 ##############################')
        utterance = "the boys' ball is blue. He ask me to do something. is any person courageous on the laboratory"
        print("Object of this test : 'of' in plural and using more determinant")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['ball'], [], [NominalGroup(['the'], ['boy'], [], [], [])], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['blue', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['he'], [], [], [])],
                         [VerbalGroup(['ask'], [VerbalGroup(['do'], [], '',
                                                              [NominalGroup([], ['something'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])], 'present simple',
                                       [NominalGroup([], ['me'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(YES_NO_QUESTION, '',
                         [NominalGroup(['any'], ['person'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['courageous', []]], [], [])],
                                       [IndirectComplement(['on'],
                                                            [NominalGroup(['the'], ['laboratory'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sn[0].noun_cmpl[0]._quantifier = "ALL"
        rslt[2].sn[0]._quantifier = "ANY"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_48(self):
        print('')
        print('######################## test 5.8 ##############################')
        utterance = "What must be happened in the company today? The building shouldn't be built fastly. You can be here."
        print("Object of this test : Process be+verb+ed")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'situation',
            [],
                         [VerbalGroup(['must+happen'], [], 'present passive',
                             [],
                                       [IndirectComplement(['in'], [NominalGroup(['the'], ['company'], [], [], [])])],
                             [], ['today'], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['building'], [], [], [])],
                         [VerbalGroup(['should+build'], [], 'passive conditional',
                             [],
                             [],
                                       ['fastly'], [], VerbalGroup.negative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['can+be'], [], 'present simple',
                             [],
                             [],
                             [], ['here'], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_51(self):
        print('')
        print('######################## test 6.1 ##############################')
        utterance = "what size is the best one? What object is blue? How good is this"
        print("Object of this test : Generalize the w question")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(W_QUESTION, 'size',
                         [NominalGroup(['the'], ['one'], [['best', []]], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'object',
                    [],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['blue', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'good',
                         [NominalGroup(['this'], [], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_52(self):
        print('')
        print('######################## test 6.2 ##############################')
        utterance = "He Patrick, the bottle is on the table. give it to me"
        print("Object of this test : Using interjection in different cases")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence('interjection', '',
                         [NominalGroup([], ['Patrick'], [], [], [])],
            []),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                         [NominalGroup([], ['Patrick'], [], [], [])],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup([], ['it'], [], [], [])],
                                       [IndirectComplement(['to'], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_53(self):
        print('')
        print('######################## test 6.3 ##############################')
        utterance = "Jido, give me the bottle. Jido, Patrick and you will go to the cinema. Jido, Patrick and you, give me the bottle"
        print("Object of this test : Using interjection in different cases")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence('interjection', '',
                         [NominalGroup([], ['Jido'], [], [], [])],
                         [VerbalGroup([], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                         [NominalGroup([], ['Jido'], [], [], [])],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['Jido'], [], [], []), NominalGroup([], ['Patrick'], [], [], []),
                          NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['go'], [], 'future simple',
                             [],
                                       [IndirectComplement(['to'], [NominalGroup(['the'], ['cinema'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence('interjection', '',
                         [NominalGroup([], ['Jido'], [], [], []), NominalGroup([], ['Patrick'], [], [], []),
                          NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup([], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                         [NominalGroup([], ['Jido'], [], [], []), NominalGroup([], ['Patrick'], [], [], []),
                          NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_54(self):
        print('')
        print('######################## test 6.4 ##############################')

        utterance = "The bottle is not blue but it is red. It is not the glass but the bottle. it is blue or red"
        print("Object of this test : Process 'BUT' as conjunction and adverbial")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['blue', []]], [], [])],
                             [],
                             [], [], VerbalGroup.negative, [Sentence('subsentence+statement', 'but',
                                                                      [NominalGroup([], ['it'], [], [], [])],
                                                                      [VerbalGroup(['be'], [], 'present simple',
                                                                                    [NominalGroup([], [],
                                                                                                     [['red', []]], [],
                                                                                        [])],
                                                                          [],
                                                                          [], [], VerbalGroup.affirmative, [])])])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup(['the'], ['glass'], [], [], []),
                                        NominalGroup(['the'], ['bottle'], [], [], [])],
                             [],
                             [], [], VerbalGroup.negative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['blue', []]], [], []),
                                        NominalGroup([], [], [['red', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[1].sv[0].d_obj[1]._conjunction = "BUT"
        rslt[2].sv[0].d_obj[1]._conjunction = "OR"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_55(self):
        print('')
        print('######################## test 6.5 ##############################')

        utterance = "It is not red but blue. this is my banana. bananas are fruits."
        print("Object of this test : Process plural")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['red', []]], [], []),
                                        NominalGroup([], [], [['blue', []]], [], [])],
                             [],
                             [], [], VerbalGroup.negative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['this'], [], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup(['my'], ['banana'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['banana'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], ['fruit'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[1]._conjunction = "BUT"
        rslt[2].sn[0]._quantifier = "ALL"
        rslt[2].sv[0].d_obj[0]._quantifier = "ALL"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_56(self):
        print('')
        print('######################## test 6.6 ##############################')
        utterance = "there are no bananas. All bananas are here. give me more information about the bottle."
        print("Object of this test : More determinants and transformation of the indirect complement" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['no'], ['banana'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['all'], ['banana'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], ['here'], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                    [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['more'], ['information'], [], [], [Sentence(RELATIVE, 'which',
                                           [],
                                                                                                   [VerbalGroup(['be'],
                                                                                                       [],
                                                                                                                 'present simple',
                                                                                                       [],
                                                                                                                 [
                                                                                                                     IndirectComplement(
                                                                                                                         [
                                                                                                                             'about'],
                                                                                                                         [
                                                                                                                             NominalGroup(
                                                                                                                                 [
                                                                                                                                     'the'],
                                                                                                                                 [
                                                                                                                                     'bottle'],
                                                                                                                                 [],
                                                                                                                                 [],
                                                                                                                                 [])])],
                                                                                                       [], [],
                                                                                                                 VerbalGroup.affirmative,
                                                                                                       [])])])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sn[0]._quantifier = "SOME"
        rslt[0].sn[0]._quantifier = "ANY"
        rslt[1].sn[0]._quantifier = "ALL"
        rslt[2].sv[0].d_obj[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_57(self):
        print('')
        print('######################## test 6.7 ##############################')
        utterance = "Jido, tell me where you go. Goodbye. Bye. there is nothing. it is another one."
        print("Object of this test : More determinants and ending the dialog" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence('interjection', '',
                         [NominalGroup([], ['Jido'], [], [], [])],
                         [VerbalGroup([], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                         [NominalGroup([], ['Jido'], [], [], [])],
                         [VerbalGroup(['tell'], [], 'present simple',
                             [],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])]),
                                        IndirectComplement([],
                                                              [NominalGroup(['the'], ['location'], [], [],
                                                                             [Sentence(RELATIVE, 'where',
                                                                                       [NominalGroup([],
                                                                                                        ['you'], [], [],
                                                                                           [])],
                                                                                       [VerbalGroup(
                                                                                           ['go'], [],
                                                                                           'present simple',
                                                                                           [],
                                                                                           [],
                                                                                           [], [],
                                                                                           VerbalGroup.affirmative,
                                                                                           [])])])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(END, '', [], []),
                Sentence(END, '', [], []),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['nothing'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup(['another'], ['one'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[4].sn[0]._quantifier = "NONE"
        rslt[5].sv[0].d_obj[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_58(self):
        print('')
        print('######################## test 6.8 ##############################')
        utterance = "The bottle becomes blue. One piece could become two, if you smoldered it."
        print("Object of this test : More state verb and numbers" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [])],
                         [VerbalGroup(['become'], [], 'present simple',
                                       [NominalGroup([], [], [['blue', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['1'], ['piece'], [], [], [])],
                         [VerbalGroup(['could+become'], [], 'present conditional',
                                       [NominalGroup(['2'], [], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'if',
                                                                         [NominalGroup([], ['you'], [], [], [])],
                                                                         [VerbalGroup(['smolder'], [], 'past simple',
                                                                                       [NominalGroup([], ['it'], [],
                                                                                           [], [])],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])])]

        rslt[1].sn[0]._quantifier = "DIGIT"
        rslt[1].sv[0].d_obj[0]._quantifier = "DIGIT"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_61(self):
        print('')
        print('######################## test 7.1 ##############################')
        utterance = "This one is not the bottle of my uncle but it is the bottle of my brother. It is not on the table but on the shelf."
        print("Object of this test : Using 'but' with indirect complement")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['this'], ['one'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [],
                                                      [NominalGroup(['my'], ['uncle'], [], [], [])], [])],
                             [],
                             [], [], VerbalGroup.negative, [Sentence('subsentence+statement', 'but',
                                                                      [NominalGroup([], ['it'], [], [], [])],
                                                                      [VerbalGroup(['be'], [], 'present simple',
                                                                                    [NominalGroup(['the'], ['bottle'],
                                                                                        [], [NominalGroup(['my'],
                                                                                                           ['brother'],
                                                                                            [], [], [])], [])],
                                                                          [],
                                                                          [], [], VerbalGroup.affirmative, [])])])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], []),
                                                                     NominalGroup(['the'], ['shelf'], [], [], [])])],
                             [], [], VerbalGroup.negative, [])])]

        rslt[1].sv[0].i_cmpl[0].gn[1]._conjunction = "BUT"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_62(self):
        print('')
        print('######################## test 7.2 ##############################')
        utterance = "Give me the fourth and seventh bottle. Give me the one thousand ninth and the thirty thousand twenty eighth bottle."
        print("Object of this test : Porcess adjective numbers")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(IMPERATIVE, '',
            [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [['4th', []]], [], []),
                                        NominalGroup(['the'], ['bottle'], [['7th', []]], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                    [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['bottle'], [['1009th', []]], [], []),
                                        NominalGroup(['the'], ['bottle'], [['30028th', []]], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_63(self):
        print('')
        print('######################## test 7.3 ##############################')
        utterance = "the evil tyrant is in the laboratory. I don't know what are you talking about."
        print("Object of this test : Adjectives can't be noun and complete indirect coomplement" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['tyrant'], [['evil', []]], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['in'],
                                                            [NominalGroup(['the'], ['laboratory'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['know'], [], 'present simple',
                                       [NominalGroup(['the'], ['thing'], [], [], [Sentence(RELATIVE, 'that',
                                                                                            [NominalGroup([], ['you'],
                                                                                                [], [], [])],
                                                                                            [VerbalGroup(['talk'], [],
                                                                                                          'present progressive',
                                                                                                          [
                                                                                                              NominalGroup(
                                                                                                                  [
                                                                                                                      'the'],
                                                                                                                  [
                                                                                                                      'thing'],
                                                                                                                  [],
                                                                                                                  [],
                                                                                                                  [])],
                                                                                                          [
                                                                                                              IndirectComplement(
                                                                                                                  [
                                                                                                                      'about'],
                                                                                                                  [
                                                                                                                      NominalGroup(
                                                                                                                          [],
                                                                                                                            [
                                                                                                                                'it'],
                                                                                                                          [],
                                                                                                                          [],
                                                                                                                          [])])],
                                                                                                [], [],
                                                                                                          VerbalGroup.affirmative,
                                                                                                [])])])],
                             [],
                             [], [], VerbalGroup.negative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_64(self):
        print('')
        print('######################## test 7.4 ##############################')
        utterance = "I go to the place where I was born. I study where you studied. I study where you build your house where you put the bottle."
        print("Object of this test : Duality between relative and adverbial" )
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['go'], [], 'present simple',
                             [],
                                       [IndirectComplement(['to'], [
                                           NominalGroup(['the'], ['place'], [], [], [Sentence(RELATIVE, 'where',
                                                                                               [NominalGroup([], ['I'],
                                                                                                   [], [], [])],
                                                                                               [VerbalGroup(['be'], [],
                                                                                                             'past simple',
                                                                                                             [
                                                                                                                 NominalGroup(
                                                                                                                     [],
                                                                                                                     [],
                                                                                                                       [
                                                                                                                           [
                                                                                                                               'born',
                                                                                                                               []]],
                                                                                                                     [],
                                                                                                                     [])],
                                                                                                   [],
                                                                                                   [], [],
                                                                                                             VerbalGroup.affirmative,
                                                                                                   [])])])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['study'], [], 'present simple',
                             [],
                                       [IndirectComplement(['in'], [
                                           NominalGroup(['the'], ['location'], [], [], [Sentence(RELATIVE, 'where',
                                                                                                  [NominalGroup([],
                                                                                                                   [
                                                                                                                       'you'],
                                                                                                      [], [],
                                                                                                      [])],
                                                                                                  [VerbalGroup(
                                                                                                      ['study'], [],
                                                                                                      'past simple',
                                                                                                      [],
                                                                                                      [],
                                                                                                      [], [],
                                                                                                      VerbalGroup.affirmative,
                                                                                                      [])])])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['study'], [], 'present simple',
                             [],
                                       [IndirectComplement(['in'], [
                                           NominalGroup(['the'], ['location'], [], [], [Sentence(RELATIVE, 'where',
                                                                                                  [NominalGroup([],
                                                                                                                   [
                                                                                                                       'you'],
                                                                                                      [], [],
                                                                                                      [])],
                                                                                                  [VerbalGroup(
                                                                                                      ['build'], [],
                                                                                                      'present simple',
                                                                                                      [NominalGroup(
                                                                                                          ['your'],
                                                                                                          ['house'], [],
                                                                                                          [], [Sentence(
                                                                                                              RELATIVE,
                                                                                                              'where',
                                                                                                              [
                                                                                                                  NominalGroup(
                                                                                                                      [],
                                                                                                                        [
                                                                                                                            'you'],
                                                                                                                      [],
                                                                                                                      [],
                                                                                                                      [])],
                                                                                                              [
                                                                                                                  VerbalGroup(
                                                                                                                      [
                                                                                                                          'put'],
                                                                                                                      [],
                                                                                                                      'present simple',
                                                                                                                      [
                                                                                                                          NominalGroup(
                                                                                                                              [
                                                                                                                                  'the'],
                                                                                                                              [
                                                                                                                                  'bottle'],
                                                                                                                              [],
                                                                                                                              [],
                                                                                                                              [])],
                                                                                                                      [],
                                                                                                                      [],
                                                                                                                      [],
                                                                                                                      VerbalGroup.affirmative,
                                                                                                                      [])])])],
                                                                                                      [],
                                                                                                      [], [],
                                                                                                      VerbalGroup.affirmative,
                                                                                                      [])])])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_65(self):
        print('')
        print('######################## test 7.5 ##############################')
        utterance = "apples grow on trees and plants. give me three apples."
        print("Object of this test : Plural with duplication")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['apple'], [], [], [])],
                         [VerbalGroup(['grow'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup([], ['tree'], [], [], []),
                                                                     NominalGroup([], ['plant'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                    [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['3'], ['apple'], [], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sn[0]._quantifier = "ALL"
        rslt[0].sv[0].i_cmpl[0].gn[0]._quantifier = "ALL"
        rslt[0].sv[0].i_cmpl[0].gn[1]._quantifier = "ALL"
        rslt[1].sv[0].d_obj[0]._quantifier = "DIGIT"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_66(self):
        print('')
        print('######################## test 7.6 ##############################')
        utterance = "When your father came, we was preparing the dinner. While I phoned, he made a sandwich with bacons."
        print("Object of this test : Process adverbial at the beginning of the sentence")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['we'], [], [], [])],
                         [VerbalGroup(['prepare'], [], 'past progressive',
                                       [NominalGroup(['the'], ['dinner'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'when',
                                                                         [NominalGroup(['your'], ['father'], [], [],
                                                                             [])],
                                                                         [VerbalGroup(['come'], [], 'past simple',
                                                                             [],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['he'], [], [], [])],
                         [VerbalGroup(['make'], [], 'past simple',
                                       [NominalGroup(['a'], ['sandwich'], [], [], [Sentence(RELATIVE, 'which',
                                           [],
                                                                                             [VerbalGroup(['be'], [],
                                                                                                           'present simple',
                                                                                                 [],
                                                                                                           [
                                                                                                               IndirectComplement(
                                                                                                                   [
                                                                                                                       'with'],
                                                                                                                   [
                                                                                                                       NominalGroup(
                                                                                                                           [],
                                                                                                                             [
                                                                                                                                 'bacon'],
                                                                                                                           [],
                                                                                                                           [],
                                                                                                                           [])])],
                                                                                                 [], [],
                                                                                                           VerbalGroup.affirmative,
                                                                                                 [])])])],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'while',
                                                                         [NominalGroup([], ['I'], [], [], [])],
                                                                         [VerbalGroup(['phone'], [], 'past simple',
                                                                             [],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])])]

        rslt[1].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[1].sv[0].d_obj[0].relative[0].sv[0].i_cmpl[0].gn[0]._quantifier = "ALL"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_67(self):
        print('')
        print('######################## test 7.7 ##############################')
        utterance = "the big and very strong man is on the corner. the too big and very strong man is on the corner."
        print("Object of this test : Add contifier for adjectives")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['man'], [['big', []], ['strong', ['very']]], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['corner'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['man'], [['big', ['too']], ['strong', ['very']]], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['corner'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_68(self):
        print('')
        print('######################## test 7.8 ##############################')
        utterance = "red apples grow on green trees and plants. a kind of thing. It can be played by thirty thousand twenty eight players."
        print("Object of this test : Using adjectives wuth plural")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['apple'], [['red', []]], [], [])],
                         [VerbalGroup(['grow'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'],
                                                            [NominalGroup([], ['tree'], [['green', []]], [], []),
                                                             NominalGroup([], ['plant'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['a'], ['kind'], [], [NominalGroup(['a'], ['thing'], [], [], [])], [])],
                    []),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['can+play'], [], 'present passive',
                             [],
                                       [IndirectComplement(['by'],
                                                            [NominalGroup(['30028'], ['player'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sn[0]._quantifier = "ALL"
        rslt[0].sv[0].i_cmpl[0].gn[0]._quantifier = "ALL"
        rslt[0].sv[0].i_cmpl[0].gn[1]._quantifier = "ALL"
        rslt[1].sn[0]._quantifier = "SOME"
        rslt[1].sn[0].noun_cmpl[0]._quantifier = "SOME"
        rslt[2].sv[0].i_cmpl[0].gn[0]._quantifier = "DIGIT"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_70(self):
        print('')
        print('######################## test 8.1 ##############################')
        utterance = "let the man go to the cinema. Is it the time to let you go. And where is the other tape."
        print("Object of this test : Porcess verb with many second verbs")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(IMPERATIVE, '',
            [],
                         [VerbalGroup(['let'], [VerbalGroup(['go'],
                             [], '',
                             [],
                                                              [IndirectComplement(['to'], [
                                                                  NominalGroup(['the'], ['cinema'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])], 'present simple',
                                       [NominalGroup(['the'], ['man'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(YES_NO_QUESTION, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['be'], [VerbalGroup(['let'],
                                                             [VerbalGroup(['go'],
                                                                 [], '',
                                                                 [],
                                                                 [],
                                                                 [], [], VerbalGroup.affirmative, [])], '',
                                                             [NominalGroup([], ['you'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])], 'present simple',
                                       [NominalGroup(['the'], ['time'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'place',
                         [NominalGroup(['the'], ['tape'], [['other', []]], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_71(self):
        print('')
        print('######################## test 8.2 ##############################')
        utterance = "And now, can you reach the tape. it could have been them. It is just me at the door. A strong clause can stand on its own"
        print("Object of this test : Process with 'and' in the beginning and more examples")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(YES_NO_QUESTION, '',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['can+reach'], [], 'present simple',
                                       [NominalGroup(['the'], ['tape'], [], [], [])],
                             [],
                             [], ['now'], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['could+be'], [], 'passive conditional',
                                       [NominalGroup([], ['them'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['it'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], ['me'], [], [], [])],
                                       [IndirectComplement(['at'], [NominalGroup(['the'], ['door'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['a'], ['clause'], [['strong', []]], [], [])],
                         [VerbalGroup(['can+stand'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['its'], ['own'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[3].sn[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_72(self):
        print('')
        print('######################## test 8.3 ##############################')
        utterance = "tell me what to do. No, I can not reach it."
        print("Object of this test : Using sentences like 'agree' with another sentence (seperatite by comma)")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(IMPERATIVE, '',
            [],
                         [VerbalGroup(['tell'], [], 'present simple',
                             [],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])]),
                                        IndirectComplement([],
                                                              [NominalGroup(['the'], ['thing'], [], [],
                                                                             [Sentence(RELATIVE, 'that',
                                                                                 [],
                                                                                       [VerbalGroup(['be'], [
                                                                                           VerbalGroup(
                                                                                               ['do'], [], '',
                                                                                               [],
                                                                                               [],
                                                                                               [], [],
                                                                                               VerbalGroup.affirmative,
                                                                                               [])],
                                                                                                     'present simple',
                                                                                           [],
                                                                                           [],
                                                                                           [], [],
                                                                                                     VerbalGroup.affirmative,
                                                                                           [])])])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence('disagree', 'no.', [], []),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['can+reach'], [], 'present simple',
                                       [NominalGroup([], ['it'], [], [], [])],
                             [],
                             [], [], VerbalGroup.negative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_73(self):
        print('')
        print('######################## test 8.4 ##############################')
        utterance = "I will come back on monday. I'll play with guitar. I'll play football"
        print("Object of this test : Using sentences like 'agree' with another sentence (seperatite by comma)")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['come+back'], [], 'future simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup([], ['Monday'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'future simple',
                             [],
                                       [IndirectComplement(['with'], [NominalGroup(['a'], ['guitar'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'future simple',
                                       [NominalGroup(['a'], ['football'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[1].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"
        rslt[2].sv[0].d_obj[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_74(self):
        print('')
        print('######################## test 8.5 ##############################')
        utterance = "I'll play guitar, piano and violon. I'll play with guitar, piano and violon. give me everything"
        print("Object of this test : To take off determinant")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'future simple',
                                       [NominalGroup(['a'], ['guitar'], [], [], []),
                                        NominalGroup(['a'], ['piano'], [], [], []),
                                        NominalGroup(['a'], ['violon'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'future simple',
                             [],
                                       [IndirectComplement(['with'], [NominalGroup(['a'], ['guitar'], [], [], []),
                                                                       NominalGroup(['a'], ['piano'], [], [], []),
                                                                       NominalGroup(['a'], ['violon'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                    [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup([], ['everything'], [], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[0].sv[0].d_obj[1]._quantifier = "SOME"
        rslt[0].sv[0].d_obj[2]._quantifier = "SOME"
        rslt[1].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"
        rslt[1].sv[0].i_cmpl[0].gn[1]._quantifier = "SOME"
        rslt[1].sv[0].i_cmpl[0].gn[2]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_75(self):
        print('')
        print('######################## test 8.6 ##############################')
        utterance = "I will come back at seven o'clock tomorrow. He finish the project 10 minutes before."
        print("Object of this test : Process some time with digit")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['come+back'], [], 'future simple',
                             [],
                                       [IndirectComplement(['at'], [NominalGroup(['7'], ["o'clock"], [], [], [])])],
                             [], ['tomorrow'], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['he'], [], [], [])],
                         [VerbalGroup(['finish'], [], 'present simple',
                                       [NominalGroup(['the'], ['project'], [], [], [])],
                                       [IndirectComplement(['before'],
                                                            [NominalGroup(['10'], ['minute'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].i_cmpl[0].gn[0]._quantifier = "DIGIT"
        rslt[1].sv[0].i_cmpl[0].gn[0]._quantifier = "DIGIT"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_76(self):
        print('')
        print('######################## test 8.7 ##############################')
        utterance = "I'll play a guitar a piano and a violon. I'll play with a guitar a piano and a violon. the boss you and me are here"
        print("Object of this test : To take off comma between the nominal groups")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'future simple',
                                       [NominalGroup(['a'], ['guitar'], [], [], []),
                                        NominalGroup(['a'], ['piano'], [], [], []),
                                        NominalGroup(['a'], ['violon'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'future simple',
                             [],
                                       [IndirectComplement(['with'], [NominalGroup(['a'], ['guitar'], [], [], []),
                                                                       NominalGroup(['a'], ['piano'], [], [], []),
                                                                       NominalGroup(['a'], ['violon'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['boss'], [], [], []), NominalGroup([], ['you'], [], [], []),
                          NominalGroup([], ['me'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], ['here'], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[0].sv[0].d_obj[1]._quantifier = "SOME"
        rslt[0].sv[0].d_obj[2]._quantifier = "SOME"
        rslt[1].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"
        rslt[1].sv[0].i_cmpl[0].gn[1]._quantifier = "SOME"
        rslt[1].sv[0].i_cmpl[0].gn[2]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


    def test_77(self):
        print('')
        print('######################## test 8.8 ##############################')
        utterance = "The time of speaking sentence is the best. I come at 10pm. I will come tomorrow evening"
        print("Object of this test : Add test to take off determinant and for timescale")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['time'], [],
                                        [NominalGroup(['a'], ['sentence'], [['speaking', []]], [], [])], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup(['the'], [], [['best', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['come'], [], 'present simple',
                             [],
                                       [IndirectComplement(['at'], [NominalGroup(['10'], ['pm'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['come'], [], 'future simple',
                             [],
                                       [IndirectComplement([], [NominalGroup(['a'], ['evening'], [], [], [])])],
                             [], ['tomorrow'], VerbalGroup.affirmative, [])])]

        rslt[0].sn[0].noun_cmpl[0]._quantifier = 'SOME'
        rslt[1].sv[0].i_cmpl[0].gn[0]._quantifier = "DIGIT"
        rslt[2].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_81(self):
        print('')
        print('######################## test 9.1 ##############################')
        utterance = "I think that I know who is he. see you. So I want to go"
        print("Object of this test : Process relative without object, so we duplicate the nominal group")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['think'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'that',
                                                                         [NominalGroup([], ['I'], [], [], [])],
                                                                         [VerbalGroup(['know'], [], 'present simple',
                                                                                       [NominalGroup([], ['he'], [],
                                                                                           [], [Sentence(RELATIVE,
                                                                                                         'who',
                                                                                               [],
                                                                                                         [VerbalGroup(
                                                                                                             ['be'], [],
                                                                                                             'present simple',
                                                                                                             [
                                                                                                                 NominalGroup(
                                                                                                                     [],
                                                                                                                       [
                                                                                                                           'he'],
                                                                                                                     [],
                                                                                                                     [],
                                                                                                                     [])],
                                                                                                             [],
                                                                                                             [], [],
                                                                                                             VerbalGroup.affirmative,
                                                                                                             [])])])],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])]),
                Sentence(END, '', [], []),
                Sentence('', '', [],
                         [VerbalGroup([], [], '', [], [], [], [], VerbalGroup.affirmative,
                                         [Sentence('subsentence+statement', 'so',
                                                   [NominalGroup([], ['I'], [], [], [])],
                                                   [VerbalGroup(['want'], [VerbalGroup(['go'], [], '',
                                                       [],
                                                       [],
                                                       [], [], VerbalGroup.affirmative, [])], 'present simple',
                                                       [],
                                                       [],
                                                       [], [], VerbalGroup.affirmative, [])])])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_82(self):
        print('')
        print('######################## test 9.2 ##############################')
        utterance = "the interpretation is to find a defenition or a rule for something. and in a dialog, there is an interaction between them"
        print("Object of this test : Put indirect complement or second verb before the sentence")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['interpretation'], [], [], [])],
                         [VerbalGroup(['be'], [VerbalGroup(['find'], [], '',
                                                             [NominalGroup(['a'], ['defenition'], [], [], []),
                                                              NominalGroup(['a'], ['rule'], [], [], [])],
                                                             [IndirectComplement(['for'], [
                                                                 NominalGroup([], ['something'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup(['an'], ['interaction'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['between'], [NominalGroup([], ['them'], [], [], [])]),
                                        IndirectComplement(['in'], [NominalGroup(['a'], ['dialog'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].sv_sec[0].d_obj[0]._quantifier = "SOME"
        rslt[0].sv[0].sv_sec[0].d_obj[1]._quantifier = "SOME"
        rslt[0].sv[0].sv_sec[0].d_obj[1]._conjunction = "OR"
        rslt[1].sn[0]._quantifier = "SOME"
        rslt[1].sv[0].i_cmpl[1].gn[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_83(self):
        print('')
        print('######################## test 9.3 ##############################')
        utterance = "To have a dialog, we need more than 1 protagonist. I finish the dialog, and I check many problems"
        print(
            "Object of this test : Having indirect complement before the sentence and to have more one sentence in utterance")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['we'], [], [], [])],
                         [VerbalGroup(['need'], [VerbalGroup(['have'], [], '',
                                                               [NominalGroup(['a'], ['dialog'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['finish'], [], 'present simple',
                                       [NominalGroup(['the'], ['dialog'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['check'], [], 'present simple',
                                       [NominalGroup([], ['problem'], [['many', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].sv_sec[0].d_obj[0]._quantifier = "SOME"
        rslt[2].sv[0].d_obj[0]._quantifier = "ALL"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_84(self):
        print('')
        print('######################## test 9.4 ##############################')
        utterance = "the left of what? Jido, what do you do? throw one of them. Very good"
        print("Object of this test : Question at the end of sentence")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['left'], [], [NominalGroup(['a'], ['what'], [], [], [])], [])],
                         [VerbalGroup([], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence('interjection', '',
                         [NominalGroup([], ['Jido'], [], [], [])],
                         [VerbalGroup([], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'thing',
                         [NominalGroup([], ['you'], [], [], [])],
                         [VerbalGroup(['do'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(IMPERATIVE, '',
                         [NominalGroup([], ['Jido'], [], [], [])],
                         [VerbalGroup(['throw'], [], 'present simple',
                                       [NominalGroup(['1'], [], [], [NominalGroup([], ['them'], [], [], [])], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence('agree', 'good.', [], [])]

        rslt[0].sn[0].noun_cmpl[0]._quantifier = "SOME"
        rslt[3].sv[0].d_obj[0]._quantifier = "DIGIT"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_85(self):
        print('')
        print('######################## test 9.5 ##############################')
        utterance = "the bottle on the table, is blue. where is this tape"
        print("Object of this test : add relative and process nominal group with this as determinant and be as a verb")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [], [Sentence(RELATIVE, 'which',
                             [],
                                                                               [VerbalGroup(['be'], [],
                                                                                             'present simple',
                                                                                   [],
                                                                                             [IndirectComplement(
                                                                                                 ['on'], [NominalGroup(
                                                                                                     ['the'], ['table'],
                                                                                                     [], [], [])])],
                                                                                   [], [], VerbalGroup.affirmative,
                                                                                   [])])])],
                         [VerbalGroup(['be'], [], 'present simple',
                                       [NominalGroup([], [], [['blue', []]], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(W_QUESTION, 'place',
                         [NominalGroup(['this'], ['tape'], [], [], [])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                             [],
                             [], [], VerbalGroup.affirmative, [])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_86(self):
        print('')
        print('######################## test 9.6 ##############################')
        utterance = "the bottle of Jido which is blue, is on the table. I do my homework before he comes"
        print("Object of this test : nominal group with relative and noun complement and using before as subsentence")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup(['the'], ['bottle'], [], [NominalGroup([], ['Jido'], [], [], [])],
                                        [Sentence(RELATIVE, 'which',
                                            [],
                                                  [VerbalGroup(['be'], [], 'present simple',
                                                                [NominalGroup([], [], [['blue', []]], [], [])],
                                                      [],
                                                      [], [], VerbalGroup.affirmative, [])])])],
                         [VerbalGroup(['be'], [], 'present simple',
                             [],
                                       [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['do'], [], 'present simple',
                                       [NominalGroup(['my'], ['homework'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'before',
                                                                         [NominalGroup([], ['he'], [], [], [])],
                                                                         [VerbalGroup(['come'], [], 'present simple',
                                                                             [],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])])]

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_87(self):
        print('')
        print('######################## test 9.7 ##############################')
        utterance = "before he comes, I do my homework. I have played foot since I was a young boy."
        print("Object of this test : Using proposal like 'before' as subsentence, i_cmpl and adjective")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['do'], [], 'present simple',
                                       [NominalGroup(['my'], ['homework'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'before',
                                                                         [NominalGroup([], ['he'], [], [], [])],
                                                                         [VerbalGroup(['come'], [], 'present simple',
                                                                             [],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])]),
                Sentence(STATEMENT, '',
                         [NominalGroup([], ['I'], [], [], [])],
                         [VerbalGroup(['play'], [], 'present perfect',
                                       [NominalGroup(['a'], ['foot'], [], [], [])],
                             [],
                             [], [], VerbalGroup.affirmative, [Sentence('subsentence+statement', 'since',
                                                                         [NominalGroup([], ['I'], [], [], [])],
                                                                         [VerbalGroup(['be'], [], 'past simple',
                                                                                       [NominalGroup(['a'], ['boy'],
                                                                                                      [['young', []]],
                                                                                           [], [])],
                                                                             [],
                                                                             [], [], VerbalGroup.affirmative,
                                                                             [])])])])]

        rslt[1].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[1].sv[0].vrb_sub_sentence[0].sv[0].d_obj[0]._quantifier = "SOME"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)

    def test_88(self):
        print('')
        print('######################## test 9.8 ##############################')
        utterance = "They haven't played tennis since 1987. give me the glass the paper and the bottle."
        print("Object of this test : Final test with present perfect and parsing and with many nominal group")
        print(utterance)
        print('#################################################################')
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        rslt = [Sentence(STATEMENT, '',
                         [NominalGroup([], ['they'], [], [], [])],
                         [VerbalGroup(['play'], [], 'present perfect',
                                       [NominalGroup(['a'], ['tennis'], [], [], [])],
                                       [IndirectComplement(['since'], [NominalGroup(['1987'], [], [], [], [])])],
                             [], [], VerbalGroup.negative, [])]),
                Sentence(IMPERATIVE, '',
                    [],
                         [VerbalGroup(['give'], [], 'present simple',
                                       [NominalGroup(['the'], ['glass'], [], [], []),
                                        NominalGroup(['the'], ['paper'], [], [], []),
                                        NominalGroup(['the'], ['bottle'], [], [], [])],
                                       [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                             [], [], VerbalGroup.affirmative, [])])]

        rslt[0].sv[0].d_obj[0]._quantifier = "SOME"
        rslt[0].sv[0].i_cmpl[0].gn[0]._quantifier = "DIGIT"

        result_test = compare_utterance(class_list, rslt, sentence_list)
        self.assertEquals(result_test, 0)


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestParsing)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite())

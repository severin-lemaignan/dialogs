#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi
 08/07/2010
 The package contains functions to perform test
 It is more used for the subject
 Functions:
    unit_tests : to perform unit tests
"""

import unittest
import logging

logger = logging.getLogger("dialogs")

from dialogs.dialog_core import Dialog

from dialogs.parsing.parser import Parser
from dialogs.sentence import *
from dialogs.sentence_types import *
from dialogs.verbalization import utterance_rebuilding


class TestVerbalization(unittest.TestCase):
    """
    Function to compare 2 nominal groups   
    """


    def test_01(self):
        logger.info('\n######################## test 1.1 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The bottle is on the table. The bottle is blue. The bottle is Blue."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['bottle'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['table'], [], [], [])])],
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_02(self):
        logger.info('\n######################## test 1.2 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Jido's blue bottle is on the table. I'll play a guitar, a piano and a violon."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['bottle'], [['blue', []]],
                                             [NominalGroup([], ['Jido'], [], [], [])], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['table'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['play'], [], 'future simple',
                                            [NominalGroup(['a'], ['guitar'], [], [], []),
                                             NominalGroup(['a'], ['piano'], [], [], []),
                                             NominalGroup(['a'], ['violon'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)


    def test_03(self):
        logger.info('\n######################## test 1.3 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "It's on the table. I give it to you. Give me the bottle. I don't give the bottle to you."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup([], ['it'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['table'], [], [], [])])],
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_04(self):
        logger.info('\n######################## test 1.4 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "You aren't preparing the car and my father's moto at the same time. Is my brother's bottle in your right?"

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['prepare'], [], 'present progressive',
                                            [NominalGroup(['the'], ['car'], [], [], []),
                                             NominalGroup(['the'], ['moto'], [],
                                                           [NominalGroup(['my'], ['father'], [], [], [])], [])],
                                            [IndirectComplement(['at'], [
                                                NominalGroup(['the'], ['time'], [['same', []]], [], [])])],
                                  [], [], VerbalGroup.negative, [])]),
                     Sentence(YES_NO_QUESTION, '',
                              [NominalGroup(['the'], ['bottle'], [], [NominalGroup(['my'], ['brother'], [], [], [])],
                                  [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['in'],
                                                                 [NominalGroup(['your'], ['right'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_05(self):
        logger.info('\n######################## test 1.5 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "You shouldn't drive his poorest uncle's wife's big new car. Should I give you the bottle? Shall I go?"

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['should+drive'], [], 'present conditional',
                                            [NominalGroup(['the'], ['car'], [['big', []], ['new', []]],
                                                           [NominalGroup(['the'], ['wife'], [],
                                                                          [NominalGroup(['his'], ['uncle'],
                                                                                         [['poorest', []]], [], [])],
                                                               [])], [])],
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)


    def test_06(self):
        logger.info('\n######################## test 1.6 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Isn't he doing his homework and his game now? Can't he take this bottle? Hello."

        sentences = [Sentence(YES_NO_QUESTION, '',
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
                     Sentence(START, '', [], [])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_07(self):
        logger.info('\n######################## test 1.7 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Don't quickly give me the blue bottle. I want to play with my guitar. I'd like to go to the cinema."

        sentences = [Sentence(IMPERATIVE, '',
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
                                                                        NominalGroup(['my'], ['guitar'], [], [],
                                                                            [])])],
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
                                                                        NominalGroup(['the'], ['cinema'], [], [],
                                                                            [])])],
                                  [], [], VerbalGroup.affirmative, [])],
                                            'present conditional',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_08(self):
        logger.info('\n######################## test 1.8 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The man who talks, has a new car. I play the guitar that I bought yesterday."

        sentences = [Sentence(STATEMENT, '',
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
                                                                                                  [NominalGroup([],
                                                                                                      ['I'], [], [],
                                                                                                      [])],
                                                                                                  [VerbalGroup(['buy'],
                                                                                                      [], 'past simple',
                                                                                                      [],
                                                                                                      [],
                                                                                                      [], ['yesterday'],
                                                                                                                VerbalGroup.affirmative,
                                                                                                      [])])])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_09(self):
        logger.info('\n######################## test 1.9 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Don't quickly give me the bottle which is on the table, and the glass which I cleaned yesterday, at my left."

        sentences = [Sentence(IMPERATIVE, '',
            [],
                              [VerbalGroup(['give'], [], 'present simple',
                                            [NominalGroup(['the'], ['bottle'], [], [], [Sentence(RELATIVE, 'which',
                                                [],
                                                                                                  [VerbalGroup(['be'],
                                                                                                      [],
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
                                                                                                 [NominalGroup([],
                                                                                                     ['I'], [], [],
                                                                                                     [])],
                                                                                                 [VerbalGroup(
                                                                                                     ['clean'], [],
                                                                                                     'past simple',
                                                                                                     [],
                                                                                                     [],
                                                                                                     [], ['yesterday'],
                                                                                                     VerbalGroup.affirmative,
                                                                                                     [])])])],
                                            [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])]),
                                             IndirectComplement(['at'],
                                                                 [NominalGroup(['my'], ['left'], [], [], [])])],
                                            ['quickly'], [], VerbalGroup.negative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_10(self):
        logger.info('\n######################## test 1.10 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The bottle that I bought from the store which is in the shopping center, is yours."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['bottle'], [], [], [Sentence(RELATIVE, 'that',
                                                                                    [NominalGroup([], ['I'], [], [],
                                                                                        [])],
                                                                                    [VerbalGroup(['buy'], [],
                                                                                                  'past simple',
                                                                                        [],
                                                                                                  [IndirectComplement(
                                                                                                      ['from'], [
                                                                                                          NominalGroup(
                                                                                                              ['the'],
                                                                                                              ['store'],
                                                                                                              [], [], [
                                                                                                                  Sentence(
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
                                                                                        [], [],
                                                                                                  VerbalGroup.affirmative,
                                                                                        [])])])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup([], ['yours'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_11(self):
        logger.info('\n######################## test 1.11 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "When won't the planning session take place? When must you take the bus?"

        sentences = [Sentence(W_QUESTION, 'date',
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_12(self):
        logger.info('\n######################## test 1.12 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Where is Broyen? Where are you going? Where must Jido and you be from?"

        sentences = [Sentence(W_QUESTION, 'place',
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_13(self):
        logger.info('\n######################## test 1.13 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What time is the news on TV? What size do you wear? The code is written by me. Is Mahdi going to the Laas?"

        sentences = [Sentence(W_QUESTION, 'time',
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
                                            [IndirectComplement(['to'],
                                                                 [NominalGroup(['the'], ['Laas'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_14(self):
        logger.info('\n######################## test 1.14 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What's the weather like in the winter here? What were you doing? What isn't Jido going to do tomorrow?"

        sentences = [Sentence(W_QUESTION, 'description',
                              [NominalGroup(['the'], ['weather'], [], [], [])],
                              [VerbalGroup(['like'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['in'],
                                                                 [NominalGroup(['the'], ['winter'], [], [], [])])],
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_15(self):
        logger.info('\n######################## test 1.15 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What's happening? What must happen in the company today? What didn't happen here? No, sorry."

        sentences = [Sentence(W_QUESTION, 'situation',
            [],
                              [VerbalGroup(['happen'], [], 'present progressive',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'situation',
                         [],
                              [VerbalGroup(['must+happen'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['in'],
                                                                 [NominalGroup(['the'], ['company'], [], [], [])])],
                                  [], ['today'], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'situation',
                         [],
                              [VerbalGroup(['happen'], [], 'past simple',
                                  [],
                                  [],
                                  [], ['here'], VerbalGroup.negative, [])]),
                     Sentence('disagree', '', [], [])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_16(self):
        logger.info('\n######################## test 1.16 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What's the biggest bottle's color on your left? What does your brother do for a living?"

        sentences = [Sentence(W_QUESTION, 'thing',
                              [NominalGroup(['the'], ['color'], [],
                                             [NominalGroup(['the'], ['bottle'], [['biggest', []]], [], [])], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['your'], ['left'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'explication',
                              [NominalGroup(['your'], ['brother'], [], [], [])],
                              [VerbalGroup(['do'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['for'],
                                                                 [NominalGroup(['a'], [], [['living', []]], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_17(self):
        logger.info('\n######################## test 1.17 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What kind of people don't read this magazine? What kind of music must he listen to everyday?"

        sentences = [Sentence(W_QUESTION, 'classification+people',
            [],
                              [VerbalGroup(['read'], [], 'present simple',
                                            [NominalGroup(['this'], ['magazine'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.negative, [])]),
                     Sentence(W_QUESTION, 'classification+music',
                              [NominalGroup([], ['he'], [], [], [])],
                              [VerbalGroup(['must+listen+to'], [], 'present simple',
                                  [],
                                  [],
                                  [], ['everyday'], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_18(self):
        logger.info('\n######################## test 1.18 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What kind of sport is your favorite? What's the problem with him? What's the matter with this person?"

        sentences = [Sentence(W_QUESTION, 'classification+sport',
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_19(self):
        logger.info('\n######################## test 1.19 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "How old are you? How long is your uncle's store opened tonight? How long is your uncle's store open tonight?"

        sentences = [Sentence(W_QUESTION, 'old',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'long',
                              [NominalGroup(['the'], ['store'], [], [NominalGroup(['your'], ['uncle'], [], [], [])],
                                  [])],
                              [VerbalGroup(['open'], [], 'present passive',
                                  [],
                                  [],
                                  [], ['tonight'], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'long',
                              [NominalGroup(['the'], ['store'], [], [NominalGroup(['your'], ['uncle'], [], [], [])],
                                  [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup([], [], [['open', []]], [], [])],
                                  [],
                                  [], ['tonight'], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_20(self):
        logger.info('\n######################## test 1.20 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "How far is it from the hotel to the restaurant? How soon can you be here? How often does Jido go skiing?"

        sentences = [Sentence(W_QUESTION, 'far',
                              [NominalGroup([], ['it'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['from'],
                                                                 [NominalGroup(['the'], ['hotel'], [], [], [])]),
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_21(self):
        logger.info('\n######################## test 1.21 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "How much water should they transport? How much guests weren't at the party? How much does the motocycle cost?"

        sentences = [Sentence(W_QUESTION, 'quantity',
                              [NominalGroup([], ['they'], [], [], [])],
                              [VerbalGroup(['should+transport'], [], 'present conditional',
                                            [NominalGroup(['a'], ['water'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'quantity',
                              [NominalGroup(['a'], ['guests'], [], [], [])],
                              [VerbalGroup(['be'], [], 'past simple',
                                  [],
                                            [IndirectComplement(['at'],
                                                                 [NominalGroup(['the'], ['party'], [], [], [])])],
                                  [], [], VerbalGroup.negative, [])]),
                     Sentence(W_QUESTION, 'quantity',
                              [NominalGroup(['the'], ['motocycle'], [], [], [])],
                              [VerbalGroup(['cost'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_22(self):
        logger.info('\n######################## test 1.22 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "How about going to the cinema? How haven't they gotten a loan for their business? OK."

        sentences = [Sentence(W_QUESTION, 'invitation',
            [],
                              [VerbalGroup(['go'], [], 'present progressive',
                                  [],
                                            [IndirectComplement(['to'],
                                                                 [NominalGroup(['the'], ['cinema'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'manner',
                              [NominalGroup([], ['they'], [], [], [])],
                              [VerbalGroup(['get'], [], 'present perfect',
                                            [NominalGroup(['a'], ['loan'], [], [], [])],
                                            [IndirectComplement(['for'],
                                                                 [NominalGroup(['their'], ['business'], [], [], [])])],
                                  [], [], VerbalGroup.negative, [])]),
                     Sentence(AGREEMENT, '', [], [])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_23(self):
        logger.info('\n######################## test 1.23 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What did you think of Steven Spilburg's new movie? How could I get to the restaurant from here?"

        sentences = [Sentence(W_QUESTION, 'opinion',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['like'], [], 'past simple',
                                            [NominalGroup(['the'], ['movie'], [['new', []]],
                                                           [NominalGroup([], ['Steven', 'Spilburg'], [], [], [])],
                                                [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'manner',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['could+get+to'], [], 'present conditional',
                                            [NominalGroup(['the'], ['restaurant'], [], [], [])],
                                            [IndirectComplement(['from'], [NominalGroup([], ['here'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_24(self):
        logger.info('\n######################## test 1.24 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Why should she go to Toulouse? Who could you talk to on the phone? Whose blue bottle and red glass are these?"

        sentences = [Sentence(W_QUESTION, 'reason',
                              [NominalGroup([], ['she'], [], [], [])],
                              [VerbalGroup(['should+go'], [], 'present conditional',
                                  [],
                                            [IndirectComplement(['to'],
                                                                 [NominalGroup([], ['Toulouse'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'people',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['could+talk+to'], [], 'present conditional',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['phone'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(W_QUESTION, 'owner',
                              [NominalGroup([], ['bottle'], [['blue', []]], [], []),
                               NominalGroup([], ['glass'], [['red', []]], [], [])],
                              [VerbalGroup(['be'], [], '',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_25(self):
        logger.info('\n######################## test 1.25 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What are you thinking about the idea that I present you? What color is the bottle which you bought?"

        sentences = [Sentence(W_QUESTION, 'opinion',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['think+about'], [], 'present progressive',
                                            [NominalGroup(['the'], ['idea'], [], [], [Sentence(RELATIVE, 'that',
                                                                                                [NominalGroup([],
                                                                                                    ['I'], [], [], [])],
                                                                                                [VerbalGroup(
                                                                                                    ['present'], [],
                                                                                                    'present simple',
                                                                                                    [],
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
                              [NominalGroup(['the'], ['bottle'], [], [], [Sentence(RELATIVE, 'which',
                                                                                    [NominalGroup([], ['you'], [], [],
                                                                                        [])],
                                                                                    [VerbalGroup(['buy'], [],
                                                                                                  'past simple',
                                                                                        [],
                                                                                        [],
                                                                                        [], [],
                                                                                                  VerbalGroup.affirmative,
                                                                                        [])])])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_26(self):
        logger.info('\n######################## test 1.26 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Which salesperson's competition won the award which we won in the last years?"

        sentences = [Sentence(W_QUESTION, 'choice',
                              [NominalGroup(['the'], ['competition'], [],
                                             [NominalGroup(['the'], ['salesperson'], [], [], [])], [])],
                              [VerbalGroup(['win'], [], 'past simple',
                                            [NominalGroup(['the'], ['award'], [], [], [Sentence(RELATIVE, 'which',
                                                                                                 [NominalGroup([],
                                                                                                     ['we'], [], [],
                                                                                                     [])],
                                                                                                 [VerbalGroup(['win'],
                                                                                                     [], 'past simple',
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

        sentences[0].sv[0].d_obj[0].relative[0].sv[0].i_cmpl[0].gn[0]._quantifier = "ALL"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_27(self):
        logger.info('\n######################## test 1.27 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What will your house look like? What do you think of the latest novel which Jido wrote?"

        sentences = [Sentence(W_QUESTION, 'description',
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
                                                                         [],
                                                                         [],
                                                                         [], [], VerbalGroup.affirmative, [])])])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_28(self):
        logger.info('\n######################## test 1.28 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Learn that I want you to give me the blue bottle. You'll be happy, if you do your job."

        sentences = [Sentence(IMPERATIVE, '',
            [],
                              [VerbalGroup(['learn'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'that',
                                                                              [NominalGroup([], ['I'], [], [], [])],
                                                                              [VerbalGroup(['want'], [
                                                                                  VerbalGroup(['give'], [], '',
                                                                                               [NominalGroup(['the'], [
                                                                                                   'bottle'], [['blue',
                                                                                                                   []]],
                                                                                                   [], [])],
                                                                                               [IndirectComplement([],
                                                                                                   [NominalGroup([],
                                                                                                       ['me'], [], [],
                                                                                                       [])])],
                                                                                      [], [], VerbalGroup.affirmative,
                                                                                      [])], 'present simple',
                                                                                            [NominalGroup([], ['you'],
                                                                                                [], [], [])],
                                                                                  [],
                                                                                  [], [], VerbalGroup.affirmative,
                                                                                  [])])])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['be'], [], 'future simple',
                                            [NominalGroup([], [], [['happy', []]], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'if',
                                                                              [NominalGroup([], ['you'], [], [], [])],
                                                                              [VerbalGroup(['do'], [],
                                                                                            'present simple',
                                                                                            [NominalGroup(['your'],
                                                                                                           ['job'], [],
                                                                                                [], [])],
                                                                                  [],
                                                                                  [], [], VerbalGroup.affirmative,
                                                                                  [])])])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)


    def test_29(self):
        logger.info('\n######################## test 1.29 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "You'll be happy, if you do your job. Do you want the blue or green bottle?"

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['be'], [], 'future simple',
                                            [NominalGroup([], [], [['happy', []]], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'if',
                                                                              [NominalGroup([], ['you'], [], [], [])],
                                                                              [VerbalGroup(['do'], [],
                                                                                            'present simple',
                                                                                            [NominalGroup(['your'],
                                                                                                           ['job'], [],
                                                                                                [], [])],
                                                                                  [],
                                                                                  [], [], VerbalGroup.affirmative,
                                                                                  [])])])]),
                     Sentence(YES_NO_QUESTION, '',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['want'], [],
                                            'present simple',
                                            [NominalGroup(['the'], [], [['blue', []]], [], []),
                                             NominalGroup([], ['bottle'], [['green', []]], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[1].sv[0].d_obj[1]._conjunction = "OR"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_30(self):
        logger.info('\n######################## test 1.30 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What's wrong with him? I'll play a guitar or a piano and a violon. I played a guitar a year ago."

        sentences = [Sentence(W_QUESTION, 'thing',
                              [NominalGroup([], [], [['wrong', []]], [], [])],
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
                                            [IndirectComplement(['ago'],
                                                                 [NominalGroup(['a'], ['year'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[1].sv[0].d_obj[1]._conjunction = "OR"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_31(self):
        logger.info('\n######################## test 1.31 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Who are you talking to? You should have the bottle. Would you've played a guitar? You'd have played a guitar."

        sentences = [Sentence(W_QUESTION, 'people',
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_32(self):
        logger.info('\n######################## test 1.32 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What do you do for a living in this building? What does your brother do for a living here?"

        sentences = [Sentence(W_QUESTION, 'explication',
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_33(self):
        logger.info('\n######################## test 1.33 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "This is a bottle. There is a bottle on the table."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['this'], [], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup(['a'], ['bottle'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup(['there'], [], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup(['a'], ['bottle'], [], [], [])],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['table'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_34(self):
        logger.info('\n######################## test 1.34 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Is it on the table or the shelf?"

        sentences = [Sentence(YES_NO_QUESTION, '',
                              [NominalGroup([], ['it'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['table'], [], [], [])]),
                                             IndirectComplement([], [NominalGroup(['the'], ['shelf'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[0].sv[0].i_cmpl[1].gn[0]._conjunction = "OR"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_35(self):
        logger.info('\n######################## test 1.35 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Where is it? On the table or on the shelf?"

        sentences = [Sentence(W_QUESTION, 'place',
                              [NominalGroup([], ['it'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(YES_NO_QUESTION, '',
                         [],
                              [VerbalGroup([], [], '',
                                  [],
                                                    [IndirectComplement(['on'], [
                                                        NominalGroup(['the'], ['table'], [], [], [])]),
                                                     IndirectComplement(['on'], [
                                                         NominalGroup(['the'], ['shelf'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[1].sv[0].i_cmpl[1].gn[0]._conjunction = "OR"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_36(self):
        logger.info('\n######################## test 1.36 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Is it on your left or in front of you?"

        sentences = [Sentence(YES_NO_QUESTION, '',
                              [NominalGroup([], ['it'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['your'], ['left'], [], [], [])]),
                                             IndirectComplement(['in+front+of'],
                                                                 [NominalGroup([], ['you'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[0].sv[0].i_cmpl[1].gn[0]._conjunction = "OR"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_37(self):
        logger.info('\n######################## test 1.37 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Where is it? On your left or in front of you?"

        sentences = [Sentence(W_QUESTION, 'place',
                              [NominalGroup([], ['it'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(YES_NO_QUESTION, '',
                              [NominalGroup([], [], [], [], [])],
                              [VerbalGroup([], [], '',
                                  [],
                                                    [IndirectComplement(['on'], [
                                                        NominalGroup(['your'], ['left'], [], [], [])]),
                                                     IndirectComplement(['in+front+of'],
                                                                         [NominalGroup([], ['you'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[1].sv[0].i_cmpl[1].gn[0]._conjunction = "OR"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_38(self):
        logger.info('\n######################## test 1.38 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The blue bottle? What do you mean?"

        sentences = [Sentence(YES_NO_QUESTION, '',
                              [NominalGroup(['the'], ['bottle'], [['blue', []]], [], [])],
            []),
                     Sentence(W_QUESTION, 'thing',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['mean'], [], 'present simple', [], [], [], [], VerbalGroup.affirmative,
                                  [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_39(self):
        logger.info('\n######################## test 1.39 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Would you like the blue bottle or the glass? The green or blue bottle is on the table. Is the green or blue glass mine?"

        sentences = [Sentence(YES_NO_QUESTION, '',
                              [NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['like'], [], 'present conditional',
                                            [NominalGroup(['the'], ['bottle'], [['blue', []]], [], []),
                                             NominalGroup(['the'], ['glass'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup(['the'], [], [['green', []]], [], []),
                               NominalGroup([], ['bottle'], [['blue', []]], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['table'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(YES_NO_QUESTION, '',
                              [NominalGroup(['the'], [], [['green', []]], [], []),
                               NominalGroup([], ['glass'], [['blue', []]], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup([], ['mine'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[0].sv[0].d_obj[1]._conjunction = "OR"
        sentences[1].sn[1]._conjunction = "OR"
        sentences[2].sn[1]._conjunction = "OR"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_40(self):
        logger.info('\n######################## test 1.40 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Learn that I want you to give me the blue bottle that's blue."

        sentences = [Sentence(IMPERATIVE, '',
            [],
                              [VerbalGroup(['learn'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'that',
                                                                              [NominalGroup([], ['I'], [], [], [])],
                                                                              [VerbalGroup(['want'], [
                                                                                  VerbalGroup(['give'], [], '',
                                                                                               [NominalGroup(['the'], [
                                                                                                   'bottle'], [['blue',
                                                                                                                   []]],
                                                                                                   [], [Sentence(
                                                                                                       RELATIVE, 'that',
                                                                                                       [],
                                                                                                       [VerbalGroup(
                                                                                                           ['be'], [],
                                                                                                           'present simple',
                                                                                                           [
                                                                                                               NominalGroup(
                                                                                                                   [],
                                                                                                                   [], [
                                                                                                                           [
                                                                                                                               'blue',
                                                                                                                               []]],
                                                                                                                   [],
                                                                                                                   [])],
                                                                                                           [],
                                                                                                           [], [],
                                                                                                           VerbalGroup.affirmative,
                                                                                                           [])])])],
                                                                                               [IndirectComplement([],
                                                                                                   [NominalGroup([],
                                                                                                       ['me'], [], [],
                                                                                                       [])])],
                                                                                      [], [], VerbalGroup.affirmative,
                                                                                      [])], 'present simple',
                                                                                            [NominalGroup([], ['you'],
                                                                                                [], [], [])],
                                                                                  [],
                                                                                  [], [], VerbalGroup.affirmative,
                                                                                  [])])])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_41(self):
        logger.info('\n######################## test 1.41 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The bottle is behind to me. The bottle is next to the table in front of the kitchen."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['bottle'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['behind+to'],
                                                                 [NominalGroup([], ['me'], [], [], [])])],
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_42(self):
        logger.info('\n######################## test 1.42 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Carefully take the bottle. I take that bottle that I drink in. I take 22 bottles."

        sentences = [Sentence(IMPERATIVE, '',
            [],
                              [VerbalGroup(['take'], [], 'present simple',
                                            [NominalGroup(['the'], ['bottle'], [], [], [])],
                                  [],
                                            ['carefully'], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['take'], [], 'present simple',
                                            [NominalGroup(['that'], ['bottle'], [], [], [Sentence(RELATIVE, 'that',
                                                                                                   [NominalGroup([],
                                                                                                       ['I'], [], [],
                                                                                                       [])],
                                                                                                   [VerbalGroup(
                                                                                                       ['drink'], [],
                                                                                                       'present simple',
                                                                                                       [],
                                                                                                       [
                                                                                                           IndirectComplement(
                                                                                                               ['in'],
                                                                                                               [])],
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

        sentences[2].sv[0].d_obj[0]._quantifier = "DIGIT"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)


    def test_43(self):
        logger.info('\n######################## test 1.43 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "I'll play Jido's guitar, a saxophone, my oncle's wife's piano and Patrick's violon."

        sentences = [Sentence(STATEMENT, '',
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_44(self):
        logger.info('\n######################## test 1.44 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Give me 2 or 3 bottles. The bottle is blue big funny. Give me the bottle which is on the table."

        sentences = [Sentence(IMPERATIVE, '',
            [],
                              [VerbalGroup(['give'], [], 'present simple',
                                            [NominalGroup(['2'], [], [], [], []),
                                             NominalGroup(['3'], ['bottle'], [], [], [])],
                                            [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['bottle'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup([], [], [['blue', []], ['big', []], ['funny', []]], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(IMPERATIVE, '',
                         [],
                              [VerbalGroup(['give'], [], 'present simple',
                                            [NominalGroup(['the'], ['bottle'], [], [], [Sentence(RELATIVE, 'which',
                                                [],
                                                                                                  [VerbalGroup(['be'],
                                                                                                      [],
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

        sentences[0].sv[0].d_obj[1]._conjunction = "OR"
        sentences[0].sv[0].d_obj[0]._quantifier = "DIGIT"
        sentences[0].sv[0].d_obj[1]._quantifier = "DIGIT"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_45(self):
        logger.info('\n######################## test 1.45 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The boys' ball is blue. He asks me to do something. Is any person courageous on the laboratory?"

        sentences = [Sentence(STATEMENT, '',
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

        sentences[0].sn[0].noun_cmpl[0]._quantifier = "ALL"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_46(self):
        logger.info('\n######################## test 1.46 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What must be happened in the company today? The building shouldn't fastly be built. You can be here."

        sentences = [Sentence(W_QUESTION, 'situation',
            [],
                              [VerbalGroup(['must+happen'], [], 'present passive',
                                  [],
                                            [IndirectComplement(['in'],
                                                                 [NominalGroup(['the'], ['company'], [], [], [])])],
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_47(self):
        logger.info('\n######################## test 1.47 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "What size is the best one? What object is blue? How good is this?"

        sentences = [Sentence(W_QUESTION, 'size',
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_48(self):
        logger.info('\n######################## test 1.48 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Patrick, the bottle is on the table. Give it to me."

        sentences = [Sentence('interjection', '',
                              [NominalGroup([], ['Patrick'], [], [], [])],
            []),
                     Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['bottle'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['table'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(IMPERATIVE, '',
                              [NominalGroup([], ['Patrick'], [], [], [])],
                              [VerbalGroup(['give'], [], 'present simple',
                                            [NominalGroup([], ['it'], [], [], [])],
                                            [IndirectComplement(['to'], [NominalGroup([], ['me'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_49(self):
        logger.info('\n######################## test 1.49 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Jido, give me the bottle. Jido, Patrick and you will go to the cinema. Jido, Patrick and you, give me the bottle."

        sentences = [Sentence('interjection', '',
                              [NominalGroup([], ['Jido'], [], [], [])],
            []),
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
                                            [IndirectComplement(['to'],
                                                                 [NominalGroup(['the'], ['cinema'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence('interjection', '',
                              [NominalGroup([], ['Jido'], [], [], []), NominalGroup([], ['Patrick'], [], [], []),
                               NominalGroup([], ['you'], [], [], [])],
                         []),
                     Sentence(IMPERATIVE, '',
                              [NominalGroup([], ['Jido'], [], [], []), NominalGroup([], ['Patrick'], [], [], []),
                               NominalGroup([], ['you'], [], [], [])],
                              [VerbalGroup(['give'], [], 'present simple',
                                            [NominalGroup(['the'], ['bottle'], [], [], [])],
                                            [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_50(self):
        logger.info('\n######################## test 1.50 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The bottle isn't blue but it's red. It isn't the glass but the bottle. It's blue or red."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['bottle'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup([], [], [['blue', []]], [], [])],
                                  [],
                                  [], [], VerbalGroup.negative, [Sentence('subsentence', 'but',
                                                                           [NominalGroup([], ['it'], [], [], [])],
                                                                           [VerbalGroup(['be'], [], 'present simple',
                                                                                         [NominalGroup([], [],
                                                                                             [['red', []]], [], [])],
                                                                               [],
                                                                               [], [], VerbalGroup.affirmative,
                                                                               [])])])]),
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

        sentences[1].sv[0].d_obj[1]._conjunction = "BUT"
        sentences[2].sv[0].d_obj[1]._conjunction = "OR"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_51(self):
        logger.info('\n######################## test 1.51 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "It isn't red but blue. This is my banana. Bananas are fruits."

        sentences = [Sentence(STATEMENT, '',
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

        sentences[0].sv[0].d_obj[1]._conjunction = "BUT"
        sentences[2].sn[0]._quantifier = "ALL"
        sentences[2].sv[0].d_obj[0]._quantifier = "ALL"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_52(self):
        logger.info('\n######################## test 1.52 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "There are no bananas. All bananas are here. Give me more information which are about the bottle."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['there'], [], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup(['no'], ['banana'], [], [], [])],
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
                                            [NominalGroup(['more'], ['information'], [], [],
                                                           [Sentence(RELATIVE, 'which',
                                                               [],
                                                                     [VerbalGroup(['be'], [], 'present simple',
                                                                         [],
                                                                                   [IndirectComplement(['about'], [
                                                                                       NominalGroup(['the'],
                                                                                                     ['bottle'], [], [],
                                                                                           [])])],
                                                                         [], [], VerbalGroup.affirmative, [])])])],
                                            [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[0].sn[0]._quantifier = "SOME"
        sentences[0].sv[0].d_obj[0]._quantifier = "ANY"
        sentences[1].sn[0]._quantifier = "ALL"
        sentences[2].sv[0].d_obj[0]._quantifier = "SOME"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_53(self):
        logger.info('\n######################## test 1.53 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Jido, tell me where you go. Goodbye. There is nothing. It's another one."

        sentences = [Sentence('interjection', '',
                              [NominalGroup([], ['Jido'], [], [], [])],
            []),
                     Sentence(IMPERATIVE, '',
                              [NominalGroup([], ['Jido'], [], [], [])],
                              [VerbalGroup(['tell'], [], 'present simple',
                                  [],
                                            [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'where',
                                                                              [NominalGroup([], ['you'], [], [], [])],
                                                                              [VerbalGroup(['go'], [],
                                                                                            'present simple',
                                                                                  [],
                                                                                  [],
                                                                                  [], [], VerbalGroup.affirmative,
                                                                                  [])])])]),
                     Sentence(END, '', [], []),
                     Sentence(STATEMENT, '',
                              [NominalGroup(['there'], [], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup([], ['nothing'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['it'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup(['another'], ['one'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)


    def test_54(self):
        logger.info('\n######################## test 1.54 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The bottle becomes blue. 1 piece could become 2, if you smoldered it."

        sentences = [Sentence(STATEMENT, '',
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
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'if',
                                                                              [NominalGroup([], ['you'], [], [], [])],
                                                                              [VerbalGroup(['smolder'], [],
                                                                                            'past simple',
                                                                                            [NominalGroup([], ['it'],
                                                                                                [], [], [])],
                                                                                  [],
                                                                                  [], [], VerbalGroup.affirmative,
                                                                                  [])])])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_55(self):
        logger.info('\n######################## test 1.55 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "This one isn't my uncle's bottle but it's my brother's bottle. It isn't on the table but on the shelf."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['this'], ['one'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                            [NominalGroup(['the'], ['bottle'], [],
                                                           [NominalGroup(['my'], ['uncle'], [], [], [])], [])],
                                  [],
                                  [], [], VerbalGroup.negative, [Sentence('subsentence', 'but',
                                                                           [NominalGroup([], ['it'], [], [], [])],
                                                                           [VerbalGroup(['be'], [], 'present simple',
                                                                                         [NominalGroup(['the'],
                                                                                                        ['bottle'], [],
                                                                                                        [NominalGroup(
                                                                                                            ['my'],
                                                                                                            ['brother'],
                                                                                                            [], [],
                                                                                                            [])], [])],
                                                                               [],
                                                                               [], [], VerbalGroup.affirmative,
                                                                               [])])])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['it'], [], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], []),
                                                                          NominalGroup(['the'], ['shelf'], [], [],
                                                                              [])])],
                                  [], [], VerbalGroup.negative, [])])]

        sentences[1].sv[0].i_cmpl[0].gn[1]._conjunction = "BUT"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_56(self):
        logger.info('\n######################## test 1.56 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Give me the fourth and seventh bottle. Give me the one thousand ninth and the thirty thousand twenty eighth bottle."

        sentences = [Sentence(IMPERATIVE, '',
            [],
                              [VerbalGroup(['give'], [], 'present simple',
                                            [NominalGroup(['the'], [], [['fourth', []]], [], []),
                                             NominalGroup([], ['bottle'], [['seventh', []]], [], [])],
                                            [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(IMPERATIVE, '',
                         [],
                              [VerbalGroup(['give'], [], 'present simple',
                                            [NominalGroup(['the'], [], [['one+thousand+ninth', []]], [], []),
                                             NominalGroup(['the'], ['bottle'], [['thirty+thousand+twenty+eighth', []]],
                                                 [], [])],
                                            [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_57(self):
        logger.info('\n######################## test 1.57 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The evil tyran is in the laboratory. I don't know what you're talking about."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['tyran'], [['evil', []]], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['in'],
                                                                 [NominalGroup(['the'], ['laboratory'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['know'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.negative, [Sentence('subsentence', 'what',
                                                                           [NominalGroup([], ['you'], [], [], [])],
                                                                           [VerbalGroup(['talk'], [],
                                                                                         'present progressive',
                                                                               [],
                                                                                         [IndirectComplement(['about'],
                                                                                             [])],
                                                                               [], [], VerbalGroup.affirmative,
                                                                               [])])])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)


    def test_58(self):
        logger.info('\n######################## test 1.58 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "I go to the place where I was born. I study where you studied. I study where you build your house where you put the bottle."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['go'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['to'], [
                                                NominalGroup(['the'], ['place'], [], [], [Sentence(RELATIVE, 'where',
                                                                                                    [NominalGroup([],
                                                                                                        ['I'], [], [],
                                                                                                        [])],
                                                                                                    [VerbalGroup(
                                                                                                        ['be'], [],
                                                                                                        'past simple',
                                                                                                        [NominalGroup(
                                                                                                            [], [], [[
                                                                                                                         'born',
                                                                                                                         []]],
                                                                                                            [], [])],
                                                                                                        [],
                                                                                                        [], [],
                                                                                                        VerbalGroup.affirmative,
                                                                                                        [])])])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['study'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'where',
                                                                              [NominalGroup([], ['you'], [], [], [])],
                                                                              [VerbalGroup(['study'], [],
                                                                                            'past simple',
                                                                                  [],
                                                                                  [],
                                                                                  [], [], VerbalGroup.affirmative,
                                                                                  [])])])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['study'], [], 'present simple',
                                  [],
                                  [],
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'where',
                                                                              [NominalGroup([], ['you'], [], [], [])],
                                                                              [VerbalGroup(['build'], [],
                                                                                            'present simple',
                                                                                            [NominalGroup(['your'],
                                                                                                           ['house'],
                                                                                                [], [], [Sentence(
                                                                                                    RELATIVE, 'where',
                                                                                                    [NominalGroup([],
                                                                                                        ['you'], [], [],
                                                                                                        [])],
                                                                                                    [VerbalGroup(
                                                                                                        ['put'], [],
                                                                                                        'present simple',
                                                                                                        [NominalGroup(
                                                                                                            ['the'],
                                                                                                            ['bottle'],
                                                                                                            [], [],
                                                                                                            [])],
                                                                                                        [],
                                                                                                        [], [],
                                                                                                        VerbalGroup.affirmative,
                                                                                                        [])])])],
                                                                                  [],
                                                                                  [], [], VerbalGroup.affirmative,
                                                                                  [])])])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_59(self):
        logger.info('\n######################## test 1.59 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Apples grow on trees and plants. Give me 3 apples."

        sentences = [Sentence(STATEMENT, '',
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

        sentences[0].sn[0]._quantifier = "ALL"
        sentences[0].sv[0].i_cmpl[0].gn[0]._quantifier = "ALL"
        sentences[0].sv[0].i_cmpl[0].gn[1]._quantifier = "ALL"
        sentences[1].sv[0].d_obj[0]._quantifier = "DIGIT"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_60(self):
        logger.info('\n######################## test 1.56 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "We were preparing the dinner when your father came. He made a sandwich which is with bacon, while I phoned."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup([], ['we'], [], [], [])],
                              [VerbalGroup(['prepare'], [], 'past progressive',
                                            [NominalGroup(['the'], ['dinner'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'when',
                                                                              [NominalGroup(['your'], ['father'], [],
                                                                                  [], [])],
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
                                                                                                  [VerbalGroup(['be'],
                                                                                                      [],
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
                                  [], [], VerbalGroup.affirmative, [Sentence('subsentence', 'while',
                                                                              [NominalGroup([], ['I'], [], [], [])],
                                                                              [VerbalGroup(['phone'], [],
                                                                                            'past simple',
                                                                                  [],
                                                                                  [],
                                                                                  [], [], VerbalGroup.affirmative,
                                                                                  [])])])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_61(self):
        logger.info('\n######################## test 1.54 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "The big very strong man is on the corner. The too big very strong man is on the corner."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['man'], [['big', []], ['strong', ['very']]], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['corner'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup(['the'], ['man'], [['big', ['too']], ['strong', ['very']]], [], [])],
                              [VerbalGroup(['be'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['the'], ['corner'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_62(self):
        logger.info('\n######################## test 1.55 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Red apples grow on green trees and plants. A kind of thing. It can be played by 30028 players."

        sentences = [Sentence(STATEMENT, '',
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

        sentences[0].sn[0]._quantifier = "ALL"
        sentences[0].sv[0].i_cmpl[0].gn[0]._quantifier = "ALL"
        sentences[0].sv[0].i_cmpl[0].gn[1]._quantifier = "ALL"
        sentences[1].sn[0]._quantifier = "SOME"
        sentences[1].sn[0].noun_cmpl[0]._quantifier = "SOME"
        sentences[2].sv[0].i_cmpl[0].gn[0]._quantifier = "DIGIT"

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_63(self):
        logger.info('\n######################## test 1.56 ##############################')
        logger.info('#################################################################\n')

        original_utterance = "Let the man go to the cinema. Is it the time to let you go? Where is the other tape?"

        sentences = [Sentence(IMPERATIVE, '',
            [],
                              [VerbalGroup(['let'], [VerbalGroup(['go'],
                                  [], '',
                                  [],
                                                                   [IndirectComplement(['to'], [
                                                                       NominalGroup(['the'], ['cinema'], [], [],
                                                                           [])])],
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

        utterance = utterance_rebuilding.verbalising(sentences)

        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)

        self.assertEquals(original_utterance, utterance)

    def test_64(self):
        print('')
        print('######################## test 1.57 ##############################')
        print('#################################################################')
        print('')

        original_utterance = "And now, can you reach the tape. it could have been them. It is just me at the door. A strong clause can stand on its own."

        sentences = [Sentence(YES_NO_QUESTION, '',
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
                                            [IndirectComplement(['at'],
                                                                 [NominalGroup(['the'], ['door'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup(['a'], ['clause'], [['strong', []]], [], [])],
                              [VerbalGroup(['can+stand'], [], 'present simple',
                                  [],
                                            [IndirectComplement(['on'],
                                                                 [NominalGroup(['its'], ['own'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        print("The original utterance is : ", original_utterance)
        print("The result obtained is :    ", utterance)

        self.assertEquals(original_utterance, utterance)

    def test_65(self):
        print('')
        print('######################## test 1.58 ##############################')
        print('#################################################################')
        print('')

        original_utterance = "Tell me what to do. No, I can not reach it."

        sentences = [Sentence(IMPERATIVE, '',
            [],
                              [VerbalGroup(['tell'], [], 'present simple',
                                  [],
                                            [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])]),
                                             IndirectComplement([],
                                                 [NominalGroup(['the'], ['thing'], [], [], [Sentence(RELATIVE, 'that',
                                                     [],
                                                                                                      [VerbalGroup(
                                                                                                          ['be'], [
                                                                                                              VerbalGroup(
                                                                                                                  [
                                                                                                                      'do'],
                                                                                                                  [],
                                                                                                                  '',
                                                                                                                  [],
                                                                                                                  [],
                                                                                                                  [],
                                                                                                                  [],
                                                                                                                  VerbalGroup.affirmative,
                                                                                                                  [])],
                                                                                                          'present simple',
                                                                                                          [],
                                                                                                          [],
                                                                                                          [], [],
                                                                                                          VerbalGroup.affirmative,
                                                                                                          [])])])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(DISAGREEMENT, '', [], []),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['can+reach'], [], 'present simple',
                                            [NominalGroup([], ['it'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.negative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        print("The original utterance is : ", original_utterance)
        print("The result obtained is :    ", utterance)

        self.assertEquals(original_utterance, utterance)

    def test_66(self):
        print('')
        print('######################## test 1.59 ##############################')
        print('#################################################################')
        print('')

        original_utterance = "I'll come back on Monday. I'll play with a guitar. I'll play football."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['come+back'], [], 'future simple',
                                  [],
                                            [IndirectComplement(['on'], [NominalGroup([], ['Monday'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['play'], [], 'future simple',
                                  [],
                                            [IndirectComplement(['with'],
                                                                 [NominalGroup(['a'], ['guitar'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['play'], [], 'future simple',
                                            [NominalGroup([], ['football'], [], [], [])],
                                  [],
                                  [], [], VerbalGroup.affirmative, [])])]

        utterance = utterance_rebuilding.verbalising(sentences)

        print("The original utterance is : ", original_utterance)
        print("The result obtained is :    ", utterance)

        self.assertEquals(original_utterance, utterance)

    def test_67(self):
        print('')
        print('######################## test 1.60 ##############################')
        print('#################################################################')
        print('')

        original_utterance = "I'll play a guitar, a piano and a violon. I'll play with a guitar, a piano and a violon. Give me everything."

        sentences = [Sentence(STATEMENT, '',
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
                                            [IndirectComplement(['with'],
                                                                 [NominalGroup(['a'], ['guitar'], [], [], []),
                                                                  NominalGroup(['a'], ['piano'], [], [], []),
                                                                  NominalGroup(['a'], ['violon'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])]),
                     Sentence(IMPERATIVE, '',
                         [],
                              [VerbalGroup(['give'], [], 'present simple',
                                            [NominalGroup([], ['everything'], [], [], [])],
                                            [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[0].sv[0].d_obj[0]._quantifier = "SOME"
        sentences[0].sv[0].d_obj[1]._quantifier = "SOME"
        sentences[0].sv[0].d_obj[2]._quantifier = "SOME"
        sentences[1].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"
        sentences[1].sv[0].i_cmpl[0].gn[1]._quantifier = "SOME"
        sentences[1].sv[0].i_cmpl[0].gn[2]._quantifier = "SOME"

        utterance = utterance_rebuilding.verbalising(sentences)

        print("The original utterance is : ", original_utterance)
        print("The result obtained is :    ", utterance)

        self.assertEquals(original_utterance, utterance)

    def test_68(self):
        print('')
        print('######################## test 1.61 ##############################')
        print('#################################################################')
        print('')

        original_utterance = "I'll come back at 7 o'clock tomorrow. He finishes the project 10 minutes before."

        sentences = [Sentence(STATEMENT, '',
                              [NominalGroup([], ['I'], [], [], [])],
                              [VerbalGroup(['come+back'], [], 'future simple',
                                  [],
                                            [IndirectComplement(['at'],
                                                                 [NominalGroup(['7'], ["o'clock"], [], [], [])])],
                                  [], ['tomorrow'], VerbalGroup.affirmative, [])]),
                     Sentence(STATEMENT, '',
                              [NominalGroup([], ['he'], [], [], [])],
                              [VerbalGroup(['finish'], [], 'present simple',
                                            [NominalGroup(['the'], ['project'], [], [], [])],
                                            [IndirectComplement(['before'],
                                                                 [NominalGroup(['10'], ['minute'], [], [], [])])],
                                  [], [], VerbalGroup.affirmative, [])])]

        sentences[0].sv[0].i_cmpl[0].gn[0]._quantifier = "DIGIT"
        sentences[1].sv[0].i_cmpl[0].gn[0]._quantifier = "DIGIT"

        utterance = utterance_rebuilding.verbalising(sentences)

        print("The original utterance is : ", original_utterance)
        print("The result obtained is :    ", utterance)

        self.assertEquals(original_utterance, utterance)

    def test_69(self):
        print('')
        print('######################## test 1.62 ##############################')
        print('#################################################################')
        print('')

        original_utterance = "I'll play a guitar, a piano and a violon. I'll play with a guitar, a piano and a violon. The boss, you and me are here."

        sentences = [Sentence(STATEMENT, '',
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
                                            [IndirectComplement(['with'],
                                                                 [NominalGroup(['a'], ['guitar'], [], [], []),
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

        sentences[0].sv[0].d_obj[0]._quantifier = "SOME"
        sentences[0].sv[0].d_obj[1]._quantifier = "SOME"
        sentences[0].sv[0].d_obj[2]._quantifier = "SOME"
        sentences[1].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"
        sentences[1].sv[0].i_cmpl[0].gn[1]._quantifier = "SOME"
        sentences[1].sv[0].i_cmpl[0].gn[2]._quantifier = "SOME"

        utterance = utterance_rebuilding.verbalising(sentences)

        print("The original utterance is : ", original_utterance)
        print("The result obtained is :    ", utterance)

        self.assertEquals(original_utterance, utterance)

    def test_70(self):
        print('')
        print('######################## test 1.63 ##############################')
        print('#################################################################')
        print('')

        original_utterance = "A speaking sentence's time is the best. I come at 10 pm. I'll come an evening tomorrow."

        sentences = [Sentence(STATEMENT, '',
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
                                            [IndirectComplement([], [NominalGroup(['an'], ['evening'], [], [], [])])],
                                  [], ['tomorrow'], VerbalGroup.affirmative, [])])]

        sentences[0].sn[0].noun_cmpl[0]._quantifier = 'SOME'
        sentences[1].sv[0].i_cmpl[0].gn[0]._quantifier = "DIGIT"
        sentences[2].sv[0].i_cmpl[0].gn[0]._quantifier = "SOME"

        utterance = utterance_rebuilding.verbalising(sentences)

        print("The original utterance is : ", original_utterance)
        print("The result obtained is :    ", utterance)

        self.assertEquals(original_utterance, utterance)


class TestVerbalizationCompleteLoop(unittest.TestCase):
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()

    def test_verbalize1(self):
        logger.info("\n##################### test_verbalize1: simple statements ########################\n")
        myP = Parser()
        stmt = "The cup is on the desk."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

        logger.info("\n####\n")

        stmt = "The green bottle is next to Joe."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

    def test_verbalize2(self):
        logger.info("\n##################### test_verbalize2: yes/no questions ########################\n")
        myP = Parser()

        stmt = "Are you a robot?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)


    def test_verbalize3(self):
        logger.info("\n##################### test_verbalize3: orders ########################\n")
        myP = Parser()

        stmt = "Put the yellow banana on the shelf."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

        logger.info("\n####\n")

        stmt = "Give me the green banana."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

        logger.info("\n####\n")

        stmt = "Give the green banana to me."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

        logger.info("\n####\n")

        stmt = "Get the box which is on the table."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

        logger.info("\n####\n")

        stmt = "Get the box which is in the trashbin."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

    def test_verbalize4(self):
        logger.info("\n##################### test_verbalize4: W questions ########################\n")
        myP = Parser()

        stmt = "Where is the box?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

        logger.info("\n####\n")

        stmt = "What are you doing now?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('input: ' + stmt)
        logger.info('output:' + res)
        self.assertEquals(stmt, res)


    def test_verbalize5(self):
        logger.info("\n##################### test_verbalize5 ########################\n")
        myP = Parser()

        stmt = "Jido, tell me where you go."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

    def test_verbalize6(self):
        logger.info("\n##################### test_verbalize 6 ########################\n")
        myP = Parser()

        stmt = "What blue object do you know?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVerbalization)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestVerbalizationCompleteLoop))

    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite())

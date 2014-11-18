# coding=utf-8
"""
 Created by Chouayakh Mahdi                                                       
 23/08/2010                                                                       
 The package contains the unit test of anaphora function                                       
    unit_tests : to perform unit tests                                           
"""
import unittest
import logging

from dialogs.sentence import *
from dialogs.parsing import preprocessing
from dialogs.parsing import analyse_sentence
from dialogs.parsing import parser
from anaphora_matching import *
from dialogs.parsing.parser_test import compare_nominal_group


"""
Function to perform unit tests                                                   
"""
"""
"""
## Aim of this test : To use the complement of the noun and the duplication with 'and'
"""
print('')
print(('######################## test 1.1 ##############################'))

utterance="Using 'one' with adding an adjective and deletion of another one"
print('The object of our test is this utterance :')
print(utterance)
print('#################################################################')
print('')
sentences=[Sentence('statement', '', 
        [NominalGroup(['the'],['bottle'],['blue'],[NominalGroup([],['Jido'],[],[],[])],[])],
        [VerbalGroup(['be'], [],'present simple',
            [], 
            [IndirectComplement(['on'],[NominalGroup(['the'],['table'],[],[],[])])],
            [], [] ,'affirmative',[])]),
    Sentence('statement', '', 
        [NominalGroup([],['I'],[],[],[])],
        [VerbalGroup(['play'], [],'future simple',
            [NominalGroup(['a'],['guitar'],[],[],[]),NominalGroup(['a'],['piano'],[],[],[]),NominalGroup(['a'],['violon'],[],[],[])],
            [],
            [], [] ,'affirmative',[])])]
    
sentences[0].sn[0].id='azeaz'
sentences[1].sn[0].id='eaz'
sentences[1].sv[0].d_obj[0].id='s'
sentences[1].sv[0].d_obj[1].id='z'
sentences[1].sv[0].d_obj[2].id='e'
    
    
"""
## Aim of this test : To use the complement of the noun and the duplication with 'and'
"""
print('')
print(('######################## test 1.1 ##############################'))

utterance="Using 'one' with adding an adjective and without deletion of another one"
print('The object of our test is this utterance :')
print(utterance)
print('#################################################################')
print('')
sentences=[Sentence('statement', '', 
        [NominalGroup(['the'],['bottle'],['blue'],[NominalGroup([],['Jido'],[],[],[])],[])],
        [VerbalGroup(['be'], [],'present simple',
            [], 
            [IndirectComplement(['on'],[NominalGroup(['the'],['table'],[],[],[])])],
            [], [] ,'affirmative',[])]),
    Sentence('statement', '', 
        [NominalGroup([],['I'],[],[],[])],
        [VerbalGroup(['play'], [],'future simple',
            [NominalGroup(['a'],['guitar'],[],[],[]),NominalGroup(['a'],['piano'],[],[],[]),NominalGroup(['a'],['violon'],[],[],[])],
            [],
            [], [] ,'affirmative',[])])]

sentences[0].sn[0].id='azeaz'
sentences[1].sn[0].id='eaz'
sentences[1].sv[0].d_obj[0].id='s'
sentences[1].sv[0].d_obj[1].id='z'
sentences[1].sv[0].d_obj[2].id='e'
"""

"""
## Aim of this test : Present the duality between the direct and indirect complement
"""
print('')
print('######################## test 1 ##############################')

utterance = "Using 'it' so we have to replace automatically"
print('The object of our test is this utterance :')
print(utterance)
print('###############################################################')
print('')

sentences = [Sentence('statement', '',
                      [NominalGroup([], ['it'], [], [], [])],
                      [VerbalGroup(['be'], [], 'present simple',
                          [],
                                    [IndirectComplement(['on'], [NominalGroup(['the'], ['table'], [], [], [])])],
                          [], [], 'affirmative', [])]),
             Sentence('imperative', '',
                 [],
                      [VerbalGroup(['give'], [], 'present simple',
                                    [NominalGroup(['the'], ['bottle'], [], [], [])],
                                    [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])])],
                          [], [], 'affirmative', [])]),
             Sentence('statement', '',
                      [NominalGroup([], ['I'], [], [], [])],
                      [VerbalGroup(['give'], [], 'present simple',
                                    [NominalGroup(['the'], ['shelf'], [], [], [])],
                                    [IndirectComplement(['to'], [NominalGroup([], ['you'], [], [], [])])],
                          [], [], 'negative', [])])]

sentences[0].sn[0].id = 'azeaz'
sentences[0].sv[0].i_cmpl[0].gn[0].id = "4"
sentences[1].sv[0].d_obj[0].id = 'sghj'
sentences[1].sv[0].i_cmpl[0].gn[0].id = "9"
sentences[2].sn[0].id = 'eaz'
sentences[2].sv[0].d_obj[0].id = '10'
sentences[2].sv[0].i_cmpl[0].gn[0].id = "6"


class TestAnaphora(unittest.TestCase):
    def test_01(self):
        """
        ## TEST 1
        """
        print('')
        print('######################## test 1.1 ##############################')

        utterance = "Using 'it' so we have to replace automatically"
        print('The object of our test is this utterance :')
        print(utterance)
        print('#################################################################')
        print('')
        list_gr = recover_nominal_group_list(sentences)
        print('The list of the nominal group')
        for i in list_gr:
            print((str(i)))

        print('#####################################')
        print('')
        print('the nominal group that we have to change')
        nominal_group_struc = NominalGroup([], ['it'], [], [], [])
        print((str(nominal_group_struc)))

        print('#####################################')
        print('After the first replacement')
        gr = first_replacement(list_gr, nominal_group_struc)
        print("the id of the nominal group: ", gr.id)
        print((str(gr)))
        print('')

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([gr], [result])
        self.assertEquals(result_test, 0)

        print('#####################################')
        utterance = "no. I mean the shelf."
        print('The speaker said :')
        print(utterance)
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        print('#####################################')
        nominal_group_struc = replacement(class_list, nominal_group_struc, list_gr[1:], gr)
        print('the nominal group after processing')
        print((str(nominal_group_struc[0])))
        print('the flag')
        print((str(nominal_group_struc[1])))

        result = NominalGroup(['the'], ['shelf'], [], [], [])
        result_test = compare_nominal_group([nominal_group_struc[0]], [result])
        self.assertEquals(result_test, 0)

    def test_02(self):
        """
        ## TEST 2
        """
        print('')
        print('######################## test 1.2 ##############################')

        utterance = "Using 'it' so we have to replace automatically"
        print('The object of our test is this utterance :')
        print(utterance)
        print('#################################################################')
        print('')

        list_gr = recover_nominal_group_list(sentences)
        print('The list of the nominal group')
        for i in list_gr:
            print((str(i)))

        print('#####################################')
        print('')
        print('the nominal group that we have to change')
        nominal_group_struc = NominalGroup([], ['it'], [], [], [])
        print((str(nominal_group_struc)))

        print('#####################################')
        print('After the first replacement')
        gr = first_replacement(list_gr, nominal_group_struc)
        print("the id of the nominal group: ", gr.id)
        print((str(gr)))
        print('')

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([gr], [result])
        self.assertEquals(result_test, 0)

        print('#####################################')
        utterance = "no."
        print('The speaker said :')
        print(utterance)
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        print('#####################################')
        nominal_group_struc = replacement(class_list, nominal_group_struc, list_gr[1:], gr)
        print('the nominal group after processing')
        print((str(nominal_group_struc[0])))
        print('the flag')
        print((str(nominal_group_struc[1])))

        result = NominalGroup(['the'], ['bottle'], [], [], [])
        result_test = compare_nominal_group([nominal_group_struc[0]], [result])
        self.assertEquals(result_test, 0)

    def test_03(self):
        """
        ## TEST 3
        """
        print('')
        print('######################## test 1.3 ##############################')

        utterance = "Using 'it' so we have to replace automatically"
        print('The object of our test is this utterance :')
        print(utterance)
        print('#################################################################')
        print('')

        list_gr = recover_nominal_group_list(sentences)
        print('The list of the nominal group')
        for i in list_gr:
            print((str(i)))

        print('#####################################')
        print('')
        print('the nominal group that we have to change')
        nominal_group_struc = NominalGroup([], ['it'], [], [], [])
        print((str(nominal_group_struc)))

        print('#####################################')
        print('After the first replacement')
        gr = first_replacement(list_gr, nominal_group_struc)
        print("the id of the nominal group: ", gr.id)
        print((str(gr)))
        print('')

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([gr], [result])
        self.assertEquals(result_test, 0)

        print('#####################################')
        utterance = "no. I mean the blue bottle."
        print('The speaker said :')
        print(utterance)
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        print('#####################################')
        nominal_group_struc = replacement(class_list, nominal_group_struc, list_gr[1:], gr)
        print('the nominal group after processing')
        print((str(nominal_group_struc[0])))
        print('the flag')
        print((str(nominal_group_struc[1])))

        result = NominalGroup(['the'], ['bottle'], [['blue', []]], [], [])
        result_test = compare_nominal_group([nominal_group_struc[0]], [result])
        self.assertEquals(result_test, 0)

    def test_04(self):
        """
        ## TEST 4
        """
        print('')
        print('######################## test 1.4 ##############################')

        utterance = "Using 'it' so we have to replace automatically"
        print('The object of our test is this utterance :')
        print(utterance)
        print('#################################################################')
        print('')

        list_gr = recover_nominal_group_list(sentences)
        print('The list of the nominal group')
        for i in list_gr:
            print((str(i)))

        print('#####################################')
        print('')
        print('the nominal group that we have to change')
        nominal_group_struc = NominalGroup([], ['it'], [], [], [])
        print((str(nominal_group_struc)))

        print('#####################################')
        print('After the first replacement')
        gr = first_replacement(list_gr, nominal_group_struc)
        print("the id of the nominal group: ", gr.id)
        print((str(gr)))
        print('')

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([gr], [result])
        self.assertEquals(result_test, 0)

        print('#####################################')
        utterance = "yes"
        print('The speaker said :')
        print(utterance)
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        print('#####################################')
        nominal_group_struc = replacement(class_list, nominal_group_struc, list_gr[1:], gr)
        print('the nominal group after processing')
        print((str(nominal_group_struc[0])))
        print('the flag')
        print((str(nominal_group_struc[1])))

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([nominal_group_struc[0]], [result])
        self.assertEquals(result_test, 0)

    def test_05(self):
        """
        ## TEST 5
        """
        print('')
        print('######################## test 1.5 ##############################')

        utterance = "Using 'it' so we have to replace automatically"
        print('The object of our test is this utterance :')
        print(utterance)
        print('#################################################################')
        print('')

        list_gr = recover_nominal_group_list(sentences)
        print('The list of the nominal group')
        for i in list_gr:
            print((str(i)))

        print('#####################################')
        print('')
        print('the nominal group that we have to change')
        nominal_group_struc = NominalGroup(['this'], ['one'], [], [], [])
        print((str(nominal_group_struc)))

        print('#####################################')
        print('After the first replacement')
        gr = first_replacement(list_gr, nominal_group_struc)
        print("the id of the nominal group: ", gr.id)
        print((str(gr)))
        print('')

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([gr], [result])
        self.assertEquals(result_test, 0)

        print('#####################################')
        utterance = "yes"
        print('The speaker said :')
        print(utterance)
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        print('#####################################')
        nominal_group_struc = replacement(class_list, nominal_group_struc, list_gr[1:], gr)
        print('the nominal group after processing')
        print((str(nominal_group_struc[0])))
        print('the flag')
        print((str(nominal_group_struc[1])))

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([nominal_group_struc[0]], [result])
        self.assertEquals(result_test, 0)

    def test_06(self):
        """
        ## TEST 6
        """
        print('')
        print('######################## test 1.6 ##############################')

        utterance = "Using 'it' so we have to replace automatically"
        print('The object of our test is this utterance :')
        print(utterance)
        print('#################################################################')
        print('')

        list_gr = recover_nominal_group_list(sentences)
        print('The list of the nominal group')
        for i in list_gr:
            print((str(i)))

        print('#####################################')
        print('')
        print('the nominal group that we have to change')
        nominal_group_struc = NominalGroup(['this'], ['one'], [], [], [])
        print((str(nominal_group_struc)))

        print('#####################################')
        print('After the first replacement')
        gr = first_replacement(list_gr, nominal_group_struc)
        print("the id of the nominal group: ", gr.id)
        print((str(gr)))
        print('')

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([gr], [result])
        self.assertEquals(result_test, 0)

        print('#####################################')
        utterance = "no. I mean the blue bottle."
        print('The speaker said :')
        print(utterance)
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        print('#####################################')
        nominal_group_struc = replacement(class_list, nominal_group_struc, list_gr[1:], gr)
        print('the nominal group after processing')
        print((str(nominal_group_struc[0])))
        print('the flag')
        print((str(nominal_group_struc[1])))

        result = NominalGroup(['the'], ['bottle'], [['blue', []]], [], [])
        result_test = compare_nominal_group([nominal_group_struc[0]], [result])
        self.assertEquals(result_test, 0)

    def test_07(self):
        """
        ## TEST 7
        """
        print('')
        print('######################## test 1.7 ##############################')

        utterance = "Using 'it' so we have to replace automatically"
        print('The object of our test is this utterance :')
        print(utterance)
        print('#################################################################')
        print('')

        list_gr = recover_nominal_group_list(sentences)
        print('The list of the nominal group')
        for i in list_gr:
            print((str(i)))

        print('#####################################')
        print('')
        print('the nominal group that we have to change')
        nominal_group_struc = NominalGroup(['this'], [], [], [], [])
        print((str(nominal_group_struc)))

        print('#####################################')
        print('After the first replacement')
        gr = first_replacement(list_gr, nominal_group_struc)
        print("the id of the nominal group: ", gr.id)
        print((str(gr)))
        print('')

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([gr], [result])
        self.assertEquals(result_test, 0)

        print('#####################################')
        utterance = "yes"
        print('The speaker said :')
        print(utterance)
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        print('#####################################')
        nominal_group_struc = replacement(class_list, nominal_group_struc, list_gr[1:], gr)
        print('the nominal group after processing')
        print((str(nominal_group_struc[0])))
        print('the flag')
        print((str(nominal_group_struc[1])))

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([nominal_group_struc[0]], [result])
        self.assertEquals(result_test, 0)

    def test_08(self):
        """
        ## TEST 8
        """
        print('')
        print('######################## test 1.8 ##############################')

        utterance = "Using 'it' so we have to replace automatically"
        print('The object of our test is this utterance :')
        print(utterance)
        print('#################################################################')
        print('')

        list_gr = recover_nominal_group_list(sentences)
        print('The list of the nominal group')
        for i in list_gr:
            print((str(i)))

        print('#####################################')
        print('')
        print('the nominal group that we have to change')
        nominal_group_struc = NominalGroup(['this'], [], [], [], [])
        print((str(nominal_group_struc)))

        print('#####################################')
        print('After the first replacement')
        gr = first_replacement(list_gr, nominal_group_struc)
        print("the id of the nominal group: ", gr.id)
        print((str(gr)))
        print('')

        result = NominalGroup(['the'], ['table'], [], [], [])
        result_test = compare_nominal_group([gr], [result])
        self.assertEquals(result_test, 0)

        print('#####################################')
        utterance = "no. I mean the blue bottle."
        print('The speaker said :')
        print(utterance)
        print('')
        sentence_list = preprocessing.process_sentence(utterance)
        class_list = analyse_sentence.sentences_analyzer(sentence_list)

        print('#####################################')
        nominal_group_struc = replacement(class_list, nominal_group_struc, list_gr[1:], gr)
        print('the nominal group after processing')
        print((str(nominal_group_struc[0])))
        print('the flag')
        print((str(nominal_group_struc[1])))

        result = NominalGroup(['the'], ['bottle'], [['blue', []]], [], [])
        result_test = compare_nominal_group([nominal_group_struc[0]], [result])
        self.assertEquals(result_test, 0)


def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestAnaphora)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite())

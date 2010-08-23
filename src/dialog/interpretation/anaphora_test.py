
"""
 Created by Chouayakh Mahdi                                                       
 23/08/2010                                                                       
 The package contains the unit test of anaphora function                                       
    unit_tests : to perform unit tests                                           
"""

from dialog.sentence import *
from dialog.parsing import preprocessing
from dialog.parsing import analyse_sentence
from dialog.parsing import parser
from anaphora_matching import *


def anapohora_unit_tests():
    
    """
    Function to perform unit tests                                                   
    """ 
    """
    """
    ## Aim of this test : To use the complement of the noun and the duplication with 'and'
    """
    print ''
    print ('######################## test 1.1 ##############################')

    utterance="Using 'one' with adding an adjective and deletion of another one"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentences=[Sentence('statement', '', 
            [Nominal_Group(['the'],['bottle'],['blue'],[Nominal_Group([],['Jido'],[],[],[])],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['play'], [],'future simple', 
                [Nominal_Group(['a'],['guitar'],[],[],[]),Nominal_Group(['a'],['piano'],[],[],[]),Nominal_Group(['a'],['violon'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])])]
    
    sentences[0].sn[0].id='azeaz'
    sentences[1].sn[0].id='eaz'
    sentences[1].sv[0].d_obj[0].id='s'
    sentences[1].sv[0].d_obj[1].id='z'
    sentences[1].sv[0].d_obj[2].id='e'
    
    list_gr=recover_nom_gr_list(sentences)
    
    c_gr=Nominal_Group(['the'],['one'],['blue'],[],[])
    gr = first_replacement(list_gr, c_gr)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    
    
    """
    ## Aim of this test : To use the complement of the noun and the duplication with 'and'
    """
    print ''
    print ('######################## test 1.1 ##############################')

    utterance="Using 'one' with adding an adjective and without deletion of another one"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentences=[Sentence('statement', '', 
            [Nominal_Group(['the'],['bottle'],['blue'],[Nominal_Group([],['Jido'],[],[],[])],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['play'], [],'future simple', 
                [Nominal_Group(['a'],['guitar'],[],[],[]),Nominal_Group(['a'],['piano'],[],[],[]),Nominal_Group(['a'],['violon'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])])]
    
    sentences[0].sn[0].id='azeaz'
    sentences[1].sn[0].id='eaz'
    sentences[1].sv[0].d_obj[0].id='s'
    sentences[1].sv[0].d_obj[1].id='z'
    sentences[1].sv[0].d_obj[2].id='e'
    
    list_gr=recover_nom_gr_list(sentences)
    
    c_gr=Nominal_Group(['the'],['one'],['big'],[],[])
    gr = first_replacement(list_gr, c_gr)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    """
    
    
    """
    ## Aim of this test : Present the duality between the direct and indirect complement
    """
    print ''
    print ('######################## test 1 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '###############################################################'
    print ''
    
    sentences=[Sentence('statement', '', 
            [Nominal_Group([],['it'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('imperative', '', 
            [], 
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['I'],[],[],[])],
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group(['the'],['shelf'],[],[],[])], 
                [Indirect_Complement(['to'],[Nominal_Group([],['you'],[],[],[])])],
                [], [] ,'negative',[])])]

    sentences[0].sn[0].id='azeaz'
    sentences[0].sv[0].i_cmpl[0].nominal_group[0].id="4"
    sentences[1].sv[0].d_obj[0].id='sghj'
    sentences[1].sv[0].i_cmpl[0].nominal_group[0].id="9"
    sentences[2].sn[0].id='eaz'
    sentences[2].sv[0].d_obj[0].id='10'
    sentences[2].sv[0].i_cmpl[0].nominal_group[0].id="6"
    
    
    """
    ## TEST 1
    """
    print ''
    print ('######################## test 1.1 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    list_gr=recover_nom_gr_list(sentences)
    print 'The list of the nominal group'
    for i in list_gr:
        print (str(i))
    
    print '#####################################'
    print ''
    print 'the nominal group that we have to change'
    nom_gr_struc=Nominal_Group([],['it'],[],[],[])
    print (str(nom_gr_struc))
    
    print '#####################################'
    print 'After the first replacement'
    gr = first_replacement(list_gr, nom_gr_struc)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    print ''
    
    print '#####################################'
    utterance="no. I mean the shelf."
    print 'The speaker said :'
    print utterance
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    
    print '#####################################'
    nom_gr_struc=replacement(class_list, nom_gr_struc, list_gr[1:],gr)
    print 'the nominal group after processing'
    print (str(nom_gr_struc[0]))
    print 'the flag'
    print (str(nom_gr_struc[1]))


    """
    ## TEST 2
    """
    print ''
    print ('######################## test 1.2 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    
    list_gr=recover_nom_gr_list(sentences)
    print 'The list of the nominal group'
    for i in list_gr:
        print (str(i))
    
    print '#####################################'
    print ''
    print 'the nominal group that we have to change'
    nom_gr_struc=Nominal_Group([],['it'],[],[],[])
    print (str(nom_gr_struc))
    
    print '#####################################'
    print 'After the first replacement'
    gr = first_replacement(list_gr, nom_gr_struc)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    print ''
    
    print '#####################################'
    utterance="no."
    print 'The speaker said :'
    print utterance
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    
    print '#####################################'
    nom_gr_struc=replacement(class_list, nom_gr_struc, list_gr[1:],gr)
    print 'the nominal group after processing'
    print (str(nom_gr_struc[0]))
    print 'the flag'
    print (str(nom_gr_struc[1]))
    
    
    """
    ## TEST 3
    """
    print ''
    print ('######################## test 1.3 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    
    list_gr=recover_nom_gr_list(sentences)
    print 'The list of the nominal group'
    for i in list_gr:
        print (str(i))
    
    print '#####################################'
    print ''
    print 'the nominal group that we have to change'
    nom_gr_struc=Nominal_Group([],['it'],[],[],[])
    print (str(nom_gr_struc))
    
    print '#####################################'
    print 'After the first replacement'
    gr = first_replacement(list_gr, nom_gr_struc)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    print ''
    
    print '#####################################'
    utterance="no. I mean the blue bottle."
    print 'The speaker said :'
    print utterance
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    
    print '#####################################'
    nom_gr_struc=replacement(class_list, nom_gr_struc, list_gr[1:],gr)
    print 'the nominal group after processing'
    print (str(nom_gr_struc[0]))
    print 'the flag'
    print (str(nom_gr_struc[1]))
    
    """
    ## TEST 4
    """
    print ''
    print ('######################## test 1.4 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    
    list_gr=recover_nom_gr_list(sentences)
    print 'The list of the nominal group'
    for i in list_gr:
        print (str(i))
    
    print '#####################################'
    print ''
    print 'the nominal group that we have to change'
    nom_gr_struc=Nominal_Group([],['it'],[],[],[])
    print (str(nom_gr_struc))
    
    print '#####################################'
    print 'After the first replacement'
    gr = first_replacement(list_gr, nom_gr_struc)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    print ''
    
    print '#####################################'
    utterance="yes"
    print 'The speaker said :'
    print utterance
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    
    print '#####################################'
    nom_gr_struc=replacement(class_list, nom_gr_struc, list_gr[1:],gr)
    print 'the nominal group after processing'
    print (str(nom_gr_struc[0]))
    print 'the flag'
    print (str(nom_gr_struc[1]))
    
    
    
    """
    ## TEST 5
    """
    print ''
    print ('######################## test 1.5 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    
    list_gr=recover_nom_gr_list(sentences)
    print 'The list of the nominal group'
    for i in list_gr:
        print (str(i))
    
    print '#####################################'
    print ''
    print 'the nominal group that we have to change'
    nom_gr_struc=Nominal_Group(['this'],['one'],[],[],[])
    print (str(nom_gr_struc))
    
    print '#####################################'
    print 'After the first replacement'
    gr = first_replacement(list_gr, nom_gr_struc)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    print ''
    
    print '#####################################'
    utterance="yes"
    print 'The speaker said :'
    print utterance
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    
    print '#####################################'
    nom_gr_struc=replacement(class_list, nom_gr_struc, list_gr[1:],gr)
    print 'the nominal group after processing'
    print (str(nom_gr_struc[0]))
    print 'the flag'
    print (str(nom_gr_struc[1]))



    """
    ## TEST 6
    """
    print ''
    print ('######################## test 1.6 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    
    list_gr=recover_nom_gr_list(sentences)
    print 'The list of the nominal group'
    for i in list_gr:
        print (str(i))
    
    print '#####################################'
    print ''
    print 'the nominal group that we have to change'
    nom_gr_struc=Nominal_Group(['this'],['one'],[],[],[])
    print (str(nom_gr_struc))
    
    print '#####################################'
    print 'After the first replacement'
    gr = first_replacement(list_gr, nom_gr_struc)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    print ''
    
    print '#####################################'
    utterance="no. I mean the blue bottle."
    print 'The speaker said :'
    print utterance
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    
    print '#####################################'
    nom_gr_struc=replacement(class_list, nom_gr_struc, list_gr[1:],gr)
    print 'the nominal group after processing'
    print (str(nom_gr_struc[0]))
    print 'the flag'
    print (str(nom_gr_struc[1]))


    """
    ## TEST 7
    """
    print ''
    print ('######################## test 1.7 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    
    list_gr=recover_nom_gr_list(sentences)
    print 'The list of the nominal group'
    for i in list_gr:
        print (str(i))
    
    print '#####################################'
    print ''
    print 'the nominal group that we have to change'
    nom_gr_struc=Nominal_Group(['this'],[],[],[],[])
    print (str(nom_gr_struc))
    
    print '#####################################'
    print 'After the first replacement'
    gr = first_replacement(list_gr, nom_gr_struc)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    print ''
    
    print '#####################################'
    utterance="yes"
    print 'The speaker said :'
    print utterance
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    
    print '#####################################'
    nom_gr_struc=replacement(class_list, nom_gr_struc, list_gr[1:],gr)
    print 'the nominal group after processing'
    print (str(nom_gr_struc[0]))
    print 'the flag'
    print (str(nom_gr_struc[1]))



    """
    ## TEST 8
    """
    print ''
    print ('######################## test 1.8 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    
    list_gr=recover_nom_gr_list(sentences)
    print 'The list of the nominal group'
    for i in list_gr:
        print (str(i))
    
    print '#####################################'
    print ''
    print 'the nominal group that we have to change'
    nom_gr_struc=Nominal_Group(['this'],[],[],[],[])
    print (str(nom_gr_struc))
    
    print '#####################################'
    print 'After the first replacement'
    gr = first_replacement(list_gr, nom_gr_struc)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    print ''
    
    print '#####################################'
    utterance="no. I mean the blue bottle."
    print 'The speaker said :'
    print utterance
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    
    print '#####################################'
    nom_gr_struc=replacement(class_list, nom_gr_struc, list_gr[1:],gr)
    print 'the nominal group after processing'
    print (str(nom_gr_struc[0]))
    print 'the flag'
    print (str(nom_gr_struc[1]))
    
    
    
if __name__ == '__main__':
    anapohora_unit_tests()
    
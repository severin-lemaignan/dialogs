
"""
 Created by Chouayakh Mahdi                                                       
 23/07/2010                                                                       
 The package contains the unit test of remerge function                                       
    unit_tests : to perform unit tests                                           
"""
from sentence import *
from parsing import preprocessing
from parsing import analyse_sentence
from parsing import parser


def unit_tests():
    
    print ''
    print ('######################## test 1.1 ##############################')

    utterance="sorry"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='SUCCESS'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],[],[],[])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
        
    
    
    print ''
    print ('######################## test 1.2 ##############################')

    utterance="sorry"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='FAILURE'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],[],[],[])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
    
    
    
    print ''
    print ('######################## test 1.3 ##############################')

    utterance="the blue one"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='SUCCESS'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],['blue'],[],[])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
        
    
    print ''
    print ('######################## test 1.4 ##############################')

    utterance="the blue one. I mean"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='FAILURE'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],['blue'],[],[])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
    
    
    
    print ''
    print ('######################## test 1.5 ##############################')

    utterance="it is on the table"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='SUCCESS'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                    [],  
                    [Verbal_Group(['be'],[],'present simple', 
                        [], 
                        [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                        [], [] ,'affirmative',[])])])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
        
        
        
    print ''
    print ('######################## test 1.6 ##############################')

    utterance="the bottle on the table"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='SUCCESS'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                    [],  
                    [Verbal_Group(['be'],[],'present simple', 
                        [], 
                        [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                        [], [] ,'affirmative',[])])])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
    
    
    
    print ''
    print ('######################## test 1.7 ##############################')

    utterance="I'm talking about the green bottle"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='FAILURE'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],['blue'],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],['green'],[],[])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
        
        
        
    print ''
    print ('######################## test 1.8 ##############################')

    utterance="sorry. I mean the green one"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='FAILURE'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],['green'],[],[])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
        
    """
    
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 1.2 ##############################')

    utterance="sorry. I want to say the dark one"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='FAILURE'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],[],[],[])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
    
    
    
    
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 1.3 ##############################')

    utterance="No. He means the one which he bought yesterday."
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='FAILURE'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],['blue'],[],[])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
        
        
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 1.4 ##############################')

    utterance="I mean the bottle of Jido"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='SUCCESS'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],['blue'],[],[])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
    
    
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 1.5 ##############################')

    utterance="He mean that he want the bottle of Jido"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='FAILURE'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                    [],  
                    [Verbal_Group(['be'],[],'present simple', 
                        [], 
                        [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                        [], [] ,'affirmative',[])])])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
        
        
        
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 1.1 ##############################')

    utterance="it is the best one"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='SUCCESS'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                    [],  
                    [Verbal_Group(['be'],[],'present simple', 
                        [], 
                        [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                        [], [] ,'affirmative',[])])])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''
    
    
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 1.1 ##############################')

    utterance="it is the best one"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list=analyse_sentence.sentences_analyzer(sentence_list)
    flag='FAILURE'
    
    nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
    print 'the nominal group of the last out put'
    print (str(nom_gr_struc))
    
    nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
    print 'the nominal group after processing'
    print (str(nom_gr_struc))
    
    rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                    [],  
                    [Verbal_Group(['be'],[],'present simple', 
                        [], 
                        [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                        [], [] ,'affirmative',[])])])
    
    if parser.compare_nom_gr([nom_gr_struc],[rslt])==0:
        print "############### Parsing is OK ###############"
        print ''
    else:
        print "There is a problem with parsing this sentence"
        print ''    
    """

if __name__ == '__main__':
    unit_tests()

"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 07/07/2010                                                                       ##
## The package contains functions needed to perform verbalisation of sentences      ##
## Functions:                                                                       ##
##    statement : to verbalise a statment                                           ##
##    imperative : to verbalise an imperative                                       ##
##    y_o_question : to verbalise an yes or no question                             ##
##    w_question : to verbalise a w_question                                        ##
##    quantity_ques : to verbalise a question about quantity                        ##
##    choice_ques : to verbalise a question about choice                            ##
##    possession_ques : to verbalise a question about possession                    ##
##    sub_treat : to verbalises a subsentence                                       ##
######################################################################################
"""
import element_recovery
import other_functions


"""
######################################################################################
## This function verbalises a statment                                              ##
## Input=class sentence                              Output=sentence                ##
######################################################################################
"""
def statement(analysis):

    #Recovering the subject
    phrase=element_recovery.nom_struc_recovery(analysis.sn)
    
    #Recovering the end of the sentence
    phrase=element_recovery.end_statement_recovery(phrase, analysis.sv, analysis.sn, analysis.data_type)
    
    #Recovering subsentences
    for s in analysis.sv[0].vrb_sub_sentence:
        phrase=phrase+sub_treat(s)

    #Eliminate redundancies if there are
    phrase=other_functions.eliminate_redundancy(phrase)
    
    #If it is a relative form
    if analysis.data_type=='relative' or analysis.data_type=='subsentence':
        return phrase+[';']
    
    return phrase+['.']


"""
######################################################################################
## This function verbalises an imperative                                           ##
## Input=class sentence                              Output=sentence                ##
######################################################################################
"""
def imperative(analysis):

    #init
    phrase=[]
    
    #Recovering the basic part of the sentence
    phrase=element_recovery.end_statement_recovery(phrase, analysis.sv, analysis.sn, analysis.data_type)

    #Recovering subsentences
    for s in analysis.sv[0].vrb_sub_sentence:
        phrase=phrase+sub_treat(s)
        
    #Eliminate redundancies if there are
    phrase=other_functions.eliminate_redundancy(phrase)
    return phrase+['.']


"""
######################################################################################
## This function verbalises an yes or no question                                   ##
## Input=class sentence                              Output=sentence                ##
######################################################################################
"""
def y_o_question(analysis):
    
    #init
    phrase=[]
    
    #Recovering the subject
    subject=element_recovery.nom_struc_recovery(analysis.sn)

    #Recovering the end of the sentence
    phrase=element_recovery.end_question_recovery(phrase, analysis.sv, analysis.sn)

    #We need special treatment to find the position of the subject
    if analysis.sv[0].state=='negative':
        phrase=phrase[0:2]+subject+phrase[2:]
    else:
        phrase=[phrase[0]]+subject+phrase[1:]

    #Recovering subsentences
    for s in analysis.sv[0].vrb_sub_sentence:
        phrase=phrase+sub_treat(s)

    #Eliminate redundancies if there are
    phrase=other_functions.eliminate_redundancy(phrase)
    
    #If it is a question about the origin
    if analysis.aim=='origin':
        return phrase+['from']+['?']
    
    return phrase+['?']


"""
######################################################################################
## This function verbalises a w_question                                            ##
## Input=class sentence                              Output=sentence                ##
######################################################################################
"""
def w_question(analysis):
    
    #Opinion is a what question so we have to make some changes
    if analysis.sv[0].vrb_main[0].endswith('like'):
        verb=analysis.sv[0].vrb_main[0]
        analysis.sv[0].vrb_main[0]=verb[:len(verb)-4]+'think+of'

    #Treatment as yes or no question
    phrase=y_o_question(analysis)

    #Specific treatment for invitation
    if analysis.aim=='invitation':
        return ['how', 'about']+phrase[1:]

    #Specific treatment for classification
    if analysis.aim.startswith('classification'):
        aim_question=other_functions.list_recovery(analysis.aim)
        return ['what','kind','of']+aim_question[1:]+phrase

    return ['what']+phrase


"""
######################################################################################
## This function verbalises a question about quantity                               ##
## Input=class sentence                              Output=sentence                ##
######################################################################################
"""
def quantity_ques(analysis):
    
    #init
    phrase=[]
    
    #We have to memorise the verb
    verb=other_functions.list_recovery(analysis.sv[0].vrb_main[0])

    #First case : aim is the subject with verb be
    if analysis.sv[0].d_obj==[] and (verb[0]=='be' or (len(verb)>1 and  verb[1]=='be')):
        phrase=statement(analysis)
        return ['how','much']+phrase[1:len(phrase)-1]+['?']

    #Second case : aim is the subject without verb be
    elif  analysis.sv[0].d_obj==[]:
        return ['how','much']+y_o_question(analysis)

    #Third case : as yes no question without the direct complement
    else:
        subject=element_recovery.nom_struc_recovery(analysis.sn)
    
        #Same treatment with yes no question
        phrase=element_recovery.vrb_ques_recovery(analysis.sv[0].vrb_tense, analysis.sv[0].vrb_main, analysis.sv[0].vrb_adv, analysis.sn, analysis.sv[0].state)
        phrase=phrase+element_recovery.indirect_compl_recovery(analysis.sv[0].i_cmpl)
        phrase=phrase+analysis.sv[0].advrb
        if analysis.sv[0].sv_sec!=[]:
            phrase=phrase+['to']+analysis.sv[0].sv_sec[0].vrb_adv+other_functions.list_recovery(analysis.sv[0].sv_sec[0].vrb_main[0])
            phrase=phrase+element_recovery.nom_struc_recovery(analysis.sv[0].sv_sec[0].d_obj)
            phrase=phrase+element_recovery.indirect_compl_recovery(analysis.sv[0].sv_sec[0].i_cmpl)
            phrase=phrase+analysis.sv[0].sv_sec[0].advrb

        for s in analysis.sv[0].vrb_sub_sentence:
            phrase=phrase+sub_treat(s)
        
        #Treatment of the state
        if analysis.sv[0].state=='negative':
            phrase=phrase[0:2]+subject+phrase[2:]
        else:
            phrase=[phrase[0]]+subject+phrase[1:]

        return ['how', 'much']+analysis.sv[0].d_obj[0].noun+phrase+['?']


"""
######################################################################################
## This function verbalises a question about choice                                 ##
## Input=class sentence                              Output=sentence                ##
######################################################################################
"""
def choice_ques(analysis):

    #Treatment as statement
    phrase=statement(analysis)
    phrase[0]='which'
    return phrase


"""
######################################################################################
## This function verbalises a question about possession                             ##
## Input=class sentence                              Output=sentence                ##
######################################################################################
"""
def possession_ques(analysis):

    #Treatment as statement
    phrase=statement(analysis)

    #We have to know if it is plural or singular
    if len(analysis.sn)>1 or analysis.sn[0].noun[0].endswith('s'):
        return ['whose']+phrase[:len(phrase)-1]+['these']+['?']
    else:
        return ['whose']+phrase[1:len(phrase)-1]+['this']+['?']


"""
######################################################################################
## This function verbalises a subsentence                                           ##
## Input=class sentence                              Output=sentence                ##
######################################################################################
"""
def sub_treat(analysis):

    #Treatment as statement
    subsentence=statement(analysis)
    return [analysis.aim]+subsentence

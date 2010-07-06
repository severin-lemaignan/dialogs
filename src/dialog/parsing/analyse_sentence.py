#!/usr/bin/python
# -*- coding: utf-8 -*-
# SVN:rev202 + PythonTidy

"""
cette fonction nous permet de traiter une phrase recuperee sous forme
de liste de chaine de caracteres et de retourner une liste de class
contenant les information necessaire pour interroger le serveur

v.0.2: 21:frt_wd from ResourcePool
"""


"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 25/06/2010                                                                       ##
## The package contains functions to analyse all sentence of a reply                ##
## Functions:                                                                       ##
##    dispatching : to distribute the sentence                                      ##
##    w_quest_where : to treat many different type of where question                ##
##    w_quest_what  : to treat many different type of what question                 ##
##    w_quest_quant : to treat many different type of how question                  ##
##    w_quest_how : to treat many different type of how question                    ##
##    condi_sentence : to treat the conditionnal sentence                           ##
##    w_quest_whose : to treat many different type of whose question                ##
##    y_n_ques : to treat the yes or no question from of a sentence                 ##
##    other_sentence : to treat the other from of a sentence                        ##
##    sentences_analyzer : is the basic fonction of parsing                         ##
######################################################################################
"""
from sentence import *
from resources_manager import ResourcePool
import analyse_nominal_group
import analyse_nominal_structure
import analyse_verb
import analyse_verbal_structure
import other_functions


"""
############################## Statement of lists ####################################
"""
modal_list=['must', 'should', 'may', 'might', 'can', 'could', 'shall']


"""
######################################################################################
## We have to read all words that sentence can begin with                           ##
######################################################################################
"""
frt_wd = ResourcePool().sentence_starts.keys()


"""
######################################################################################
## This function distributes the sentence according to:                             ##
## their functionality and their type                                               ##
## Input=sentence, beginning sentence list          Output=class Sentence           ##
######################################################################################
"""
def dispatching(sentence):

    if len(sentence)>0:
        
        #For interjection
        if sentence[len(sentence)-1]=='!':
            return Sentence('interjection', '', [], [])

        #When others
        for x in frt_wd:
            #If we find a knowing case
            if sentence[0]==x[0]:


                #For
                if x[1] == '0':
                    return Sentence('start', '', [], [])

                #It's a w_question
                if x[1] == '1':

                    #For 'when'
                    if x[2]=='1':
                        #If we remove the first word => it becomes like y_n_question
                        return y_n_ques('w_question', 'date', sentence[1:])

                    #For 'where'
                    elif x[2]=='2':
                        return w_quest_where('w_question', 'place', sentence)

                    #For 'what'
                    elif x[2]=='3':

                        #We have different type of question with 'what'
                        if sentence[1]=='time':
                            return y_n_ques('w_question', 'time', sentence[2:])

                        elif sentence[1]=='color':
                            return y_n_ques('w_question', 'color', sentence[2:])
                            
                        elif sentence[1]=='size':
                            return y_n_ques('w_question', 'size', sentence[2:])

                        #Here we have to use a specific treatment for 'type' and 'kind'
                        elif sentence[1]=='type' or sentence[1]=='kind':
                            #We start by treating the end of the sentence like a y_n_question
                            return y_n_ques('w_question', 'classification'+'+'+sentence[3],sentence[4:])

                        #For other type of 'what' question
                        else:
                            return w_quest_what('w_question', sentence, 2)

                    #For 'how'
                    elif x[2]=='4':
                        if sentence[1]== 'old':
                            return y_n_ques('w_question', 'age', sentence[2:])

                        elif sentence[1]== 'long':
                            return y_n_ques('w_question', 'duration', sentence[2:])

                        elif sentence[1]=='often':
                            return y_n_ques('w_question', 'frequency', sentence[2:])

                        elif sentence[1]=='many' or sentence[1]=='much' :
                            return w_quest_quant('w_question', 'quantity', sentence)

                        elif sentence[1]=='far':
                            return y_n_ques('w_question', 'distance', sentence[2:])

                        elif sentence[1]=='soon':
                            return y_n_ques('w_question', 'time', sentence[2:])

                        elif sentence[1]=='about':
                            #We replace 'about' by 'is' to have a y_n_question
                            sentence[1]='is'
                            return y_n_ques('w_question', 'invitation', sentence[1:])

                        #For other type of 'how' question
                        else:
                            return w_quest_how('w_question', sentence)

                    #For 'why'
                    elif x[2]=='5':
                        return y_n_ques('w_question', 'purpose', sentence[1:])

                    #For 'whose'
                    elif x[2]=='6':
                        return w_quest_whose('w_question', 'possession', sentence)

                    #For 'who'
                    elif x[2]=='7':
                        return y_n_ques('w_question', 'people', sentence[1:])

                    #For 'which'
                    elif x[2]=='8':
                        return other_sentence('w_question', 'choice', sentence[1:])

                #It's a y_n_question
                elif x[1] == '2':
                    return y_n_ques('yes_no_question', '', sentence)

                #It's a conditionnal sentence
                elif x[1]=='3':
                    return condi_sentence(sentence)

                #Agree
                elif x[1]=='4':
                    return Sentence('agree', '', [], [])

                #Disagree
                elif x[1]=='5':
                    return Sentence('disagree', '', [], [])

                #It's a y_n_question
                elif x[1]=='6':
                    return Sentence('gratulation', '', [], [])

        #It's a statement or an imperative sentence
        if sentence[len(sentence)-1]=='?':
            return other_sentence('yes_no_question', '', sentence)
        else:
            return other_sentence('', '', sentence)

    #Default case
    return []


"""
######################################################################################
## This function treats many different type of where question                       ##
## Input=type and requestion of sentence, the sentence      Output=class Sentence   ##
######################################################################################
"""
def w_quest_where(type, request, stc):

    #If there is 'form' at the end => question about the origin
    if stc[len(stc)-1]=='from' or (stc[len(stc)-1]=='?' and stc[len(stc)-2]=='from'):

        #If we remove the first word => it becomes like y_n_question
        return y_n_ques(type, 'origin', stc[1:])
    else:
        #If we remove the first word => it becomes like y_n_question
        return y_n_ques(type, request, stc[1:])


"""
######################################################################################
## This function treats many different type of what question                        ##
## Input=type of sentence, the sentence and position of suject                      ##
## Output=class Sentence                                                            ##
######################################################################################
"""
def w_quest_what(type, sentence,sbj_pos):
    
    #We start with a treatment with the function of y_n_question's case
    analysis=y_n_ques(type, 'thing',sentence[sbj_pos-1:])
    
    #The case when we have 'happen'
    if analysis.sv[0].vrb_main[0].endswith('happen'):
        analysis.aim='situation'

    #The case when we have 'think'
    elif analysis.sv[0].vrb_main[0].endswith('think+of') or analysis.sv[0].vrb_main[0].endswith('think+about'):
        analysis.aim='opinion'

    #The case when we have 'like' + conditionnal
    elif analysis.sv[0].vrb_main[0].endswith('like') and not(analysis.sv[0].vrb_tense.endswith('conditionnal')):
        analysis.aim='descrition'

    #The case when we have 'do' + ing form
    elif analysis.sv[0].vrb_main[0].endswith('do') and analysis.sv[0].i_cmpl!=[] and analysis.sv[0].i_cmpl[0].nominal_group[0].noun[0].endswith('ing'):
        analysis.aim='explication'

    return analysis


"""
######################################################################################
## This function treats many different type of quantity question                    ##
## Input=type and requestion of sentence, the sentence and beginning sentence list  ##
## Output=class Sentence                                                            ##
######################################################################################
"""
def w_quest_quant(type, request, sentence):

    for j in frt_wd :
        if sentence[2]==j[0]:
            if j[1]=='2':
                #This case is the same with y_n_question
                return y_n_ques(type, request,sentence[2:], 1)

    analysis=y_n_ques(type, request,sentence[3:])

    #There is not sn in the sentence
    if analysis.sn==[]:
        analysis.sn=[Nominal_Group(['a'],[sentence[2]],[],[],[],0)]

    #There is not direct object in the sentence
    else:
        analysis.sv[0].d_obj=[Nominal_Group(['a'],[sentence[2]],[],[],[],0)]
    
    return analysis


"""
######################################################################################
## This function treats many different type of how question                         ##
## Input=type of sentence, the sentence      Output=class Sentence                  ##
######################################################################################
"""
def w_quest_how(type, sentence):
    
    analysis=y_n_ques(type, 'manner', sentence[1:])

    #The case when we have 'do' + ing form
    if analysis.sv[0].vrb_main[0].endswith('like'):
        analysis.aim='opinion'
    return analysis


"""
######################################################################################
## This function treats the conditionnal sentence                                   ##
## Input=sentence                                          Output=class Sentence    ##
######################################################################################
"""
def condi_sentence(sentence):

    #We recover the conditionnal sentence
    conditionnal_sentence=sentence[1:sentence.index(';')]

    #We perform the 2 treatments
    analysis=other_sentence('statement', '', sentence[sentence.index(';')+1:])
    analysis.sv[0].vrb_sub_sentence=[other_sentence('condition', 'if', conditionnal_sentence)]

    return analysis


"""
######################################################################################
## This function treats many different type of whose question                       ##
## Input=type and requestion of sentence and the sentence                           ##
## Output=class Sentence                                                            ##
######################################################################################
"""
def w_quest_whose(type, request, sentence):

    vg=Verbal_Group(['be'], [],'', [], [], [], [] ,'affirmative',[])
    analysis=Sentence(type, request, [], [])


    #We replace 'whose' by 'that' to have a nominal group
    sentence[0]='that'

    #We recover the subject
    sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 0)

    if sentence[1]=='not':
        vg.state='negative'

    analysis.sv=[vg]
    return analysis


"""
######################################################################################
## This function treats the yes or no question from of a sentence                   ##
## Input=type and requestion of sentence and the sentence                           ##
## Output=class Sentence                                                            ##
######################################################################################
"""
def y_n_ques(type, request, sentence):
    
    #init
    vg=Verbal_Group([], [],'', [], [], [], [] ,'affirmative',[])
    analysis=Sentence(type, request, [], [])
    modal=[]

    #We recover the auxilary 
    aux=sentence[0]
    
    #We have to know if there is a modal
    for m in modal_list:
        if aux==m:
            modal=aux

    #If we have a negative form
    if sentence[1]=='not':
        vg.state='negative'
        #We remove 'not'
        sentence=sentence[:1]+ sentence[2:]

    #In this case we have an imperative sentence
    if analyse_nominal_group.find_sn_pos(sentence, 0)==[] and type!='w_question':
        #We have to reput the 'not'
        if vg.state=='negative':
            sentence=sentence[:1]+['not']+sentence[1:]
        return other_sentence(type, request, sentence)

    #We delete the auxilary
    sentence=sentence[1:]

    #We recover the subject
    sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 0)
    
    #If there is one element => it is an auxiliary => verb 'be'
    if len(sentence)==1:
        vg.vrb_tense = analyse_verb.find_tense_statement(aux, vg.vrb_adv)
        vg.vrb_main=['be']
    else:
        vg.vrb_adv=analyse_verbal_structure.find_vrb_adv(sentence)
        vg.vrb_tense = analyse_verb.find_tense_question(sentence, aux, vg.vrb_adv)

        #We treat the verb
        verb=analyse_verb.find_verb_question(sentence, vg.vrb_adv, aux, vg.vrb_tense)
        verb_main=analyse_verb.return_verb(sentence, verb, vg.vrb_tense)
        vg.vrb_main=[other_functions.convert_to_string(verb_main)]
        
        #We delete the verb if the aux is not the verb 'be'
        if vg.vrb_main!=['be']:
            sentence= sentence[sentence.index(verb[0])+len(verb_main):]
        
        #In case there is a state verb followed by an adjective
        if vg.vrb_main[0]=='be' and analyse_nominal_group.adjective_pos(sentence,0)-1!=0:
            pos=analyse_nominal_group.adjective_pos(sentence,0)
            analysis.sn[0].adj=analysis.sn[0].adj+sentence[:pos-1]
            sentence=sentence[pos:]
        
        #Here we have special treatment for different cases
        if sentence!=[]:
            #For 'what' descrition case
            if sentence[0]=='like' and aux!='would':
                vg.vrb_main=['like']
                sentence=sentence[1:]

            #For 'how' questions with often
            elif sentence[0].endswith('ing'):
                vg.vrb_main[0]=vg.vrb_main[0]+'+'+sentence[0]

        #It verifies if there is a secondary verb
        sec_vrb=analyse_verbal_structure.find_scd_vrb(sentence)
        if sec_vrb!=[]:
            sentence=analyse_verbal_structure.treat_scd_sentence(sentence, vg, sec_vrb)

        #We recover the subsentence
        sentence=analyse_verbal_structure.treat_subsentence(sentence, vg)
        
        #We recover the direct, indirect complement and the adverbial
        sentence=analyse_verbal_structure.recover_obj_iobj(sentence, vg)
    
        #We have to take off abverbs form the sentence
        vg.advrb=analyse_verbal_structure.find_adv(sentence)

    #We perform the treatment with the modal
    if modal!=[]:
        vg.vrb_main=[modal+'+'+vg.vrb_main[0]]
        
    analysis.sv=[vg]
    return analysis


"""
######################################################################################
## This function treats the other from of a sentence                                ##
## Input=type and requestion of sentence and the sentence                           ##
## Output=class Sentence                                                            ##
######################################################################################
"""
def other_sentence(type, request, sentence):
    
    #init
    vg=Verbal_Group([], [],'', [], [], [], [] ,'affirmative',[])
    analysis=Sentence(type, request, [], [])
    modal=[]

    #We search the subject
    sbj=analyse_nominal_group.find_sn_pos(sentence, 0)
    if sbj!=[] or type=='relative' :
        #If we haven't a data type => it is a statement
        if type=='':
            analysis.data_type='statement'


        #We recover the subject
        sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 0)

        #We have to know if there is a modal
        for m in modal_list:
            if sentence[0]==m:
                modal=sentence[0]
                
        
        #We must take into account all possible cases to recover the sentence's tense
        if len(sentence)>1 and sentence[1]=='not':
            vg.state='negative'

            #Before the negative form we have an auxilary for the negation
            if sentence[0]=='do' or sentence[0]=='does' or sentence[0]=='did' :
                vg.vrb_tense = analyse_verb.find_tense_statement([sentence[0]], [])
                sentence=sentence[2:]
                vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
            
            #There is a modal
            elif modal!=[]:
                sentence=sentence[2:]
                vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
                vg.vrb_tense = analyse_verb.find_tense_statement(sentence, vg.vrb_adv)

            else:
                #We remove 'not' and find the tense
                sentence=sentence[:1]+ sentence[2:]
                vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
                vg.vrb_tense = analyse_verb.find_tense_statement(sentence, vg.vrb_adv)
        
        #For the affirmative treatment
        else:
            vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
            vg.vrb_tense = analyse_verb.find_tense_statement(sentence, vg.vrb_adv)
        
        verb=analyse_verb.find_verb_statement(sentence,vg.vrb_adv, vg.vrb_tense)
        verb_main=analyse_verb.return_verb(sentence, verb, vg.vrb_tense)
        vg.vrb_main=[other_functions.convert_to_string(verb_main)]
        
        #We delete the verb
        sentence= sentence[sentence.index(verb[0])+len(verb_main):]
        
        #In case there is a state verb followed by an adjective
        if vg.vrb_main[0]=='be' and analyse_nominal_group.adjective_pos(sentence,0)-1!=0:
            pos=analyse_nominal_group.adjective_pos(sentence,0)
            analysis.sn[0].adj=analysis.sn[0].adj+sentence[:pos-1]
            sentence=sentence[pos:]
            
        #We perform the treatment with the modal
        if modal!=[]:
            vg.vrb_main=[modal+'+'+vg.vrb_main[0]]
            #We force the time
            if modal=='should' or modal=='might' or modal=='could':
                vg.vrb_tense='present conditionnal'


    #This is a imperative form
    else:
        #re-init
        analysis.data_type='imperative'
        vg.vrb_tense='present simple'

        #Negative form
        if sentence[1]=='not':
            sentence=sentence[sentence.index('not')+1:]
            vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)
            vg.state='negative'
        else:
            vg.vrb_adv=analyse_verbal_structure.find_vrb_adv (sentence)

        #We treat the verb
        verb=[sentence[0+len(vg.vrb_adv)]]
        vg.vrb_main=[other_functions.convert_to_string(analyse_verb.return_verb(sentence, verb, vg.vrb_tense))]
        
        #We delete the verb
        sentence= sentence[sentence.index(verb[0])+len(verb):]
    
    #We recover the subsentence
    sentence=analyse_verbal_structure.treat_subsentence(sentence, vg)
    
    #It verifies if there is a secondary verb
    sec_vrb=analyse_verbal_structure.find_scd_vrb(sentence)
    if sec_vrb!=[]:
        sentence=analyse_verbal_structure.treat_scd_sentence(sentence, vg, sec_vrb)
    
    #We recover the direct, indirect complement and the adverbial
    sentence=analyse_verbal_structure.recover_obj_iobj(sentence, vg)

    #We have to take off abverbs form the sentence
    vg.advrb=analyse_verbal_structure.find_adv(sentence)

    analysis.sv=[vg]
    return analysis


"""
######################################################################################
## This function is the basic fonction of parsing                                   ##
## Input=list of sentences and beginning sentence list                              ##
## Output=list of class Sentence                                                    ##
######################################################################################
"""
def sentences_analyzer(sentences):

    #init
    class_sentence_list=[]

    #We treat all sentences of the list
    for i in sentences:
        class_sentence_list=class_sentence_list+[dispatching(i)]

    return class_sentence_list

#!/usr/bin/python
# -*- coding: utf-8 -*-
# SVN:rev202 + PythonTidy

"""
 Created by Chouayakh Mahdi                                                       
 25/06/2010                                                                       
 The package contains functions to analyse all sentence of a utterance            
 Functions:                                 
    recover_aux_list : to recover the auxiliary list  
    dispatching : to distribute the sentence           
    exclama_sentence : to process exclamatively sentence                     
    w_quest_where : to process many different type of where question                
    w_quest_what  : to process many different type of what question                 
    w_quest_quant : to process many different type of how question
    w_quest_how : to process many different type of how question                    
    condi_sentence : to process the conditional sentence                           
    w_quest_whose : to process many different type of whose question   
    w_quest_whom : to process whom question
    y_n_ques : to process the yes or no question from of a sentence                 
    other_sentence : to process the other from of a sentence                        
    sentences_analyzer : is the basic function of parsing                         
"""
from dialog.sentence import *
from dialog.resources_manager import ResourcePool
import analyse_nominal_group
import analyse_nominal_structure
import analyse_verb
import analyse_verbal_structure
import other_functions


"""
Statement of lists
"""
frt_wd = ResourcePool().sentence_starts
det_dem_list = ResourcePool().demonstrative_det
modal_list = ResourcePool().modal



def dispatching(sentence):
    """
    This function distributes the sentence according to:                             
    Their functionality and their type                                               
    Input=sentence, beginning sentence list          Output=class Sentence           
    """
    
    if len(sentence)>0:
        
        #For ending dialogue
        if sentence[0].endswith('bye'):
            return [Sentence('end', '', [], [])]
        
        #When others
        for x in frt_wd:
            #If we find a knowing case
            if sentence[0]==x[0]:

                #For
                if x[1] == '1':
                    return [Sentence('start', '', [], [])]
                
                #It's a w_question or subsentence
                if x[1] == '2':
                    
                    #If there is which or no nominal group it is a question
                    if sentence[0]!='which' and analyse_nominal_group.find_sn_pos(sentence, 1)!=[]:
                        #Here we have the condition of the subsentences
                        return [stc_start_subsentence(sentence)]
                    
                    #For 'when'
                    if x[2]=='1':
                        #If we remove the first word => it becomes like y_n_question
                        return [y_n_ques('w_question', 'date', sentence[1:])]

                    #For 'where'
                    elif x[2]=='2':
                        return [w_quest_where('w_question', 'place', sentence)]
                    
                    #For 'what'
                    elif x[2]=='3':
                        #Here we have to use a specific processing for 'type' and 'kind'
                        if sentence[1]=='type' or sentence[1]=='kind':
                            #We start by processing the end of the sentence like a y_n_question
                            return [y_n_ques('w_question', 'classification'+'+'+sentence[4],sentence[5:])]

                        #For other type of 'what' question
                        else:
                            return [w_quest_what('w_question', sentence)]

                    #For 'how'
                    elif x[2]=='4':

                        if sentence[1]=='many' or sentence[1]=='much' :
                            return [w_quest_quant('w_question', 'quantity', sentence)]
                        
                        elif sentence[1]=='about':
                            #We replace 'about' by 'is' to have a y_n_question
                            sentence[1]='is'
                            return [y_n_ques('w_question', 'invitation', sentence[1:])]

                        #For other type of 'how' question
                        else:
                            return [w_quest_how('w_question', sentence)]

                    #For 'why'
                    elif x[2]=='5':
                        return [y_n_ques('w_question', 'reason', sentence[1:])]

                    #For 'whose'
                    elif x[2]=='6':
                        return [w_quest_whose('w_question', 'owner', sentence)]

                    #For 'who'
                    elif x[2]=='7':
                        return [y_n_ques('w_question', 'people', sentence[1:])]

                    #For 'which'
                    elif x[2]=='8':
                        return [other_sentence('w_question', 'choice', sentence[1:])]
                    
                    #For 'to whom'
                    elif x[2]=='9':
                        return [w_quest_whom('w_question', 'people', sentence[1:])]

                #It's a y_n_question
                elif x[1] == '3':
                    return [y_n_ques('yes_no_question', '', sentence)]

                #It's a conditional sentence
                elif x[1]=='4':
                    return [stc_start_subsentence(sentence)]

                #Agree
                elif x[1]=='5':
                    return separ_sentence(sentence, 'agree')
                    
                #Disagree
                elif x[1]=='6':
                    return separ_sentence(sentence, 'disagree')

                #It's a y_n_question
                elif x[1]=='7':
                    return separ_sentence(sentence, 'gratulation')
                
        #For exclamatively
        if sentence[len(sentence)-1]=='!':
            return [exclama_sentence(sentence)]
        
        #It's a statement or an imperative sentence
        if sentence[len(sentence)-1]=='?':
            return [other_sentence('yes_no_question', '', sentence)]
        else:
            return [other_sentence('', '', sentence)]

    #Default case
    return []



def separ_sentence(sentence, data_type):
    sentences=[Sentence(data_type, '', [], [])]
    for i in sentence:
        if i==';':
            sentences = sentences + dispatching(sentence[sentence.index(i)+1:])
    return sentences



def exclama_sentence(sentence):
    """
    This function process exclamatively sentence                       
    Input=the sentence                                   Output=class Sentence   
    """
    
    #init
    analysis=Sentence('interjection', '', [], [])
    
    for i in frt_wd:
        if i[0]==sentence[0]:
            #We recover the subject
            sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 1)
            return analysis
        elif i[1]>0:
            #We recover the subject
            sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 0)
            return analysis
     


def w_quest_where(type, request, stc):
    """
    This function process many different type of where question                       
    Input=type and requesting of sentence, the sentence      Output=class Sentence   
    """
    
    #If there is 'form' at the end => question about the origin
    if stc[len(stc)-1]=='from' or (stc[len(stc)-1]=='?' and stc[len(stc)-2]=='from'):
        #If we remove the first word => it becomes like y_n_question
        return y_n_ques(type, 'origin', stc[1:])
    else:
        #If we remove the first word => it becomes like y_n_question
        return y_n_ques(type, request, stc[1:])


def w_quest_what(type, sentence):
    """
    This function process many different type of what question                        
    Input=type of sentence, the sentence and position of subject                      
    Output=class Sentence                                                            
    """
    
    aux_list = other_functions.recover_aux_list()
    for l in aux_list:
        if sentence[1]==l:
            #We start with a processing with the function of y_n_question's case
            analysis=y_n_ques(type, 'thing',sentence[1:])
            
            vg=analysis.sv[0]
            #The case when we have 'happen'
            if analysis.sv[0].vrb_main[0].endswith('happen'):
                analysis.aim='situation'

            #The case when we have 'think'
            elif analysis.sv[0].vrb_main[0].endswith('think+of') or analysis.sv[0].vrb_main[0].endswith('think+about'):
                analysis.aim='opinion'

            #The case when we have 'like' + conditional
            elif analysis.sv[0].vrb_main[0].endswith('like') and not(analysis.sv[0].vrb_tense.endswith('conditional')):
                analysis.aim='description'

            #The case when we have 'do' + ing form
            elif vg.vrb_main[0].endswith('do') and vg.i_cmpl!=[] and vg.i_cmpl[0].nominal_group[0].adj!=[] and vg.i_cmpl[0].nominal_group[0].adj[0][0].endswith('ing'):
                analysis.aim='explication'
            
            return analysis
    
    analysis=y_n_ques(type, sentence[1],sentence[2:])
    return analysis



def w_quest_quant(type, request, sentence):
    """
    This function process many different type of quantity question                    
    Input=type and requesting of sentence, the sentence and beginning sentence list  
    Output=class Sentence                                                            
    """

    for j in frt_wd :
        if sentence[2]==j[0]:
            if j[1]=='3':
                #This case is the same with y_n_question
                return y_n_ques(type, request,sentence[2:])

    analysis=y_n_ques(type, request,sentence[3:])

    #There is not sn in the sentence
    if analysis.sn==[]:
        analysis.sn=[Nominal_Group(['a'],[sentence[2]],[],[],[])]

    #There is not direct object in the sentence
    else:
        analysis.sv[0].d_obj=[Nominal_Group(['a'],[sentence[2]],[],[],[])]
    
    return analysis



def w_quest_how(type, sentence):
    """
    This function process many different type of how question                         
    Input=type of sentence, the sentence      Output=class Sentence                  
    """
    
    aux_list = other_functions.recover_aux_list()
    for l in aux_list:    
        if sentence[1]==l:
            analysis=y_n_ques(type, 'manner', sentence[1:])
        
            #The case when we have 'do' + ing form
            if analysis.sv[0].vrb_main[0].endswith('like'):
                analysis.aim='opinion'
            return analysis
        
    analysis=y_n_ques(type, sentence[1],sentence[2:])
    return analysis



def stc_start_subsentence(sentence):
    """
    This function process the conditional sentence
    Input=sentence                                          Output=class Sentence    
    """

    #We recover the conditional sentence
    subsentence=sentence[1:sentence.index(';')]

    #We perform the 2 processing
    analysis=other_sentence('statement', '', sentence[sentence.index(';')+1:])
    analysis.sv[0].vrb_sub_sentence=[other_sentence('subsentence', sentence[0], subsentence)]

    return analysis



def w_quest_whose(type, request, sentence):
    """
    This function process many different type of whose question                       
    Input=type and requesting of sentence and the sentence                           
    Output=class Sentence                                                           
    """

    #init
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



def w_quest_whom(type, request, sentence):
    """
    This function process whom question                                            
    Input=type and requesting of sentence and the sentence
    Output=class Sentence                                                            
    """
    
    #It is the same with yes or no question
    analysis=y_n_ques(type, request, sentence)
    
    #We have to add 'to' to the verb
    analysis.sv[0].vrb_main[0]=analysis.sv[0].vrb_main[0]+'+to'
    
    return analysis



def y_n_ques(type, request, sentence):
    """
    This function process the yes or no question from of a sentence
    Input=type and requesting of sentence and the sentence                           
    Output=class Sentence                                                            
    """
    
    #init
    vg=Verbal_Group([], [],'', [], [], [], [] ,'affirmative',[])
    analysis=Sentence(type, request, [], [])
    modal=[]
    
    #We start with determination of probably second verb in subsentence
    sentence=other_functions.find_scd_verb_sub(sentence)
    
    #We recover the auxiliary 
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

    #Wrong is a noun but not followed by the determinant
    if sentence[1]=='wrong' and request=='thing':
        analysis.sn=[Nominal_Group([],[],['wrong'],[],[])]
        sentence=[sentence[0]]+sentence[2:]
    
    #In this case we have an imperative sentence
    elif analyse_nominal_group.find_sn_pos(sentence, 1)==[] and type!='w_question':
        #We have to reput the 'not'
        if vg.state=='negative':
            sentence=sentence[:1]+['not']+sentence[1:]
        return other_sentence(type, request, sentence)

    #We delete the auxiliary
    sentence=sentence[1:]
    
    #We recover the subject
    sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 0)
    
    #If there is one element => it is an auxiliary => verb 'be'
    if len(sentence)==0:
        vg.vrb_tense = analyse_verb.find_tense_statement(aux)
        vg.vrb_main=['be']
    else:
        sentence=analyse_verbal_structure.find_vrb_adv (sentence, vg)
        vg.vrb_tense = analyse_verb.find_tense_question(sentence, aux)

        #We process the verb
        verb=analyse_verb.find_verb_question(sentence, aux, vg.vrb_tense)
        verb_main=analyse_verb.return_verb(sentence, verb, vg.vrb_tense)
        vg.vrb_main=[other_functions.convert_to_string(verb_main)]
        
        #We delete the verb if the aux is not the verb 'be'
        if vg.vrb_main!=['be']:
            sentence= sentence[sentence.index(verb[0])+len(verb_main):]
        elif sentence[0]=='be':
            sentence=sentence[1:]
        
        #Here we have special processing for different cases
        if sentence!=[]:
            #For 'what' descrition case
            if sentence[0]=='like' and aux!='would':
                vg.vrb_main=['like']
                sentence=sentence[1:]

            #For 'how' questions with often
            elif sentence[0].endswith('ing'):
                vg.vrb_main[0]=vg.vrb_main[0]+'+'+sentence[0]
                sentence=sentence[1:]
        
        #We recover the conjunctive subsentence
        sentence=analyse_verbal_structure.process_conjunctive_sub(sentence, vg)
        
        #It verifies if there is a secondary verb
        sec_vrb=analyse_verbal_structure.find_scd_vrb(sentence)
        if sec_vrb!=[]:
            sentence=analyse_verbal_structure.process_scd_sentence(sentence, vg, sec_vrb)
            
        #We recover the subsentence
        sentence=analyse_verbal_structure.process_subsentence(sentence, vg)
        
        #Process relative changes
        sentence=analyse_verbal_structure.correct_i_compl(sentence,vg.vrb_main[0])
        
        sentence=analyse_nominal_group.find_plural(sentence)
        #We recover the direct, indirect complement and the adverbial
        sentence=analyse_verbal_structure.recover_obj_iobj(sentence, vg)
        
        #We have to take off adverbs form the sentence
        sentence=analyse_verbal_structure.find_adv(sentence, vg)

    #We perform the processing with the modal
    if modal!=[]:
        vg.vrb_main=[modal+'+'+vg.vrb_main[0]]
    
    #If there is a forgotten
    sentence=analyse_verbal_structure.find_vrb_adv (sentence, vg)
    
    #In case there is a state verb followed by an adjective
    sentence=analyse_verbal_structure.state_adjective(sentence, vg)
    
    vg=analyse_verbal_structure.DOC_to_IOC(vg)

    while len(sentence)>1:
        stc=analyse_verbal_structure.add_it(sentence,request)
        #We recover the direct, indirect complement and the adverbial
        stc=analyse_verbal_structure.recover_obj_iobj(stc, vg)
        if stc==sentence:
            break
        else:
            sentence=stc
    
    vg=analyse_verbal_structure.refine_indirect_complement(vg)
    vg=analyse_verbal_structure.refine_subsentence(vg)
    
    analysis.sv=[vg]
    return analysis



def other_sentence(type, request, sentence):
    """
    This function process the other from of a sentence                                
    Input=type and requesting of sentence and the sentence                               
    Output=class Sentence                                                            
    """

    #init
    vg=Verbal_Group([], [],'', [], [], [], [] ,'affirmative',[])
    analysis=Sentence(type, request, [], [])
    modal=[]
    
    if sentence==[]:
        return []
    
    #We have to add punctuation if there is not
    if sentence[len(sentence)-1]!='.' and sentence[len(sentence)-1]!='?' and sentence[len(sentence)-1]!='!':
        sentence=sentence+['.']
        
    #We start with determination of probably second verb in subsentence
    sentence=other_functions.find_scd_verb_sub(sentence)
    
    #We search the subject
    sbj=analyse_nominal_group.find_sn_pos(sentence, 0)
    if sbj!=[] or type=='relative' :
        #If we haven't a data type => it is a statement
        if type=='':
            analysis.data_type='statement'

        
        #We have to separate the case using these, this or there
        for p in det_dem_list:
            
            if p==sentence[0] and analyse_verb.infinitive([sentence[1]], 'present simple')==['be']:
                #We recover this information and remove it
                analysis.sn=[Nominal_Group([p],[],[],[],[])]
                if p=='there' and sentence[1]=='are':
                    analysis.sn[0]._quantifier='SOME'
                sentence=sentence[1:]
        
        if analysis.sn==[]:
            #We recover the subject
            sentence=analyse_nominal_structure.recover_ns(sentence, analysis, 0)
        
        if sentence!=[]:
            #We have to know if there is a modal
            for m in modal_list:
                if sentence[0]==m:
                    modal=sentence[0]
                    if modal=='can' or modal=='must' or modal=='shall' or modal=='may':
                        sentence=sentence[1:]
                    
            #We must take into account all possible cases to recover the sentence's tense
            if len(sentence)>1 and sentence[1]=='not':
                vg.state='negative'
    
                #Before the negative form we have an auxiliary for the negation
                if sentence[0]=='do' or sentence[0]=='does' or sentence[0]=='did' :
                    vg.vrb_tense = analyse_verb.find_tense_statement([sentence[0]])
                    sentence=sentence[2:]
                    sentence=analyse_verbal_structure.find_vrb_adv (sentence,vg)
                
                #There is a modal
                elif modal!=[]:
                    sentence=[sentence[0]]+sentence[2:]
                    sentence=analyse_verbal_structure.find_vrb_adv (sentence,vg)
                    vg.vrb_tense = analyse_verb.find_tense_statement(sentence)
    
                else:
                    #We remove 'not' and find the tense
                    sentence=sentence[:1]+ sentence[2:]
                    sentence=analyse_verbal_structure.find_vrb_adv (sentence,vg)
                    vg.vrb_tense = analyse_verb.find_tense_statement(sentence)
                
            #For the affirmative processing
            else:
                if sentence[0]=='not':
                    vg.state='negative'
                    sentence=sentence[1:]
                    
                sentence=analyse_verbal_structure.find_vrb_adv (sentence,vg)
                vg.vrb_tense = analyse_verb.find_tense_statement(sentence)
            
            verb=analyse_verb.find_verb_statement(sentence, vg.vrb_tense)
            verb_main=analyse_verb.return_verb(sentence, verb, vg.vrb_tense)
            vg.vrb_main=[other_functions.convert_to_string(verb_main)]
            
            #We delete the verb
            sentence= sentence[sentence.index(verb[0])+len(verb_main):]
                
            #We perform the processing with the modal
            if modal!=[]:
                vg.vrb_main=[modal+'+'+vg.vrb_main[0]]

    #This is a imperative form
    else:
        #re-init
        analysis.data_type='imperative'
        vg.vrb_tense='present simple'

        #Negative form
        if sentence[1]=='not':
            sentence=sentence[sentence.index('not')+1:]
            sentence=analyse_verbal_structure.find_vrb_adv (sentence,vg)
            vg.state='negative'
        else:
            sentence=analyse_verbal_structure.find_vrb_adv (sentence,vg)

        #We process the verb
        verb=[sentence[0]]
        vg.vrb_main=[other_functions.convert_to_string(analyse_verb.return_verb(sentence, verb, vg.vrb_tense))]
        
        #We delete the verb
        sentence= sentence[sentence.index(verb[0])+len(verb):]
    
    #We recover the conjunctive subsentence
    sentence=analyse_verbal_structure.process_conjunctive_sub(sentence, vg)
    
    #It verifies if there is a secondary verb
    sec_vrb=analyse_verbal_structure.find_scd_vrb(sentence)
    if sec_vrb!=[]:
        sentence=analyse_verbal_structure.process_scd_sentence(sentence, vg, sec_vrb)
    
    #We recover the subsentence
    sentence=analyse_verbal_structure.process_subsentence(sentence, vg)
    
    if sentence!=[] and vg.vrb_main!=[]:
        #Process relative changes
        sentence=analyse_verbal_structure.correct_i_compl(sentence,vg.vrb_main[0])
    
    sentence=analyse_nominal_group.find_plural(sentence) 
    #We recover the direct, indirect complement and the adverbial
    sentence=analyse_verbal_structure.recover_obj_iobj(sentence, vg)
    
    #We have to take off abverbs form the sentence
    sentence=analyse_verbal_structure.find_adv(sentence, vg)
    
    #In case there is a state verb followed by an adjective
    sentence=analyse_verbal_structure.state_adjective(sentence, vg)
    
    #If there is a forgotten
    sentence=analyse_verbal_structure.find_vrb_adv (sentence, vg)
    
    vg=analyse_verbal_structure.DOC_to_IOC(vg)
    
    while len(sentence)>1:
        stc=analyse_verbal_structure.add_it(sentence,request)
        #We recover the direct, indirect complement and the adverbial
        stc=analyse_verbal_structure.recover_obj_iobj(stc, vg)
        if stc==sentence:
            break
        else:
            sentence=stc
    
    vg=analyse_verbal_structure.refine_indirect_complement(vg)
    vg=analyse_verbal_structure.refine_subsentence(vg)
    
    analysis.sv=[vg]
    return analysis



def sentences_analyzer(sentences):
    """
    This function is the basic function of parsing                                   
    Input=list of sentences and beginning sentence list                              
    Output=list of class Sentence                                                    
    """

    #init
    class_sentence_list=[]
    nom_gr=[]
    y=0

    #We process all sentences of the list
    for i in sentences:
        
        #We have to add punctuation if there is not
        if i[len(i)-1]!='.' and i[len(i)-1]!='?' and i[len(i)-1]!='!':
            i=i+['.']
        
        class_sentence_list=class_sentence_list+dispatching(i)
    
    #Add some information if there is an interjection
    while y < len(class_sentence_list):
        #If there is an interjection we have to take the nominal group
        if class_sentence_list[y].data_type=='interjection':
            nom_gr=class_sentence_list[y].sn
        #If there is an imperative sentence, we put the nominal group of interjection in the subject
        if nom_gr!=[] and class_sentence_list[y].data_type=='imperative':
            class_sentence_list[y].sn=class_sentence_list[y].sn+nom_gr
        y=y+1
    
    #To simplify the interpretation, we have to perform some changes
    for k in class_sentence_list:
        if k.sn!=[] and k.sn[0].det==['there']:
            k.sn=k.sv[0].d_obj
            k.sv[0].d_obj=[]
        
    return class_sentence_list

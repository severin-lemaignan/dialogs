#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN:rev202 + PythonTidy


"""
 Created by Chouayakh Mahdi                                                       
 21/06/2010                                                                       
 The package contains functions that affect verbal structure                      
 Functions:                                                                       
    find_vrb_adv : to recover the list of adverbs bound to verb                   
    find_adv : to recover the list of adverbs                                     
    check_proposal : to know if there is a proposal before the object             
    recover_obj_iobj : to find the direct, indirect object and the adverbial 
    state_adjective : to process adjectives after state verb     
    find_scd_vrb : to recover the second verb in a sentence                       
    process_scd_sentence : to process the second sentence found
    process_subsentence : to process the subsentence
    correct_i_compl : to transform indirect complement to relative
    DOC_to_IOC : to put the direct complement in the indirect
"""
from sentence import *
import analyse_nominal_group
import analyse_nominal_structure
import other_functions
import analyse_verb
import analyse_sentence


"""
Statement of lists
"""
aux_list=['have', 'has', 'had', 'is', 'are', 'am', 'was', 'were', 'will']
adv_list=['here','tonight', 'yesterday', 'tomorrow', 'today', 'now']
proposal_list=['in', 'on', 'at', 'from', 'to', 'about', 'for', 'next', 'last', 'ago', 'with', 'by', 'behind','behind+to','next+to','in+front+of','as', 'into']
rel_list=['which', 'who','that']
sub_list=['while', 'but','where', 'when', 'if']
pronoun_list=['you', 'I', 'we', 'he', 'she', 'me', 'it', 'he', 'they', 'yours', 'mine', 'him']
direct_trans_verb_list=['give', 'want', 'talk', 'say', 'mean']
adverbial_list=['in', 'on', 'at', 'from', 'for', 'next', 'last', 'behind','behind+to','next+to','in+front+of', 'into']
complement_pronoun=['me','you','it']
inderect_trans_verb_list=['tell', 'say']



def find_vrb_adv(phrase):
    """
    This function recovers the list of adverbs bound to verb                         
    Input=sentence                        Output=verb's adverb list                  
    """

    #If phrase is empty
    if phrase==[]:
        return []

    #If there is an auxiliary
    for i in aux_list:
        if i == phrase[0]:
            if phrase[1].endswith('ly'):
                return [phrase[1]]

    else:
        if phrase[0].endswith('ly'):
            return [phrase[0]]

    return []



def find_adv(phrase,vg):
    """
    This function recovers the list of adverbs                                       
    Input=sentence                            Output=adverbs list                    
    """

    #If phrase is empty
    if phrase ==[]:
        vg.advrb= []

    #init
    i=0
    
    #If the adverb is in the list
    while i < len(phrase):
        for j in adv_list:
            if j==phrase[i]:
                vg.advrb=[j]
                phrase=phrase[:i]+phrase[i+1:]
                phrase=find_adv(phrase,vg)
                
        #Using a rule of grammar
        if phrase[i].startswith('every'):
            vg.advrb= [phrase[i]]
            phrase=phrase[:i]+phrase[i+1:]
            phrase=find_adv(phrase,vg)
        
        i=i+1

    return phrase



def check_proposal(phrase, object):
    """
    This function to know if there is a proposal before the object                   
    Input=sentence and object            Output=proposal if the object is indirect   
    """

    if object==[]:
        return []

    #si on a une preposition on renvoie l'objet
    for i in proposal_list:
        if object!=phrase[0:len(object)] and i==phrase[phrase.index(object[0])-1]:
            return [i]

    #Default case
    return []



def recover_obj_iobj(phrase, vg):
    """
    This function finds the direct, indirect object and the adverbial                
    We, also, put these information in the class                                     
    Input=sentence and verbal class              Output=sentence and verbal class    
    """
    
    #init
    conjunction='AND'
   
    #We search the first nominal group in sentence
    object= analyse_nominal_group.find_sn(phrase)
   
    while object!=[]:

        #If it is not a direct object => there is a proposal
        proposal=check_proposal(phrase, object)
       
        if proposal!=[]:

            gr_nom_list=[]
            #This 'while' is for duplicate with 'and'
            while object!=[]:
                pos_object=phrase.index(object[0])
                
                #We refine the nominal group if there is an error like ending with question mark
                object=analyse_nominal_group.refine_nom_gr(object)
        
                #Recovering nominal group
                gr_nom_list=gr_nom_list+[analyse_nominal_structure.fill_nom_gr(phrase, object, pos_object,conjunction)]
                
                #We take off the nominal group
                phrase=analyse_nominal_group.take_off_nom_gr(phrase, object,pos_object)
                #We will take off the proposal
                phrase=phrase[:phrase.index(proposal[0])]+phrase[phrase.index(proposal[0])+1:]

                #If there is a relative
                begin_pos_rel=analyse_nominal_group.find_relative(object, phrase, pos_object,rel_list)
                
                if begin_pos_rel!=-1:
                    end_pos_rel=other_functions.recover_end_pos_sub(phrase, rel_list)
                    #We remove the relative part of the phrase
                    phrase=phrase[:begin_pos_rel]+phrase[end_pos_rel:]
                
                #If there is 'and', we need to duplicate the information
                if len(phrase)!=0 and (phrase[0]=='and' or phrase[0]=='or' or phrase[0]==':but'):
                    
                    object=analyse_nominal_group.find_sn_pos(phrase[1:], 0)
                    
                    #We process the 'or' like the 'and' and remove it
                    if phrase[0]=='or':
                        conjunction='OR'
                    elif phrase[0]==':but':
                        conjunction='BUT'
                    else:
                        conjunction='AND'
                    phrase=phrase[1:]
                
                else:
                    object=[]

            vg.i_cmpl=vg.i_cmpl+[Indirect_Complement(proposal,gr_nom_list)]


        else:
            #It is a direct complement
            gr_nom_list=[]
            #It reproduces the same code as above
            while object!=[]:
                pos_object=phrase.index(object[0])
                
                #We refine the nominal group if there is an error like ending with question mark
                object=analyse_nominal_group.refine_nom_gr(object)
                
                #Recovering nominal group
                gr_nom_list=gr_nom_list+[analyse_nominal_structure.fill_nom_gr(phrase, object, pos_object, conjunction)]
                
                #We take off the nominal group
                phrase=analyse_nominal_group.take_off_nom_gr(phrase, object, pos_object)
                
                #If there is a relative
                begin_pos_rel=analyse_nominal_group.find_relative(object, phrase, pos_object,rel_list)
                
                if begin_pos_rel!=-1:
                    end_pos_rel=other_functions.recover_end_pos_sub(phrase, rel_list)
                    #We remove the relative part of the phrase
                    phrase=phrase[:begin_pos_rel]+phrase[end_pos_rel:]
                    
                if len(phrase)!=0 and (phrase[0]=='and' or phrase[0]=='or' or phrase[0]==':but'):
                    
                    object=analyse_nominal_group.find_sn_pos(phrase[1:], 0)
                    
                    #We process the 'or' like the 'and' and remove it
                    if phrase[0]=='or':
                        conjunction='OR'
                    elif phrase[0]==':but':
                        conjunction='BUT'
                    else:
                        conjunction='AND'
                    phrase=phrase[1:]
                    
                else:
                    object=[]
            
            #If there is a second verb there is no direct complement
            if vg.sv_sec!=[]:
                vg.i_cmpl=vg.i_cmpl+[Indirect_Complement([],gr_nom_list)]
            
            #In a sentence there is just one direct complement if there is no second verb
            elif vg.d_obj==[]:
                vg.d_obj=gr_nom_list
            else:
                #Else the first nominal group found is indirect and this one is direct complement
                vg.i_cmpl=vg.i_cmpl+[Indirect_Complement([],vg.d_obj)]
                vg.d_obj=gr_nom_list

        object= analyse_nominal_group.find_sn(phrase)

    return phrase



def state_adjective(sentence, vg):
    """
    This function process adjectives after state verb                             
    Input=sentence                        Output=second verb of the sentence         
    """
    
    #In case there is a state verb followed by an adjective
    if sentence!=[] and vg.vrb_main[0]=='be' and analyse_nominal_group.adjective_pos(sentence,0)-1!=0:
        pos=analyse_nominal_group.adjective_pos(sentence,0)
        vg.d_obj=[Nominal_Group([],[],sentence[:pos-1],[],[])]
        sentence=sentence[pos-1:]
        while sentence[0]=='or' or sentence[0]==':but':
            if sentence[0]=='or':
                conjunction='OR'
            elif sentence[0]==':but':
                conjunction='BUT'
            sentence=sentence[1:]
            pos=analyse_nominal_group.adjective_pos(sentence,0)
            vg.d_obj=vg.d_obj+[Nominal_Group([],[],sentence[:pos-1],[],[])]
            vg.d_obj[len(vg.d_obj)-1]._conjunction=conjunction
            sentence=sentence[pos-1:]
    return sentence
    
    
    
def find_scd_vrb(phrase):
    """
    This function recovers the second verb in a sentence                             
    Input=sentence                        Output=second verb of the sentence         
    """
    
    for i in phrase:

        #If there is 'to'
        if i=='to':

            #It should not be followed by a noun or by an adverb
            if analyse_nominal_group.find_sn_pos(phrase, phrase.index(i)+1)==[]:

                #If there is a proposal after 'to'
                for j in proposal_list:
                    if j == phrase[phrase.index(i)+1]:
                        return []

                return [phrase[phrase.index(i)+1]]
    
    return []



def process_scd_sentence(phrase, vg, sec_vrb):
    """
    This function process the second sentence found                                   
    Input=sentence, verbal class and the second verb                                 
    Output=sentence and verbal class                                                 
    """

    #We take off the part of the sentence after 'to'
    scd_sentence=phrase[phrase.index(sec_vrb[0]):]
    phrase=phrase[:phrase.index(sec_vrb[0])]
    
    #We process the verb
    if scd_sentence[0]=='not':
        scd_verb=[other_functions.convert_to_string(analyse_verb.return_verb(scd_sentence, [scd_sentence[1]], ''))]
        vg.sv_sec=vg.sv_sec+[Verbal_Group(scd_verb, [], '', [], [], [], [], 'negative',[])]
        #We delete the verb
        scd_sentence= scd_sentence[phrase.index(scd_sentence[1])+1:]
    else:
        scd_verb=[other_functions.convert_to_string(analyse_verb.return_verb(scd_sentence, [scd_sentence[0]], ''))]
        vg.sv_sec=vg.sv_sec+[Verbal_Group(scd_verb, [], '', [], [], [], [], 'affirmative',[])]
        #We delete the verb
        scd_sentence= scd_sentence[scd_sentence.index(scd_sentence[0])+1:]

    #We recover the conjunctive subsentence
    scd_sentence=process_conjunctive_sub(scd_sentence, vg.sv_sec[0])
    
    #It verifies if there is a secondary verb
    sec_sec_vrb=find_scd_vrb(scd_sentence)
    if sec_sec_vrb!=[]:
        scd_sentence=process_scd_sentence(scd_sentence, vg.sv_sec, sec_sec_vrb)
    
    #We recover the subsentence
    scd_sentence=process_subsentence(scd_sentence, vg)
    
    #Process relative changes
    scd_sentence=correct_i_compl(scd_sentence,scd_verb)
    
    #We process the end of the second sentence
    scd_sentence=find_adv(scd_sentence,vg.sv_sec[0])
    scd_sentence=recover_obj_iobj(scd_sentence, vg.sv_sec[0])

    return phrase



def process_subsentence(phrase,vg):
    """
    This function process the subsentence                                             
    Input=sentence and verbal class         Output=sentence and verbal class         
    """
    
    #init
    begin_pos=-1

    #If phrase is empty
    if len(phrase)<0:
        return phrase

    #We look down the list to see if there is a subsentence
    for w in sub_list:
        for i in phrase:
            if i == w:
                begin_pos=phrase.index(i)

                #We include the relative's proposal if there are relatives in the subsentence
                end_pos= other_functions.recover_end_pos_sub(phrase[begin_pos:], sub_list+rel_list)

                #We have to remove the proposal
                subsentence= phrase[begin_pos+1:end_pos]
                
                #We perform processing
                vg.vrb_sub_sentence=vg.vrb_sub_sentence+[analyse_sentence.other_sentence('subsentence', w ,subsentence)]
            
                #We delete the subsentence
                phrase=phrase[:phrase.index(i)]
                phrase=phrase+phrase[end_pos:]+['.']
                
                return phrase

    return phrase



def process_conjunctive_sub(phrase,vg):
    """
    This function process the conjunctive subsentence
    Input=sentence and verbal class         Output=sentence and verbal class         
    """
    
    #init
    begin_pos=-1
    
    #We will find conjunctive subsentence if there is
    if len(phrase)>0 and phrase[0]=='that' and analyse_nominal_group.find_sn_pos(phrase, 1)!=[]:
        begin_pos=0
        
    for i in pronoun_list:
        if len(phrase)>2 and i==phrase[0] and phrase[1]=='that' and analyse_nominal_group.find_sn_pos(phrase, 2)!=[]:
            begin_pos=1
        
    
    if begin_pos!=-1:
        #We include the relative's and subsentence's proposal if there are relatives or subsentences in this subsentence
        end_pos= other_functions.recover_end_pos_sub(phrase[begin_pos:], ['that']+sub_list+rel_list)
        
        #We have to remove the proposal
        subsentence= phrase[begin_pos+1:end_pos]
        
        #We perform processing
        vg.vrb_sub_sentence=vg.vrb_sub_sentence+[analyse_sentence.other_sentence('subsentence', 'that' ,subsentence)]
        
        
        #We delete the subsentence
        phrase=phrase[:phrase.index('that')]
        phrase=phrase+phrase[end_pos:]+['.']
                
    return phrase



def correct_i_compl(phrase,verb):
    """
    This function transform indirect complement to relative
    Input=sentence and verbal class         Output=sentence and verbal class         
    """
    
    for i in direct_trans_verb_list:
        #If we have a direct transitive verb
        if i==verb:
        
            #init
            x=0
            while x<len(phrase):
                for y in adverbial_list:

                    #If there is a proposal with an adverbial
                    if x+1<len(phrase)-1 and phrase[x]==y and analyse_nominal_group.find_sn_pos(phrase, x+1)!=[]:
                        adverbial=analyse_nominal_group.find_sn_pos(phrase, x+1)
                        begin_pos=x-1
                        
                        #We will find the subject of the relative
                        while analyse_nominal_group.find_sn_pos(phrase, begin_pos)==[]:
                            begin_pos=begin_pos-1
                        nom_gr=analyse_nominal_group.find_sn_pos(phrase, begin_pos)
                        
                        #If there nominal group is just before the adverbial
                        if begin_pos+len(nom_gr)==x:
                            phrase=phrase[:x]+['which','is']+[phrase[x]]+adverbial+[';']+phrase[x+len(adverbial)+1:]
                            break
                x=x+1
    return phrase



def DOC_to_IOC(vg):
    """
    This function put the direct complement in the indirect
    Input=sentence and verbal class         Output=sentence and verbal class         
    """
    
    for x in inderect_trans_verb_list:
        if vg.vrb_main!=[] and x==vg.vrb_main[0]:
            for j in complement_pronoun:
                #In this case we have just one direct compelment
                if vg.d_obj[0].noun[0]==j:
                    vg.i_cmpl=vg.i_cmpl+[Indirect_Complement([],vg.d_obj)]
                    vg.d_obj=[]
                    return vg
    return vg

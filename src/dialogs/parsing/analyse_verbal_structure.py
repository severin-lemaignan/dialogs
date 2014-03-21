#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN:rev202 + PythonTidy


"""
 Created by Chouayakh Mahdi                                                       
 21/06/2010                                                                       
 The package contains functions that affect verbal structure                      
 Functions:                                  
    is_cmpl_pr : to return 1 if it is pronoun else 0 
    delete_unusable_word : to delete the word that is no parssable 
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
    create_nom_gr_and : to add determinant after 'and' if there is
    create_nom_gr : to add it or a determinant if it is necessary
    refine_indirect_complement : to put indirect complements with same proposal together
    refine_subsentence : to transform some subsentence to relative
    process_compare : to process the compare
    can_be_imperative : to return the possibility to have an imperative
"""
from dialogs.resources_manager import ResourcePool
from dialogs.sentence import *
import analyse_nominal_group
import analyse_nominal_structure
import other_functions
import analyse_verb
import analyse_sentence
import preprocessing

def is_cmpl_pr(word):
    """
    This function return 1 if it is pronoun else 0                         
    Input=word                 Output=1 or 0                 
    """
    
    if word in ResourcePool().complement_pronouns:
        return 1
    return 0



def delete_unusable_word(phrase):
    """
    deletes the word that is no parssable                        
    Input=sentence                        Output=sentence                 
    """
    
    for i in ResourcePool().unusable_words:
        if phrase[0]==i:
            phrase=phrase[1:]
            delete_unusable_word(phrase) 
    return phrase
    
    
    
def find_vrb_adv(phrase, vg):
    """
    recovers the list of adverbs bound to verb                         
    Input=sentence                        Output=sentence                 
    """

    #If phrase is empty
    if not phrase:
        return phrase

    #If there is an auxiliary
    if phrase[0] in ResourcePool().auxiliary:
        if phrase[1].endswith('ly'):
            vg.vrb_adv=vg.vrb_adv+[phrase[1]]
            return [phrase[0]]+phrase[2:]
    else:
        #Using a rule of grammar
        if phrase[0].endswith('ly'):
            vg.vrb_adv=vg.vrb_adv+[phrase[0]]
            return phrase[1:]

    return phrase



def find_adv(phrase,vg):
    """
    recovers the list of adverbs                                       
    Input=sentence                            Output=adverbs list                    
    """

    #If phrase is empty
    if not phrase:
        vg.advrb= []

    #init
    i=0
    
    #If the adverb is in the list
    while i < len(phrase):
        
        #Using a rule of grammar
        if phrase[i].startswith('every'):
            vg.advrb= vg.advrb+[phrase[i]]
            phrase=phrase[:i]+phrase[i+1:]
            
        if phrase[i] in ResourcePool().adverbs:
            if i>0 and phrase[i-1] in ResourcePool().proposals:
                vg.i_cmpl=vg.i_cmpl+[Indirect_Complement([phrase[i-1]],[Nominal_Group([],[phrase[i]],[],[],[])])]
                phrase=phrase[:i-1]+phrase[i+1:]
            else:
                vg.advrb=vg.advrb+[phrase[i]]
                phrase=phrase[:i]+phrase[i+1:]

        i += 1
    return phrase



def check_proposal(phrase, object):
    """
    know if there is a proposal before the object                   
    Input=sentence and object            Output=proposal if the object is indirect   
    """

    if not object:
        return []

    #if there is a proposal which recovery an object
    if object!=phrase[0:len(object)] and phrase[phrase.index(object[0])-1] in ResourcePool().proposals:
        return [phrase[phrase.index(object[0])-1]]

    #Default case
    return []



def recover_obj_iobj(phrase, vg):
    """
    finds the direct, indirect object and the adverbial                
    We, also, put these information in the class                                     
    Input=sentence and verbal class              Output=sentence and verbal class    
    """
    
    #init
    conjunction='AND'
   
    object= analyse_nominal_group.find_sn(phrase)

    if phrase and \
       not object and \
       phrase[0] in ResourcePool().adverbs_at_end:
           vg.advrb= [phrase[0]]

    while object:

        #If it is not a direct object => there is a proposal
        proposal=check_proposal(phrase, object)
        
        
        if proposal:
            
            gr_nom_list=[]
            #This 'while' is for duplicate with 'and'
            while object:
                pos_object=phrase.index(object[0])
                
                #We refine the nominal group if there is an error like ending with question mark
                object=analyse_nominal_group.refine_nom_gr(object)
        
                #Recovering nominal group
                gr_nom_list=gr_nom_list+[analyse_nominal_structure.fill_nom_gr(phrase, object, pos_object,conjunction)]
                
                #We take off the nominal group
                phrase=analyse_nominal_group.take_off_nom_gr(phrase, object,pos_object)
                #We will take off the proposal
                phrase=phrase[:phrase.index(proposal[0])]+phrase[phrase.index(proposal[0])+1:]
                conjunction='AND'
                
                #If there is a relative
                begin_pos_rel=analyse_nominal_group.find_relative(object, phrase, pos_object,ResourcePool().relatives)
                
                if begin_pos_rel!=-1:
                    end_pos_rel=other_functions.recover_end_pos_sub(phrase, ResourcePool().relatives)
                    #We remove the relative part of the phrase
                    phrase=phrase[:begin_pos_rel]+phrase[end_pos_rel:]
                
                #If there is 'and', we need to duplicate the information with the proposal if there is
                if len(phrase)!=0 and (phrase[0]=='and' or phrase[0]=='or' or phrase[0]==':but'):
                    
                    phrase=[phrase[0]]+analyse_nominal_group.find_plural(phrase[1:])
                    
                    #We have not duplicate the proposal, it depends on the presence of the nominal group after  
                    if analyse_nominal_group.find_sn_pos(phrase, 1):
                        phrase=[phrase[0]]+proposal+phrase[1:]
                    else:   
                        phrase=[phrase[0]]+phrase[1:]
                    
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
            while object:
                pos_object=phrase.index(object[0])
                
                #We refine the nominal group if there is an error like ending with question mark
                object=analyse_nominal_group.refine_nom_gr(object)
        
                #Recovering nominal group
                gr_nom_list=gr_nom_list+[analyse_nominal_structure.fill_nom_gr(phrase, object, pos_object, conjunction)]
        
                #We take off the nominal group
                phrase=analyse_nominal_group.take_off_nom_gr(phrase, object, pos_object)
                conjunction='AND'
                
                #If there is a relative
                begin_pos_rel=analyse_nominal_group.find_relative(object, phrase, pos_object,ResourcePool().relatives)
                
                if begin_pos_rel!=-1:
                    end_pos_rel=other_functions.recover_end_pos_sub(phrase, ResourcePool().relatives)
                    #We remove the relative part of the phrase
                    phrase=phrase[:begin_pos_rel]+phrase[end_pos_rel:]
                
                if len(phrase)!=0 and (phrase[0]=='and' or phrase[0]=='or' or phrase[0]==':but'):
                    
                    phrase=[phrase[0]]+analyse_nominal_group.find_plural(phrase[1:])
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
            
            #In a sentence there is just one direct complement if there is no second verb
            if not vg.d_obj:
                vg.d_obj=gr_nom_list
            else:
                #Else the first nominal group found is indirect and this one is direct complement
                vg.i_cmpl=vg.i_cmpl+[Indirect_Complement([],vg.d_obj)]
                vg.d_obj=gr_nom_list
        
        #If the last nominal group is followed by another one in plural form 
        phrase=analyse_nominal_group.find_plural(phrase)
        object= analyse_nominal_group.find_sn(phrase)
    
    return phrase



def state_adjective(sentence, vg):
    """
    This function process adjectives after state verb                             
    Input=sentence                        Output=second verb of the sentence         
    """
    
    #In case there is a state verb followed by an adjective
    if sentence:
        if vg.vrb_main[0] in ResourcePool().state and analyse_nominal_group.adjective_pos(sentence,0)-1!=0:
            
            #Here we have juist to process adjectives, nominal groups are processed
            pos=analyse_nominal_group.adjective_pos(sentence,0)
            adj_list=analyse_nominal_group.process_adj_quantifier(sentence[:pos-1])
            vg.d_obj=[Nominal_Group([],[],adj_list,[],[])]
            sentence=sentence[pos-1:]
            
            #Same as nominal groups but with adjectives
            conjunction = None
            while sentence[0]=='or' or sentence[0]==':but':
                if sentence[0]=='or':
                    conjunction='OR'
                elif sentence[0]==':but':
                    conjunction='BUT'
                sentence=sentence[1:]
                
                pos=analyse_nominal_group.adjective_pos(sentence,0)
                adj_list=analyse_nominal_group.process_adj_quantifier(sentence[:pos-1])
                #We put all adjectives in the direct complement
                vg.d_obj=vg.d_obj+[Nominal_Group([],[],adj_list,[],[])]
                vg.d_obj[len(vg.d_obj)-1]._conjunction = conjunction
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
            if not analyse_nominal_group.find_sn_pos(phrase, phrase.index(i) + 1):
                #If there is a proposal after 'to'
                if phrase[phrase.index(i)+1] in ResourcePool().proposals:
                    return []
                return [phrase[phrase.index(i)+1]]
    return []



def process_scd_sentence(phrase, vg, sec_vrb):
    """
    process the second sentence found                                   
    Input=sentence, verbal class and the second verb                                 
    Output=sentence and verbal class                                                 
    """
    
    #We take off the part of the sentence after 'to'
    scd_sentence=phrase[phrase.index(sec_vrb[0]):]
    phrase=phrase[:phrase.index(sec_vrb[0])]
    
    #We process the verb
    if scd_sentence[0]=='not':
        scd_verb=[other_functions.convert_to_string(analyse_verb.return_verb(scd_sentence, [scd_sentence[1]], ''))]
        vg.sv_sec=vg.sv_sec+[Verbal_Group(scd_verb, [], '', [], [], [], [], Verbal_Group.negative,[])]
        #We delete the verb
        scd_sentence= scd_sentence[phrase.index(scd_sentence[1])+1:]
    else:
        scd_verb=[other_functions.convert_to_string(analyse_verb.return_verb(scd_sentence, [scd_sentence[0]], ''))]
        vg.sv_sec=vg.sv_sec+[Verbal_Group(scd_verb, [], '', [], [], [], [], Verbal_Group.affirmative,[])]
        #We delete the verb
        scd_sentence= scd_sentence[scd_sentence.index(scd_sentence[0])+1:]
    
    #We recover the conjunctive subsentence
    scd_sentence=process_conjunctive_sub(scd_sentence, vg.sv_sec[0])
    
    #It verifies if there is a secondary verb
    sec_sec_vrb=find_scd_vrb(scd_sentence)
    if sec_sec_vrb:
        #print vg.sv_sec[0].sv_sec
        scd_sentence=process_scd_sentence(scd_sentence, vg.sv_sec[0], sec_sec_vrb)
    
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
    process the subsentence                                             
    Input=sentence and verbal class         Output=sentence and verbal class         
    """
    
    #init
    begin_pos=-1

    #If phrase is empty
    if len(phrase)<0:
        return phrase
    
    #We look down the list to see if there is a subsentence
    for w in ResourcePool().subsentences:
        if w in phrase:
                
            begin_pos=phrase.index(w)
                
            #We include the relative's proposal if there are relatives in the subsentence
            end_pos= other_functions.recover_end_pos_sub(phrase[begin_pos:], ResourcePool().subsentences+ResourcePool().relatives)
                
            #If it is 'where', it can be relative if before we have nominal group
            if w=='where' or w=='which':
                position=phrase.index(w)-1
                   
                gr=analyse_nominal_group.find_sn_pos(phrase, position)
                    
                #We have to find the nominal group just before
                while position>0 and gr==[]:
                    position -= 1
                    gr=analyse_nominal_group.find_sn_pos(phrase, position)
                #For exceptions, if the nominal group end with the proposal 
                if gr!=[] and gr[len(gr)-1]==w:
                    gr=gr[:len(gr)-1]
            
            #Else we return the sentence and we assume it as relative
            if (w!='where' and w!='which') or (len(gr)+position!=phrase.index(w) or (len(gr)==1 and is_cmpl_pr(gr[0])==1)):
                #We have to remove the proposal
                subsentence= phrase[begin_pos+1:begin_pos+end_pos]
                if len(subsentence)>1:
                    subsentence=other_functions.recover_scd_verb_sub(subsentence)
                        
                    if w!='which':
                        #We perform processing
                        vg.vrb_sub_sentence=vg.vrb_sub_sentence+analyse_sentence.dispatching(subsentence)
                        vg.vrb_sub_sentence[len(vg.vrb_sub_sentence)-1].data_type=SUBSENTENCE+'+'+vg.vrb_sub_sentence[len(vg.vrb_sub_sentence)-1].data_type
                        if w[0]==':':
                            vg.vrb_sub_sentence[len(vg.vrb_sub_sentence)-1].aim=w[1:]
                        else:
                            vg.vrb_sub_sentence[len(vg.vrb_sub_sentence)-1].aim=w
                    else:
                        #Exception for which
                        vg.vrb_sub_sentence=vg.vrb_sub_sentence+[analyse_sentence.w_quest_which(W_QUESTION, 'choice', ['the']+subsentence)]
                        vg.vrb_sub_sentence[len(vg.vrb_sub_sentence)-1].data_type=SUBSENTENCE+'+'+vg.vrb_sub_sentence[len(vg.vrb_sub_sentence)-1].data_type
                        vg.vrb_sub_sentence[len(vg.vrb_sub_sentence)-1].aim=w
                    
                    #If 'but' is between 2 nominal group and not before subsentence
                    if w=='but':
                        #If the main verb is not a verb but a part of verbal structure => we have nominal groups
                        for k in ['.','?','!',''] + ResourcePool().proposals:
                            if not vg.vrb_sub_sentence[len(vg.vrb_sub_sentence)-1].sv \
                                or \
                                vg.vrb_sub_sentence[len(vg.vrb_sub_sentence)-1].sv[0].vrb_main[0]==k:
                                    
                                #We make changes and return the sentence with but of nominal groups
                                phrase[phrase.index(w)]=':but'
                                vg.vrb_sub_sentence=vg.vrb_sub_sentence[:len(vg.vrb_sub_sentence)-1]
                                return phrase
                       
                    #We delete the subsentence
                    phrase=phrase[:begin_pos]+phrase[begin_pos+end_pos:]+['.']
                    return phrase
    return phrase



def process_conjunctive_sub(phrase,vg):
    """
    process the conjunctive subsentence
    Input=sentence and verbal class         Output=sentence and verbal class         
    """
    
    #init
    begin_pos=-1
    
    #We will find conjunctive subsentence if there is
    if len(phrase)>0 and phrase[0]=='that' and analyse_nominal_group.find_sn_pos(phrase, 1)!=[]:
        begin_pos=0
        
    if len(phrase)>2 and phrase[0] in ResourcePool().pronouns and phrase[1]=='that' and analyse_nominal_group.find_sn_pos(phrase, 2)!=[]:
        begin_pos=1
        
    
    if begin_pos!=-1:
        #We include the relative's and subsentence's proposal if there are relatives or subsentences in this subsentence
        phrase = [phrase[0]]+preprocessing.remerge_sentences(phrase[1:])
        end_pos= other_functions.recover_end_pos_sub(phrase[begin_pos:], ['that']+ResourcePool().subsentences+ResourcePool().relatives)
        
        #We have to remove the proposal
        subsentence= phrase[begin_pos+1:end_pos]
        subsentence=other_functions.recover_scd_verb_sub(subsentence)
        
        #We perform processing
        vg.vrb_sub_sentence=vg.vrb_sub_sentence+[analyse_sentence.other_sentence(SUBSENTENCE, 'that' ,subsentence)]
        vg.vrb_sub_sentence[len(vg.vrb_sub_sentence) - 1].data_type += '+statement'
        
        #We delete the subsentence
        phrase=phrase[:phrase.index('that')]
        phrase=phrase+phrase[end_pos:]+['.']
                
    return phrase



def correct_i_compl(phrase,verb):
    """
    transform indirect complement to relative
    Input=sentence and verbal class         Output=sentence and verbal class         
    """
    
    #If we have a direct transitive verb
    if verb in ResourcePool().direct_transitive:
            
        #init
        x=0
        while x<len(phrase):
            #If there is a proposal with an adverbial
            if x+1<len(phrase) and phrase[x] in ResourcePool().compelement_proposals:
                #If there is a plural
                phrase=phrase[:x]+analyse_nominal_group.find_plural(phrase[x:])
                        
                if analyse_nominal_group.find_sn_pos(phrase, x + 1):
                    adverbial=analyse_nominal_group.find_sn_pos(phrase, x+1)
                    begin_pos=x-1
                            
                    #We will find the subject of the relative
                    while not analyse_nominal_group.find_sn_pos(phrase, begin_pos):
                        begin_pos -= 1
                    nom_gr=analyse_nominal_group.find_sn_pos(phrase, begin_pos)
                            
                    #If there nominal group is just before the adverbial
                    if begin_pos+len(nom_gr)==x:
                        phrase=phrase[:x]+['which','is']+[phrase[x]]+adverbial+[';']+phrase[x+len(adverbial)+1:]
            x += 1
    return phrase



def DOC_to_IOC(vg):
    """
    puts the direct complement in the indirect
    Input=sentence and verbal class         Output=sentence and verbal class         
    """
    
    for x in ResourcePool().indirect_transitive:
        #The case of the verb only and his modal form
        if vg.vrb_main!=[] and (vg.vrb_main[0]==x or vg.vrb_main[0].endswith('+'+x)):
            #In this case we have just one direct complement
            if vg.d_obj:
                vg.i_cmpl=vg.i_cmpl+[Indirect_Complement([],vg.d_obj)]
                vg.d_obj=[]
                return vg
    return vg



def create_nom_gr_and(sentence):
    """ 
    adds determinant after 'and' if there is                 
    Input=sentence                                  Output=sentence                      
    """ 
    #init
    i=0
    
    while i < len(sentence):
        #If we have a nominal group
        nom_gr=analyse_nominal_group.find_sn_pos(sentence, i)
        i += len(nom_gr)
    
        while nom_gr!=[] and i < len(sentence) and (sentence[i]=='and' or sentence[i]==';'):
            #If we have 'and'
            if sentence[i]==';':
                sentence[i]='and'
            #We add the determinant
            sentence=sentence[:i+1]+['a']+sentence[i+1:]
            i += 1
            #We continue
            nom_gr=analyse_nominal_group.find_sn_pos(sentence, i)
            i += len(nom_gr)
        i += 1

    return sentence



def create_nom_gr(sentence,aim):
    """
    adds it or a determinant if it is necessary
    Input=sentence                         Output=sentence       
    """
    
    if sentence[0]=='.' or sentence[0]=='?' or sentence[0]=='!' or sentence[0]==';':
        return sentence[1:] 
    
    #We delete word that we don't use
    if sentence[0] in ResourcePool().unusable_words:
        return sentence[1:] 
    
    #Some word linked to the questions
    if sentence[0]=='from' and aim=='origin':
        return sentence[1:]
    
    #If we have a proposal
    if sentence[0] in ResourcePool().proposals:
        if sentence[1]!='.' and sentence[1]!='?' and sentence[1]!='!' and sentence[1]!=';':
            #We add a determinant
            sentence = [sentence[0]]+['a']+sentence[1:]
            sentence = [sentence[0]]+ create_nom_gr_and(sentence[1:])
        else:
            #If we have a punctuation we add 'it', except if we
            # recognize it as an adverb.
            if sentence[0] in ResourcePool().adverbs_at_end:
                pass
            else:
                return [sentence[0]]+['it']+sentence[1:]
    else:
        #Default case : we add object
        sentence = ['a']+sentence
        sentence = create_nom_gr_and(sentence)
    
    return sentence



def refine_indirect_complement(vg):
    """
    This function put indirect complements with same proposal together
    Input=verbal structure                         Output=verbal structure        
    """
    
    #init
    i=0
    
    while i < len(vg.i_cmpl):
        j=i+1
        if vg.i_cmpl[i].prep:
            while j < len(vg.i_cmpl):
                #If we have the same proposal, we concatenate them
                if vg.i_cmpl[j].prep!=[] and vg.i_cmpl[i].prep==vg.i_cmpl[j].prep:
                    vg.i_cmpl[i].gn=vg.i_cmpl[i].gn+vg.i_cmpl[j].gn
                    vg.i_cmpl=vg.i_cmpl[:j]+vg.i_cmpl[j+1:]
                else:
                    j += 1
        i += 1
    return vg    



def refine_subsentence(vg):
    """
    transform some subsentence to relative
    Input=verbal structure                         Output=verbal structure        
    """
    
    #init
    i=0
    
    while i < len(vg.vrb_sub_sentence):
        
        if vg.vrb_sub_sentence[i].aim=='what':
            #We have to make some changers
            vg.vrb_sub_sentence[i].aim='that'
            vg.vrb_sub_sentence[i].data_type=RELATIVE
            #We add nominal group in relative as direct object
            vg.vrb_sub_sentence[i].sv[0].d_obj=vg.vrb_sub_sentence[i].sv[0].d_obj+[Nominal_Group(['the'],['thing'],[],[],[])]
            #We create a nominal group
            gn=Nominal_Group(['the'],['thing'],[],[],[vg.vrb_sub_sentence[i]])
            vg.d_obj=vg.d_obj+[gn]
            #We delete the subsentence
            vg.vrb_sub_sentence=vg.vrb_sub_sentence[:i]+vg.vrb_sub_sentence[i+1:]
            i -= 1
            
        if i>=0 and vg.vrb_sub_sentence[i].aim=='where':
            #We have to make some changers
            vg.vrb_sub_sentence[i].data_type=RELATIVE
            #We create a nominal group
            gn=Nominal_Group(['the'],['location'],[],[],[vg.vrb_sub_sentence[i]])
            #We add the relative and the nominal group into the sentence
            vg.i_cmpl=vg.i_cmpl+[Indirect_Complement(['in'],[gn])]
            
            for l in ResourcePool().indirect_transitive:
                if l==vg.vrb_main[0]:
                    vg.i_cmpl[len(vg.i_cmpl)-1].prep=[]
                    break
                
            #We delete the subsentence
            vg.vrb_sub_sentence=vg.vrb_sub_sentence[:i]+vg.vrb_sub_sentence[i+1:]
            i -= 1

        i += 1
    return vg



def process_compare(sentence,vg):
    """
    process the compare
    Input=sentence and verbal structure      Output=sentence verbal structure        
    """
    
    #init
    i=0
    conjunction='AND'
    gr_nom_list=[]
    
    while i<len(sentence):
        #We will find 'than'
        if sentence[i]=='than':
            compare={'nom_gr':[],'object':''}
            
            object= analyse_nominal_group.find_sn_pos(sentence, i+1)
            #It reproduces the same code as above
            while object:
                #We refine the nominal group if there is an error like ending with question mark
                object=analyse_nominal_group.refine_nom_gr(object)
                #Recovering nominal group
                gr_nom_list=gr_nom_list+[analyse_nominal_structure.fill_nom_gr(sentence, object, i+1, conjunction)]
                #We take off the nominal group
                sentence=analyse_nominal_group.take_off_nom_gr(sentence, object, i+1)
                conjunction='AND'
                #If there is a relative
                begin_pos_rel=analyse_nominal_group.find_relative(object, sentence, i+1,ResourcePool().relatives)
                if begin_pos_rel!=-1:
                    end_pos_rel=other_functions.recover_end_pos_sub(sentence, ResourcePool().relatives)
                    #We remove the relative part of the sentence
                    sentence=sentence[:begin_pos_rel]+sentence[end_pos_rel:]
                if len(sentence)!=i+1 and (sentence[i+1]=='and' or sentence[i+1]=='or' or sentence[i+1]==':but'):
                    sentence=[sentence[i+1]]+analyse_nominal_group.find_plural(sentence[1:])
                    object=analyse_nominal_group.find_sn_pos(sentence[i+2:], i+1)
                    #We process the 'or' like the 'and' and remove it
                    if sentence[i+1]=='or':
                        conjunction='OR'
                    elif sentence[i+1]==':but':
                        conjunction='BUT'
                    else:
                        conjunction='AND'
                    sentence=sentence[i+1:]       
                else:
                    object=[]
            
            #Add the nominal group
            compare['nom_gr']=gr_nom_list
            
            #Comparator : ends with 'er'
            if sentence[i-1].endswith('er'):
                compare['object']=sentence[i-1]
                sentence=sentence[:i-1]+sentence[i+1:]
            
            #Comparator : with 2 words
            elif sentence[i-2]=='more' or sentence[i-2]=='less':
                compare['object']=sentence[i-2]+'+'+sentence[i-1]
                sentence=sentence[:i-1]+sentence[i+1:]
            
            #Comparator : exceptions
            elif sentence[i-1]=='more' or sentence[i-1]=='less':
                compare['object']=sentence[i-1]
                sentence=sentence[:i-1]+sentence[i+1:]
            
            vg.comparator=vg.comparator+[compare]
        i += 1
    return sentence



def can_be_imperative(sentence):
    """
    This function return the possibility to have an imperative
    Input=sentence        Output=0 can be imperative and 1 no
    """
    
    if not sentence:
        return False
    if sentence[0] in ResourcePool().adverbs + ResourcePool().proposals:
        return False
    if sentence[0]=='.' or sentence[0]=='?' or sentence[0]=='!':
        return False

    return True

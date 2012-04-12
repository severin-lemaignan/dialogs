#!/usr/bin/python
# -*- coding: utf-8 -*-
# SVN:rev202 + PythonTidy

"""
 Created by Chouayakh Mahdi                                                       
 22/06/2010                                                                       
 The package contains functions which are important for the pre-parsing
 We return a list of all sentence in the utterance to do processing                    
 Functions:            
    adverbial_or_subsentence : to define the subsentence and the indirect complement with before, after...  
    process_and_beginning_sentence : to process the beginning of the sentence
    delete_and_from_number : to delete 'and' between two numbers
    concat_number : to concatenate numbers with '+'
    upper_to_lower : to process the upper case at the beginning of the sentence   
    but : to find 'but' that need preporcessing     
    concatenate_pos : to concatenate an element in a position given               
    compound_nouns: replace spaces in compound nouns by '+'
    case_apostrophe_s_to_is : to know if there is this kind of "'s"               
    expand_contractions : to perform expand contraction using concatenate_pos     
    determination_nominal_group : to return the nominal group with his complement
    and_nominal_group_comma : to process the case when there is a comma between nominal groups                                               
    and_nominal_group : to add 'and' between nominal groups separated with nothing  
    find_nominal_group_list : take off noun chain linked by 'of'                         
    create_possession_claus : to transform a noun chain to string's list with 'of'
    possesion_form : to exchange the "'s" to 'of' by using 2 latest functions    
    other_processing : to perform other processing                                 
    move_prep : to put the preposition before the nominal group
    conjunction_processing : to create a nominal group before and after the 'or'
    reorganize_adj : to delete ',' and 'and' if it is between adjectives*
    subsentence_comma : to delete ',' or changed on ';'
    take_off_comma : to delete ';' if it is before relative or subsentence
    delete_empty : to delete '' from sentence
    remerge_sentences : to transform some sentences of the remerge part
    add_scd_vrb : to transform the verb after the first verb into second verb    
    interjection : to find and create interjections
    what_to_relative : to change what+to into relative form 
    day_month : to find day or month to put them with upper case  
    am_pm : to separate 'am' or 'pm' from the digit
    and_between_sentence : to separate sentences if between them there is 'and' 
    double_det : to delete all first determinants if there is more than one
    processing : is used by process_sentence
    process_sentence : to split utterance into many sentences using all other functions 
"""
from dialogs.resources_manager import ResourcePool, ThematicRolesDict
import analyse_nominal_group
import other_functions



def adverbial_or_subsentence(sentence):
    """
    define the subsentence and the indirect complement with before, after...                                 
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    while i <len(sentence):
        #If we have a proposal which can be for subsentence and for indirect object
        
        for z in ResourcePool().adv_sub:
            if sentence[i]==z[1:]:
                #We recovery the nominal group after
                gr=determination_nominal_group(sentence, i+1,'of')
              
                if len(gr)+i+1>=len(sentence) or sentence[len(gr)+i+1] in ResourcePool().proposals+['?','.','!'] :
                    #It is an indirect complement
                    pass
                else:
                    #It is a subsentence
                    sentence[i]=':'+sentence[i]
        i=i+1
    return sentence
        
        
        
def process_and_beginning_sentence(sentence):
    """
    process the beginning of the sentence
    For example if there is adverb, we put it at the end (i_cmpl also)                              
    Input=sentence                                     Output=sentence               
    """
    
    #If sentence is empty
    if sentence==[]:
        return []
    
    #Using flag is for the ending of this function
    if other_functions.find_cap_lettre(sentence[0])==1:
        flg=1
        sentence[0]=sentence[0][0].lower()+sentence[0][1:]
    else:
        flg=0
        
    #We have to take off this words
    if sentence[0]==';' or sentence[0]=='and' or sentence[0]=='ah' or sentence[0]==',' or sentence[0]=='very':
        sentence=sentence[1:]
    
    #If it starts with proposal
    if sentence[0] in ResourcePool().proposals:
        gr=determination_nominal_group(sentence, 1,'of')
        #We put the nominal group at the end of the sentence
        if gr!=[]:
            sentence=sentence[len(gr)+1:]+[',']+[sentence[0]]+gr
            sentence=process_and_beginning_sentence(sentence)
        else:
            #In this case we don't find a nominal group but there is a i_cmpl
            for z in sentence:
                if z==';' or z=='.' or z==',':
                    #The final point of i_cmpl is the punctuation
                    phrase=sentence[:sentence.index(z)]
                    if sentence[len(sentence)-1]=='.' or sentence[len(sentence)-1]=='?' or sentence[len(sentence)-1]=='!':
                        sentence=sentence[sentence.index(z)+1:len(sentence)-1]+[',']+phrase+[sentence[len(sentence)-1]]
                    else:
                        sentence=sentence[sentence.index(z)+1:]+[',']+phrase
    
    #If it starts with adverb
    if sentence[0] in ResourcePool().adverbs:
        if sentence[len(sentence)-1]=='.' or sentence[len(sentence)-1]=='?' or sentence[len(sentence)-1]=='!':
            sentence=sentence[1:len(sentence)-1]+[sentence[0]]+[sentence[len(sentence)-1]]
            sentence=process_and_beginning_sentence(sentence)
        else:   
            sentence=sentence[1:]+[',']+[sentence[0]]
            sentence=process_and_beginning_sentence(sentence)
    
    #If flag is 1 => we have a capitol letter at the beginning
    if flg==1:
        sentence[0]=sentence[0][0].upper()+sentence[0][1:]
    
    return sentence



def delete_and_from_number(sentence):
    """
    delete 'and' between two numbers                                 
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    while i < len(sentence):
        if sentence[i]=='and' and other_functions.number(sentence[i-1])==1 and other_functions.number(sentence[i+1])==1:
            sentence=sentence[:i]+sentence[i+1:]
        i=i+1
    return sentence


            
def concat_number(sentence):
    """
    concatenate numbers with '+'                                 
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    sentence = delete_and_from_number(sentence)
    
    while i < len(sentence):
        #There is a number
        if other_functions.number(sentence[i])==1:
            begin_pos=i
                
            while i<len(sentence) and other_functions.number(sentence[i])==1:
                i=i+1
            end_pos=i
            
            #We have to concatenate the last number if it is superlative
            if i < len(sentence) and other_functions.number(sentence[i])==2:
                end_pos=end_pos+1
            if i < len(sentence) and sentence[i] in ResourcePool().adjective_numbers:
                    end_pos=end_pos+1
                    
            sentence=sentence[:begin_pos]+[other_functions.convert_to_string(sentence[begin_pos:end_pos])]+sentence[end_pos:]
            
        i=i+1    
    return sentence
        
        
        
def upper_to_lower(sentence):
    """
    converts the upper case to lower case
    Input=sentence, beginning sentence list                  Output=sentence         
    """
      
    #If the sentence begins with upper case
    if other_functions.find_cap_lettre(sentence[0]):
        
        #We convert upper case to lower case if it is not 'I'
        if sentence[0]=='I':
            sentence=expand_contractions(sentence)
            return sentence
        else:
            sentence[0]=sentence[0][0].lower()+sentence[0][1:]
        
        #We make changes here because we need lower case and not upper case
        sentence=expand_contractions(sentence)
        sentence = adverbial_or_subsentence(sentence)
        stc = process_and_beginning_sentence(sentence)
        
        #If sentence is modified we can return it
        if stc!=sentence:
            return stc
        
        #We find an action verb => it is an imperative sentence        
        if sentence[0] in ThematicRolesDict().get_all_verbs():
            return sentence
         
        #If we find the word in the Beginning_sentence list
        for v in ResourcePool().sentence_starts:
            if sentence[0]==v[0]:
                return sentence
            
        #We find a number
        if other_functions.number(sentence[0])==1:
            return sentence
        
        #If there is plural
        sentence=analyse_nominal_group.find_plural(sentence)
        #If it still start with adjective
        if analyse_nominal_group.is_an_adj(sentence[0])==1:
            sentence=['the']+sentence
            
        #If there is a nominal group
        if analyse_nominal_group.find_sn_pos (sentence,0):
            return sentence
        
        #Default case: we assume a proper name, we convert lowercase to uppercase
        sentence[0]=sentence[0][0].upper()+sentence[0][1:]
        
    #If the sentence begins with lower case
    else:
        #We make changes here because we need lower case and not upper case
        sentence=expand_contractions(sentence)
        sentence = adverbial_or_subsentence(sentence)
        sentence = process_and_beginning_sentence(sentence)
        
        #If we find the word in the Beginning_sentence list so we can return it
        for v in ResourcePool().sentence_starts:
            if sentence[0]==v[0]:
                return sentence
            
        #If there is plural
        sentence=analyse_nominal_group.find_plural(sentence)
        #If it still start with adjective
        if analyse_nominal_group.is_an_adj(sentence[0])==1:
            sentence=['the']+sentence
    
    return sentence
    


def but(sentence):
    """
    find 'but' that need preporcessing                    
    Input=sentence                         Output=sentence               
    """
    
    #init
    i=0
    
    while i < len(sentence):
        #The 'but' must be between 2 nominal groups
        if sentence[i]=='but':
            #After 'but' of subsentence we must have a nominal group (subject)
            scd_nominal_group=analyse_nominal_group.find_sn_pos (sentence, i+1)
            if scd_nominal_group==[]:
                sentence[i]=':but'
            else:
                
                #We have to find the first nominal group
                begin_pos=i-1
                fst_nominal_group=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
                while fst_nominal_group==[] and begin_pos>0:
                    begin_pos=begin_pos-1
                    fst_nominal_group=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
                #The case when but is between 2 adjectives and we have the same noun
                if fst_nominal_group[len(fst_nominal_group)-1]=='but':
                    sentence[i]=':but'
        i=i+1
    return sentence



def concatenate_pos(sentence, position, element, pos_rem):
    """
    concatenate an element in sentence at a position                     
    Input=sentence, position+element to concatenate, letter's number to remove        
    Output=sentence                                                                  
    """

    #We perform concatenation
    sentence = sentence[:position+1] + element + sentence[position+1:]
    #We remove the superfusion part
    sentence[position] = sentence[position][:len(sentence[position])-pos_rem]
    return sentence



def case_apostrophe_s_to_is(word):
    """
    know if we have to expand contraction 's to is (return 1)            
    Input=word                      Output=flag(0 if no or 1 if yes)                 
    """
    
    word=word[0].lower()+word[1:]
    if word in ResourcePool().be_pronoun:
        return 1
    return 0



def expand_contractions(sentence):
    """
    Replaces the contractions by the equivalent meaning, but without contraction
    Input=sentence                       Output=sentence
    """
    
    #init
    i=0
    
    while i < len(sentence):

        if case_apostrophe_s_to_is(sentence[i])==1:
            sentence = concatenate_pos(sentence, i, ['is'], 2)
            i=i+1
        
        for j in ResourcePool().replace_tuples:
            if sentence[i]==j[0]:
                sentence = sentence[:i] + j[1] + sentence[i+1:]
                i=i+1
                break
            
        for j in ResourcePool().change_tuples:
            if sentence[i].endswith(j[0]):
                sentence = concatenate_pos(sentence, i, [j[1]], int(j[2]))
                i=i+1
                break
        i=i+1
        
    return sentence



def preposition_concat(sentence):
    """
    concatenate some words to have a preposition 
    Input=sentence                                     Output=sentence               
    """    
    
    #init
    i=0
    
    #For the case of whom
    if sentence[0:2]==['To', 'whom']:
        sentence=['To+whom']+sentence[2:]
    
    #For all other prepositions
    while i < len(sentence):
        
        for j in ResourcePool().concatenate_proposals:
            if i+len(j) <= len(sentence) and sentence[i:i+len(j)]==j:
                sentence=sentence[:i]+[other_functions.convert_to_string(j)]+sentence[i+len(j):]
                break
                
        i=i+1
    return sentence
    
def compound_nouns(sentence):
    """
    Replaces all compound nouns defined in the 'nouns' data file by
    concatenated versions (ie, with a '+' between tokens)
    """
    #init
    i=0

    while i < len(sentence) - 1: # '- 1' because compound nouns have a length >= 2

        for cn in ResourcePool().compound_nouns:
            if i + len(cn) <= len(sentence) and \
               sentence[i:i+len(cn)] == cn:
                sentence = sentence[:i] + \
                           [other_functions.convert_to_string(cn)] + \
                           sentence[i+len(cn):]
                break
        i += 1

    return sentence
    
def determination_nominal_group(sentence, position,prop):
    """
    return the nominal group with his complement                             
    Input=sentence                             Output=nominal group               
    """
    
    nominal_group=analyse_nominal_group.find_sn_pos(sentence, position)
    list_nominal_group=nominal_group
    
    while position+len(nominal_group)<len(sentence) and sentence[position+len(nominal_group)] == prop:
        position=position+len(nominal_group)+1
        nominal_group=analyse_nominal_group.find_sn_pos(sentence, position)
        list_nominal_group=list_nominal_group+[prop]+nominal_group
        
    return list_nominal_group
        
        

def and_nominal_group_comma(sentence):
    """
    process the case when there is a comma between nominal groups                             
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    flag=2
    list_nominal_group=[]
    
    #If we find ','
    while i < len(sentence):
        if sentence[i]==',':
            nominal_group=determination_nominal_group(sentence, i+1, 'of')
            end_pos=len(nominal_group)+i+1
            
            #First we recover the all nominal groups preceded by ','
            while nominal_group!=[] and sentence[end_pos]==',':
                list_nominal_group=['and']+nominal_group
                nominal_group=determination_nominal_group(sentence, end_pos+1,'of')
                end_pos=len(nominal_group)+end_pos+1
                #Flag still 2 because this stage is not compulsory
                flag=2
            
            #We will find the last nominal group of this phrase
            if nominal_group!=[] and sentence[end_pos]=='and':
                list_nominal_group=list_nominal_group+['and']+nominal_group
                nominal_group=determination_nominal_group(sentence, end_pos+1,'of')
                end_pos=len(nominal_group)+end_pos+1
                list_nominal_group=list_nominal_group+['and']+nominal_group
                #Flag will be 1 because this stage is compulsory
                flag=flag-1
            
            #If flag=1 => we can have the and_nominal_group_comma case
            if flag==1:
                #We have to find the first nominal group
                begin_pos=i-1
                nominal_group=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
                while nominal_group==[] and begin_pos>0:
                    begin_pos=begin_pos-1
                    nominal_group=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
                #If this nominal group preceded the first ',' => OK
                if nominal_group!=[] and begin_pos+len(nominal_group)==i:
                    flag=flag-1
                    list_nominal_group=nominal_group+list_nominal_group
                   
            #We have an and_nominal_group_comma case 
            if flag==0:
                sentence=sentence[:begin_pos]+list_nominal_group+sentence[end_pos:]
                i=end_pos
    
        i=i+1
    
    return sentence



def and_nominal_group(sentence):
    """
    add 'and' between nominal groups separated with nothing                             
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    list_nominal_group=our_list=[]
    
    while i < len(sentence):
        #We start by finding the first nominal group
        nominal_group=determination_nominal_group(sentence, i, 'of')
        position=i
        
        #We recovery all nominal groups followed the first one
        while nominal_group!=[]:
            list_nominal_group=list_nominal_group+[nominal_group]
            i=i+len(nominal_group)
            nominal_group=determination_nominal_group(sentence, i, 'of')
        
        #If we have 'and' just after, we recovery the nominal group followed
        if i<len(sentence) and sentence[i]=='and' and list_nominal_group!=[]:
            i=i+1
            nominal_group=determination_nominal_group(sentence, i, 'of')
           
            #If the first one of the list is not a pronoun => OK
            if other_functions.there_is_pronoun(list_nominal_group+[nominal_group])==0:
                
                for j in list_nominal_group:
                    our_list=our_list+j+['and']
                sentence=sentence[:position]+our_list+sentence[i:]
                i=i+len(nominal_group)+len(list_nominal_group)
                list_nominal_group=our_list=[]
            
            #We forgot the first nominal group and we continue just after it
            else:
                i=position+len(list_nominal_group[0])
                list_nominal_group=[]
        else:
            i=i+1
            list_nominal_group=[]
   
    return sentence



def find_nominal_group_list(phrase):
    """
    break phrase into nominal groups with ('s)                         
    And return also the elements number of the end of this list in the sentence       
    Input=sentence                    Output=list of nominal group                   
    """
    
    #init
    list=[]
    nb_element=0
    
    nominal_group=analyse_nominal_group.find_sn_pos(phrase, 0)
    #We use the length of the nominal group because it will be different with len(nominal_group)
    nominal_group_lent=len(nominal_group)

    #We loop until there is no more nominal group
    while nominal_group!=[] and (nominal_group[len(nominal_group)-1].endswith("'s") or nominal_group[len(nominal_group)-1].endswith("s'")):

        list=[nominal_group]+list
        nb_element=nb_element+nominal_group_lent

        #re-init phrase and nominal group
        phrase=phrase[nominal_group_lent:]
        nominal_group=analyse_nominal_group.find_sn_pos(phrase, 0)
        nominal_group_lent=len(nominal_group)

        #We need to have a nominal group so we forced it
        if nominal_group == []:
            nominal_group=analyse_nominal_group.find_sn_pos(['the']+phrase, 0)
            nominal_group_lent=len(nominal_group)-1

    list=[nominal_group]+list
    nb_element=nb_element+nominal_group_lent

    #We put the elments number at the end of the list
    list=list+[nb_element]
    
    return list



def create_possession_claus(list):
    """
    create phrase with 'of'                                            
    Input=list of nominal group                 Output=phrase of nominal group       
    """
    
    #init
    i=1
    #To take the first element
    phrase=list[i-1]

    #We concatenate
    while i < len(list):
        phrase=phrase+['of']+list[i]
        i=i+1

    #We delete the 's
    for j in phrase:
        if j.endswith("'s"):
            word= phrase[phrase.index(j)]
            phrase[phrase.index(j)]= word[:len(word)-2]
        if j.endswith("s'"):
            word= phrase[phrase.index(j)]
            phrase[phrase.index(j)]= word[:len(word)-1]

    return phrase



def possesion_form(sentence): 
    """
    convert 's to possession form 'of'                                 
    Input=sentence                                     Output=sentence               
    """

    #init
    begin_pos=0
    flag=0

    #We will find the possession case
    while (begin_pos<len(sentence)):

        #We found a posssession case
        if sentence[begin_pos].endswith("'s") or sentence[begin_pos].endswith("s'"):

            #We have to find the first nominal group
            nominal_group=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
    
            #In the case of a propre name
            while nominal_group!=[] and begin_pos!=0 and other_functions.find_cap_lettre(nominal_group[0])==1:
                begin_pos=begin_pos-1

                nominal_group=analyse_nominal_group.find_sn_pos(sentence, begin_pos)
                flag=1

            #If flag=1 => there is a propre name so we haven't decrement the begin_pos
            if flag==0:
                while nominal_group == []:
                    begin_pos=begin_pos-1
                    nominal_group=analyse_nominal_group.find_sn_pos(sentence, begin_pos)

            else:
                #If there is a propre name, begin_pos is wrong, we have to increment
                begin_pos=begin_pos+1
                flag=0

            #We recover the list of nominal groups
            nominal_group_list=find_nominal_group_list(sentence[begin_pos:])
            #We create the final phrase
            end_pos=nominal_group_list[len(nominal_group_list)-1]+begin_pos
            sentence=sentence[:begin_pos]+create_possession_claus(nominal_group_list[:len(nominal_group_list)-1])+sentence[end_pos:]

            #We continue processing from the end's position
            begin_pos=end_pos
            
        else:
            begin_pos=begin_pos+1

    return sentence



def refine_possesion_form(sentence):
    """
    add determinant after 'of' if there is not                              
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    while i < len(sentence):
        if sentence[i]=='of' and analyse_nominal_group.find_sn_pos(sentence, i+1)==[]:
            sentence=sentence[:i+1]+['a']+sentence[i+1:]
        i=i+1
        
    return sentence



def other_processing(sentence):
    """
    This function performs processing to facilitate the analysis that comes after    
    Input=sentence                              Output=sentence                      
    """
    
    #init
    i=0
    
    #Question with which starts with nominal group without determinant
    if sentence!=[] and sentence[0]=='which':
        sentence=[sentence[0]]+['the']+sentence[1:]
    
    while i <len(sentence):
        #When we have 'think', in some case we need to have 'that'
        if sentence[i]=='think' and sentence[i+1]!='that' and analyse_nominal_group.find_sn_pos(sentence, i+1)!=[]:
            sentence=sentence[:i+1]+['that']+sentence[i+1:]
        
        #'in front of' is the same with 'at the front of'
        if sentence[i]=='front' and sentence[i-1]=='in' and sentence[i+1]=='of':
            #sentence=sentence[:i-1]+['at'] +['the']+sentence[i:]
            sentence=sentence[:i-1]+['in+front+of'] + sentence[i+2:]
            
        if sentence[i]=='i':
            sentence[i]='I'

        # Split 'another' into 'an other' -> undefinite det + other
        if sentence[i]=='another':
            sentence=sentence[:i-1] + ['an', 'other'] + sentence[i+1:]

        i += 1
    return sentence
 
 
 
def move_prep(sentence):
    """ 
    put the preposition before the nominal group                     
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i < len(sentence):
        for p in ResourcePool().prep_change_place:
            
            #If there is a preposal
            if sentence[i]==p:
                position=i
                
                #If after preposition we have nominal group, it is for this nominal group 
                if analyse_nominal_group.find_sn_pos(sentence, i+1)==[]:        
                    #We have to find the nominal group just before
                    while analyse_nominal_group.find_sn_pos(sentence, position)==[]:
                        position=position-1                
                    sentence=sentence[:position]+[p]+sentence[position:i]+sentence[i+1:]
        i=i+1
    return sentence 

                

def conjunction_processing(sentence, cjt):
    """ 
    creates a nominal group before and after the 'or'                  
    Input=sentence and the conjunction                     Output=sentence                      
    """ 
    
    #init
    i=0
    fst_nominal_group=[]
    
    while i < len(sentence):
        
        if sentence[i]==cjt:
            #We have to find the first and the second nominal group in the sentence
            position=i
            #Until we find the first nominal group
            while position>0 and fst_nominal_group==[]:
                position=position-1
                fst_nominal_group=analyse_nominal_group.find_sn_pos(sentence, position)
                
            if fst_nominal_group!=[]:
                
                #We will find the second nominal group
                scd_nominal_group=analyse_nominal_group.find_sn_pos(sentence, i+1)
                
                if fst_nominal_group[len(fst_nominal_group)-1]==cjt and scd_nominal_group==[]:
                    #We have to know the second nominal group
                    sentence=sentence[:i+1]+[fst_nominal_group[0]]+sentence[i+1:]
                    scd_nominal_group=analyse_nominal_group.find_sn_pos(sentence, i+1)
                    
                    #We insert word to have 2 nominal groups in the sentence
                    sentence=sentence[:position]+fst_nominal_group[:len(fst_nominal_group)-1]+[scd_nominal_group[len(scd_nominal_group)-1]]+[cjt]+sentence[i+1:]
                
                elif fst_nominal_group[len(fst_nominal_group)-1]==cjt:
                    #We insert word to have 1 nominal group in the sentence
                    sentence=sentence[:position]+fst_nominal_group[:len(fst_nominal_group)-1]+[scd_nominal_group[len(scd_nominal_group)-1]]+sentence[i:]
                i=i+1
        i=i+1
        
    return sentence



def reorganize_adj(sentence):
    """ 
    deletes ',' and 'and' if it is between adjectives                  
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i < len(sentence)-1:
        if sentence[i] ==',' or sentence[i] =='and':
            if analyse_nominal_group.is_an_adj(sentence[i+1]) and analyse_nominal_group.is_an_adj(sentence[i-1]):
                if other_functions.number(sentence[i+1])==0 and other_functions.number(sentence[i-1])==0:
                    sentence=sentence[:i]+sentence[i+1:]    
        i=i+1
    return sentence
    
    
    
def subsentence_comma(sentence):
    """ 
    delete ',' or changed on ';'                  
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=0
    while i < len(sentence):
        if sentence[i]==',':
            sentence[i]=';'
            
            #We delete it if it is at the end of the sentence
            if i==len(sentence)-1:
                sentence=sentence[:i]
            elif sentence[i+1]=='?' or sentence[i+1]=='!' or sentence[i+1]=='.':
                sentence=sentence[:i]+sentence[i+1:]
        i=i+1
    return sentence
    
    
    
def take_off_comma(sentences):
    """ 
    delete ';' if it is before relative or subsentence                  
    Input=list of sentence                  Output=sentence                      
    """ 
    
    #init
    i=k=0
    
    while k < len(sentences):
        while i < len(sentences[k]):
            if sentences[k][i]==';':
                if sentences[k][i+1] in ResourcePool().subsentences+ResourcePool().relatives:
                    sentences[k]=sentences[k][:i]+sentences[k][i+1:]
            i=i+1
        k=k+1
    return sentences
          
    
                        
def delete_empty_word(sentence):
    """ 
    delete '' from sentence                  
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=0

    while i < len(sentence):
        if sentence[i]=='' or sentence[i]=='please' or sentence[i]=='Please':
            sentence=sentence[:i]+sentence[i+1:]
        i=i+1
        
    return sentence   
    
    
    
def remerge_sentences(sentence):
    """ 
    This function transform some sentences of the remerge part                  
    Input=sentence                              Output=sentence                      
    """ 
    
    gr=determination_nominal_group(sentence, 0,'of')
    if gr and len(gr) < len(sentence):
        
        next_token = sentence[len(gr)]
	#Case of 'the bottle on the table'
        if next_token in ResourcePool().compelement_proposals:
            if analyse_nominal_group.find_sn_pos(sentence, len(gr)+1):
                sentence=gr+['which','is']+sentence[sentence.index(sentence[len(gr)]):]
        
    return sentence    
   


def add_scd_vrb(sentence):
    """ 
    transform the verb after the first verb into second verb                 
    Input=sentence                              Output=sentence                      
    """ 
    #init
    i=0
    
    while i < len(sentence):
        #If we have a verb that need a second verb
        if sentence[i] in ResourcePool().verb_need_to:
            nominal_group=analyse_nominal_group.find_sn_pos(sentence, i+1)
            if nominal_group!=[]:
                sentence=sentence[:i+len(nominal_group)+1]+['to']+sentence[i+len(nominal_group)+1:]
            else:
                sentence=sentence[:i+1]+['to']+sentence[i+1:]
        i=i+1
    
    return sentence
    
    
    
def interjection(sentence):
    """ 
    finds and creates interjections                 
    Input=sentence                     Output=list of sentence                      
    """ 
   
    #init
    i=pos=0

    #We will find the position of the first ','
    while i < len(sentence) and pos==0:
        if sentence[i]==';':
            pos=i
        i=i+1
   
    if pos==0:
        return [sentence]
    else:
        #If the comma is for relative or subsentence
        for k in sentence[:pos]:
            if k in ResourcePool().subsentences+ResourcePool().relatives:
                return [sentence]
          
        #If we have an interjection we replace ',' by '!'
        for m in ResourcePool().sentence_starts:
            #We identify the interjection with the beginning of the sentence
            if sentence[0]==m[0] and m[1]=='0':
                sentence[pos]='!'
                return [sentence[:pos+1], sentence[pos+1:]]
        
        #We have to know if there is just a nominal group before
        nominal_group=determination_nominal_group(sentence, 0,'and')
        if nominal_group==sentence[:pos]:
            sentence[pos]='!'
            return [sentence[:pos+1], sentence[pos+1:]]
        
    return [sentence]
   
   
   
def what_to_relative(sentence):
    """ 
    change what+to into relative form                 
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i<len(sentence)-1:
        if sentence[i]=='what' and sentence[i+1]=='to':
            sentence=sentence[:i]+['the','thing','that','is']+sentence[i+1:]
        i=i+1
    return sentence
    


def day_month(sentence):
    """ 
    find day or month to put them with upper case                   
    Input=sentence                            Output=sentence                      
    """ 

    for i in sentence:
        for j in ResourcePool().days_list+ResourcePool().months_list:
            if j[0].lower()==i:
                sentence[sentence.index(i)]=i[0].upper()+i[1:]  
    return sentence
   
   
        
def am_pm(sentence):
    """ 
    This function separate 'am' or 'pm' to the digit                   
    Input=sentence                            Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i<len(sentence):
        if sentence[i].endswith('am') or sentence[i].endswith('pm'):
            if other_functions.number(sentence[i])==1:
                sentence=sentence[:i]+[sentence[i][:len(sentence[i])-2]]+[sentence[i][len(sentence[i])-2:]]+sentence[i+1:]
                i=i+1
        i=i+1
        
    return sentence
        


def and_between_sentence(sentence):
    """ 
    separate sentences if between them there is 'and'                  
    Input=sentence                            Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i < len(sentence):
        j=0
        while j < len(sentence[i]):
            if sentence[i][j]=='and' and sentence[i][j-1]==';':
                stc=sentence[i][:j-1]
                sentence[i]=sentence[i][j+1:]
                sentence=sentence[:i]+[stc]+sentence[i:]      
            j=j+1
        i=i+1
        
    return sentence



def double_det(sentence):
    """ 
    delete all first determinants if there is more than one                  
    Input=sentence                            Output=sentence                      
    """ 
    
    #init
    i=0
    
    while i<len(sentence):
        if sentence[i]=='all':
            for k in ResourcePool().determinants:
                if k==sentence[i+1]:
                    sentence=sentence[:i]+sentence[i+1:]
        i=i+1
    return sentence


                    
def processing(sentence):
    """ 
    This function is used by process_sentence                  
    Input=sentence                              Output=sentence                      
    """ 
    
    sentence = preposition_concat(sentence)
    sentence = compound_nouns(sentence)
    sentence = upper_to_lower(sentence)
    sentence = delete_empty_word(sentence)
    sentence = concat_number(sentence)
    sentence = conjunction_processing(sentence,'or')
    sentence = conjunction_processing(sentence,'but')
    sentence = reorganize_adj(sentence)
    sentence = conjunction_processing(sentence,'and')
    sentence = other_processing(sentence)
    sentence = possesion_form(sentence)
    sentence = refine_possesion_form(sentence)
    sentence = and_nominal_group(sentence)
    sentence = and_nominal_group_comma(sentence)
    sentence = move_prep(sentence)
    sentence = but(sentence)
    sentence = subsentence_comma(sentence)
    sentence = remerge_sentences(sentence)
    sentence = what_to_relative(sentence)
    sentence = add_scd_vrb(sentence)
    sentence = day_month(sentence)
    sentence = am_pm(sentence)
    sentence = double_det(sentence)
    sentence = adverbial_or_subsentence(sentence)
    sentence = process_and_beginning_sentence(sentence)
    sentence = interjection(sentence)
    sentence = take_off_comma(sentence)
    sentence = and_between_sentence(sentence)
    return sentence

    
    
def process_sentence(utterance):
    """
    breaks the utterance (as a list) into sentences                        
    And does the processing of punctuation                                            
    Input=utterance and beginning sentence list         Output=list of sentence          
    """

    #init
    sentence=[]
    sentence_list=[]
    utterance = utterance.split()
   
    for j in utterance:

        #If user put space between the last word and the punctuation
        if j=='.' or j=='?' or j=='!':
            sentence = sentence+[j]
            sentence = processing(sentence)
            sentence_list=sentence_list+sentence
            sentence=[]

        elif j.endswith('.') or j.endswith('?') or j.endswith('!'):
            sentence = sentence+[j[:len(j)-1]] + [j[len(j)-1]]
            sentence[len(sentence)-2]=other_functions.get_off_point(sentence[len(sentence)-2])
            sentence = processing(sentence)
            sentence_list=sentence_list+sentence
            sentence=[]

        else:
            sentence=sentence+[j]
            
    #If the user forget the punctuation at the end
    if sentence!=[]:
        sentence = processing(sentence)
        sentence_list=sentence_list+sentence

    return sentence_list

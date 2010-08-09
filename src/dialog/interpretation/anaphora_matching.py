#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi                                                       
 06/08/2010                                                                       
 The package contains functions perform the anaphora processing
 Functions:   
    delete_redon_nom_group : to delete the redundancy in the list of nominal groups                                                                     
    delete_unuse_nom_gr : to delete the pronoun from the list of the nominal groups          
    recover_nom_gr_list : to return the list of the nominal groups used by anaphora processing 
    first_replacement : to perform the first replacement (before the loop)
"""
from sentence import *

class AnaphoraMatcher:
    
    def match_object(self):
        return "method 1"
        
        
    def match_first_object(self, sentences):
        print(sentences[0])
        list_gr=recover_nom_gr_list(sentences)
        gr = first_replacement(list_gr, c_gr)
        return [gr, 'FAILLURE']
        
        
"""
Statement of lists
"""
pronoun_list=['you', 'I', 'we', 'he', 'she', 'me', 'it', 'he', 'they', 'yours', 'mine', 'him']


def delete_redon_nom_group(nom_gr_list):
    """
    This function delete the redundancy in the list of nominal groups                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    i=0
    j=0
    
    #We have to loop the list twice
    while i < len(nom_gr_list):
        j=i+1
        while j < len(nom_gr_list):
            #If same id => same nominal group
            if nom_gr_list[j].id==nom_gr_list[i].id:
                nom_gr_list=nom_gr_list[:j]+nom_gr_list[j+1:]
                #When we delete => we increment j
                j=j-1
            j=j+1
        i=i+1 
    
    return nom_gr_list



def delete_unuse_nom_gr(nom_gr_list):
    """
    This function delete the pronoun from the list of the nominal groups                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    i=0
    
    while i < len(nom_gr_list):
        for j in pronoun_list:
            #If the nominal group is a pronoun
            if [j]==nom_gr_list[i].noun and nom_gr_list[i].det==[]:
                nom_gr_list=nom_gr_list[:i]+nom_gr_list[i+1:]
                #When we delete => we increment i
                i=i-1
                break
        i=i+1
    return nom_gr_list



def recover_nom_gr_list(sentences):
    """
    This function return the list of the nominal groups used by anaphora processing                              
    Input=nominal group list                Output=nominal group list                     
    """
    
    #init
    nom_gr_list=[]
    
    #We recover all nominal groups of the sentences
    for i in sentences:
        nom_gr_list=nom_gr_list+i.sn
        for j in i.sv:
            nom_gr_list=nom_gr_list+j.d_obj
            for x in j.i_cmpl:
                nom_gr_list=nom_gr_list+x.nominal_group
            nom_gr_list=nom_gr_list+recover_nom_gr_list(j.vrb_sub_sentence)
    
    #We perform deletions
    nom_gr_list=delete_redon_nom_group(nom_gr_list)
    nom_gr_list=delete_unuse_nom_gr(nom_gr_list)
    
    #If sentence is empty, we return an empty list      
    return nom_gr_list



def first_replacement(nom_gr_list, current_nom_gr):
    """
    This function perform the first replacement (before the loop)                          
    Input=nominal group list and the current one       Output=a nominal group or NONE         
    """
    
    #init
    flg=0
    
    if nom_gr_list==[]:
        return None
    
    if current_nom_gr.noun==['it']:
        return nom_gr_list[0]
    
    #We have to change only the noun
    elif current_nom_gr.noun==['one']:
        current_nom_gr.noun=nom_gr_list[0].noun
        
        #We add adjectives and delete the redundancy
        for i in nom_gr_list[0].adj:
            for j in current_nom_gr.adj:
                if i==j:
                    flg=1
            if flg==1:
                flg=0
            else:
                current_nom_gr.adj=current_nom_gr.adj+[i]
        
        #For all other information, we perform an addition
        current_nom_gr.noun_cmpl=current_nom_gr.noun_cmpl+nom_gr_list[0].noun_cmpl
        current_nom_gr.relative=current_nom_gr.relative+nom_gr_list[0].relative 
        
        #We affect the if
        current_nom_gr.id=nom_gr_list[0].id
        
        return current_nom_gr
    
    return None
    
    

def unit_tests():
    
    """
    Function to perform unit tests                                                   
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
    ## Aim of this test : Present the duality between the direct and indirect complement
    """
    print ''
    print ('######################## test 1.3 ##############################')

    utterance="Using 'it' so we have to replace automatically"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
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
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Indirect_Complement(['to'],[Nominal_Group([],['you'],[],[],[])])],
                [], [] ,'negative',[])])]

    sentences[0].sn[0].id='azeaz'
    sentences[0].sv[0].i_cmpl[0].nominal_group[0].id="4"
    sentences[1].sv[0].d_obj[0].id='sghj'
    sentences[1].sv[0].i_cmpl[0].nominal_group[0].id="9"
    sentences[2].sn[0].id='eaz'
    sentences[2].sv[0].d_obj[0].id='9'
    sentences[2].sv[0].i_cmpl[0].nominal_group[0].id="6"
    
    list_gr=recover_nom_gr_list(sentences)
    
    c_gr=Nominal_Group([],['it'],[],[],[])
    gr = first_replacement(list_gr, c_gr)
    print "the id of the nominal group: ", gr.id
    print (str(gr))
    
    
if __name__ == '__main__':
    unit_tests()
    

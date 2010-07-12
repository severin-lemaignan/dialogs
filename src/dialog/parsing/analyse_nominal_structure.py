#SVN:rev202


"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 21/06/2010                                                                       ##
## The package contains functions that affect nominal structure                     ##
## It is more used for the subject                                                  ##
## Functions:                                                                       ##
##    fill_nom_gr : to fulfill a structure Nominal_Group                            ##
##    recover_ns : to recovers the nominal structure of the sentence                ##
######################################################################################
"""
from sentence import *
import analyse_nominal_group
import other_functions
import analyse_sentence


"""
############################## Statement of lists ####################################
"""
propo_rel_list=['who', 'which']


"""
######################################################################################
## This function fulfills a structure Nominal_Group with given information          ##
## Input=sentence, nominal group with his position                                  ##
## Output=the nominal group class                                                   ##
######################################################################################
"""
def fill_nom_gr (phrase, nom_gr, pos_nom_gr,conjunction):

    #init
    relative=[]
    
    #We start by recovering all information we need
    nom_gr_compl=analyse_nominal_group.find_nom_gr_compl (nom_gr, phrase, pos_nom_gr)
    det=analyse_nominal_group.return_det(nom_gr)
    adj=analyse_nominal_group.return_adj(nom_gr)
    noun=analyse_nominal_group.return_noun(nom_gr, adj, det)

    #We will treat the relative
    begin_pos_rel=analyse_nominal_group.find_relative(nom_gr, phrase, pos_nom_gr, propo_rel_list)
    end_pos_rel=other_functions.recover_end_pos_sub(phrase[begin_pos_rel:], propo_rel_list)

    #There is a relatve
    if begin_pos_rel!=-1:
        relative_phrase=phrase[begin_pos_rel+1:begin_pos_rel+end_pos_rel-1]
        
        relative = relative+[analyse_sentence.other_sentence('relative', '',relative_phrase)]

    #If there is a nom_gr_compl, we must make a recursive process for embedded complement
    if nom_gr_compl!=[]:
        gn=Nominal_Group(det,noun,adj,[fill_nom_gr(phrase,nom_gr_compl,pos_nom_gr+len(nom_gr)+1,'AND')],relative)

    else:
        gn=Nominal_Group(det,noun,adj,[],relative)
        
    #We recover the conjunction    
    gn._conjunction=conjunction
            
    return gn


"""
######################################################################################
## This function recovers the nominal structure of the sentence                     ##
## Input=sentence, the class sentence and the position of the nominal structure     ##
## Output=the class sentence and sentence                                           ##
######################################################################################
"""
def recover_ns(phrase, analysis, position):
    
    #init
    conjunction='AND'
        
    #We recover the first part of the subject
    sbj=analyse_nominal_group.find_sn_pos(phrase, position)
    
    #We loop until we don't have a nominal group
    while sbj!=[]:
        
        #We refine the nominal group if there is an error like ending with question mark
        sbj=analyse_nominal_group.refine_nom_gr(sbj)
        
        analysis.sn=analysis.sn+[fill_nom_gr(phrase, sbj, position,conjunction)]
    
        #We take off the nominal group
        phrase=analyse_nominal_group.take_off_nom_gr(phrase, sbj, phrase.index(sbj[0]))
        
        #Pre-treatment to remove the 
        begin_pos_rel=analyse_nominal_group.find_relative(sbj, phrase, position, propo_rel_list)
        end_pos_rel=other_functions.recover_end_pos_sub(phrase, propo_rel_list)
        
        if  begin_pos_rel!=-1:
            #We remove the relative part of the phrase
            phrase=phrase[:begin_pos_rel]+phrase[end_pos_rel:]
            
        #If there is 'and', we need to duplicate the information
        if len(phrase)>position and (phrase[position]=='and' or phrase[position]=='or'):
            
            #Reperform the 'and' or 'or' treatment
            sbj=analyse_nominal_group.find_sn_pos(phrase[1:], position)
            
            #We treat the 'or' like the 'and' and remove it
            if phrase[position]=='or':
                conjunction='OR'
            else:
                conjunction='AND'
            phrase=phrase[1:]
            
            #This case is used by whose
            if sbj==[]:
                phrase=['that']+phrase
                sbj=analyse_nominal_group.find_sn_pos(phrase, position)
               
        else:
            sbj=[]
    
    return phrase

"""
 Created by Chouayakh Mahdi
 21/06/2010
 The package contains functions that affect nominal structure
 It is more used for the subject

 Functions:
    recover_quantifier : to recover the quantifier and put the noun in singular form if it's in plural
    put_rela_from_nncompl_noun : to put the relative of the complement in the main noun 
    fill_nom_gr : to fulfill a structure Nominal_Group
    recover_ns : to recovers the nominal structure of the sentence
"""
from dialogs.resources_manager import ResourcePool
from dialogs.sentence import *
import analyse_nominal_group
import other_functions
import analyse_sentence
import preprocessing



def recover_quantifier(nom_gr):
    """
    recovers the quantifier and put the noun in singular form if it's in plural
    Input=nominal group class                     Output=nominal group class
    """

    #init
    flg=0

    #The default case is 'ONE'
    if nom_gr.det==[]:
        #If the noun starts with 'any' => we have 'all'
        if nom_gr.noun!=[] and nom_gr.noun[0].startswith('any'):
            nom_gr._quantifier='ALL'
        #If the noun starts with 'no' => we have 'none'
        if nom_gr.noun!=[] and nom_gr.noun[0].startswith('no'):
            nom_gr._quantifier='NONE'

    else:

        #If it is a number
        if other_functions.number(nom_gr.det[0])==1:
            nom_gr._quantifier='DIGIT'
            nom_gr.det=[other_functions.convert_to_digit(nom_gr.det[0])]

        #Here we will use the quantifier list
        for i in ResourcePool().det_quantifiers:
            if i[0]==nom_gr.det[0]:
                nom_gr._quantifier=i[1]

        #If we have a plural
        if nom_gr.noun!=[] and nom_gr.noun[0].endswith('s'):
            for x in ResourcePool().nouns_end_s:
                if x==nom_gr.noun[0]:
                    #It is a noun singular with 's' at the end
                    flg=1
                    break
            if flg==0:
                #We delete determinant added in processing with his quantifier
                if nom_gr.det[0]=='a':
                    nom_gr.det=[]
                    nom_gr._quantifier='ONE'
                elif nom_gr.det[0]=='no':
                    nom_gr._quantifier='ANY'

                #We have to put the noun in singular form
                for y in ResourcePool().plural_nouns:
                    #If it is an irregular noun
                    if y[0]==nom_gr.noun[0]:
                        nom_gr.noun[0]=y[1]
                        if nom_gr._quantifier=='ONE':
                            nom_gr._quantifier='ALL'
                        return nom_gr
                #Else
                nom_gr.noun[0]=nom_gr.noun[0][:len(nom_gr.noun[0])-1]
                if nom_gr._quantifier=='ONE':
                    nom_gr._quantifier='ALL'
                return nom_gr

        return nom_gr

def put_rela_from_nncompl_noun(gn):
    """Puts the relative of the complement in the main noun

    :param Nominal_Group gn: nominal group class

    :return: nominal group class
    """

    if gn != []:
        #If empty
        if gn.noun_cmpl == []:
            pass
        else:
            put_rela_from_nncompl_noun(gn.noun_cmpl[0])
            gn.relative=gn.relative+gn.noun_cmpl[0].relative
            gn.noun_cmpl[0].relative=[]

    return gn

def fill_nom_gr (phrase, nom_gr, pos_nom_gr, conjunction):
    """Fills a structure Nominal_Group with given information

    param: list phrase: the raw sentence
    param: nom_gr: the nominal group
    param: pos_nom_gr: its position
    param: conjunction: 'and', 'or' or 'but'

    :return: the nominal group class
    """

    #init
    relative=[]

    #We start by recovering all information we need
    nom_gr_compl = analyse_nominal_group.find_nom_gr_compl (nom_gr, phrase, pos_nom_gr)
    det = analyse_nominal_group.return_det(nom_gr)
    adj = analyse_nominal_group.return_adj(nom_gr)
    adj = analyse_nominal_group.convert_adj_to_digit(adj)
    noun = analyse_nominal_group.return_noun(nom_gr, adj, det)
    adj = analyse_nominal_group.process_adj_quantifier(adj)

    #We process the relative
    begin_pos_rel=analyse_nominal_group.find_relative(nom_gr, phrase, pos_nom_gr, ResourcePool().relatives)
    end_pos_rel=other_functions.recover_end_pos_sub(phrase[begin_pos_rel:], ResourcePool().relatives)

    #There is a relative
    if begin_pos_rel != -1:
        relative_phrase = phrase[begin_pos_rel+1:begin_pos_rel+end_pos_rel-1]
        relative_phrase = other_functions.recover_scd_verb_sub(relative_phrase)

        #If it is a place, we have not to duplicate the nominal group
        if phrase[begin_pos_rel] != 'where':
            relative_phrase = analyse_nominal_group.complete_relative(relative_phrase,nom_gr)

        relative = relative + [analyse_sentence.other_sentence(RELATIVE, phrase[begin_pos_rel], relative_phrase)]

    #If there is a nom_gr_compl, we must make a recursive process for embedded complement
    if nom_gr_compl!=[]:
        gn=Nominal_Group(det,noun,adj,[fill_nom_gr(phrase,nom_gr_compl,pos_nom_gr+len(nom_gr)+1,'AND')],relative)

    else:
        gn=Nominal_Group(det,noun,adj,[],relative)

    #We recover the conjunction
    gn._conjunction=conjunction

    #We recover the quantifier
    recover_quantifier(gn)

    gn=put_rela_from_nncompl_noun(gn)
    return gn



def recover_ns(phrase, analysis, position):
    """ Retrieves the nominal structure of the sentence

    :param list phrase: sentence
    :param Sentence analysis: the instance of class sentence
    :param position: the position of the nominal structure

    :return: the class sentence and sentence
    """

    #init
    conjunction='AND'

    #We recover the first part of the subject
    sbj=analyse_nominal_group.find_sn_pos(phrase, position)

    #We loop until we don't have a nominal group
    while sbj!=[]:

        #We refine the nominal group if there is an error like ending with question mark
        sbj=analyse_nominal_group.refine_nom_gr(sbj)

        analysis.sn= analysis.sn + [fill_nom_gr(phrase, sbj, position, conjunction)]

        #We take off the nominal group
        phrase=analyse_nominal_group.take_off_nom_gr(phrase, sbj, phrase.index(sbj[0]))

        if  phrase[0] in ResourcePool().relatives:
            end_pos_rel=other_functions.recover_end_pos_sub(phrase, ResourcePool().relatives)
            #We remove the relative part of the phrase
            phrase=phrase[end_pos_rel:]

        #If there is 'and', we need to duplicate the information
        if len(phrase)>position and (phrase[position]=='and' or phrase[position]=='or' or phrase[position]==':but'):

            #Reperform the 'and' or 'or' processing
            sbj=analyse_nominal_group.find_sn_pos(phrase[1:], position)

            #We process the 'or' like the 'and' and remove it
            if phrase[position]=='or':
                conjunction='OR'
            elif phrase[position]==':but':
                conjunction='BUT'
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

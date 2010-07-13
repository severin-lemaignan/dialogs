
"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 06/07/2010                                                                       ##
## The package contains functions that recovering all elements of the class sentence##
## We return all elements of a nominal group                                        ##
## Functions:                                                                       ##
##    nom_struc_recovery : to recover nominal structure                             ##
##    indirect_compl_recovery : to recover the indirect object                      ##
##    conjugate_vrb : to conjugate the verb                                         ##
##    vrb_stat_recovery : to recover the verb part of a statement                   ##
##    vrb_ques_recovery : to recover the verb part of a question                    ##
##    end_statement_recovery : to recover the end of the statement                  ##
##    end_question_recovery : to recover the end of the question                    ##
######################################################################################
"""
from resources_manager import ResourcePool
from sentence import *
import sentence_recovery
import other_functions


"""
############################## Statement of lists ####################################
"""
modal_list=['must', 'should', 'may', 'might', 'can', 'could', 'shall']



"""
######################################################################################
## We have to read all past irregular verb forms                                    ##
######################################################################################
"""
past_irreg_vrb = ResourcePool().irregular_verbs_past


"""
######################################################################################
## We have to read all past irregular verb forms                                    ##
######################################################################################
"""
present_irreg_vrb = ResourcePool().irregular_verbs_present


"""
######################################################################################
## This function recovers nominal structure                                         ##
## Input=class nominal structure                                                    ##
## Output=phrase containe all information of this class                             ##
######################################################################################
"""
def nom_struc_recovery(nom_struc):

    #init
    nominal_structure=[]
    i=0

    while i < len(nom_struc):

        #The first nominal group not preceded
        if i > 0:
            #With the flag we put 'or' or 'and'
            if nom_struc[i]._conjunction=='AND':
                nominal_structure=nominal_structure+['and']
            elif nom_struc[i]._conjunction=='OR':
                nominal_structure=nominal_structure+['or']

        #We recover the nominal group and his complement
        nominal_structure = nominal_structure + nom_struc[i].det + nom_struc[i].adj + nom_struc[i].noun
        if nom_struc[i].noun_cmpl!=[]:
            nominal_structure = nominal_structure + ['of']
            nominal_structure=nominal_structure+nom_struc_recovery(nom_struc[i].noun_cmpl)

        #We recover the relative
        for j in nom_struc[i].relative:
            nominal_structure=nominal_structure+['that']+sentence_recovery.statement(j)

        i=i+1

    return nominal_structure


"""
######################################################################################
## This function recovers the indirect object                                       ##
## Input=class indirect object                                                      ##
## Output=phrase containe all information of this class                             ##
######################################################################################
"""
def indirect_compl_recovery(indirect_compl):

    #init
    ind_cmpl=[]

    #We have 2 cases : with preposal and without
    for i in indirect_compl:
        if i.prep!=[]:
            ind_cmpl=ind_cmpl + i.prep + nom_struc_recovery(i.nominal_group)
        else:
            """
            if i.nominal_group[0].adj!=[] and (i.nominal_group[0].adj[0]=='last' or i.nominal_group[0].adj[0]=='next'):
                gr_ind_cmpl=gr_ind_cmpl+gr_nominal(i.nominal_group)
            else:
            """
            ind_cmpl=ind_cmpl+['to']+nom_struc_recovery(i.nominal_group)

    return ind_cmpl


"""
######################################################################################
## This function conjugates the verb                                                ##
## Input=tense, verb in infinitive form, the adverb and subject                     ##
## Output=the verb conjugated                                                       ##
######################################################################################
"""
def conjugate_vrb(tense, verb, sn, type):

    #If there is no tense => we use the present simple
    if tense=='':
        tense='present simple'
    
    
    if sn==[]:
        if type=='imperative':
            #If no subject, we use the third person of plural
            sn=[Nominal_Group([],['they'],[],[],[])]
            
        else:
            #If no subject, we use the third person of singular
            sn=[Nominal_Group([],['it'],[],[],[])]
            
        return conjugate_vrb(tense, verb, sn, type)

    #For future simple
    if tense=='future simple':
        return ['will']+verb

    #For present simple
    elif tense=='present simple':

        if verb[0]=='be':
            #Plural nouns
            if len(sn)>1 or sn[0].noun[0].endswith('s'):
                return ['are']+verb[1:]
            elif sn[0].noun==['I']:
                return ['am']+verb[1:]
            elif sn[0].noun==['we'] or sn[0].noun==['you'] or sn[0].noun==['they']:
                return ['are']+verb[1:]
            else:
                #Singular nouns
                return ['is']+verb[1:]

        else:
            #Plural nouns
            if len(sn)>1 or sn[0].noun[0].endswith('s') or sn[0].noun==['we'] or sn[0].noun==['I'] or sn[0].noun==['you'] or sn[0].noun==['they']:
                return verb
            else:
                #Singular nouns
                for i in present_irreg_vrb:
                    if i[0]==verb[0]:
                        return [i[1]]+verb[1:]
                return [verb[0]+'s']+verb[1:]

    #For past simple
    elif tense=='past simple':

        if verb[0]=='be':
            #Plural nouns
            if len(sn)>1 or sn[0].noun[0].endswith('s') or sn[0].noun==['we'] or sn[0].noun==['I'] or sn[0].noun==['you'] or sn[0].noun==['they']:
                return ['were']+verb[1:]
            else:
                #Singular nouns
                return ['was']+verb[1:]

        else:
            for i in past_irreg_vrb:
                if i[0]==verb[0]:
                    return [i[1]]+verb[1:]
            return [verb[0]+'ed']+verb[1:]

    #For pprogressive forms
    elif tense=='present progressive':
        for m in present_irreg_vrb:
            if m[0]==verb[0]:
                return conjugate_vrb('present simple', ['be'], sn, type)+[m[2]]+verb[1:]
        return conjugate_vrb('present simple', ['be'], sn, type)+[verb[0]+'ing']+verb[1:]
    elif tense=='past progressive':
        for m in present_irreg_vrb:
            if m[0]==verb[0]:
                return conjugate_vrb('past simple', ['be'], sn, type)+[m[2]]+verb[1:]
        return conjugate_vrb('past simple', ['be'], sn, type)+[verb[0]+'ing']+verb[1:]

    #For perfect forms
    elif tense=='present perfect':
        for i in past_irreg_vrb:
            if verb[0]==i[0]:
                return conjugate_vrb('present simple', ['have'], sn, type)+[i[2]]+verb[1:]
        return conjugate_vrb('present simple', ['have'], sn, type)+[verb[0]+'ed']+verb[1:]
    elif tense=='present perfect':
        for i in past_irreg_vrb:
            if verb[0]==i[0]:
                return ['had']+[i[2]]+verb[1:]
        return ['had']+[verb[0]+'ed']+verb[1:]

    #For passive forms
    elif tense=='present passive':
        return conjugate_vrb('present simple', ['be'], sn, type)+conjugate_vrb('present perfect', verb, sn, type)[1:]
    elif tense=='past passive':
        return conjugate_vrb('past simple', ['be'], sn, type)+conjugate_vrb('present perfect', verb, sn, type)[1:]

    #For conditionnal forms
    elif tense=='present conditionnal':
        return ['would']+verb
    elif tense=='past conditionnal':
        return ['would']+conjugate_vrb('present perfect', ['be'], sn, type)

    #Default case
    return []


"""
######################################################################################
## This function recovers the verb part of a statement                              ##
## Input=tense, verb in infinitive form, his state, the adverb and subject          ##
## Output=verb part                                                                 ##
######################################################################################
"""
def vrb_stat_recovery(tense, verb, adv, sn, state, type):

    #init
    vrb_condjugated=[]
    
    #We take of the '+'
    vrb=other_functions.list_recovery(verb[0])

    #If there is modal => no processing
    for i in modal_list:
        if i==vrb[0]:
            vrb_condjugated=vrb
    
    #No modal => normal processing
    if vrb_condjugated==[]:
        vrb_condjugated=conjugate_vrb(tense, vrb, sn, type)

    #Affirmative case
    if state=='affirmative':
        if len(vrb)>1:
            return [vrb_condjugated[0]]+adv+vrb_condjugated[1:]
        else:
            return adv+vrb_condjugated

    #Negative case : we have to use do or have or be or modal if there is no
    elif state=='negative':

        if vrb[0]=='be' or vrb[0]=='do' or vrb[0]=='have':
            return [vrb_condjugated[0]]+['not']+adv+vrb_condjugated[1:]
        if tense!='present simple' and tense!='past simple':
            return [vrb_condjugated[0]]+['not']+adv+vrb_condjugated[1:]
        for i in modal_list:
            if i==vrb[0]:
                return [vrb_condjugated[0]]+['not']+adv+vrb_condjugated[1:]

        return conjugate_vrb(tense, ['do'], sn, type)+['not']+adv+vrb


"""
######################################################################################
## This function recovers the verb part of a question                               ##
## Input=tense, verb in infinitive form, his state, the adverb and subject          ##
## Output=verb part                                                                 ##
######################################################################################
"""
def vrb_ques_recovery(tense, verb, adverb, sn, state):
    
    #We take of the '+'
    vrb=other_functions.list_recovery(verb[0])

    #If there is be or have : it is ok
    if vrb[0]=='be' or vrb[0]=='have':
        vrb_condjugated=conjugate_vrb(tense, vrb, sn, '')
        if state=='negative':
            return [vrb_condjugated[0]]+['not']+adverb+vrb_condjugated[1:]
        return [vrb_condjugated[0]]+adverb+vrb_condjugated[1:]

    #Modal also
    for i in modal_list:
        if i==vrb[0]:
            if state=='negative':
                return [vrb[0]]+['not']+adverb+vrb[1:]
            return [vrb[0]]+adverb+vrb[1:]
    
    if tense=='present simple' or tense=='past simple':
        #We need to add the auxilary
        aux=conjugate_vrb(tense, ['do'], sn,'')
        if state=='negative':
            return aux+['not']+adverb+vrb
        return aux+adverb+vrb
    else:
        vrb_condjugated=conjugate_vrb(tense, vrb, sn,'')
        if state=='negative':
            return [vrb_condjugated[0]]+['not']+adverb+vrb_condjugated[1:]
        return [vrb_condjugated[0]]+adverb+vrb_condjugated[1:]
    

"""
######################################################################################
## This function recovers the end of the statement                                   ##
## Input=class sentence, subject and the verbal structure                           ##
## Output=end of the sentence                                                       ##
######################################################################################
"""
def end_statement_recovery(sentence, sv ,sn, type):

    #Recovering the verb in the correct form
    phrase=vrb_stat_recovery(sv[0].vrb_tense, sv[0].vrb_main, sv[0].vrb_adv, sn, sv[0].state, type)

    #We add the direct and indirect complement
    phrase=phrase+nom_struc_recovery(sv[0].d_obj)
    phrase=phrase+indirect_compl_recovery(sv[0].i_cmpl)

    #We add the adverb of the sentence
    phrase=phrase+sv[0].advrb

    #If there is a second verb
    if sv[0].sv_sec!=[]:
        #Add this verb with 'to'
        phrase=phrase+['to']+sv[0].sv_sec[0].vrb_adv+other_functions.list_recovery(sv[0].sv_sec[0].vrb_main[0])

        #We add the direct and indirect complement
        phrase=phrase+nom_struc_recovery(sv[0].sv_sec[0].d_obj)
        phrase=phrase+indirect_compl_recovery(sv[0].sv_sec[0].i_cmpl)

        #We add the adverb of the sentence
        phrase=phrase+sv[0].sv_sec[0].advrb

    return sentence+phrase


"""
######################################################################################
## This function recovers the end of the question                                   ##
## Input=class sentence, subject and the verbal structure                           ##
## Output=end of the sentence                                                       ##
######################################################################################
"""
def end_question_recovery(sentence, sv ,sn):

    #Recovering the verb in the correct form
    phrase=vrb_ques_recovery(sv[0].vrb_tense, sv[0].vrb_main, sv[0].vrb_adv, sn, sv[0].state)

    #We add the direct and indirect complement
    phrase=phrase+nom_struc_recovery(sv[0].d_obj)
    phrase=phrase+indirect_compl_recovery(sv[0].i_cmpl)

    #We add the adverb of the sentence
    phrase=phrase+sv[0].advrb

    #If there is a second verb
    if sv[0].sv_sec!=[]:
        #Add this verb with 'to'
        phrase=phrase+['to']+sv[0].sv_sec[0].vrb_adv+other_functions.list_recovery(sv[0].sv_sec[0].vrb_main[0])

        #We add the direct and indirect complement
        phrase=phrase+nom_struc_recovery(sv[0].sv_sec[0].d_obj)
        phrase=phrase+indirect_compl_recovery(sv[0].sv_sec[0].i_cmpl)

        #We add the adverb of the sentence
        phrase=phrase+sv[0].sv_sec[0].advrb

    return sentence+phrase


"""
 Created by Chouayakh Mahdi                                                       
 06/07/2010                                                                       
 The package contains functions that recovering all elements of the class sentence
 We return all elements of a nominal group                                        
 Functions:                                                                       
    nom_struc_rebuilding : to recover nominal structure                             
    indirect_compl_rebuilding : to recover the indirect object                      
    conjugate_vrb : to conjugate the verb                                         
    vrb_stat_rebuilding : to recover the verb part of a statement                   
    vrb_ques_rebuilding : to recover the verb part of a question                    
    end_statement_rebuilding : to recover the end of the statement                  
    end_question_rebuilding : to recover the end of the question                    
"""
from dialogs.resources_manager import ResourcePool
from dialogs.sentence import *
import sentence_rebuilding
import other_functions

def nom_struc_rebuilding(nom_struc):
    """
    This function recovers nominal structure                                         
    Input=class nominal structure                                                    
    Output=phrase concatenate all information of this class                             
    """
    
    #init
    nominal_structure=ns=nn=[]
    i=0 
    
    while i < len(nom_struc):
        
        if nom_struc[i]._quantifier=='SOME' and (nom_struc[i].det==['a'] or nom_struc[i].det==['an']):
            nom_struc[i]._quantifier='ONE'
            
        #The first nominal group not preceded but 'and' if there is
        if nom_struc[i]._conjunction=='AND' and i > 0:
            nominal_structure=nominal_structure+['and']
        elif nom_struc[i]._conjunction=='OR':
            nominal_structure=nominal_structure+['or']
        elif nom_struc[i]._conjunction=='BUT':
            nominal_structure=nominal_structure+['but']
        
        #We recover the nominal group and his complement
        if nom_struc[i]._quantifier=='SOME' or nom_struc[i]._quantifier=='ALL' or nom_struc[i]._quantifier=='ANY' or (nom_struc[i]._quantifier=='DIGIT' and nom_struc[i].det!='one'):
            #If there is a specific quantifier (plural)
            for n in ResourcePool().plural_nouns:
                if nom_struc[i].noun!=[] and n[1]==nom_struc[i].noun[0]:
                    nn=[n[0]]
            
            #If it is not a specific plural, we add 's'
            if nom_struc[i].noun!=[] and nn==[]:
                nn=[nom_struc[i].noun[0]+'s']
            
            #We reconver the other information   
            nominal_structure = nominal_structure + nom_struc[i].det
            for z in nom_struc[i].adj:
                nominal_structure = nominal_structure+z[1]+[z[0]]
            nominal_structure = nominal_structure+nn
            
            #Re-init
            nn=[]
            
        else:
            #if not plural
            nominal_structure = nominal_structure + nom_struc[i].det
            for z in nom_struc[i].adj:
                nominal_structure = nominal_structure+z[1]+[z[0]]
            nominal_structure = nominal_structure+nom_struc[i].noun
        
        #We recover noun complement
        if nom_struc[i].noun_cmpl:
            nominal_structure = nominal_structure + ['of']
            nominal_structure=nominal_structure+nom_struc_rebuilding(nom_struc[i].noun_cmpl)

        #We recover the relative
        for j in nom_struc[i].relative:
            if not j.sn:
                ns=[nom_struc[i]]
        
            nominal_structure=nominal_structure+[j.aim]+sentence_rebuilding.relative(j, ns)
            ns=[]

        i += 1
    return nominal_structure



def indirect_compl_rebuilding(indirect_compl):
    """
    This function recovers the indirect object                                       
    Input=class indirect object                                                      
    Output=phrase concatenate all information of this class                             
    """

    #init
    ind_cmpl=[]
    k=0

    #We have 2 cases : with proposal and without
    if indirect_compl.prep:
        nom_gr= nom_struc_rebuilding(indirect_compl.gn)
        
        #If we have another i_cmpl with a different preposition
        if nom_gr!=[] and (nom_gr[0]=='and' or nom_gr[0]=='or' or nom_gr[0]=='but'):
            nom_gr=[nom_gr[0]]+indirect_compl.prep+nom_gr[1:]
        else:
            nom_gr=indirect_compl.prep+nom_gr
        
        #For a preposition we can have different i_cmpl with different conjunctions
        while k < len(nom_gr):
            if (nom_gr[k]=='or' or nom_gr[k]=='but') and nom_gr[k+1]!=indirect_compl.prep[0]:
                nom_gr=nom_gr[:k+1]+indirect_compl.prep+nom_gr[k+1:]
            k += 1
        
    else:
        nom_gr= indirect_compl.prep + nom_struc_rebuilding(indirect_compl.gn)
            
    ind_cmpl=ind_cmpl+nom_gr
    return ind_cmpl



def conjugate_vrb(tense, verb, sn, type, aim):
    """
    conjugates the verb                                                
    Input=tense, verb in infinitive form, the adverb and subject                     
    Output=the verb conjugated                                                       
    """
    
    #If there is no tense => we use the present simple
    if tense=='':
        tense='present simple'
    
    if aim.startswith('classification'):
        if not sn:
            sn=[Nominal_Group([],[aim[15:]],[],[],[])]
        elif not sn[0].noun:
            sn[0].noun=[aim[15:]]
            
    if not sn:
        if type==IMPERATIVE:
            #If no subject, we use the third person of plural
            sn=[Nominal_Group([],['they'],[],[],[])]
        else:
            #If no subject, we use the third person of singular
            sn=[Nominal_Group([],['it'],[],[],[])]

    #For future simple
    if tense=='future simple':
        return ['will']+verb

    #For present simple
    elif tense=='present simple':

        if verb[0]=='be':
            #Plural nouns
            if sn[0].noun==['I']:
                return ['am']+verb[1:]
            elif other_functions.plural_noun(sn)==1:
                return ['are']+verb[1:]
            elif sn[0].noun==['we'] or sn[0].noun==['you'] or sn[0].noun==['they']:
                return ['are']+verb[1:]
            else:
                #Singular nouns
                return ['is']+verb[1:]

        else:
            #Plural nouns
            if other_functions.plural_noun(sn)==1:
                return verb
            else:
                #Singular nouns
                for i in ResourcePool().irregular_verbs_present:
                    if i[0]==verb[0]:
                        return [i[1]]+verb[1:]
                return [verb[0]+'s']+verb[1:]

    #For past simple
    elif tense=='past simple':

        if verb[0]=='be':
            if sn[0].noun==['I']:
                return ['was']+verb[1:]
            #Plural nouns
            elif other_functions.plural_noun(sn)==1:
                return ['were']+verb[1:]
            else:
                #Singular nouns
                return ['was']+verb[1:]

        else:
            for i in ResourcePool().irregular_verbs_past:
                if i[0]==verb[0]:
                    return [i[1]]+verb[1:]
            return [verb[0]+'ed']+verb[1:]

    #For progressive forms
    elif tense=='present progressive':
        for m in ResourcePool().irregular_verbs_present:
            if m[0]==verb[0]:
                return conjugate_vrb('present simple', ['be'], sn, type, aim)+[m[2]]+verb[1:]
        return conjugate_vrb('present simple', ['be'], sn, type, aim)+[verb[0]+'ing']+verb[1:]
    elif tense=='past progressive':
        for m in ResourcePool().irregular_verbs_present:
            if m[0]==verb[0]:
                return conjugate_vrb('past simple', ['be'], sn, type, aim)+[m[2]]+verb[1:]
        return conjugate_vrb('past simple', ['be'], sn, type, aim)+[verb[0]+'ing']+verb[1:]

    #For perfect forms
    elif tense=='present perfect':
        for i in ResourcePool().irregular_verbs_past:
            if verb[0]==i[0]:
                return conjugate_vrb('present simple', ['have'], sn, type, aim)+[i[2]]+verb[1:]
        return conjugate_vrb('present simple', ['have'], sn, type, aim)+[verb[0]+'ed']+verb[1:]
    elif tense=='present perfect':
        for i in ResourcePool().irregular_verbs_past:
            if verb[0]==i[0]:
                return ['had']+[i[2]]+verb[1:]
        return ['had']+[verb[0]+'ed']+verb[1:]

    #For passive forms
    elif tense=='present passive':
        return conjugate_vrb('present simple', ['be'], sn, type, aim)+conjugate_vrb('present perfect', verb, sn, type, aim)[1:]
    elif tense=='past passive':
        return conjugate_vrb('past simple', ['be'], sn, type, aim)+conjugate_vrb('present perfect', verb, sn, type, aim)[1:]

    #For conditional forms
    elif tense=='present conditional':
        return ['would']+verb
    elif tense=='past conditional':
        return ['would']+conjugate_vrb('present perfect', verb, sn, type, aim)

    #Default case
    return []



def vrb_stat_rebuilding(tense, verb, adv, sn, state, type, aim):
    """
    This function recovers the verb part of a statement                              
    Input=tense, verb in infinitive form, his state, the adverb and subject          
    Output=verb part                                                                 
    """

    #init
    vrb_condjugated=[]
    
    #If verb is empty
    if not verb:
        return []
    
    #We take of the '+'
    vrb=other_functions.list_rebuilding(verb[0])

    #If there is modal => no processing
    for i in ResourcePool().modal:
        if i==vrb[0]:
            vrb_condjugated=vrb
    
    #No modal => normal processing
    if not vrb_condjugated:
        vrb_condjugated=conjugate_vrb(tense, vrb, sn, type, aim)
    elif tense=='present passive' or tense=='passive conditional':
        vrb_condjugated=[vrb[0]]+['be']+conjugate_vrb('present passive', vrb[1:], sn,'', aim)[1:]

    #Affirmative case
    if state==Verbal_Group.affirmative:
        if len(vrb)>1:
            return [vrb_condjugated[0]]+adv+vrb_condjugated[1:]
        else:
            return adv+vrb_condjugated

    #Negative case : we have to use do or have or be or modal if there is no
    elif state==Verbal_Group.negative:

        if vrb[0]=='be' or vrb[0]=='do' or vrb[0]=='have':
            return [vrb_condjugated[0]]+['not']+adv+vrb_condjugated[1:]
        if tense!='present simple' and tense!='past simple':
            return [vrb_condjugated[0]]+['not']+adv+vrb_condjugated[1:]
        for i in ResourcePool().modal:
            if i==vrb[0]:
                return [vrb_condjugated[0]]+['not']+adv+vrb_condjugated[1:]

        return conjugate_vrb(tense, ['do'], sn, type, aim)+['not']+adv+vrb



def vrb_ques_rebuilding(tense, verb, adverb, sn, state, aim):
    """
    recovers the verb part of a question                               
    Input=tense, verb in infinitive form, his state, the adverb and subject          
    Output=verb part                                                                 
    """
    #If verb is empty
    if not verb:
        return []
    
    #We take of the '+'
    vrb=other_functions.list_rebuilding(verb[0])
    
    #If there is be or have : it is ok
    if vrb[0]=='be' or vrb[0]=='have':
        vrb_condjugated=conjugate_vrb(tense, vrb, sn, '', aim)
        if state==Verbal_Group.negative:
            return [vrb_condjugated[0]]+['not']+adverb+vrb_condjugated[1:]
        return [vrb_condjugated[0]]+adverb+vrb_condjugated[1:]

    #Modal also
    for i in ResourcePool().modal:
        if i==vrb[0]:
            if state==Verbal_Group.negative:
                if tense=='present passive' or tense=='passive conditional':
                    return [vrb[0]]+['not']+adverb+['be']+conjugate_vrb('present passive', vrb[1:], sn,'', aim)[1:]
                return [vrb[0]]+['not']+adverb+vrb[1:]
            elif tense=='present passive' or tense=='passive conditional':
                return [vrb[0]]+adverb+['be']+conjugate_vrb('present passive', vrb[1:], sn,'', aim)[1:]
            return [vrb[0]]+adverb+vrb[1:]
    
    if tense=='present simple' or tense=='past simple':
        #We need to add the auxilary
        aux=conjugate_vrb(tense, ['do'], sn,'', aim)
        if state==Verbal_Group.negative:
            return aux+['not']+adverb+vrb
        return aux+adverb+vrb
    else:
        vrb_condjugated=conjugate_vrb(tense, vrb, sn,'', aim)
        if state==Verbal_Group.negative:
            return [vrb_condjugated[0]]+['not']+adverb+vrb_condjugated[1:]
        return [vrb_condjugated[0]]+adverb+vrb_condjugated[1:]
    
    

def scd_vrb_rebuilding(sec_vrb, phrase, flg):
    """
    recovers the part of the second verb                                 
    Input=class sentence, phrase and a flag                       
    Output=phrase                                                    
    """
    
    if flg==1:
        phrase=phrase+sec_vrb.vrb_adv+other_functions.list_rebuilding(sec_vrb.vrb_main[0])
    else:
        #Add this verb with 'to'
        phrase=phrase+['to']+sec_vrb.vrb_adv+other_functions.list_rebuilding(sec_vrb.vrb_main[0])

    #We add the direct and indirect complement
    if sec_vrb.i_cmpl!=[] and sec_vrb.i_cmpl[0].prep!=[]:
        phrase=phrase+nom_struc_rebuilding(sec_vrb.d_obj)
        for x in sec_vrb.i_cmpl:
            phrase=phrase+indirect_compl_rebuilding(x)
    else:
        if sec_vrb.i_cmpl:
            phrase=phrase+indirect_compl_rebuilding(sec_vrb.i_cmpl[0])
        phrase=phrase+nom_struc_rebuilding(sec_vrb.d_obj)
        #init
        x=1
        while x < len(sec_vrb.i_cmpl):
            phrase=phrase+indirect_compl_rebuilding(sec_vrb.i_cmpl[x])
            x += 1
    
    flag=0
    for j in ResourcePool().verb_need_to:
        if sec_vrb.vrb_main[0]==j:
            flag=1      
    
    for z in sec_vrb.sv_sec:       
        phrase=scd_vrb_rebuilding(z, phrase,flag)
        
    #We add the adverb of the sentence
    phrase=phrase+sec_vrb.advrb
        
    return phrase



def end_statement_rebuilding(sentence, sv ,sn, type, aim):
    """
    recovers the end of the statement                                   
    Input=class sentence, subject and the verbal structure                           
    Output=end of the sentence                                                       
    """

    #Recovering the verb in the correct form
    phrase=vrb_stat_rebuilding(sv[0].vrb_tense, sv[0].vrb_main, sv[0].vrb_adv, sn, sv[0].state, type, aim)

    #We add the direct and indirect complement
    if sv[0].i_cmpl!=[] and sv[0].i_cmpl[0].prep!=[]:
        phrase=phrase+nom_struc_rebuilding(sv[0].d_obj)
        for x in sv[0].i_cmpl:
            phrase=phrase+indirect_compl_rebuilding(x)
    else:
        if sv[0].i_cmpl:
            phrase=phrase+indirect_compl_rebuilding(sv[0].i_cmpl[0])
        phrase=phrase+nom_struc_rebuilding(sv[0].d_obj)
        #init
        x=1
        while x < len(sv[0].i_cmpl):
            phrase=phrase+indirect_compl_rebuilding(sv[0].i_cmpl[x])
            x += 1

    #We add the adverb of the sentence
    phrase=phrase+sv[0].advrb
    
    flag=0
    for j in ResourcePool().verb_need_to:
        if sv[0].vrb_main==[j]:
            flag=1
    
    #If there is a second verb
    for k in sv[0].sv_sec:
        phrase= scd_vrb_rebuilding(k, phrase, flag)

    return sentence+phrase



def end_question_rebuilding(sentence, sv ,sn, aim):
    """
    recovers the end of the question                                   
    Input=class sentence, subject and the verbal structure                           
    Output=end of the sentence                                                       
    """
    
    #Recovering the verb in the correct form
    phrase=vrb_ques_rebuilding(sv[0].vrb_tense, sv[0].vrb_main, sv[0].vrb_adv, sn, sv[0].state, aim)

    #We add the direct and indirect complement
    if sv[0].i_cmpl!=[] and sv[0].i_cmpl[0].prep!=[]:
        phrase=phrase+nom_struc_rebuilding(sv[0].d_obj)
        for x in sv[0].i_cmpl:
            phrase=phrase+indirect_compl_rebuilding(x)
    else:
        if sv[0].i_cmpl:
            phrase=phrase+indirect_compl_rebuilding(sv[0].i_cmpl[0])
        phrase=phrase+nom_struc_rebuilding(sv[0].d_obj)
        
        #init
        x=1
        while x < x < len(sv[0].i_cmpl):
            phrase=phrase+indirect_compl_rebuilding(sv[0].i_cmpl[x])
            x += 1
        
        flag=0
        for j in ResourcePool().verb_need_to:
            if sv[0].vrb_main==[j]:
                flag=1
                
        #If there is a second verb
        for k in sv[0].sv_sec:
            phrase= scd_vrb_rebuilding(k, phrase,flag)
        
    #We add the adverb of the sentence
    phrase=phrase+sv[0].advrb
    return sentence+phrase

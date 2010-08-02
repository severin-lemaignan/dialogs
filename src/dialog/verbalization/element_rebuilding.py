
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
from resources_manager import ResourcePool
from sentence import *
import sentence_rebuilding
import other_functions


"""
Statement of lists
"""
modal_list=['must', 'should', 'may', 'might', 'can', 'could', 'shall']
pronoun_list=['you', 'I', 'we', 'he', 'she', 'me', 'it', 'he', 'they', 'yours', 'mine', 'him']
irreg_plur_noun=[('glasses','glass'),('busses','bus')]



"""
We have to read all past irregular verb forms                                    
"""
past_irreg_vrb = ResourcePool().irregular_verbs_past


"""
We have to read all past irregular verb forms                                    
"""
present_irreg_vrb = ResourcePool().irregular_verbs_present



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
        #The first nominal group not preceded
        if i > 0:
            #With the flag we put 'or' or 'and'
            if nom_struc[i]._conjunction=='AND':
                nominal_structure=nominal_structure+['and']
            elif nom_struc[i]._conjunction=='OR':
                nominal_structure=nominal_structure+['or']
            elif nom_struc[i]._conjunction=='BUT':
                nominal_structure=nominal_structure+['but']
        
        #We can have an 'or' with the first element if it is an indirect complement       
        if nom_struc[i]._conjunction=='OR':
            nominal_structure=nominal_structure+['or']
        
        #We recover the nominal group and his complement
        if nom_struc[i]._quantifier=='SOME' or nom_struc[i]._quantifier=='ALL' or (nom_struc[i]._quantifier=='DIGIT' and nom_struc[i].det!='one'):
            for n in irreg_plur_noun:
                if nom_struc[i].noun!=[] and n[1]==nom_struc[i].noun[0]:
                    nn=[n[0]]
            if nom_struc[i].noun!=[] and nn==[]:
                nn=[nom_struc[i].noun[0]+'s']
            nominal_structure = nominal_structure + nom_struc[i].det + nom_struc[i].adj +nn
        else:
            nominal_structure = nominal_structure + nom_struc[i].det + nom_struc[i].adj +nom_struc[i].noun
        
        if nom_struc[i].noun_cmpl!=[]:
            nominal_structure = nominal_structure + ['of']
            nominal_structure=nominal_structure+nom_struc_rebuilding(nom_struc[i].noun_cmpl)

        #We recover the relative
        for j in nom_struc[i].relative:
            if j.sn==[]:
                ns=[nom_struc[i]]
        
            nominal_structure=nominal_structure+[j.aim]+sentence_rebuilding.relative(j, ns)
            ns=[]

        i=i+1

    return nominal_structure



def indirect_compl_rebuilding(indirect_compl):
    """
    This function recovers the indirect object                                       
    Input=class indirect object                                                      
    Output=phrase concatenate all information of this class                             
    """

    #init
    ind_cmpl=[]

    #We have 2 cases : with preposal and without
    if indirect_compl.prep!=[]:
        nom_gr= nom_struc_rebuilding(indirect_compl.nominal_group)
        
        if nom_gr!=[] and (nom_gr[0]=='and' or nom_gr[0]=='or'):
            nom_gr=[nom_gr[0]]+indirect_compl.prep+nom_gr[1:]
        else:
            nom_gr=indirect_compl.prep+nom_gr
           
    else:
        """
        if i.nominal_group[0].adj!=[] and (i.nominal_group[0].adj[0]=='last' or i.nominal_group[0].adj[0]=='next'):
            gr_ind_cmpl=gr_ind_cmpl+gr_nominal(i.nominal_group)
        else:
        """
        nom_gr= indirect_compl.prep + nom_struc_rebuilding(indirect_compl.nominal_group)
            
    ind_cmpl=ind_cmpl+nom_gr
    return ind_cmpl



def conjugate_vrb(tense, verb, sn, type, aim):
    """
    This function conjugates the verb                                                
    Input=tense, verb in infinitive form, the adverb and subject                     
    Output=the verb conjugated                                                       
    """
    
    #If there is no tense => we use the present simple
    if tense=='':
        tense='present simple'
    
    if aim.startswith('classification'):
        if sn==[]:
            sn=[Nominal_Group([],[aim[15:]],[],[],[])]
        elif sn[0].noun==[]:
            sn[0].noun=[aim[15:]]
            
    if sn==[]:
        if type=='imperative':
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
                for i in present_irreg_vrb:
                    if i[0]==verb[0]:
                        return [i[1]]+verb[1:]
                return [verb[0]+'s']+verb[1:]

    #For past simple
    elif tense=='past simple':

        if verb[0]=='be':
            #Plural nouns
            if other_functions.plural_noun(sn)==1:
                return ['were']+verb[1:]
            else:
                #Singular nouns
                return ['was']+verb[1:]

        else:
            for i in past_irreg_vrb:
                if i[0]==verb[0]:
                    return [i[1]]+verb[1:]
            return [verb[0]+'ed']+verb[1:]

    #For progressive forms
    elif tense=='present progressive':
        for m in present_irreg_vrb:
            if m[0]==verb[0]:
                return conjugate_vrb('present simple', ['be'], sn, type, aim)+[m[2]]+verb[1:]
        return conjugate_vrb('present simple', ['be'], sn, type, aim)+[verb[0]+'ing']+verb[1:]
    elif tense=='past progressive':
        for m in present_irreg_vrb:
            if m[0]==verb[0]:
                return conjugate_vrb('past simple', ['be'], sn, type, aim)+[m[2]]+verb[1:]
        return conjugate_vrb('past simple', ['be'], sn, type, aim)+[verb[0]+'ing']+verb[1:]

    #For perfect forms
    elif tense=='present perfect':
        for i in past_irreg_vrb:
            if verb[0]==i[0]:
                return conjugate_vrb('present simple', ['have'], sn, type, aim)+[i[2]]+verb[1:]
        return conjugate_vrb('present simple', ['have'], sn, type, aim)+[verb[0]+'ed']+verb[1:]
    elif tense=='present perfect':
        for i in past_irreg_vrb:
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
    if verb==[]:
        return []
    
    #We take of the '+'
    vrb=other_functions.list_rebuilding(verb[0])

    #If there is modal => no processing
    for i in modal_list:
        if i==vrb[0]:
            vrb_condjugated=vrb
    
    #No modal => normal processing
    if vrb_condjugated==[]:
        vrb_condjugated=conjugate_vrb(tense, vrb, sn, type, aim)
    elif tense=='present passive' or tense=='passive conditional':
        vrb_condjugated=[vrb[0]]+['be']+conjugate_vrb('present passive', vrb[1:], sn,'', aim)[1:]

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

        return conjugate_vrb(tense, ['do'], sn, type, aim)+['not']+adv+vrb



def vrb_ques_rebuilding(tense, verb, adverb, sn, state, aim):
    """
    This function recovers the verb part of a question                               
    Input=tense, verb in infinitive form, his state, the adverb and subject          
    Output=verb part                                                                 
    """
    #If verb is empty
    if verb==[]:
        return []
    
    #We take of the '+'
    vrb=other_functions.list_rebuilding(verb[0])
    
    #If there is be or have : it is ok
    if vrb[0]=='be' or vrb[0]=='have':
        vrb_condjugated=conjugate_vrb(tense, vrb, sn, '', aim)
        if state=='negative':
            return [vrb_condjugated[0]]+['not']+adverb+vrb_condjugated[1:]
        return [vrb_condjugated[0]]+adverb+vrb_condjugated[1:]

    #Modal also
    for i in modal_list:
        if i==vrb[0]:
            if state=='negative':
                if tense=='present passive' or tense=='passive conditional':
                    return [vrb[0]]+['not']+adverb+['be']+conjugate_vrb('present passive', vrb[1:], sn,'', aim)[1:]
                return [vrb[0]]+['not']+adverb+vrb[1:]
            elif tense=='present passive' or tense=='passive conditional':
                return [vrb[0]]+adverb+['be']+conjugate_vrb('present passive', vrb[1:], sn,'', aim)[1:]
            return [vrb[0]]+adverb+vrb[1:]
    
    if tense=='present simple' or tense=='past simple':
        #We need to add the auxilary
        aux=conjugate_vrb(tense, ['do'], sn,'', aim)
        if state=='negative':
            return aux+['not']+adverb+vrb
        return aux+adverb+vrb
    else:
        vrb_condjugated=conjugate_vrb(tense, vrb, sn,'', aim)
        if state=='negative':
            return [vrb_condjugated[0]]+['not']+adverb+vrb_condjugated[1:]
        return [vrb_condjugated[0]]+adverb+vrb_condjugated[1:]
    


def end_statement_rebuilding(sentence, sv ,sn, type, aim):
    """
    This function recovers the end of the statement                                   
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
        if sv[0].i_cmpl!= []:
            phrase=phrase+indirect_compl_rebuilding(sv[0].i_cmpl[0])
        phrase=phrase+nom_struc_rebuilding(sv[0].d_obj)
        #init
        x=1
        while x < len(sv[0].i_cmpl):
            phrase=phrase+indirect_compl_rebuilding(sv[0].i_cmpl[x])
            x=x+1

    #We add the adverb of the sentence
    phrase=phrase+sv[0].advrb

    #If there is a second verb
    for k in sv[0].sv_sec:
        #Add this verb with 'to'
        phrase=phrase+['to']+k.vrb_adv+other_functions.list_rebuilding(k.vrb_main[0])
        
        #We add the direct and indirect complement
        if k.i_cmpl!=[] and k.i_cmpl[0].prep!=[]:
            phrase=phrase+nom_struc_rebuilding(k.d_obj)
            for x in k.i_cmpl:
                phrase=phrase+indirect_compl_rebuilding(x)
        else:
            if k.i_cmpl!=[]:
                phrase=phrase+indirect_compl_rebuilding(k.i_cmpl[0])
            phrase=phrase+nom_struc_rebuilding(k.d_obj)
            #init
            x=1
            while x < len(k.i_cmpl):
                phrase=phrase+indirect_compl_rebuilding(k.i_cmpl[x])
                x=x+1

        #We add the adverb of the sentence
        phrase=phrase+k.advrb

    return sentence+phrase



def end_question_rebuilding(sentence, sv ,sn, aim):
    """
    This function recovers the end of the question                                   
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
        if sv[0].i_cmpl!= []:
            phrase=phrase+indirect_compl_rebuilding(sv[0].i_cmpl[0])
        phrase=phrase+nom_struc_rebuilding(sv[0].d_obj)
        
        #init
        x=1
        while x < x < len(sv[0].i_cmpl):
            phrase=phrase+indirect_compl_rebuilding(sv[0].i_cmpl[x])
            x=x+1
            
            
    #We add the adverb of the sentence
    phrase=phrase+sv[0].advrb

    #If there is a second verb
    for k in sv[0].sv_sec:
        #Add this verb with 'to'
        phrase=phrase+['to']+k.vrb_adv+other_functions.list_rebuilding(k.vrb_main[0])

        #We add the direct and indirect complement
        if k.i_cmpl!=[] and k.i_cmpl[0].prep!=[]:
            phrase=phrase+nom_struc_rebuilding(k.d_obj)
            for x in k.i_cmpl:
                phrase=phrase+indirect_compl_rebuilding(x)
        else:
            if k.i_cmpl!=[]:
                phrase=phrase+indirect_compl_rebuilding(k.i_cmpl[0])
            phrase=phrase+nom_struc_rebuilding(k.d_obj)
            #init
            x=1
            while x < len(k.i_cmpl):
                phrase=phrase+indirect_compl_rebuilding(k.i_cmpl[x])
                x=x+1

        #We add the adverb of the sentence
        phrase=phrase+k.advrb

    return sentence+phrase

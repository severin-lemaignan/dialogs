#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN:rev202 + PythonTidy + rewrite 'toString' methods using Python __str__ + test cases

from helpers import colored_print #to colorize the sentence output
from resources_manager import ResourcePool


"""
Statement of lists
"""
pronoun_list=['you', 'I', 'we', 'he', 'she', 'me', 'it', 'he', 'they', 'yours', 'mine', 'him']
adverbial_list=['in', 'on', 'at', 'from', 'for', 'next', 'last', 'behind','behind+to',
                'next+to','in+front+of', 'into','in+spite+of','because+of','despite']


class SentenceFactory:
    
    def create_w_question_choice(self, obj_name, feature, values):
        """ Creates sentences of type: 
            Which color is the bottle? Blue or yellow.
        """
        
        nominal_groupL = [Nominal_Group([],[],[val],[],[]) for val in values]
        
        sentence = [Sentence('w_question', 'choice', 
                        [Nominal_Group([],[feature],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [Nominal_Group(['the'],[obj_name],[],[],[])], 
                            [], [], [] ,'affirmative',[])]),
                    Sentence('statement', '',nominal_groupL,[])]
        
                            
        for i in range(len(values)-1):
            sentence[1].sn[i+1]._conjunction = 'OR'
        
        return sentence
        
    def create_w_question_location(self, obj_name, feature, values):
        """ Creates sentences of type: 
                "Where is the box? On the table or on the shelf?"
        """
        indirect_complL = [Indirect_Complement([feature],[Nominal_Group(['the'],[val],[],[],[])]) \
                            for val in values]
                            
        sentence = [Sentence('w_question', 'place',
                        [Nominal_Group(['the'],[obj_name],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                        [], [], [], [] ,'affirmative',[])]),
                    Sentence('yes_no_question', '', [], 
                        [Verbal_Group([], [],'', 
                            [], indirect_complL, [], [] ,'affirmative',[])])]
                
        for i in range(len(values)-1):
            sentence[1].sv[0].i_cmpl[i+1].nominal_group[0]._conjunction = 'OR'
            
        return sentence

    def create_w_question_location_PT(self, values, agent):
        """ Creates sentences of type: 
            "Is it on your left or in front of you?"
        """
        
        indirect_complL = []
        
        for val in values:
            
            if 'right' in val.lower() or 'left' in val.lower():
                if agent == 'myself': det = 'my'
                else: det = 'your'
                indirect_complL.append(Indirect_Complement(['on'],[Nominal_Group([det],[val],[],[],[])]))
            else:
                if agent == 'myself': det = 'me'
                else: det = 'you'

                if 'back' in val.lower(): prep = 'behind'
                elif 'front' in val.lower(): prep = 'in front of'
                else: prep = None
                
                indirect_complL.append(Indirect_Complement([prep],[Nominal_Group([],[det],[],[],[])]))

        sentence = [Sentence('yes_no_question', '', 
                        [Nominal_Group([],['it'],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [], indirect_complL, [], [] ,'affirmative',[])])]
                    
        for i in range(len(values)-1):
            sentence[0].sv[0].i_cmpl[i+1].nominal_group[0]._conjunction = 'OR'
            
        return sentence
    
    def create_what_do_you_mean_reference(self, object):
        """ Creates sentences of type: 
            "The bottle? What do you mean?"
        """
        
        sentence = [Sentence('yes_no_question', '', [object], []),
                    Sentence('w_question', 'thing', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['mean'], [],'present simple', [], [], [], [] ,'affirmative',[])])]
        return sentence
    
    
    def create_do_you_mean_reference(self, object):
        """ Creates sentences: 
            "Do you mean the bottle?"
        """
        
        return [Sentence('yes_no_question', '', 
                    [Nominal_Group([],['you'],[],[],[])], 
                    [Verbal_Group(['mean'], [],'present simple', [object], [], [], [] ,'affirmative',[])])]
        
        
    
    def create_w_question_answer(self, w_question, w_answer, query_on_field):
        """Create the answer of a W-Question
            w_question is the current question
            w_answer is the response found in the ontology
            query_on_field is the part of the W_question to fill with the answer. it takes the following values:
                - None :
                - QUERY_ON_INDIRECT_OBJ
                - QUERY_ON_DIRECT_OBJ
        """
        nominal_groupL = []
        #Nominal group holding the answer
        
        
        if w_question.aim in ['color', 'size']: #TODO in ResourcePool, list of adjective with given class in the ontology
            nominal_groupL = [Nominal_Group([], [], w_answer, [], [])]
        
        else:
            for response in w_answer:
                ng = self.create_w_question_object(response)
                nominal_groupL.append(ng)
            
        #Sentence holding the answer
        
        sentence = self.reverse_personal_pronoun(w_question)
        sentence.data_type = "statement"
        
        if not query_on_field:#Default case on sentence.sn
            sentence.sn = nominal_groupL
            
        elif query_on_field == 'QUERY_ON_DIRECT_OBJ':
            sentence.sv[0].d_obj = nominal_groupL
        
        elif query_on_field == 'QUERY_ON_INDIRECT_OBJ':
            #preposition
            if w_question.aim == 'place':
                prep = ['at']
            elif w_question.aim == 'people':
                prep = ['to']
            else:
                prep = []
                
            sentence.sv[0].i_cmpl = [Indirect_Complement(prep, nominal_groupL)]
            
        
        return [sentence]
    
    
    def reverse_personal_pronoun(self, sentence):
        """ transforming all the nominal group in a sentence with the following rules:
            You -> Me, I
            I, Me -> you
            my -> your
            your -> my
         """        
        def _reverse_noun_group_personal_pronoun(nominal_groupL, subject = True):
            """Transforming within a group of nominal group"""
            for ng in nominal_groupL:
                #Determinant
                if ng.det and ng.det == ['my']:
                    ng.det = ['your']
                elif ng.det and ng.det == ['your']:
                    ng.det = ['my']
                
                #Noun
                if ng.noun and ng.noun == ['you']:
                    ng.noun = ['I'] if subject else ['me'] 
                elif ng.noun and ng.noun == ['I', 'me']:
                    ng.noun = ['you']
                else:
                    pass             
            return nominal_groupL
            
        #Subject sentence.sn
        if sentence.sn:
            sentence.sn = _reverse_noun_group_personal_pronoun(sentence.sn)
            
        for sv in sentence.sv:
            #Direct object
            if sv.d_obj:
                sv.d_obj = _reverse_noun_group_personal_pronoun(sv.d_obj, False)
                
            #Indirect complement
            for i_cmpl in sv.i_cmpl:
                i_cmpl.nominal_group = _reverse_noun_group_personal_pronoun(i_cmpl.nominal_group)
                
        
        return sentence
        
        
        
    def create_w_question_object(self, object):
        """Creating a nominal group by retrieving relevant information on 'object'."""
        
        
        def _filter_ontology_inferred_class(object_list):
            """Filtering infered class from the ontology such as SpatialThing, EnduringThing-Localized, ... that add no needed infos """
            #TODO in ResourcePool()
            filter_list = ['Object', 'Location', 
                            'Agent', 'SpatialThing-Localized', 'SpatialThing',
                            'PartiallyTangible', 
                            'EnduringThing-Localized', 'Object-SupportingFurniture', 
                            'Artifact', 'PhysicalSupport', 'owl:Thing', 'owl:thing',
                            'Place', 'Furniture']
                        
            if not object_list:
                return ['owl:thing']
            
            result_list = []
            for item in object_list:
                if not item in filter_list:
                    result_list.append(item)
            
            return result_list if result_list else ['owl:thing']
            
        #end of _filter_ontology_inferred_class
        
        #Creating object components : Det, Noun, noun-cmpl, etc.
        
        # Label if Proper noun
        object_noun = []
        object_determiner = []
        
        onto = []
        try:
           onto = ResourcePool().ontology_server.find('?concept', [object + ' rdfs:label ?concept'])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
        
        if onto:
            object_noun = onto # name must be unique for a given object
            
            return Nominal_Group([], object_noun, [], [], [])#No need to go further as we know the label now
            
            
        # Class Type if Common noun or Id
        else:
            try:
               onto = ResourcePool().ontology_server.find('?concept', [object + ' rdf:type ?concept'])
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            
            object_noun = [_filter_ontology_inferred_class(onto)[0].lower()]
            
            if object_noun == ['owl:thing']:
                object_noun = [object]
                
            object_determiner = ['the']
        
        
        
        # Adjectives or Object Features 
        object_features = []
        description = [' hasFeature ', ' hasSize ']
        for desc in description:
            onto = []
            try:
               onto = ResourcePool().ontology_server.find('?concept', [object + desc + '?concept'])
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
                
            if onto:
                object_features.extend(onto)        
        
        # Object Location
        object_location = []
        description = [' isNexto ', ' isLocated ', ' isOn ', ' isIn ', ' hasGoal ', ' receivedBy ']
                        
        for desc in description:
            onto = []
            try:
               onto = ResourcePool().ontology_server.find('?concept', [object + desc + '?concept'])
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            
            #Match preposition with description
            prep = ''
            if desc == ' isNexto ':
                prep = 'next+to'
            elif desc == ' isLocated ':
                if 'BACK' in onto:
                    prep = 'behind'
                elif 'FRONT' in onto:
                    prep = 'in+front+of'
                elif 'LEFT' in onto:
                    prep = 'at+the+left+of'
                elif 'RIGHT' in onto:
                    prep = 'at+the+right+of'
                else:
                    pass
            elif desc == ' isIn ':
                prep = 'in'
            elif desc in  [' hasGoal ', ' receivedBy ']:
                prep = 'to'
            elif desc == ' isOn ':
                prep = 'on'
            else:
                prep = 'at'
            
            for i_c_object in onto:
                object_location.append(Indirect_Complement([prep], [self.create_w_question_object(i_c_object)]))        
        
        #Keep Location in a relative description => relative
        object_relative_description = []
        if object_location:
            object_relative_description = [Sentence("relative", "", [],
                                                        [Verbal_Group(['be'],                                               
                                                                       [],
                                                                       'present_simple',
                                                                       [],
                                                                       object_location,
                                                                       [],
                                                                       [],
                                                                       'affirmative',
                                                                       [])])]
        
        
        
        
        
        # Noun Complement or Object owner if there exists
        object_owner = []
        description = [' belongsTo ']
        onto = []
        try:
            onto = ResourcePool().ontology_server.find('?concept', [object + desc + '?concept'])
        except AttributeError:
            pass
            
        for n_cmpl_object in onto:
            object_owner.append(self.create_w_question_object(n_cmpl_object))
        
            
                
        # Nominal Groupp to return
        return Nominal_Group(object_determiner, 
                            object_noun, 
                            object_features, 
                            object_owner,
                            object_relative_description)
        
        
        
    def create_yes_no_answer(self, yes_no_question, answer):
        
        sentence = self.reverse_personal_pronoun(yes_no_question)
        
        if answer:
            return [Sentence("agreement",
                                "", 
                                [],
                                []),
                    sentence]
        
        else:
            for sv in sentence.sv:
                sv.state = "negative"
                
            return [Sentence("disagreement",
                                "",
                                [],
                                []),
                    sentence]
            
            
            
               
class Sentence:
    """
    A sentence is formed from:
    sn : a nominal structure typed into a Nominal_group
    sv : a verbal structure typed into a Verbal_Group
    aim : is used for retrieveing the aim of a question
    """

    def __init__(
        self,
        data_type,
        aim,
        sn,
        sv,
        ):
        self.data_type = data_type
        self.aim = aim
        self.sn = sn
        self.sv = sv
            
    def resolved(self):
        """returns True when the whole sentence is completely resolved
        to concepts known by the robot."""
        return  reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.sn), 
                        True) \
                and \
                reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.sv), 
                        True)

    
    def __str__(self):
        res =   colored_print(">> " + self.data_type.upper(), 'bold')
        if self.aim:
            res += " (aim: " + self.aim + ')'
        res += '\n'
        
        if self.sn:
            for s in self.sn:
                res += colored_print('nominal grp', 'bold') + ':\n\t' + str(s).replace("\n", "\n\t") + "\n"
        if self.sv:
            for s in self.sv:
                res += colored_print('verbal grp', 'bold') + ':\n\t' + str(s).replace("\n", "\n\t") + "\n"
        
        #res += "This sentence is " + ("fully resolved." if self.resolved() else "not fully resolved.")
        return res
    
    def flatten(self):
        return [self.data_type,
                self.aim,
                map(lambda x: x.flatten(), self.sn),
                map(lambda x: x.flatten(), self.sv)]


class Nominal_Group:
    """
    Nominal group class declaration
    det : determinant
    noun: a simple noun
    adj: a list of adjectives describing the noun
    noun_cmpl: a list of noun complements
    relative : is a relative sentence typed into Sentence
    """

    def __init__(   self,
                    det,
                    noun,
                    adj,
                    noun_cmpl,
                    relative,
                    ):
        self.det = det
        self.noun = noun
        self.adj = adj
        self.noun_cmpl = noun_cmpl
        self.relative = relative
                
        """This field is True when this nominal group is resolved to a concept
        known by the robot."""
        self._resolved = False
        
        """This field hold the ID of the concept represented by this group.
        When the group is resolved, id must be different from None
        """
        self.id = None
        
        self._conjunction = 'AND' #could be 'AND' or 'OR'... TODO: use constants!
        self._quantifier = 'ONE'  #could be 'ONE' or 'SOME'... TODO: use constants!

    def __str__(self):
        
        res = ''
        
        if self._conjunction != 'AND':
            res += colored_print('[' + self._conjunction + "] ", 'bold')
        
        if self._quantifier != 'ONE':
            res += colored_print('[' + self._quantifier + "] ", 'bold')
            
        if self._resolved:
            res += colored_print(self.id, 'white', 'blue') + '\n' + colored_print('>resolved<', 'green')
            
        else:
            
            
            if self.det:
                res +=   colored_print(self.det, 'yellow') + " " 
            
            
            for k in self.adj:
                res +=  colored_print(k[1], 'red') + " " 
                res +=  colored_print([k[0]], 'green') + " " 
            
            if self.noun:
                res +=   colored_print(self.noun, 'blue') + '\n'
            
            
            if self.noun_cmpl:
                for s in self.noun_cmpl:
                    res += '[OF] \n\t' + str(s).replace("\n", "\n\t") + "\n"
            
            if self.relative:
                for rel in self.relative:
                    res += 'relative:\n\t' + str(rel).replace("\n", "\n\t") + "\n"
        
        return res
    
    
    def flatten(self):
        return [self.det,
                self.noun,
                self.adj,
                map(lambda x: x.flatten(), self.noun_cmpl),
                map(lambda x: x.flatten(), self.relative)]
        
        
    def adjectives_only(self):
        """This method returns True when this nominal group holds only a set of adjectives.
        E.g: the banana is yellow. The parser provides an object sentence with two nominal groups:
        - Nominal_Group(['the'], ['banana'], [], [],[]) and adjectives_only returns False
        - Nominal_Group([], [], ['yellow'], [],[]) and adjectives_only returns True
        """
        if self.adj and \
                not self.noun and \
                not self.noun_cmpl and \
                not self.relative:
            return True
        else:
            return False
        
    
class Indirect_Complement:
    """
    Indirect complement class declaration
    gn : nominal group
    prep : preposition
    """
    
    def __init__(self, prep, nominal_group):
        self.prep = prep
        self.nominal_group = nominal_group
        
    def resolved(self):
        return  reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.nominal_group), 
                        True)
        
    def __str__(self):
        res = colored_print(self.prep, 'yellow') + "..."
        
        if self.nominal_group:
            for s in self.nominal_group:
                res += '\n\t' + str(s).replace("\n", "\n\t") + "\n"
        
        return res

    
    def flatten(self):
        return [self.prep,
                map(lambda x: x.flatten(), self.nominal_group)]

class Verbal_Group:
    """
    Verbal_group class declaration
    vrb_main: the main verb of a sentence
    vrb_sec : an accompanying verb of the main verb
    vrb_tense: the main verb tense
    d_obj : the  direct object referred by the main verb
    i_cmpl : the indirect object referred by the main verb or an adverbial formed from a nominal group
    vrb_adv : an adverb describing the verb
    advrb : an adverb used as an adverbial of the whole sentence
    """

    def __init__(
            self,
            vrb_main,
            sv_sec,
            vrb_tense,
            d_obj,
            i_cmpl,
            vrb_adv,
            advrb,
            state,
            vrb_sub_sentence,
            ):
        self.vrb_main = vrb_main
        self.sv_sec = sv_sec
        self.vrb_tense = vrb_tense
        self.d_obj = d_obj
        self.i_cmpl = i_cmpl
        self.advrb = advrb
        self.vrb_adv = vrb_adv
        self.state = state
        self.vrb_sub_sentence = vrb_sub_sentence
        
        """This field is True when this verbal group is resolved to a concept
        known by the robot."""
        self._resolved = False
        
    def resolved(self):
        return  self._resolved \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x._resolved, self.d_obj), True) \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x.resolved(), self.i_cmpl), True) \
                and \
                (self.sv_sec.resolved() if self.sv_sec else True) \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x.resolved(), self.vrb_sub_sentence), True)
    
    def __str__(self):
        res =   colored_print(self.vrb_main, 'magenta') + " (" + str(self.vrb_tense) + ")\n"
        if self.advrb:
            res += 'adverb: ' + colored_print(self.advrb, 'yellow') + "\n"
        if self.vrb_adv:
            res += 'vrb adv: ' + colored_print(self.vrb_adv, 'green') + "\n"
                
        if self.d_obj:
            res += 'direct objects:\n'
            for cmpl in self.d_obj:
                res += '\t' + str(cmpl).replace("\n", "\n\t") + "\n"
        
        if self.i_cmpl:
            res += 'indirect objects:\n'
            for cmpl in self.i_cmpl:
                res += '\t' + str(cmpl).replace("\n", "\n\t") + "\n"
        
        if self.vrb_sub_sentence:
            for vrb_sub_s in self.vrb_sub_sentence:
                res += 'vrb_sub_sentence:\n\t' + str(vrb_sub_s).replace("\n", "\n\t") + "\n"
        
        if self.sv_sec:
            for vrb_sec_s in self.sv_sec:
                res += 'secondary verbal grp:\n\t' + str(vrb_sec_s).replace("\n", "\n\t") + "\n"
        
        res += colored_print(">resolved<", 'green') if self.resolved() else colored_print(">not resolved<", 'red')
        
        return res


    def flatten(self):
        return [self.vrb_main,
                map(lambda x: x.flatten(), self.sv_sec),
                self.vrb_tense,
                map(lambda x: x.flatten(), self.d_obj),
                map(lambda x: x.flatten(), self.i_cmpl),
                self.vrb_adv,
                self.advrb,
                self.state,
                map(lambda x: x.flatten(), self.vrb_sub_sentence)]



class Comparator():
    """
    This class holds a single method that compares two objects and return True or False.
    The objects should hold a method 'flatten', turning it into a list
    
    """    
    def __init__(self):
        pass
    
    def compare(self, obj1, obj2):
        return obj1.__class__ == obj2.__class__ and \
                obj1.flatten() == obj2.flatten()
      
        

def it_is_pronoun(word):
    for p in pronoun_list:
        if word==p:
            return 1
    return 0
                    
                    
                    
def concat_gn(nom_gr_struc, new_class, flag):      
    """
    This function concatenate 2 nominal groups                                      
    Input=2 nominal groups and the flag           Output= nominal group                   
    """
    
    #If failure we need to change information else we add 
    if nom_gr_struc.adj!=new_class.adj:
        if flag=='FAILURE':
            nom_gr_struc.adj=new_class.adj
        elif flag=='SUCCESS':
            nom_gr_struc.adj=nom_gr_struc.adj+new_class.adj
    
    #If there is a difference may be it can from 'a' to  'the' or 'this'        
    if new_class.det!= [] and nom_gr_struc.det!=new_class.det:
        nom_gr_struc.det=new_class.det
    
    #We make change if there is 'one' or difference
    if new_class.noun!=[] and nom_gr_struc.noun!=new_class.noun and new_class.noun!=['one']:
        nom_gr_struc.noun=new_class.noun

    if flag=='FAILURE' :
        nom_gr_struc.relative=new_class.relative
    else:
        nom_gr_struc.relative=nom_gr_struc.relative+new_class.relative
    
    if flag=='FAILURE':    
        nom_gr_struc.noun_cmpl=new_class.noun_cmpl
    else:
        nom_gr_struc.noun_cmpl=nom_gr_struc.noun_cmpl+new_class.noun_cmpl



def process_vg_part(vg,nom_gr_struc, flag):  
    """
    This function process merge in the verbal part                                      
    Input=nominal groups, the verbal part and the flag      Output= nominal group                   
    """
    
    #init 
    flg=0
    
    #The direct complement is a nominal group
    for object in vg.d_obj:
        concat_gn(nom_gr_struc, object, flag)
    
    #For indirect complement
    for i in vg.i_cmpl:
        #If it is an adverbial related to the noun, we have to add it like a relative
        for j in adverbial_list:
            if j==i.prep[0]:
                rltv=Sentence('relative', 'which',[],[vg])
                nom_gr_struc.relative=nom_gr_struc.relative+[rltv]
                flg=1
                break
        
        #Else we process the concatenate with the nominal part of the indirect complement    
        if flg==1:
            flg=0
        else:
            for k in i.nominal_group:
                concat_gn(nom_gr_struc, k, flag)
    
    for i in vg.sv_sec:
        process_vg_part(i,nom_gr_struc, flag)
    
    #For the subsentences
    nom_gr_remerge(vg.vrb_sub_sentence, flag , nom_gr_struc)
    
    return nom_gr_struc



def process_vg_nega_part(vg,nom_gr_struc, flag):  
    """
    This function process merge in the verbal part when we have negative sentence                                    
    Input=nominal groups, the verbal part and the flag      Output= nominal group                   
    """
    
    #init 
    flg=0
    
    #The direct complement is a nominal group
    for object in vg.d_obj:
        if object._conjunction=='BUT':
            concat_gn(nom_gr_struc, object, flag)
    
    #For indirect complement
    for i in vg.i_cmpl:
        #If it is an adverbial related to the noun, we have to add it like a relative
        for j in adverbial_list:
            if j==i.prep[0] and i.nominal_group[0]._conjunction=='BUT':
                i.nominal_group[0]._conjunction='AND'
                vg.i_cmpl=vg.i_cmpl[vg.i_cmpl.index(i):]
                vg.state='affirmative'
                rltv=Sentence('relative', 'which',[],[vg])
                if flag=='FAILURE' and nom_gr_struc.relative!=[]:
                    nom_gr_struc.relative=[rltv]
                else :
                    nom_gr_struc.relative=nom_gr_struc.relative+[rltv]
                flg=1
                break
        
        #Else we process the concatenate with the nominal part of the indirect complement    
        if flg==1:
            flg=0
        else:
            for k in i.nominal_group:
                if k._conjunction=='BUT':
                    concat_gn(nom_gr_struc, k, flag)
    
    for i in vg.sv_sec:
        process_vg_part(i,nom_gr_struc, flag)
    
    #For the subsentences
    nom_gr_remerge(vg.vrb_sub_sentence, flag , nom_gr_struc)
    
    return nom_gr_struc



def refine_nom_group_relative_sv (vs,nom_gr):
    """
    This function replace one by the noun in verbal part of relative                                      
    Input=nominal groups and verbal part          Output= nominal group                   
    """
    
    for object in vs.d_obj:
        if object.noun==['one']:
            object.noun=nom_gr.noun
        refine_nom_group_relative(object)
    for i_object in vs.i_cmpl:
        for ng in i_object.nominal_group:
            if ng.noun==['one']:
                ng.noun=nom_gr.noun
            refine_nom_group_relative(ng)
    for second_vrb in vs.sv_sec:
            refine_nom_group_relative_sv(second_vrb,nom_gr)


def refine_nom_group_relative(nom_gr):
    """
    This function replace one by the noun in relative                                      
    Input=nominal groups                      Output= nominal group                   
    """
    
    for i in nom_gr.relative:
        for ns in i.sn:
            if ns.noun==['one']:
                ns.noun=nom_gr.noun
            refine_nom_group_relative(ns)
        for vs in i.sv:
            refine_nom_group_relative_sv(vs,nom_gr)
            
            
    
def nom_gr_remerge(utterance, flag , nom_gr_struc):
    """
    This function process merge                                      
    Input=nominal groups, the use utterance and the flag      Output= nominal group                   
    """

    for i in utterance: 
        if (i.data_type=='statement' or i.data_type=='subsentence') :

            if i.sv[0].state=='affirmative':
            
                if  flag=='FAILURE':
                    #We can have just the subject
                    if i.sv[0].d_obj==[] and i.sv[0].i_cmpl==[] and i.sv[0].sv_sec==[] and i.sv[0].vrb_sub_sentence==[]:
                        for k in i.sn:
                            concat_gn(nom_gr_struc, k, flag)
                        refine_nom_group_relative(nom_gr_struc)
                        return nom_gr_struc
                    #Else there is no subject and the information is on the verbal structure
                    for v in i.sv:
                        nom_gr_struc=process_vg_part(v,nom_gr_struc, flag)
        
                elif flag=='SUCCESS':
                    #We can have just the subject
                    if i.sv[0].d_obj==[] and i.sv[0].i_cmpl==[] and i.sv[0].sv_sec==[] and i.sv[0].vrb_sub_sentence==[]:
                        for k in i.sn:
                            concat_gn(nom_gr_struc, k, flag)
                        refine_nom_group_relative(nom_gr_struc)
                        return nom_gr_struc
                    
                    for k in i.sn:
                        if it_is_pronoun(k.noun[0])==0:
                            concat_gn(nom_gr_struc, k, flag)
                    
                    #We finish the process with the verbal part
                    for v in i.sv:
                        nom_gr_struc=process_vg_part(v,nom_gr_struc, flag)        
            
            elif i.sv[0].state=='negative':
                #For all other sentences flag will be FAILURE
                flag='FAILURE'
                
                for k in i.sn:
                    if it_is_pronoun(k.noun[0])==0:
                        concat_gn(nom_gr_struc, k, flag)
                        
                #We finish the process with the verbal part
                for v in i.sv:
                    nom_gr_struc=process_vg_nega_part(v,nom_gr_struc, flag)   
                
            
    refine_nom_group_relative(nom_gr_struc)
    return nom_gr_struc



def unit_tests():

    sentence1 = Sentence('w_question',
                        'location',
                        [Nominal_Group(['the'],  ['mother'],[],[], [])],
                        [Verbal_Group(['be'], [],'present simple',[], [],['today'], [], [], [])])
    
    print("*********************************")
    print(sentence1)
    
    sentence2 = Sentence('statement', 
                        '', 
                        [Nominal_Group([],["Jido"],[],[],[]), Nominal_Group([],["Danny"],[],[],[])], 
                        [Verbal_Group(["want"],[], 'infinitive',[],[],[],[],'affirmative', [])])
    
    print("*********************************")
    print(sentence2)
    
    sentence3 = Sentence('statement', 
                        '', 
                        [Nominal_Group([],["Holmes"],[],[],[]), Nominal_Group([],["Sherlock"],[],[],[])], 
                        [Verbal_Group(["want"],
                                    [Verbal_Group(["eat"],[], 'infinitive',[],[],[],[],'affirmative', [])], 
                                    'past simple',
                                    [],
                                    [],
                                    [],
                                    [],
                                    'negative', 
                                    [])])
    
    print("*********************************")
    print(sentence3)
    
    sentence4 = Sentence('statement',
                        '',
                        [Nominal_Group( ['the'],  
                                        ['bottle'],
                                        ['blue', 'gray'],
                                        [Nominal_Group(['my'],  ['mother'],[],[], [sentence2]), Nominal_Group(['my'],  ['father'],[],[], [])], 
                                        [])], 
                        [Verbal_Group(['know'], 
                                    [],
                                    'present simple',
                                    [Nominal_Group(['the'],  ["land"],['old'],[], []), Nominal_Group(['the'],  ["brand"],['lazy'],[], [])],
                                    [
                                        Indirect_Complement(['in'], 
                                                            [Nominal_Group(['the'],  ['garden'],['green'],[], [])]), 
                                        Indirect_Complement(['to'], 
                                                            [Nominal_Group(['the'],  ['car'],['red'],[], [])])
                                    ],
                                    ["slowly"], 
                                    ["now"], 
                                    "affirmative", 
                                    [sentence3])])
    print("*********************************")
    print(sentence4)
    
    
    
    sentence4bis = Sentence('statement',
                        '',
                        [Nominal_Group( ['the'],  
                                        ['bottle'],
                                        ['blue', 'gray'],
                                        [Nominal_Group(['my'],  ['mother'],[],[], [sentence2]), Nominal_Group(['my'],  ['father'],[],[], [])], 
                                        [])], 
                        [Verbal_Group(['know'], 
                                    [],
                                    'present simple',
                                    [Nominal_Group(['the'],  ["land"],['old'],[], []), Nominal_Group(['the'],  ["brand"],['lazy'],[], [])],
                                    [
                                        Indirect_Complement(['in'], 
                                                            [Nominal_Group(['the'],  ['garden'],['green'],[], [])]), 
                                        Indirect_Complement(['to'], 
                                                            [Nominal_Group(['the'],  ['car'],['red'],[], [])])
                                    ],
                                    ["slowly"], 
                                    ["now"], 
                                    "affirmative", 
                                    [sentence3])])
    print("*********************************")
    print(sentence4bis)
    
    
    print "*************  Sentence Comparison ****************"
    
    cmp = Comparator()    
    print "sentence4 == sentence4bis: ", cmp.compare(sentence4, sentence4bis)    
    print "sentence3 == sentence4: ", cmp.compare(sentence3, sentence4)
    
    print "*************  Nominal group adjective only ****************"
    print "Nominal_Group(['the'],['man'],[],[],[]) is adjective only: ", Nominal_Group(['the'],['man'],[],[],[]).adjectives_only()
    print "Nominal_Group([],[],['blue'],[],[]) is adjective only: ", Nominal_Group([],[],['blue'],[],[]).adjectives_only()
    
if __name__ == '__main__':
    unit_tests()

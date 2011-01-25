# -*- coding: utf-8 -*-

import logging

from helpers import colored_print, level_marker
from resources_manager import ResourcePool
from sentence import *

class SentenceFactory:
    
    def create_w_question_choice(self, obj_name, feature, values):
        """ Creates sentences of type: 
            Which color is the bottle? Blue or yellow.
        """
        nominal_groupL = [Nominal_Group([],[],[[val.lower(),[]]],[],[]) for val in values]
        
        sentence = [Sentence(Sentence.w_question, 'choice', 
                        [Nominal_Group([],[feature],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [Nominal_Group(['the'],[obj_name.lower()],[],[],[])], 
                            [], [], [] ,Verbal_Group.affirmative,[])]),
                    Sentence(Sentence.statement, '',nominal_groupL,[])]
        
                            
        for i in range(len(values)-1):
            sentence[1].sn[i+1]._conjunction = 'OR'
        
        return sentence
        
    def create_w_question_location(self, obj_name, feature, values):
        """ Creates sentences of type: 
                "Where is the box? On the table or on the shelf?"
        """
        indirect_complL = [Indirect_Complement([feature],[Nominal_Group(['the'],[val],[],[],[])]) \
                            for val in values]
                            
        sentence = [Sentence(Sentence.w_question, 'place',
                        [Nominal_Group(['the'],[obj_name],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                        [], [], [], [] ,Verbal_Group.affirmative,[])]),
                    Sentence(Sentence.yes_no_question, '', [], 
                        [Verbal_Group([], [],'', 
                            [], indirect_complL, [], [] ,Verbal_Group.affirmative,[])])]
                
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

        sentence = [Sentence(Sentence.yes_no_question, '', 
                        [Nominal_Group([],['it'],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [], indirect_complL, [], [] ,Verbal_Group.affirmative,[])])]
                    
        for i in range(len(values)-1):
            sentence[0].sv[0].i_cmpl[i+1].nominal_group[0]._conjunction = 'OR'
            
        return sentence
    
    def create_what_do_you_mean_reference(self, object):
        """ Creates sentences of type: 
            "The bottle? What do you mean?"
        """
        
        sentence = [Sentence(Sentence.yes_no_question, '', [object], []),
                    Sentence(Sentence.w_question, 'thing', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['mean'], [],'present simple', [], [], [], [] ,Verbal_Group.affirmative,[])])]
        return sentence
    
    
    def create_do_you_mean_reference(self, object):
        """ Creates sentences: 
            "Do you mean the bottle?"
        """
        
        # Special case of an occurence of "other" in adjectives
        if object and ['other', []] in object.adj:
            object.adj = [['other', []]]
            object.noun_cmpl = []
            object.relative = []
            
        return [Sentence(Sentence.yes_no_question, '', 
                    [Nominal_Group([],['you'],[],[],[])], 
                    [Verbal_Group(['mean'], [],'present simple', [object], [], [], [] ,Verbal_Group.affirmative,[])])]
        
    
    def create_what_is_a_reference(self, object, objectL):
        """ Creates sentences of type: 
            "bottles are objects? What is a bottle?"
        """
        sentence = [object, Sentence(Sentence.w_question, 'thing', 
                        [], [Verbal_Group(['be'], [],'present simple', [], [], [], [] ,Verbal_Group.affirmative,[])])]
                        
        for obj in objectL:
            sentence[1].sn.append(Nominal_Group(['an' if obj[0].lower() in 'aeiou' else 'a'], 
                                                [obj],[],[],[]))
        
        return sentence
        
        
    
    def create_w_question_answer(self, w_question, w_answer, current_speaker, query_on_field):
        """Create the answer of a W-Question
            w_question is the current question
            w_answer is the response found in the ontology
            query_on_field is the part of the W_question to fill with the answer. it takes the following values:
                - None :
                - QUERY_ON_INDIRECT_OBJ
                - QUERY_ON_DIRECT_OBJ
        """
        #Nominal group holding the answer
        nominal_groupL = []
        
        #if "me", "you", "us"
        myself = False
        yourself = False
        
        #Return. I am sorry. I don't know
        if not w_answer:
            return[Sentence(Sentence.statement,"",
                            [Nominal_Group([], ['I'], [], [], [])],
                            [Verbal_Group(['be'],[], "present simple", 
                                [Nominal_Group([], [], [['sorry',[]]], [], [])],[],[],[],"affirmative", [])]),
                    Sentence(Sentence.statement,"",
                            [Nominal_Group([], ['I'], [], [], [])],
                            [Verbal_Group(['have'],[], "present simple", 
                                [Nominal_Group(['no'], ['answer'], [], [], [])], [], [],[],"affirmative", [])])]
                    
        
        # Case of adjectives only
        if w_question.aim in ResourcePool().adjectives_ontology_classes:
            ng = Nominal_Group([], [], [[w_answer[0][1][0], []]], [], [])
            preposition = w_answer[0][0]
            ng._resolved = True
            nominal_groupL = [[preposition, [ng]]]
            
        else:
            for [preposition, response] in w_answer:
                ngL = []
                for resp in response:
                    if resp == "myself":
                        myself = True
                    if resp == current_speaker:
                        yourself = True
                        
                    ng = self.create_nominal_group_with_object(resp, current_speaker)
                    ng.id = resp
                    ng._resolved = True
                    ngL.append(ng)
                
                #Arraging preposition
                if preposition and preposition[0] in ResourcePool().direction_words:
                    if preposition[0] == 'front':
                        preposition[0] = "in+front+of"
                    
                    elif preposition[0] == "back":
                        preposition[0] == "behind"
                    
                    elif preposition[0] == "bottom":
                        preposition[0] == "underneath"
                    
                    elif preposition[0] == "top":
                        prepsosition[0] = "above"
                    
                    else:
                        # Here we try to output something similar to My left, or Your left or at the left of ACHILLE
                        # Case of "my and your"
                        if myself and yourself:
                            ngL = [Nominal_Group(["our"],preposition,[],[],[])]
                        #
                        elif myself:
                            ngL = [Nominal_Group(["my"],preposition,[],[],[])]
                        elif yourself:
                            ngL = [Nominal_Group(["your"],preposition,[],[],[])]

                        else:    
                            ngL = [Nominal_Group(["the"],preposition,[],ngL,[])]
                        
                        preposition = ["at"]
                                        
                nominal_groupL.append([preposition, ngL])
                
                
                
        
        #Sentence holding the answer
        # work on a new sentence, so that changes made here do not affect the original w_question
        sentence = Sentence(Sentence.statement,
                            w_question.aim,
                            w_question.sn,
                            w_question.sv)
                            
        sentence = self.reverse_personal_pronoun(sentence)
        
        if not query_on_field:#Default case on sentence.sn
            sentence.sn = [ng for [prep, ngL] in nominal_groupL for ng in ngL]
            sentence.sv = []
            
        elif query_on_field == 'QUERY_ON_DIRECT_OBJ':
            sentence.sv[0].d_obj = [ng for [prep, ngL] in nominal_groupL for ng in ngL]
            
            
        elif query_on_field == 'QUERY_ON_INDIRECT_OBJ':
            sentence.sv[0].i_cmpl = [Indirect_Complement(ng[0], ng[1]) for ng in nominal_groupL]
        
        sentence.aim = ""
        
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
        
        
        
    def create_nominal_group_with_object(self, object, current_speaker):
        """Creating a nominal group by retrieving relevant information on 'object'."""
        
        
        def _filter_ontology_inferred_class(object_list):
            """Filtering infered class from the ontology such as SpatialThing, EnduringThing-Localized, ... that add no needed infos """
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
        # reference to myself, current speaker, ...
        if object == "myself":
            return Nominal_Group([], ["me"], [], [], [])#No need to go further as we know "myself" ID
        
        if object == current_speaker:
            return Nominal_Group([], ["you"], [], [], [])#No need to go further as we know the current speaker's ID
        
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
               onto = ResourcePool().ontology_server.getDirectClassesOf(object)
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            
            object_noun = [_filter_ontology_inferred_class(onto.keys())[0].lower()]
                       
            if object_noun == ['owl:thing']:
                object_noun = ["object"]
                
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
                
            for obj in onto:
                object_features.append([obj, []]) # Cf Adjectives format: list[main, list[quatifiers]]
                
        """ Commented due to recursivity issues
        # Object Location
        object_location = []
        description = [' isNextTo ', ' isBehind ',' isInFrontOf ', ' isOn ', ' isIn ', ' hasGoal ', ' receivedBy ']
                        
        for desc in description:
            onto = []
            try:
               onto = ResourcePool().ontology_server.find('?concept', [object + desc + '?concept'])
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            
            #Match preposition with description
            prep = ''
            if desc == ' isNexTto ':
                prep = 'next+to'
            elif desc == ' isBehind ':
                prep = 'behind'
            elif desc == ' isInFrontOf ':
                prep = 'in+front+of'
            elif desc == ' isIn ':
                prep = 'in'
            elif desc in  [' hasGoal ', ' receivedBy ']:
                prep = 'to'
            elif desc == ' isOn ':
                prep = 'on'
            else:
                prep = 'at'
            
            for i_c_object in onto:
                #TODO: Reduce recursivity so that we don't have , the bottle that is on the table, that is in Toulouse, that is in France, that is ...
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
                                                                       Verbal_Group.affirmative,
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
            #TODO: Reduce recursivity so that we don't have , the bottle of the table, of Toulouse, of France, of ...
            object_owner.append(self.create_w_question_object(n_cmpl_object))
        
        
           
                
        # Nominal Groupp to return
        return Nominal_Group(object_determiner, 
                            object_noun, 
                            object_features, 
                            object_owner,
                            object_relative_description)
        """
        # Nominal Group to return
        return Nominal_Group(object_determiner, 
                            object_noun, 
                            object_features, 
                            [],
                            [])
        
    def create_yes_no_answer(self, yes_no_question, answer):
        
        sentence = self.reverse_personal_pronoun(yes_no_question)
        sentence.data_type = Sentence.statement
        
        if answer:
            return [Sentence(Sentence.agree,
                                "yes", 
                                [],
                                []),
                    sentence]
        
        else:
            sentence.data_type = Sentence.subsentence
            sentence.aim = "if"
            return [Sentence(Sentence.statement,
                                "",
                                [Nominal_Group([],['I'],[],[],[])],
                                [Verbal_Group(['know'],[], "present simple", [],[],[],[], "negative", [sentence])])]
            
    
    def create_gratulation_reply(self):
        """ Create a reply to gratualtion
            E.g: You are welcome.
        """
        return [Sentence(Sentence.statement, "", 
                        [Nominal_Group([],['you'],[], [],[])],
                        [Verbal_Group(['be'], [], "present simple",
                                    [Nominal_Group([],[],[['welcome',[]]], [],[])],[],[],[],"affirmative", [])])]
    
    def create_agree_reply(self):
        return [Sentence(Sentence.agree, "alright", [], [])]

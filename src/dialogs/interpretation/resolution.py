#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger("dialog")

from dialogs.helpers import colored_print

from dialogs.dialog_exceptions import UnsufficientInputError, UnknownVerb, UnidentifiedAnaphoraError, DialogError
from dialogs.resources_manager import ResourcePool
from statements_builder import NominalGroupStatementBuilder, get_class_name, generate_id #for nominal group discrimination
from discrimination import Discrimination
from anaphora_matching import AnaphoraMatcher, recover_nominal_group_list, first_replacement
from dialogs.sentence import *
from dialogs.sentence_factory import SentenceFactory


class Resolver:
    """Implements the concept resolution mechanisms.
    Three operations may be conducted:
     - references + anaphors resolution (replacing "I, you, me..." and "it, one"
     by the referred concepts)
     - noun phrase resolution (replacing "the bottle on the table" by the right
     bottle ID). This is achieved in the discrimination module.
     - verbal phrase resolution (replacing action verbs by verbs known to the 
     robot, by looking for the semantically closest one). This is done by the
     action_matcher module.
    
    """
    def __init__(self, sentences_store = []):
        self._current_sentence = None
        self._current_object = None
        self.sentences_store = sentences_store
        
    ##########################################
    #   References and anaphoric resolutions
    ##########################################
    
    def references_resolution(self, sentence, current_speaker, uae_object, uae_object_with_more_info, uae_object_list):
        #Skipping processing of sentences that are neither questions nor statements
        if not sentence.data_type in [Sentence.w_question, Sentence.yes_no_question, Sentence.statement, Sentence.imperative]:
            return sentence
        
        # Current object replacement with uae object
        if uae_object and uae_object_with_more_info:
            self._current_object = self._references_resolution_replace_current_object_with_ua_exception(sentence,
                                                                                                uae_object,
                                                                                                uae_object_with_more_info,
                                                                                                uae_object_list)
                                                                                        
        logger.info(colored_print("-> Resolving references and anaphors...", 'green'))
        #Record of current sentence
        self._current_sentence = sentence
        
        #Anaphoric resolution
        matcher = AnaphoraMatcher()
        
        #sentence sn nominal groups reference resolution
        if sentence.sn:
            sentence.sn = self._resolve_groups_references(sentence.sn, matcher, current_speaker, self._current_object)

        if sentence.sv:
            sentence.sv = self.verbal_phrases_reference_resolution(sentence.sv, matcher,current_speaker, self._current_object)

        return sentence    
    
    def _references_resolution_replace_current_object_with_ua_exception(self, sentence, uae_object, uae_object_with_more_info, uae_object_list):
        """This attempts to replace a nominal group that has failled from identifying the anaphoric word with one that holds more information.
        """
        
        current_object = None
        
        if uae_object_with_more_info[1]:
            current_object = uae_object_with_more_info[0]
        else:
            sf = SentenceFactory()
            raise UnidentifiedAnaphoraError({'object':uae_object,
                                            'object_to_confirm':uae_object_with_more_info[0],
                                            'object_with_more_info':None,
                                            'objects_list':uae_object_list,
                                            'sentence':sentence,
                                            'question':sf.create_do_you_mean_reference(uae_object_with_more_info[0])}) 
           
        return current_object
        
        
    def _resolve_references(self, nominal_group, matcher, current_speaker, current_object):
        
        # Case of a resolved nominal group
        if nominal_group._resolved: 
            return nominal_group
            
        # Case of a quantifier different from ONE
        #   means the nominal group holds an indefinite determiner. 
        #   E.g a robot, every plant, fruits, ...
        if nominal_group._quantifier in ['SOME','ALL']: 
            # Case of a state verb
            # id = the class name
            # E.g: an apple is a fruit
            #       the id of apple is Apple
            logger.info("\t Found undefinite quatifier " + nominal_group._quantifier)
            onto = []
            try:
                onto = ResourcePool().ontology_server.lookupForAgent(current_speaker, nominal_group.noun[0])
            except AttributeError:
                pass
            
            
            class_name =  get_class_name(nominal_group.noun[0], onto)
            nominal_group.id = class_name
            """
            # case of an action verbs
            # id = generated 
            # E.g: An Apple grows on a tree
            #   we get the ids of all existig apples in the ontology otherwise we generate one
            if not verb in ResourcePool().state for verb in [vrb for sv in self.sv for vrb in sv.vrb_main]:
                onto_id = []
                try:
                    onto_id = ResourcePool().findForAgent(current_speaker, '?concept', '?concept rdf:type ' + class_name)
                except AttributeError:
                    pass
                
                if 
            """
            nominal_group._resolved = True
            return nominal_group
            
        # Case of a nominal group built by only adjectives 
        #   E.g, 'big' in 'the yellow banana is big'.
        if nominal_group.adjectives_only():
            nominal_group.id = nominal_group.adj[0][0]
            nominal_group._resolved = True
            return nominal_group
        
        
        # Case of an anaphoric word in the determiner
        # E.g: This , that cube
        if nominal_group.det and \
            nominal_group.det[0].lower() in ResourcePool().demonstrative_det:
            
            onto_focus = ''
            logger.debug(colored_print("Found a demonstrative (this/that...). Trying to resolve it based on current focus...", "magenta"))
            logger.debug(colored_print("Looking for : ", "magenta") + colored_print(current_speaker + ' focusesOn ?concept', None, "magenta"))
            try:
                onto_focus = ResourcePool().ontology_server.findForAgent(current_speaker, 
                                                                            '?concept', 
                                                                            [current_speaker + ' focusesOn ?concept'])
            except AttributeError:
                pass
            
            if onto_focus:
                logger.debug(colored_print("OK, found ", "magenta") + colored_print(str(onto_focus), "blue"))
                nominal_group.id = onto_focus[0]
                nominal_group._resolved = True
                return nominal_group
            
            logger.debug(colored_print("No focus. Processing is as a classic anaphora.", "magenta"))
            
            # Case of 
            #   this + noun - E.g: Take this cube:
            if nominal_group.noun and nominal_group.noun[0].lower() != 'one':
                pass # Nothing to do appart from processing "this" as "the"
            
            # Case of 
            #   this + one -  E.g: Take this
            #   this + None - E.g: Take this one
            else:
                nominal_group.noun = self._references_resolution_with_anaphora_matcher(nominal_group, matcher, 
                                                                                    current_speaker, 
                                                                                    current_object)
            
        # Case of a nominal group with no Noun
        if not nominal_group.noun:
            return nominal_group
        
        # Case of an existing ID in the Ontology
        onto = []
        try:
            onto = ResourcePool().ontology_server.lookupForAgent(current_speaker, nominal_group.noun[0])
        except AttributeError: #the ontology server is not started or doesn't know the method
            pass
        
        if onto:
            logger.debug("... \t" + nominal_group.noun[0] + " is an existing ID in " + current_speaker + "'s model.")
            for c in onto:
                if "INSTANCE" in c:
                    nominal_group.id = c[0]
                    nominal_group._resolved = True
                    break
        
        # Case of personal prounouns
        if current_speaker and nominal_group.noun[0].lower() in ['me','i']:
            logger.debug(colored_print("Replaced \"me\" or \"I\" by \"" + current_speaker + "\"","magenta"))
            nominal_group.id = current_speaker
            nominal_group._resolved = True
        
        if nominal_group.noun[0].lower() in ['you']:
            logger.debug(colored_print("Replaced \"you\" by \"myself\"","magenta"))
            nominal_group.id = 'myself'
            nominal_group._resolved = True
        
        #Anaphoric words in the noun
        if nominal_group.noun[0].lower() in ['it', 'one']:
            nominal_group = self._references_resolution_with_anaphora_matcher(nominal_group, matcher, 
                                                                                    current_speaker, 
                                                                                    current_object)
        return nominal_group
    
    def _resolve_groups_references(self, array_sn, matcher, current_speaker, current_object):
        """This attempts to resolve every single nominal group held in a nominal group list"""
        resolved_sn = []
        for ng in array_sn:
            if self._current_sentence.learn_it():
                ng.noun_cmpl = self._resolve_groups_references(ng.noun_cmpl, matcher, current_speaker, None) if ng.noun_cmpl else []
                #resolved_relative = [self.references_resolution(relative, current_speaker, None, None, None) for relative in ng.relative]
                #ng.relative = resolved_relative
                
            resolved_sn.append(self._resolve_references(ng, matcher, current_speaker, current_object))
           
        return resolved_sn
    
    
    def _references_resolution_with_anaphora_matcher(self, nominal_group, matcher, current_speaker, current_object):
        """ This attempts to match the nominal group containing anaphoric words with an object identifed from 
            the dialog history.
            However, a confirmation is asked to user
        """
        if current_object:
            self._current_object = None
            return current_object
        
        # Trying to match anaphora
        if not self.sentences_store:
            raise DialogError("Empty Dialog history")
            
        sf = SentenceFactory()
        
        #object = [ng, [List]]
        #       Where ng is the first nominal group to match with the anaphoric word
        #       and List contains nominal group that are to be explored if ng is not confirmed from the user
        
        object = matcher.match_first_object(get_last(self.sentences_store, 10), nominal_group)
            
        # Case there exist only one nominal group identified from anaphora matching
        if object and len(object[1]) <= 1:
            nominal_group = object[0]
        
        # Ask for confirmation to the user
        else:
            raise UnidentifiedAnaphoraError({'object':nominal_group,
                                            'object_to_confirm':object[0],
                                            'object_with_more_info':None,
                                            'objects_list': object[1],
                                            'sentence':self._current_sentence,
                                            'question':sf.create_do_you_mean_reference(object[0])})
                                            
        return nominal_group
        
    ################################################
    #   Nouns phrases resolution and discrimination
    ################################################
    def noun_phrases_resolution(self, sentence, current_speaker, uie_object, uie_object_with_more_info):
        #Skipping processing of sentences that are neither questions nor statements

        logger.info(colored_print("-> Resolving noun phrases", 'green'))
        
        if not sentence.data_type in [Sentence.w_question, Sentence.yes_no_question, Sentence.statement, Sentence.imperative]:
            return sentence
        
        #Nominal group replacement possibly after uie_object and uie_object_with_more_info are sent from Dialog to resolve missing content
        if uie_object and uie_object_with_more_info:
            sentence = self._noun_phrases_replace_with_ui_exception(sentence, uie_object, uie_object_with_more_info)
            
            #No uie_objects needed after replacement
            uie_object = None
            uie_object_with_more_info = None
        
        #Record of current sentence
        self._current_sentence = sentence
        
        #NominalGroupStatementBuilder
        builder = NominalGroupStatementBuilder(None,current_speaker)
        
        #Discrimination
        discriminator = Discrimination()
        
        #sentence.sn nominal groups nouns phrase resolution
        if sentence.sn:
            sentence.sn = self._resolve_groups_nouns(sentence.sn, 
                                                    current_speaker,
                                                    discriminator,
                                                    builder)
        #sentence.sv nominal groups nouns phrase resolution
        if sentence.sv:
            sentence.sv = self.verbal_phrases_noun_resolution(sentence.sv, current_speaker, discriminator, builder)
        
                        
        return sentence
    def _resolve_nouns(self, nominal_group, current_speaker, discriminator, builder):
        """This attempts to resolve a single nominal group by the use of discrimiation routines.
            The output is the ID of the nominal group
        """
        
        if nominal_group._resolved: #already resolved: possible after asking human for more details.
            return nominal_group
        
        logger.debug(str(nominal_group))
        
        #Creating a concept description
        builder.process_nominal_group(nominal_group, '?concept', None, False)
        stmts = builder.get_statements()
        builder.clear_statements()
        
        logger.debug(colored_print("Looking for this concept in "+ current_speaker + "'s model: \n", "magenta") + '[' + colored_print(', '.join(stmts), None, 'magenta') + ']')
        
        # Special case of "other" occuring in the nominal group
        if builder.process_on_other:
            logger.debug(colored_print("\tFound 'Other'.Looking for this concept in both Dialog history and "+ current_speaker + "'s model", "magenta"))
            nominal_group, stmts = self._resolve_nouns_with_dialog_history(nominal_group, current_speaker, stmts, builder)
            if nominal_group._resolved: return nominal_group
            
        #Trying to discriminate 
        description = [[current_speaker, '?concept', stmts]]
        
        #   Features to ignore from discrimination
        features = []
        if self._current_sentence.data_type in [Sentence.w_question, Sentence.yes_no_question]:
            if self._current_sentence.aim in ResourcePool().adjectives_ontology_classes:
                # feature =["hasColor"]
                features = ["has" + self._current_sentence.aim.capitalize()]
            else:
                features = ["rdf:type"]
            
        #   Discriminate
        try:
            id = discriminator.clarify(description, features)
        except UnsufficientInputError as uie:
            #   Create a new concept instead of raising unsificient input error, as the current sentence start with "learn that ..."
            if self._current_sentence.learn_it():
                id = self._ontology_learns_new_concept(stmts, current_speaker)
            else:
                sf = SentenceFactory()
                if uie.value['status'] != 'SUCCESS':
                    uie.value['question'][:0] = sf.create_what_do_you_mean_reference(nominal_group)
                uie.value['object'] = nominal_group
                uie.value['sentence'] = self._current_sentence
                uie.value['object_with_more_info'] = None
                raise uie
        
        logger.debug(colored_print("Hurra! Found \"" + id + "\"", 'magenta'))
        
        nominal_group.id = id
        nominal_group._resolved = True
        
        return nominal_group
    
    
    def _noun_phrases_replace_with_ui_exception(self, sentence, uie_object, uie_object_with_more_info):
        """This attempts to replace a nominal group that has failled from discrimation with one that holds more information.
        """
        #Comparator
        cmp = Comparator()
        
        #Trying to replace in sentence sn
        if sentence.sn:
            for sn in sentence.sn:
                if cmp.compare(sn, uie_object):
                    sn = uie_object_with_more_info
                    return sentence
                            
        #Trying to replace in sentence sv nomina groups
        for sv in sentence.sv:
            for d_obj in sv.d_obj:
                if cmp.compare(d_obj, uie_object):
                    d_obj = uie_object_with_more_info                    
                    return sentence                    
            
            for i_cmpl in sv.i_cmpl:
                for ng in i_cmpl.nominal_group:
                    if cmp.compare(ng , uie_object):
                        ng = uie_object_with_more_info                        
                        return sentence       
        
        return sentence


    def _resolve_groups_nouns(self, nominal_groups, current_speaker, discriminator, builder):
        resolved_sn = []
        for ng in nominal_groups:
            
            if self._current_sentence.learn_it():
                ng.noun_cmpl = self._resolve_groups_nouns(ng.noun_cmpl, current_speaker, discriminator, builder) if ng.noun_cmpl else []
                #resolved_relative = [self.noun_phrases_resolution(relative, current_speaker, None, None) for relative in ng.relative]
                #ng.relative = resolved_relative
                
            resolved_sn.append(self._resolve_nouns(ng, current_speaker, discriminator, builder))
            
        return resolved_sn
    
    
    def _resolve_nouns_with_dialog_history(self, nominal_group, current_speaker, current_stmts, builder):
        """This attempts to resolve nouns that involve both a discrimination processing and searching the dialog history
            E.g: the 'other' cup.
            - if there is only one cup existing in the ontology, then we identify it by a discrimination processing.
            - if there are several cups known in the ontology, then we possibly mean a cup different from the one that has been stated earlier in the dialog.
        """
        
        obj_list = []
        try:
            obj_list = ResourcePool().ontology_server.findForAgent(current_speaker, '?concept', current_stmts)
        except AttributeError:
            pass
            
        
        if obj_list:
            if len(obj_list) == 1:
                nominal_group.id = obj_list[0]
                nominal_group._resolved = True
            
            else:
                historic_objects_list = recover_nominal_group_list(get_last(self.sentences_store, 10))
                if not historic_objects_list:
                    raise DialogError("Error: possibly due to an empty dialog history")
                
                obj_candidate = [obj for obj in historic_objects_list if obj.id in obj_list][0]
                
                # Discriminate everything different from this ID
                current_stmts.append("?concept owl:differentFrom " + obj_candidate.id)
                        
        return nominal_group, current_stmts
        
    
        
    ##########################
    # Verbal group resolutions
    ############################
    def verbal_phrases_resolution(self, sentence):
        #Skipping processing of sentences that are neither questions nor statements
        
        logger.info(colored_print("-> Resolving verbal groups", 'green'))
        
        if not sentence.data_type in [Sentence.w_question, Sentence.yes_no_question, Sentence.statement, Sentence.imperative]:
            return sentence
        
        for sv in sentence.sv:
            sv = self._resolve_verbs(sv)
                    
        return sentence
    
    def _resolve_verbs(self, verbal_group):        
        if verbal_group.resolved(): #already resolved: possible after asking human for more details.
            return verbal_group
        
        resolved_verbs = []
        modal =''
        
        for verb in verbal_group.vrb_main:
            logger.debug("* \"" + verb + "\"")
            # Case of modal verbs. E.g: can, must
            #   or verbs wit prepositions
            if '+' in verb:
                # E.g: can+do
                [first, second] = verb.split('+')
                if first in ResourcePool().modal:
                    modal = first
                    verb = second
                
                # Verb with preposition
                # E.g: look+up => lookup
                else:
                    verb = first + second
                    modal = ''
            
            # Case of to be
            if verb in  ResourcePool().state:
                resolved_verb = "be"
            
            #Goal verbs
            elif verb in ResourcePool().goal_verbs:
                resolved_verb = verb
            
            # Trying to resolve verb from thematic roles
            else:
                try:
                    resolved_verb = ResourcePool().thematic_roles.get_ref(verb)
                    logger.debug("Keeping \"" + verb + "\"" ) \
                                    if verb == resolved_verb else \
                                    ("Replacing \"" + verb + "\" by synonym \"" + resolved_verb + "\"")
                    
                    verb = resolved_verb
                    
                except UnknownVerb:
                    logger.debug("Unknown verb \"" + verb + "\": keeping it like that, but I won't do much with it.")
                    resolved_verb = verb
                
            if modal:
                resolved_verb = modal + '+' + resolved_verb
                
            resolved_verbs.append(resolved_verb)
        
        verbal_group.vrb_main = resolved_verbs
        
        # Secondary verbal group
        for sv_sec in verbal_group.sv_sec:
            sv_sec = self._resolve_verbs(sv_sec)
        
        #Forcing resolution to True
        verbal_group._resolved = True
            
        return verbal_group
     
     
    def verbal_phrases_reference_resolution(self, verbal_groups, matcher,current_speaker, current_object):
        #sentence sv nominal groups reference resolution
        for sv in verbal_groups:
            if sv.d_obj:
                sv.d_obj = self._resolve_groups_references(sv.d_obj,
                                                            matcher,
                                                            current_speaker, 
                                                            self._current_object)
            if sv.i_cmpl:
                resolved_i_cmpl = []
                for i_cmpl in sv.i_cmpl:
                    i_cmpl.nominal_group = self._resolve_groups_references(i_cmpl.nominal_group, 
                                                                                matcher,
                                                                                current_speaker,
                                                                                self._current_object)
                    resolved_i_cmpl.append(i_cmpl)
                
                sv.i_cmpl = resolved_i_cmpl
                
            if sv.sv_sec:
                sv.sv_sec = self.verbal_phrases_reference_resolution(sv.sv_sec, matcher,current_speaker, current_object)
            
            #Subsentence
            if sv.vrb_sub_sentence:
                resolved_vrb = []
                for vrb in sv.vrb_sub_sentence:
                    #sentence sn nominal groups reference resolution
                    if vrb.sn:
                        vrb.sn = self._resolve_groups_references(vrb.sn, matcher, current_speaker, current_object)

                    if vrb.sv:
                        vrb.sv = self.verbal_phrases_reference_resolution(vrb.sv, matcher,current_speaker, current_object)
                    
                    resolved_vrb.append(vrb)
                
                sv.vrb_sub_sentence = resolved_vrb
        
        return verbal_groups
        
        
    def verbal_phrases_noun_resolution(self, verbal_groups, current_speaker, discriminator, builder):
        for sv in verbal_groups:
            if sv.d_obj:
                sv.d_obj = self._resolve_groups_nouns(sv.d_obj, 
                                                     current_speaker,
                                                     discriminator,
                                                     builder)  
            if sv.i_cmpl:
                resolved_i_cmpl = []
                for i_cmpl in sv.i_cmpl:
                    i_cmpl.nominal_group = self._resolve_groups_nouns(i_cmpl.nominal_group, 
                                                       current_speaker,
                                                       discriminator,
                                                       builder)
                    resolved_i_cmpl.append(i_cmpl)
                sv.i_cmpl = resolved_i_cmpl
            
            if sv.sv_sec:
                sv.sv_sec = self.verbal_phrases_noun_resolution(sv.sv_sec, current_speaker, discriminator, builder)
        
            #Subsentence
            if sv.vrb_sub_sentence:
                resolved_vrb = []
                for vrb in sv.vrb_sub_sentence:
                    #sentence.sn nominal groups nouns phrase resolution
                    if vrb.sn:
                        vrb.sn = self._resolve_groups_nouns(vrb.sn, 
                                                                current_speaker,
                                                                discriminator,
                                                                builder)
                    #sentence.sv nominal groups nouns phrase resolution
                    if vrb.sv:
                        vrb.sv = self.verbal_phrases_noun_resolution(vrb.sv, current_speaker, discriminator, builder)
                    
                    resolved_vrb.append(vrb)
                
                sv.vrb_sub_sentence = resolved_vrb


        return verbal_groups

    ##########################
    # Learning a new concept
    ############################
    def _ontology_learns_new_concept(self, concept_description, current_speaker):
        """This method commit a new concept in the ontology regarding the description that has been provided.
            Also, it returns a randomly genrated ID of the new concept
        """
        #Genrating ID
        id = generate_id(with_question_mark = False)
        
        #Replacing '?concept' by ID
        stmts = [s.replace('?concept', id) for s in concept_description]

        #Removing remaining statements holding unbound tokens other than '?concept' 
        # in order not to add unbound references in the ontology.
        stmts = [s for s in stmts if not "?" in s]
        
        #Commiting the ontology now, in case of a research on this concept on the remaining unresolved concepts of the sentence
        logger.debug(colored_print("Learning this new concept in "+ current_speaker + "'s model: \n", "magenta") + '[' + colored_print(', '.join(stmts), None, 'magenta') + ']')
        try:
            ResourcePool().ontology_server.addForAgent(current_speaker, stmts)
        except AttributeError:
            pass
            
        if current_speaker != 'myself':
            logger.debug(colored_print("Learning this new concept in robot's model: \n", "magenta") + '[' + colored_print(', '.join(stmts), None, 'magenta') + ']')
            try:
                ResourcePool().ontology_server.add(stmts)
            except AttributeError:
                pass

        return id


def get_last(list, nb):
    """This returns the last 'Nb' elements of the list 'list' in the reverse order"""
    #Empty list
    if not list:
        return list
    
    #Not empty list but, NB > len(list).
    if nb > len(list):
        stnts = list
    # last NB elements
    else:
        last = len(list)
        stnts = list[(last - nb):last]
    
    #reverse    
    stnts.reverse()
    
    return stnts



def unit_tests():
    """This function tests the main features of the class Resolver"""
    print("This is a test...")

if __name__ == '__main__':
    unit_tests()

# coding=utf-8
import logging

logger = logging.getLogger("dialogs")

import random

from kb import KbError

from dialogs.resources_manager import ResourcePool
from dialogs.dialog_exceptions import DialogError, GrammaticalError
from dialogs.helpers.helpers import generate_id

from dialogs.sentence import *

"""This module implements ...

"""


class StatementBuilder(object):
    """ Build statements related to a sentence"""

    def __init__(self, current_speaker=None):
        #This field keeps record of the sentence that is being processed
        self._sentence = None

        #This field identifies the current speaker
        self._current_speaker = current_speaker


        #This holds the statements created from the main clause of a sentence
        self._statements = []

        #This holds the statements that are to be removed from the ontology
        #   Possibly after processing a negative sentence
        self._statements_to_remove = []

        #This holds unidentified IDs that are generated while creating the statements of a resolved sentence.
        #   Possibly in the case of a negative sentence involving an action that is to be identity in the module StatementSafeAdder
        self._unclarified_ids = []

        #This field holds concepts for class grounding
        self.lear_more_concept = []


    def clear_all(self):
        self._statements = []
        self._statements_to_remove = []
        self._unclarified_ids = []
        self.lear_more_concept = []

    def clear_statements(self):
        self._statements = []

    def set_current_speaker(self, current_speaker):
        self._current_speaker = current_speaker

    def process_sentence(self, sentence):
        """ Build statements from a resolved sentence.

        :return: a tuple (stmts, situation_id) where stmts is a list
        of produced stmts and situation_id is the id of the newly created 
        situation (like a desire) or None if no situation was created.
        """
        if not sentence.resolved():
            raise DialogError("Trying to process an unresolved sentence!")

        self._sentence = sentence

        if sentence.sn:
            self.process_nominal_groups(self._sentence.sn)
        if sentence.sv:
            situation_id = self.process_verbal_groups(self._sentence)

        return self._statements, situation_id


    def process_nominal_groups(self, nominal_groups):
        ng_stmt_builder = NominalGroupStatementBuilder(nominal_groups, self._current_speaker)
        ng_stmt_builder.process()

        self._statements.extend(ng_stmt_builder._statements)
        self._unclarified_ids.extend(ng_stmt_builder._unclarified_ids)
        self.lear_more_concept.extend(ng_stmt_builder.lear_more_concept)

    def process_verbal_groups(self, sentence):
        #VerbalGroupStatementBuilder
        vg_stmt_builder = VerbalGroupStatementBuilder(sentence.sv, self._current_speaker)

        #Setting up attribute of verbalGroupStatementBuilder:
        #    process_on_imperative
        #    process_on_question
        #     process_on_learning_new_concept
        #     process_on_resolved_sentence
        vg_stmt_builder.set_attribute_on_data_type(sentence)

        if not sentence.sn:
            vg_stmt_builder.process()

            self._statements.extend(vg_stmt_builder._statements)
            self._unclarified_ids.extend(vg_stmt_builder._unclarified_ids)
            self.lear_more_concept.extend(vg_stmt_builder.lear_more_concept)

            # Case of statement to remove due to some case of negation
            if vg_stmt_builder.process_statements_to_remove:
                self._statements_to_remove.extend(vg_stmt_builder._statements)

        for sn in sentence.sn:
            if not sn.id:
                raise EmptyNominalGroupId("Nominal group ID not resolved or not affected yet")

            vg_stmt_builder.process(subject_id=sn.id, subject_quantifier=sn._quantifier)

            self._statements.extend(vg_stmt_builder._statements)
            self._unclarified_ids.extend(vg_stmt_builder._unclarified_ids)
            self.lear_more_concept.extend(vg_stmt_builder.lear_more_concept)

            # Case of statement to remove due to some case of negation
            if vg_stmt_builder.process_statements_to_remove:
                self._statements_to_remove.extend(vg_stmt_builder._statements)

        return vg_stmt_builder.situation_id


class NominalGroupStatementBuilder(object):
    """ Build statements related to a nominal group
    """

    def __init__(self, nominal_groups, current_speaker=None):
        #This field keeps record of the nominal group that is being processed
        self._nominal_groups = nominal_groups

        #This field identifies the current speaker
        self._current_speaker = current_speaker

        #This holds the statements created from the main clause of a sentence
        self._statements = []

        #This holds unidentified IDs that are generated while creating the statements of a resolved sentence.
        #   Possibly in the case of a negative sentence involving an action that is to be identity in the module StatementSafeAdder
        self._unclarified_ids = []

        #This field holds concepts for class grounding
        self.lear_more_concept = []

        #This field is True when the special case of "other" occurs in adjectives
        #   E.g: Give me the "other" tape
        self.process_on_other = False

        #This field is True when the determiners "this", "that" occur
        #   E.g: Give me this tape
        self.process_on_demonstrative_det = False

    def clear_statements(self):
        self._statements = []

    def process(self):
        """ The following function builds a list of statement from a list of nominal group
        A NominalGroupStatementBuilder has to be instantiated before
        """

        for ng in self._nominal_groups:
            if not ng.id:
                ng.id = self.set_nominal_group_id(ng)

            self.process_nominal_group(ng, ng.id, None, False)

        return self._statements

    def get_statements(self):
        return self._statements

    def set_nominal_group_id(self, ng):
        if ng.id:
            return ng.id

        onto = ''
        try:
            onto = ResourcePool().ontology_server.lookupForAgent(ResourcePool().get_model_mapping(self._current_speaker), ng.noun[0])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass

        if onto:
            for c in onto:
                if "instance" in c:
                    return c[0]

        if ng.noun[0].lower() in ['i', 'me']:
            return self._current_speaker

        if ng.noun[0].lower() == 'you':
            return 'myself'

        id = generate_id()
        self._unclarified_ids.append(id)
        return id


    def process_nominal_group(self, ng, ng_id, subject_quantifier, negative_object):
        """ The following function processes a single nominal_group with a given resolved ID and quantifier
            the parameter 'negative_object' is to meant that the sentence hold a negative form involving the nominal group being processed
        """

        def process_all_component_of_a_nominal_group(nom_grp, id, quantifier, negative):
            """This processes all the components of a given nominal group 'nom_grp'. """
            if nom_grp.noun:
                self.process_noun_phrases(nom_grp, id, quantifier, negative)
            if nom_grp.det:
                self.process_determiners(nom_grp, id, negative)
            if nom_grp.adj:
                self.process_adjectives(nom_grp, id, negative)
            if nom_grp.noun_cmpl:
                self.process_noun_cmpl(nom_grp, id, negative)
            if nom_grp.relative:
                self.process_relative(nom_grp, id)

        # End of process_all_component_of_a_nominal_group()

        def get_concept_to_learn(nom_grp):
            if nom_grp._quantifier == 'ONE':
                return [] #Concept already known for sure

            learn_more = []

            for noun in nom_grp.noun:
                onto = ''
                try:
                    onto = ResourcePool().ontology_server.lookupForAgent(ResourcePool().get_model_mapping(self._current_speaker), noun)
                except AttributeError:
                    pass

                if not onto:
                    learn_more.append(noun)

            return learn_more

            # End of get_concept_to_learn ()


        # Case of resolved nominal group
        if ng._resolved:

            #Trying to learn more concept
            self.lear_more_concept = get_concept_to_learn(ng)

            # Case: Adjectives only
            if ng.adjectives_only():
                self.process_adjectives(ng, ng_id, negative_object)

            #Case: Quantifier of the nominal group being processed. 
            elif subject_quantifier:
                # Case of an finite nominal group described by either a finite or an infinite one
                #
                # E.g "this is 'a blue cube'" provides:
                #   [something hasColor blue, something rdf:type Cube] where something is known in the ontology as [* focusesOn something]
                # E.g "this is 'my cube'" should provide [something belongsTo *]
                if subject_quantifier == 'ONE':
                    process_all_component_of_a_nominal_group(ng, ng_id, subject_quantifier, negative_object)

                # Case of an infinite nominal group
                # E.g "Apples are Yellow Fruits",  or "An apple is a yellow fruit"
                #   it is wrong to create the statement [Apples hasColor yellow], as it transforms "Apple" into on instance
                # TODO: in this example, 'yellow' is completly dropped
                elif ng.noun and \
                                subject_quantifier in ['SOME', 'ALL'] and \
                                ng._quantifier in ['SOME', 'ALL']:
                    self.process_noun_phrases(ng, ng_id, subject_quantifier, negative_object)

        #Case of a not resolved nominal group
        else:
            process_all_component_of_a_nominal_group(ng, ng_id, subject_quantifier, negative_object)


    def process_determiners(self, nominal_group, ng_id, negative_object):
        for det in nominal_group.det:
            #logger.debug("Found determiner:\"" + det + "\"")
            # Case 1: definite article : the"""
            # Case 2: demonstratives : this, that, these, those"""
            if det in ResourcePool().demonstrative_det: #['this', 'that', 'these', 'those']:
                self.process_on_demonstrative_det = True

            # Case 3: possessives : my, your, his, her, its, our, their """
            if det == "my" and not negative_object:
                #Case of Direction: The left of, the right of ...
                if nominal_group.noun and nominal_group.noun[0] in ResourcePool().direction_words:
                    self._statements.append(
                        ng_id + " is" + nominal_group.noun[0].capitalize() + "Of " + self._current_speaker)
                else:
                    self._statements.append(ng_id + " belongsTo " + self._current_speaker)

            elif det == "your" and not negative_object:
                #Case of Direction: The leftOf, the right of ...
                if nominal_group.noun and nominal_group.noun[0] in ResourcePool().direction_words:
                    self._statements.append(ng_id + " is" + nominal_group.noun[0].capitalize() + "Of myself")
                else:
                    self._statements.append(ng_id + " belongsTo myself")

                    # Case 4: general determiners: See http://www.learnenglish.de/grammar/determinertext.htm"""


    def process_noun_phrases(self, nominal_group, ng_id, ng_quantifier, negative_object):

        def get_object_property(subject_quantifier, object_quantifier):
            """ The following returns the appropriate object property relationship between two nominal groups; the subject and the object.
                These are the rule:
                    - ONE + ONE => rdf:type ; 
                        E.g: [The blue cube] is [small]. 
                        Here, both nominal groups of 'the blue cube' and 'small' hold the quantifier 'ONE'
                    
                    - ONE + SOME => rdf:type; 
                        E.g: [The blue object] is [a robot]. 
                        Here, the nominal group of robot holds the indefinite quantifier 'SOME'
                    
                    - SOME + SOME => rdfs:subClassOf;
                        E.g: [an apple] is [a fruit].
                        Both the quantifier of the nominal groups of "apple" and "fruit" are 'SOME'.
                        This is a convention for all nomina group with an indefinite determiner
                        
                    - ALL + ALL => rdfs:subClassOf ;
                        E.g: [Apples] are [fruits].
                        E.g: [the apples] are [the fruits].
                        Here, both Apples and Fruits hold the quantifier 'ALL'. 
                        This is a convention for all nominal group with plural nouns
                    
                    for more details about quantifiers, see sentence.py 
            """
            if [subject_quantifier, object_quantifier] in [['SOME', 'SOME'],
                                                           ['ALL', 'ALL']]:
                return ' rdfs:subClassOf '

            else:#default case
                return ' rdf:type '

        # End of def get_object_property()


        for noun in nominal_group.noun:
            # Case : existing ID
            onto_id = ''
            try:
                onto_id = ResourcePool().ontology_server.lookupForAgent(ResourcePool().get_model_mapping(self._current_speaker), noun)
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            except KbError: #The agent does not exist in the ontology
                pass

            instance_id = None
            if onto_id:
                # If one of the returned concepts is an instance, take the first one.
                for c in onto_id:
                    if "instance" in c:
                        instance_id = c[0]
                        break

            if instance_id:
                #Case of Negation
                if negative_object:
                    self._statements.append(ng_id + " owl:differentFrom " + instance_id)

                elif nominal_group._resolved:
                    self._statements.append(ng_id + " owl:sameAs " + instance_id)


            # Case : Personal pronoun
            elif not nominal_group.det and noun in ResourcePool().pronouns:
                # Case of negation
                if negative_object:
                    # assign noun_id == current_speaker ID or Current receipient, or so on
                    noun_id = None

                    if noun in ["I", "me"]:
                        noun_id = self._current_speaker
                    elif noun in ["you"]:
                        noun_id = "myself"

                    if noun_id:
                        self._statements.append(ng_id + " owl:differentFrom " + noun_id)
                    else:
                        logger.debug("Aie Aie!! Personal pronoun " + noun + " Not implemented yet!")

                # Case of affirmative form
                else:
                    pass

            #Case : proper noun (Always Capitalized in sentence, and never follows a determiner) 
            elif not nominal_group.det and noun.istitle():
                logger.info(
                    "... \t" + noun + " is being processed as a proper noun in  " + self._current_speaker + "'s model.")
                self._statements.append(ng_id + " rdfs:label \"" + noun + "\"")

            # Case : common noun    
            else:
                logger.info(
                    "... \t" + noun + " is being processed as a common noun in " + self._current_speaker + "'s model.")

                # Case of Directions
                if noun in ResourcePool().direction_words:
                    class_name = 'Location'
                    if not nominal_group.noun_cmpl:
                        self._statements.append(ng_id + " is" + noun.capitalize() + "Of " + self._current_speaker)


                # get the exact class name (capitalized letters where needed)
                else:
                    class_name = get_class_name(noun, onto_id)

                # get the exact object property (subClassOf or type)
                object_property = get_object_property(ng_quantifier, nominal_group._quantifier)

                # Case of negation
                if negative_object:
                    # Case of a definite concept
                    if nominal_group._quantifier == 'ONE':
                        self._statements.append(ng_id + " owl:differentFrom " + nominal_group.id)

                    # Case of an indefinite concept
                    else:
                        #Committing ComplementOf class
                        try:
                            ResourcePool.ontology_server.safeAdd(
                                ["ComplementOf" + class_name + " owl:complementOf " + class_name,
                                 "ComplementOf" + class_name + " rdfs:subClassOf ComplementClasses"])
                        except AttributeError:
                            pass

                        self._statements.append(ng_id + object_property + "ComplementOf" + class_name)


                # Case of affirmative sentence
                else:
                    if isinstance(ng_id, basestring):
                        ng_id = [ng_id]
                    self._statements += [id + object_property + class_name for id in ng_id]


    def process_adjectives(self, nominal_group, ng_id, negative_object):
        """For any adjectives, we add it in the ontology with the objectProperty 
        'hasFeature' except if a specific category has been specified in the 
        adjectives list.
        """
        for adj in nominal_group.adj:
            #Case of 'other'
            # E.g: the other cube:
            if adj[0].lower() == "other":
                self.process_on_other = True
                pass
                #self._statements.append(ng_id + " owl:differentFrom " + nominal_group.id)

            elif adj[0].lower() == "same":
                pass


            #TODO: case of class Feature
            # Apple are yellow fruits

            # Case of features
            else:
                #Getting the object property if there exists a specific class
                object_property = ''
                try:
                    object_property = " has" + ResourcePool().adjectives[adj[0]] + " "

                #Default case, creating hasFeature object Property
                except KeyError:
                    object_property = " hasFeature "

                #Case negative assertion
                if negative_object:
                    negative_adj = generate_id(with_question_mark=not nominal_group._resolved)

                    self._statements.append(ng_id + object_property + negative_adj)
                    self._statements.append(negative_adj + ' owl:differentFrom ' + adj[0])

                #Case Affirmative assertion
                else:
                    if isinstance(ng_id, basestring):
                        ng_id = [ng_id]
                    self._statements += [id + object_property + adj[0] for id in ng_id]


    def process_noun_cmpl(self, nominal_group, ng_id, negative_object):
        """This attempts to process the noun complment attribute of a nominal group:
            E.g: The car of Danny
            This example should provide the statements [danny_car rdf:type Car, 
                                                        danny_car belongsTo DANNY]
            where 'danny_car' is the existing ID of the car of Danny in the ontology and
            'DANNY' is the ID of an existing agent named 'Danny'
        """

        for noun_cmpl in nominal_group.noun_cmpl:
            if noun_cmpl.id:
                noun_cmpl_id = noun_cmpl.id
            else:
                noun_cmpl_id = self.set_nominal_group_id(noun_cmpl)

            if not nominal_group._resolved:
                self.process_nominal_group(noun_cmpl, noun_cmpl_id, None, False)
                # Case of affirmation
            if not negative_object:
                #Case of Direction: The left of, the right of ...
                if nominal_group.noun and nominal_group.noun[0] in ResourcePool().direction_words:
                    self._statements.append(ng_id + " is" + nominal_group.noun[0].capitalize() + "Of " + noun_cmpl_id)
                else:
                    self._statements.append(ng_id + " belongsTo " + noun_cmpl_id)

    def process_relative(self, nominal_group, ng_id):
        """ The following processes the relative clause of the subject of a sentence.           
           case 1: the subject of the sentence is complement of the relative clause
                    e.g. the man that you heard from is my boss
                          => the man is my boss + you heard from the man
                          => sn != []
            
           case 2: the subject of the sentence is subject of the relative clause.
                   we process only the verbal group of the relative.
                    e.g. the man who is talking, is tall
                         => the man is tall and is talking
                         => sn == []
        """

        def set_relative_object_id_with_parent_nominal_goup_id(parent_ng, current_relative, parent_ng_id):
            #get parent ng with no relative
            current_ng = parent_ng
            current_ng.relative = []

            #set comparator
            cmp = Comparator()

            #Start comparison between current_ng and current_relative
            for sv in current_relative.sv:
                #direct object
                for d_obj in sv.d_obj:
                    if cmp.compare(d_obj, current_ng):
                        d_obj.id = parent_ng_id

                #indirect object
                for i_cmpl in sv.i_cmpl:
                    for i_cmpl_ng in i_cmpl.gn:
                        if cmp.compare(i_cmpl_ng, current_ng):
                            i_cmpl_ng.id = parent_ng_id

        for rel in nominal_group.relative:
            #logger.debug("processing relative:")
            if rel.sv:
                rel_vg_stmt_builder = VerbalGroupStatementBuilder(rel.sv, self._current_speaker)
                #case 1
            if rel.sn:
                set_relative_object_id_with_parent_nominal_goup_id(nominal_group, rel, ng_id)

                rel_ng_stmt_builder = NominalGroupStatementBuilder(rel.sn, self._current_speaker)
                for ng in rel.sn:
                    ng.id = rel_ng_stmt_builder.set_nominal_group_id(ng)

                    rel_ng_stmt_builder.process_nominal_group(ng, ng.id, None, False)
                    rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng.id, None)

                self._statements.extend(rel_ng_stmt_builder._statements)
                self._unclarified_ids.extend(rel_ng_stmt_builder._unclarified_ids)
                self.lear_more_concept.extend(rel_ng_stmt_builder.lear_more_concept)
            #case 2        
            else:
                rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng_id, None)

            self._statements.extend(rel_vg_stmt_builder._statements)
            self._unclarified_ids.extend(rel_vg_stmt_builder._unclarified_ids)
            self.lear_more_concept.extend(rel_vg_stmt_builder.lear_more_concept)


class VerbalGroupStatementBuilder(object):
    """ Build statements related to a verbal group"""

    def __init__(self, verbal_groups, current_speaker=None):
        #This field keeps record of the verbal group that is being processed
        self._verbal_groups = verbal_groups

        #This field identifies the current speaker
        self._current_speaker = current_speaker

        #The id of the situation (desire/event) generated by the processing
        self.situation_id = None

        #This holds the statements created from the main clause of a sentence
        self._statements = []

        #This holds unidentified IDs that are generated while creating the statements of a resolved sentence.
        #   Possibly in the case of a negative sentence involving an action that is to be identity in the module StatementSafeAdder
        self._unclarified_ids = []

        #This field holds the value True when the active sentence is of yes_no_question or w_question data_type
        self._process_on_question = False

        #This field holds the value True when the active sentence is of imperative data_type
        self._process_on_imperative = False

        #This field holds the value True when the active sentence is fully resolved
        self._process_on_resolved_sentence = False

        #this field is True when the verbal group is in the negative form
        self._process_on_negative = False

        #this fiels is True when the sentence that is being processed holds a negative state and 
        # more particualrly in the case of action verbs where a static situation reference is generated
        self.process_statements_to_remove = False

        #This field holds concepts for class grounding
        self.lear_more_concept = []

        #This field is set on True if dealing with a setence starting with "learn that/it ..."
        # E.g: Learn that a location is a place
        #    thus IDs are generated for concept that are possibly not known in the ontology
        self._process_on_learning_new_concept = True

    def set_attribute_on_data_type(self, sentence):
        if sentence.data_type == IMPERATIVE:
            self._process_on_imperative = True
        if sentence.data_type in [YES_NO_QUESTION, W_QUESTION]:
            self._process_on_question = True

        self._process_on_resolved_sentence = sentence.resolved()
        self._process_on_learning_new_concept = sentence.islearning()

    def clear_statements(self):
        self._statements = []

    def process(self, subject_id=None, subject_quantifier=None):
        """This processes a sentence sv attribute, given the (resolved) ID and quantifier of the subject
            and return a set of RDF statements.
        """
        #Case: an imperative sentence does not contain an sn attribute,
        #      we will assume that it is implicitly an order from the current speaker.
        #      performed by the recipient of the order.
        #      Therefore, the subject_id holds the value 'myself'
        if self._process_on_imperative:
            subject_id = 'myself'

        if not subject_id:
            subject_id = '?concept'

        self.process_verbal_groups(self._verbal_groups, subject_id, subject_quantifier)
        return self._statements

    def get_statements(self):
        return self._statements


    def process_verbal_groups(self, verbal_groups, subject_id, subject_quantifier, second_verb_sit_id=None):
        """This processes every single verbal group in the sentence sv, given the (resolved) ID and quantifier of the subject.
        """
        for vg in verbal_groups:
        #Verbal group state : Negative or affirmative
            self.process_state(vg)

            #Main verb
            if vg.vrb_main:
                self.process_verb(vg, subject_id, subject_quantifier, second_verb_sit_id)

            if vg.advrb:
                self.process_sentence_adverb(vg)

            # Subordinating clause
            if vg.vrb_sub_sentence:
                self.process_vrb_subsentence(vg)


    def process_state(self, verbal_group):
        if verbal_group.state == Verbal_Group.negative:
            self._process_on_negative = True
        else:
            self._process_on_negative = False


    def process_verb(self, verbal_group, subject_id, subject_quantifier, second_verb_sit_id):

        for verb in verbal_group.vrb_main:

            #Case 1:  the state verb 'to be'/ to become"""
            #Case 2:  actions or stative verbs with a specified 'goal' or 'thematic' role:
            #                          see '../../share/dialog/thematic_roles'
            #Case 3: actions verbs with 'passive behaviour' like 'see'
            #Case 4: special case for 'know'
            #Case 5:  other action or stative verbs

            # Modal or phrasal verbs. E.g: can+do, look+for , ...
            #                   verb = must+do
            modal = ''
            if '+' in verb:
                # Case of Modals
                [modal, verb] = verb.split('+')
                if modal in ResourcePool().modal:
                    pass
                    #self._statements.append(sit_id + " rdf:type " + verb.capitalize())
                    #self._statements.append(subject_id+ " " + modal +"Performs " + sit_id)

            #Case 1:
            if verb in ResourcePool().state:
                if isinstance(subject_id, basestring):
                    subjects_id = [subject_id]
                else:
                    subjects_id = subject_id

                try:
                    agentslist = ResourcePool().ontology_server.listAgents()
                except AttributeError:
                    agentslist = [ResourcePool().default_model, self._current_speaker]

                for subject_id in subjects_id:
                    if subject_id in agentslist:
                        sit_id = generate_id(with_question_mark=False)
                        self._statements.append(subject_id + " experiences " + sit_id)
                    else:
                        #TODO: Will keep only the last one is several ids
                        sit_id = subject_id
            else:

                # First, create a situation ID that represent the
                # semantic situation carried by the verbal phrase

                #Case : the verbal group that is being processed is the second verbs . i.e : it is held in the field sentence.sv.sv_sec
                if second_verb_sit_id:
                    sit_id = second_verb_sit_id

                # Case of question
                elif self._process_on_question:
                    sit_id = '?event'

                #case of negation : Creating a fake ID that is to find in the ontology for later removal
                #   Setting up the field process_statement_to_remove to True
                elif self._process_on_negative:
                    sit_id = generate_id(with_question_mark=True)
                    self._unclarified_ids.append(sit_id)
                    self.process_statements_to_remove = True

                # General case: we generate an ID
                else:
                    sit_id = generate_id(with_question_mark=not self._process_on_resolved_sentence)


                # Then, process the type of verb

                #Case 2:
                if verb in ResourcePool().goal_verbs:
                    self._statements.append(subject_id + " desires " + sit_id)

                    if verbal_group.sv_sec:
                        self.process_vrb_sec(verbal_group, subject_id, subject_quantifier, sit_id)

                #Case 3: action verbs wit passive behaviour
                elif verb.lower() in ResourcePool().action_verb_with_passive_behaviour.keys():
                    sit_id = subject_id

                # Case 4: 'know'
                elif verb.lower() == 'know':
                    pass

                #Case 5: other verbs -> reification
                else:
                    self._statements.append(sit_id + " rdf:type " + verb.capitalize())
                    self._statements.append(sit_id + " performedBy " + subject_id)
                    if not self._process_on_question and \
                       not self._process_on_negative \
                       and self._process_on_resolved_sentence:
                        # If I'm not processing a question, add a label
                        # to this action
                        self._statements.append(sit_id + " rdfs:label \"" + \
                                                verb.capitalize() + " action #" + sit_id + "\"")

            # Store the situation id
            self.situation_id = sit_id

            #Imperative specification, add the goal verb 'desire'
            if self._process_on_imperative:
                self._statements.append(self._current_speaker + " desires " + sit_id)


            #Direct object
            if verbal_group.d_obj:
                self.process_direct_object(verbal_group.d_obj, verb, sit_id, subject_quantifier)


            #Indirect Complement
            if verbal_group.i_cmpl:
                self.process_indirect_complement(verbal_group.i_cmpl, verb, sit_id)

            # Adverbs modifiying the manner of an action verb
            if verbal_group.vrb_adv:
                self.process_action_verb_adverb(verbal_group.vrb_adv, verb, sit_id)


            #verb tense
            if verbal_group.vrb_tense:
                self.process_verb_tense(verbal_group, verb, sit_id)


    def process_vrb_sec(self, verbal_group, subject_id, subject_quantifier, sit_id):
        vrb_sec_builder = VerbalGroupStatementBuilder(verbal_group.sv_sec, self._current_speaker)
        vrb_sec_builder.process_verbal_groups(verbal_group.sv_sec, subject_id, subject_quantifier, sit_id)
        self._statements.extend(vrb_sec_builder._statements)
        self._unclarified_ids.extend(vrb_sec_builder._unclarified_ids)
        self.lear_more_concept.extend(vrb_sec_builder.lear_more_concept)

    def process_direct_object(self, d_objects, verb, id, quantifier):
        """This processes the attribute d_obj of a sentence verbal groups."""
        #logger.debug("Processing direct object d_obj:")

        d_obj_stmt_builder = NominalGroupStatementBuilder(d_objects, self._current_speaker)

        # Retrieve the thematic role of the direct object from the library.
        # If not defined, use the generic 'involves' predicate.
        try:
            d_obj_role = " " + ResourcePool().thematic_roles.verbs[verb].roles[0].id + " "
        except  KeyError:
            d_obj_role = " involves "

        if verb.lower() in ResourcePool().action_verb_with_passive_behaviour.keys():
            d_obj_role = ' ' + ResourcePool().action_verb_with_passive_behaviour[verb.lower()] + ' '

        # Case of know
        if verb.lower() == 'know':
            d_obj_role = ''

        #nominal groups
        for d_obj in d_objects:
            #Case 1: The direct object follows the verb 'to be'.
            #        We process the d_obj with the same id as the subject of the sentence
            if verb in ResourcePool().state:
                d_obj_id = id
                d_obj_quantifier = quantifier

            #Case 2: The direct object follows another stative or action verb.
            #        we process the d_obj as involved by the situation
            else:
                if d_obj.id:
                    d_obj_id = d_obj.id
                else:
                    d_obj_id = d_obj_stmt_builder.set_nominal_group_id(d_obj)

                if d_obj_role:
                    self._statements.append(id + d_obj_role + d_obj_id)

                d_obj_quantifier = None

            d_obj_stmt_builder.process_nominal_group(d_obj, d_obj_id, d_obj_quantifier, self._process_on_negative)

        self._statements.extend(d_obj_stmt_builder._statements)
        self._unclarified_ids.extend(d_obj_stmt_builder._unclarified_ids)
        self.lear_more_concept.extend(d_obj_stmt_builder.lear_more_concept)


    def process_indirect_complement(self, indirect_cmpls, verb, sit_id):

        for ic in indirect_cmpls:

            # Case 1: if there is no preposition, the indirect complement is obviously an indirect object.
            #        Therefore, it receives the action
            #            e.g. I gave you a ball also means I gave a ball 'to' you
            #        see http://www.englishlanguageguide.com/english/grammar/indirect-object.asp

            #Case 2: if there is a preposition, the indirect complement is either an indirect object or an adverbial
            #        if the main verb is specified as a thematic role, we extract the matching object_property to the preposition.
            #            e.g I moved the bottle 'to' the table. The object_property takes the value "hasGoal"
            # 
            #        if the preposition is 'to' , by default we assume the indirect complement is an indirect object
            #            e.g. I gave a ball to Jido. The object_property takes the value "receivedBy"
            #        otherwise, the default processing is to create an object_property by concatenating is and the preposition
            #            e.g. I bought a ball for Jido. The object_property takes the value "isFor"


            i_stmt_builder = NominalGroupStatementBuilder(ic.gn, self._current_speaker)
            for ic_noun in ic.gn:

                #Indirect object ID
                if ic_noun.id:
                    ic_noun_id = ic_noun.id
                else:
                    ic_noun_id = i_stmt_builder.set_nominal_group_id(ic_noun)


                #Proposition role
                icmpl_role = None
                icmpl_qualification = None

                # Case of no preposition
                if not ic.prep:
                    icmpl_role = " receivedBy "

                    # Case of a preposition. Attempt to get from thematic roles
                else:
                    icmpl_role = ResourcePool().thematic_roles.get_cmplt_role_for_preposition(verb, ic.prep[0], True)

                    # If no thematic role exist AND the verb is not a state
                    # verb, use the generic role 'involves' and try to qualify it properly.
                    #  E.g: 'move the ball next to the table' ->
                    # action type Move, ..., action involves id1, id1 isNextTo table
                    if not icmpl_role:
                        try:
                            if verb not in ResourcePool().state:
                                icmpl_qualification = ResourcePool().preposition_rdf_object_property[ic.prep[0]][0]
                            else:
                                icmpl_role = " %s " % ResourcePool().preposition_rdf_object_property[ic.prep[0]][0]
                        except IndexError:
                            if ic.prep:
                                icmpl_qualification = "is" + ic.prep[0].capitalize()


                #Creating statements
                # Case of negation
                if self._process_on_negative:
                    negative_ic_noun_id = generate_id(with_question_mark=False)
                    self._statements.append(sit_id + icmpl_role + negative_ic_noun_id)

                    self._statements.append(negative_ic_noun_id + ' owl:differentFrom ' + ic_noun_id)

                # Case of affirmation
                else:
                    if icmpl_qualification:
                        qualification_id = generate_id(with_question_mark=False)
                        self._statements += \
                            ["%s involves %s" % (sit_id, qualification_id),
                             "%s %s %s" % (qualification_id, icmpl_qualification, ic_noun_id)]
                    else:
                        self._statements.append(sit_id + icmpl_role + ic_noun_id)

                i_stmt_builder.process_nominal_group(ic_noun, ic_noun_id, None, False)

            self._statements.extend(i_stmt_builder._statements)
            self._unclarified_ids.extend(i_stmt_builder._unclarified_ids)
            self.lear_more_concept.extend(i_stmt_builder.lear_more_concept)


    def process_sentence_adverb(self, verbal_group):
        id = generate_id(with_question_mark=False)
        for a in verbal_group.advrb:
            if a in ResourcePool().location_adverbs:
                self._statements += ["%s hasGoal %s" % (self.situation_id, id),
                                     "%s rdf:type %sZone" % (id, a.capitalize())]


    def process_action_verb_adverb(self, advrb, verb, id):
        """This provides a solution in order to process adverbs modifying the meaning of the action verbs.
            Stative verbs are not taken into consideration.
            
            Eg: Danny 'slowly' drives the blue car.
            In this example, we may want to create the following statements: 
                [ * rdf:type Drive, 
                  * performedBy id_dany,
                  * involves id_blue_car,
                  ...
                  * actionQualification SLOW]
            
            However, this solution is not appropriate for stative verb. It wouldn't make sense to say "Danny is slowly a human".
        """

        if verb == 'be':
            logger.warning("I do not know what to do with the adverb(s) " + str(
                advrb) + " that qualify the stative verb 'to be'. Skipping it.")
        else:
            for adv in advrb:
                #Creating statement [id actionQualification pattern], where if adv == carefully then pattern = CAREFUL, if adv == slowly then pattern = SLOW, ...
                self._statements.append(id + " actionQualification " + adv[:len(adv) - 2].upper())


    def process_verb_tense(self, verbal_group, verb, id):
        """This provides a solution to process verb tense for action verbs ONLY.
        we create the object property 'eventOccurs' and bind it with the flag PAST or FUTUR
        
            E.g: Danny 'went' to Toulouse.
            In this example we may want to create the statements:
            [* rdf:type Go,
             * performedBy id_anny,
             * hasGoal id_toulouse,
             ...
             
             * eventOccurs PAST]
             
            Although, we do not implement this for stative verb, it may be adapted in the case of describing objects feature, location, and so on.
            Therefore, we need to create new object properties.
                E.g : 'hasFeature' may be turned into 'hadFeature' and 'willHaveFeature'
                      'isOn' may be turned into 'wasOn' and 'willBeOn'.
            
            It would not work for object type or class, as it does not make sense to say "Fruits were Plants".
        """
        if verbal_group._resolved and not self._process_on_question:

            #Assiging the variable 'tense' with either PAST or FUTUR
            tense = '' #Nothing to do if the verb tense involves the present

            #PAST
            if 'past' in verbal_group.vrb_tense:
                tense = 'PAST'

            #FUTUR
            if 'futur' in verbal_group.vrb_tense:
                tense = 'FUTUR'

            if verb != 'be' and tense:
                self._statements.append(id + ' eventOccurs ' + tense)


    def process_vrb_subsentence(self, verbal_group):

        if self._process_on_learning_new_concept:
            vrb_subs_builder = StatementBuilder(self._current_speaker)
            for vrb_sub in verbal_group.vrb_sub_sentence:
                vrb_subs_builder.clear_all()

                if vrb_sub.sn:
                    vrb_subs_builder.process_nominal_groups(vrb_sub.sn)
                if vrb_sub.sv:
                    vrb_subs_builder.process_verbal_groups(vrb_sub)

                self._statements = vrb_subs_builder._statements
                self._unclarified_ids = vrb_subs_builder._unclarified_ids
                self.lear_more_concept = vrb_subs_builder.lear_more_concept


"""
    The following function are not implemented for a specific class
"""


def get_class_name(noun, conceptL):
    """Simple function to obtain the exact class name"""
    if conceptL:
        for c in conceptL:
            if 'CLASS' in c: return c[0]

    # Not found in the ontology? Using the capitalized version as class name
    return noun.capitalize()
     

    


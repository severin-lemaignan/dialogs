import logging
logger = logging.getLogger("dialogs")

from dialogs.helpers.helpers import colored_print
from dialogs.helpers.printers import level_marker

from dialogs.interpretation.resolution import Resolver
from dialogs.interpretation.statements_builder import *
from dialogs.sentence import *
from dialogs.sentence_factory import SentenceFactory

from dialogs.resources_manager import ResourcePool
from dialogs.dialog_exceptions import DialogError, GrammaticalError

class QuestionHandler:

    def __init__(self, current_speaker = None):
        self._sentence = None
        self._statements = []
        self._current_speaker = current_speaker

        # This field takes the value True or False when processing a
        # Yes-No-question and takes a list of returned values from
        # the ontology when processing a w_question
        self._answer = False

        # This field is set to 'None' when the answer of the question 
        # (wh-question) that is being processed aims to give information 
        # about the subject.
        #It also holds the flags 'QUERY_ON_DIRECT_OBJ' and 'QUERY_ON_INDIRECT_OBJ'.
        self._query_on_field = None

        self._process_on_location = False

        # This field is set to True, when the verb 'to know' occurs in a 
        # sentence.
        self.process_on_knowing_concept = False

        # This defines the default model used to resolve queries.
        self._default_agent = "myself"

    def clear_statements(self):
        self._statements = []


    def set_current_speaker(self, current_speaker):
        """ Updates the speaker ID.
        """
        self._current_speaker = current_speaker

    def get_query_on_field(self):
        return self._query_on_field

    def process_sentence(self, sentence):
        """This processes a w_question or yes_no_question sentence"""
        self._sentence = sentence
        #StatementBuilder
        builder = StatementBuilder(self._current_speaker)
        self._statements, situation_id = builder.process_sentence(self._sentence)
        logger.info(level_marker(level=2, color="yellow") + "Generated statements based on the sentence components: " + colored_print(str(self._statements), None, "magenta"))

        #Case the question is a y_n_question : check the fact in the ontology
        if sentence.data_type == YES_NO_QUESTION:
            self._statements = self._set_situation_id(self._statements)
            logger.info(level_marker(level=2, color="yellow") + "Generated statements for this question: " + colored_print(str(self._statements), None, "magenta"))
            #Processing :Do you know something?
            if self.process_on_knowing_concept:
                #self._statements = [agent knows object]
                for s in self._statements:
                    self._answer= True
                    
                    if "knows" in s:
                        [agent, object] = s.split( " knows ")
                    
                        onto_lookup = []
                        try:
                            logger.debug(level_marker(level=2, color="yellow") + "Looking up for " + object + " in " + agent +"'s model")
                            onto_lookup = ResourcePool().ontology_server.lookupForAgent(agent, object)
                        except AttributeError:
                            pass
                            
                        self._answer = self._answer and (True if onto_lookup else False)
                        
                self.process_on_knowing_concept = False
            else:
                try:
                    logger.debug(level_marker(level=2, color="yellow") + "Checking in the ontology: " + colored_print(str(self._statements), None, "magenta"))
                    self._answer = ResourcePool().ontology_server.check(self._statements)
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
                
        #Case the question is a w_question : find the concept the concept that answers the question
        if sentence.data_type == W_QUESTION:
            #
            self._query_on_field = self._set_query_on_field(sentence)
            statements_with_bound_tokens =  self._remove_statements_with_no_unbound_tokens(self._statements)
            
            #Agent from which the ontology model is queried
            agent = self._default_agent
            
            self._answer = []

            #For all the possible subjects of a same question
            if not self._sentence.sn:
                statements_to_query = [self._extend_statement_from_sentence_aim(statements_with_bound_tokens)]
            
            else:
                statements_to_query = [self._extend_statement_from_sentence_aim(statements_with_bound_tokens, sn) for sn in self._sentence.sn]
            
            for statements in statements_to_query:
                if self.process_on_knowing_concept:
                    #Get agent in a statement such as [agent knows object]
                    for s in statements:
                        if "knows" in s:
                            [agent, object] = s.split(" knows ")
                            break

                    #No need of statements such as [S knows O]
                    [statements.remove(s) for s in statements if "knows" in s]
                    self.process_on_knowing_concept = False

                if statements:
                    logger.info(level_marker(level=2, color="yellow") + "Generated statements for this question: " + colored_print(str(self._statements), None, "magenta"))

                    answers = []
                    if self._process_on_location:

                        prepositions_list = ResourcePool().preposition_rdf_object_property.copy()
                        roles = dict([(preposition,prepositions_list[preposition][0])\
                                for preposition in prepositions_list.keys()\
                                 if 'objectFoundInLocation' in prepositions_list[preposition]])

                        #Case of ojectFound in location
                        stmts = []
                        prepositions_already_used = []
                        for role in roles:
                            if roles[role] in prepositions_already_used:
                                continue

                            stmts = [s.replace('objectFoundInLocation', roles[role]) for s in statements]
                            try:
                                logger.debug(level_marker(level=2, color="yellow") + "Searching in "+ agent +" model: " + colored_print(str(stmts), None, "magenta"))
                                answers = ResourcePool().ontology_server.findForAgent(agent,'?concept', stmts)
                            except AttributeError: #the ontology server is not started of doesn't know the method
                                pass

                            prepositions_already_used.append(roles[role])

                            if answers:
                                ResourcePool().mark_active(answers)
                                self._answer.append([[role], answers])

                        #Case of object found in location + direction
                        stmts = [s.replace('objectFoundInLocation', 'isAt') for s in statements]
                        for role in ResourcePool().direction_words:                        
                            try:
                                logger.debug(level_marker(level=2, color="yellow") + "Searching in "+ agent +" model: " + colored_print(str(stmts + ['?concept is'+ role.capitalize() + 'Of ?obj', '?concept rdf:type Location']), None, "magenta"))
                                answers = ResourcePool().ontology_server.findForAgent(agent,'?obj', stmts + ['?concept is'+ role.capitalize() + 'Of ?obj', '?concept rdf:type Location'])
                            except AttributeError: #the ontology server is not started of doesn't know the method
                                pass

                            if answers:
                                ResourcePool().mark_active(answers)
                                self._answer.append([[role], answers])

                    else:
                        try:
                            logger.debug(level_marker(level=2, color="yellow") + "Searching in "+ agent +" model: " + colored_print(str(statements), None, "magenta"))
                            answers = ResourcePool().ontology_server.findForAgent(agent, '?concept', statements)
                        except AttributeError: #the ontology server is not started of doesn't know the method
                            pass

                        if answers:
                            ResourcePool().mark_active(answers)
                            self._answer.append([[], answers])
                else:
                    pass

                self._statements.extend(statements)

        stmts, sit_id = self._build_situation_statements()
        return self._answer, stmts, sit_id
    
    def _build_situation_statements(self):
        sit_id = generate_id(with_question_mark = False)

        stmts = ["%s experiences %s" % (self._current_speaker, sit_id)]
        stmts += ["%s rdf:type InterrogativeState" % sit_id]
        for sn in self._sentence.sn:
            stmts += ["%s hasObject %s" % (sit_id, sn.id)]
        stmts += ["%s hasAim %s_question_aim" % (sit_id, self._sentence.aim)]
        stmts += ["%s hasAnswer %s" % (sit_id, "true" if self._answer else "false")]

        return stmts, sit_id
    
    def _set_situation_id(self, statements):
        """This attempts to clarify the ID of an action verbs
            E.g: statement = [?event rdf:type Go, ?event performedBy myself, ?event actsOnObject xxx]
                We attemtps to find an existing ontology ID matching '?event'
        """
        stmts = []
        
        find_id = False
        for s in statements:
            if '?' in s:
                find_id = True
                break
        
        if find_id:
            try:
                sit_id = ResourcePool().ontology_server.find(['?event'], statements)
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
                
            if sit_id:
                logger.debug("\t/Found a staticSituation matching the yes_no_question query to be checked: "+ str(sit_id))
                for s in statements:
                    #TODO:the ontology might find severals sit ID matching the query. Should we take this consideration?
                    #The longer the query, the better the result of sit_id
                    stmts.append(s.replace('?event', sit_id[0]))
        else:
            stmts = statements
        
        # Find process on knowing concept
        for s in statements:
            if "knows" in s:
                self.process_on_knowing_concept = True
                break
            
        return stmts
    
    
    def _extend_statement_from_sentence_aim(self, current_statements, sn = None):
        """This extends the statements states so that the query answer matches the w_question aim
        
        """
        #Concept descriptor
        # E.g: Human, Object, Color ,Size...
        concept_descriptor = self.get_concept_descriptor(sn)
        
        #Case: the statement is complete from statement builder e.g: what is in the box? =>[?concept isIn ?id_box, ?id_box rdf:type Box]
        for s in current_statements:
            if '?concept' in s.split():
                return current_statements + concept_descriptor
        #case: the statement is partially build from statement builder
        
        stmts = []
        if sn:
            for sv in self._sentence.sv:
                for verb in sv.vrb_main:
                    role  = self.get_role_from_sentence_aim(self._query_on_field, verb)
                    
                    #Case of looking for the object in a location
                    if role == 'objectFoundInLocation':
                        self._process_on_location = True
                    
                    # Case of state verbs
                    if verb.lower() in ResourcePool().state:
                        stmts.append(sn.id + ' '+ role + ' ?concept')
                    # Case of action verb with a passive behaviour
                    elif verb.lower() in ResourcePool().action_verb_with_passive_behaviour.keys():
                        stmts.append(sn.id + ' '+ ResourcePool().action_verb_with_passive_behaviour[verb.lower()] + ' ?concept')
                    
                    # Case of know
                    elif verb.lower() == 'know':
                        self.process_on_knowing_concept = True
                        stmts.append(sn.id + ' knows ?concept')
                    
                    # case of action verbs
                    else:
                        stmts.append('?event ' + role + ' ?concept')
                    
        return current_statements + stmts + concept_descriptor
    
    
    
    def _set_query_on_field(self, sentence):
        """ This defines which part of a sentence is supposed to be completed once the answer of a w_question has been retrieved
            E:g - [W_question] : where is the cube
                - Answer: table
                - query_on_field = 'QUERY_ON_INDIRECT_OBJ'
                - Sentence built from answer, query_on_field, and w_question:
                    the cube is on the table
        """
        if sentence.aim == 'place':
            return 'QUERY_ON_INDIRECT_OBJ'
        
        if not sentence.sn:
            return None
                   
        if sentence.sv:
            if not sentence.sv[0].d_obj:
                query_on_field = 'QUERY_ON_DIRECT_OBJ'
            
            else:
                query_on_field = 'QUERY_ON_INDIRECT_OBJ'
        
        return query_on_field
        
            
    
    def get_role_from_sentence_aim(self, query_on_field, verb):
        """ Given specific w_question aim and verb, this function attempts to define the matching object property to built
            an RDF tuple <S P O>. Cf. QuestionAimDict() for more detail.
        """
        dic_aim = QuestionAimDict().dic_aim
        try:
            if verb.lower() in dic_aim[self._sentence.aim][query_on_field]:
                role = dic_aim[self._sentence.aim][query_on_field][verb.lower()]
            else:
                role = dic_aim[self._sentence.aim][query_on_field][None]
        except KeyError:
            if verb.lower() in dic_aim[self._sentence.aim][None]:
                role = dic_aim[self._sentence.aim][None][verb.lower()]
            else:
                role = dic_aim[self._sentence.aim][None][None]
    
        return role
    
    
    def get_concept_descriptor(self, ng):
        """ Get the type or feature of the concept to query if it is not mapped in the QuestionAimDict
            E.g: What color is the bottle?
                Here, the aim 'color' is about a feature and it is not in the QuestionAimDict.
                We return it in concept_descriptor = 'id hasColor ?concept'
                
            E.g: What Human do you see?
                Here, the aim 'human' is not a feature, and is not in the QuestionAimDict
                We return it in concept_descriptor = '?concept rdf:type Human'
                
        """
        
        concept_descriptor = []
        agent = self._default_agent
        aim = self._sentence.aim
        
        #Concept's Features
        if self._sentence.aim in ResourcePool().adjectives_ontology_classes:
            if ng:
                concept_descriptor = [ng.id + " has" + aim.capitalize() + " ?concept"]
                self._sentence.aim = "thing"
        
        #Concept's Type
        elif not self._sentence.aim in QuestionAimDict().dic_aim.keys():
            logger.debug("\tFound the aim: " + aim + ".Extending statements with [?concept rdf:type aim]")
            try:
                onto = ResourcePool().ontology_server.lookupForAgent(agent, aim)
            except AttributeError:
                onto = None
                
            concept_descriptor = ["?concept rdf:type " + get_class_name(aim, onto)]
            self._sentence.aim = "thing"
            
        elif self._sentence.aim == "people":
            concept_descriptor = ["?concept rdf:type Agent"]
        
        return concept_descriptor
            
        
    """            
        what aim => 'thing'
            what kind => aim = 'thing', sn = [the kind of]
            what type => aim = 'thing' , sn = [the type of]
            what time => aim = 'time'
        which aim => 'choice'
        when  aim => 'date'
        where aim => 'Place'
            where (from) => 'origin'
        why   aim => 'reason'
        who   aim => 'person'
        whose aim => 'owner'
        whom  aim => 'person'
        how   aim => 'place'
            how long  => aim = 'duration'
            how far   => aim = 'distance'
             how often => aim = 'Frequency'
             How much  => aim = 'Quantity'
            How many  => aim = 'Quantity'
    """    

    
    def _remove_statements_with_no_unbound_tokens(self, statements):
        """ This remove statement part with no unbound token, for querying the ontology."""
        stmts = []
        for s in statements:
            if '?' in s:
                stmts.append(s)
                
        return stmts
    

class QuestionAimDict:
    def __init__(self):
        """
        This class consits in building a map of object property regarding the 
        Question's aim attribute and the query_on_field parameter.
        Below is a description of what should be generated depending of the question that is processed.
               
        'What and which-question': 
            Case # query_on_field = 'QUERY_ON_DIRECT_OBJ'
                extend statements with [?event OBJ ?concept]
                where OBJ depends on the verb. 
                e.g: if verb == "get":
                        OBJ = "actsOnObject"
                     if verb == "drive":
                        OBJ = "involves"
                    ...                 
                                
            Case # query_on_field = None
                Nothing to extend
            Case # query_on_field = 'QUERY_ON_INDIRECT_OBJ'
                Nothing to extend

        'Who-question':
            Case # query_on_field = None
                extend statements with [* performedBy ?concept] 
            
            Case # query_on_field = 'QUERY_ON_DIRECT_OBJ' and state verbs
                extend statements with [* rdfs:label ?concept]
                E.g: Who is the car's driver?
                
            Case # query_on_field = 'QUERY_ON_DIRECT_OBJ' and action verbs
                same as "what" and "which" question for 'QUERY_ON_DIRECT_OBJ'
            
            Case # query_on_field = 'QUERY_ON_INDIRECT_OBJ'
                extend statements with [* receivedBy ?concept]       
        'Where-question':
            Case # query_on_field = 'QUERY_ON_INDIRECT_OBJ'
                extend statements with [* objectFoundInLocation ?concept]  
        """
        
        self.dic_aim = {}
        
        
        #Dictionaries related to thematice roles verbs
        verbs_dic = ResourcePool().thematic_roles.verbs
        self.dic_on_direct_obj = dict([(verb , role.id) for verb in verbs_dic.keys() for role in verbs_dic[verb].roles[0:1]])
        self.dic_on_direct_obj[None] = 'involves'
        self.dic_on_direct_obj['be'] = 'owl:sameAs'
        
        self.dic_on_indirect_obj = dict([(verb , role.id) for verb in verbs_dic.keys() for role in verbs_dic[verb].roles[1:2]])
        self.dic_on_indirect_obj['be'] = None
        self.dic_on_indirect_obj[None] = 'owl:sameAs'
    
        #Dictionary for sentence.aim = 'place' 
        self.dic_place={None:self.dic_on_indirect_obj.copy()}
        self.dic_place[None]['be'] = 'objectFoundInLocation'
                        
        #Dictionary for sentence.aim = 'thing' 
        self.dic_thing={None:self.dic_on_direct_obj.copy()}
                
        #Dictionary for sentence.aim = 'manner' 
        self.dic_manner={None:{'be':'owl:topObjectProperty'}}
        
        #Dictionary for sentence.aim = 'people'
        self.dic_people={'QUERY_ON_DIRECT_OBJ':self.dic_on_direct_obj.copy(),                                                                                              
                    'QUERY_ON_INDIRECT_OBJ':self.dic_on_indirect_obj.copy()}
        
        #Dictionary for all question aims        
        #What-question
        self.dic_aim['thing'] = self.dic_thing
        #Who-question
        self.dic_aim['people'] = self.dic_people
        #Where-question
        self.dic_aim['place'] = self.dic_place
        #How-Question
        self.dic_aim['manner'] = self.dic_manner
        #which-question
        self.dic_aim['choice'] = self.dic_thing

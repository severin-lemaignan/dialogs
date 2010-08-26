import logging
logger = logging.getLogger("dialog")

from dialog.interpretation.resolution import Resolver
from dialog.interpretation.statements_builder import *
from dialog.sentence import *

from pyoro import OroServerError
from dialog.resources_manager import ResourcePool
from dialog.dialog_exceptions import DialogError, GrammaticalError

class QuestionHandler:
    
    def __init__(self, current_speaker = None):
        self._sentence = None
        self._statements = []
        self._current_speaker = current_speaker
        
        #This field takes the value True or False when processing a Yes-No-question 
        #        and takes a list of returned values from the ontology when processing a w_question 
        self._answer = False
        
        #This field is set to 'None' when the answer of the question (wh-question) that is being processed aims to give information about the subject.
        #It also holds the flags 'QUERY_ON_DIRECT_OBJ' and 'QUERY_ON_INDIRECT_OBJ'.
        self._query_on_field = None
        
    def clear_statements(self):
        self._statements = []
    
    
    def set_current_speaker(self, current_speaker):
        self._current_speaker = current_speaker
    
    def get_query_on_field(self):
        return self._query_on_field
        
    def process_sentence(self, sentence):
        self._sentence = sentence
        #StatementBuilder
        builder = StatementBuilder(self._current_speaker)
        self._statements = builder.process_sentence(self._sentence)
        logger.info("statement from Statement Builder: " + str(self._statements))
        
        #Case the question is a y_n_question : check the fact in the ontology
        if sentence.data_type == 'yes_no_question':
            self._statements = self._set_situation_id(self._statements)
            
            try:
                logger.debug("Checking on the ontology: check(" + str(self._statements) + ")")
                self._answer = ResourcePool().ontology_server.check(self._statements)
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            
        #Case the question is a w_question : find the concept the concept that answers the question
        if sentence.data_type == 'w_question':
            
            #
            self._query_on_field = self._set_query_on_field(sentence)
            self._statements =  self._remove_statements_with_no_unbound_tokens(self._statements)
            self._statements = self._extend_statement_from_sentence_aim(self._statements)
            
            if self._statements:
                print(self._statements)
                try:
                    logger.debug("Searching the ontology: find(?concept, " + str(self._statements) + ")")
                    self._answer = ResourcePool().ontology_server.find('?concept', self._statements)
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
            else:
                pass

        
        return self._answer
        
    def _set_situation_id(self, statements):
        stmts = []
        try:

            sit_id = []
            
            try:
                sit_id = ResourcePool().ontology_server.find('?event', statements)
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
                
            if sit_id:
                logger.debug("\t/Found a staticSituation matching the yes_no_question query to be checked: "+ str(sit_id))
                for s in statements:
                    #TODO:the ontology might find severals sit ID matching the query. Should we take this consideration?
                    #The longer the query, the better the result of sit_id
                    stmts.append(s.replace('?event', sit_id[0]))
        except OroServerError:
            stmts = statements
            
        return stmts
    
    
    def _extend_statement_from_sentence_aim(self, current_statements):
        #Case: the statement is complete from statement builder e.g: what is in the box? =>[?concept isIn ?id_box, ?id_box rdf:type Box]
        for s in current_statements:
            if '?concept' in s.split():
                return current_statements
        #case: the statement is partially build from statement builder
        
        stmts = []
                    
        for sn in self._sentence.sn:
            for sv in self._sentence.sv:
                for verb in sv.vrb_main:
                    role = self.get_role_from_sentence_aim(self._query_on_field, verb)
                    if verb.lower() == 'be':
                        stmts.append(sn.id + ' '+ role + ' ?concept')
                    else:
                        stmts.append('?event ' + role + ' ?concept')
        
        
        return current_statements + stmts
    
    
    
    def _set_query_on_field(self, sentence):
        
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
        stmts = []
        for s in statements:
            if '?' in s:
                stmts.append(s)
                
        return stmts
    

class QuestionAimDict:
    def __init__(self):
        """
        Info:
            (A): A is optional
            <A|B>: either A or B
            {A}: A may be replaced
        
        'What-question': 
            Case  # query on a direct object
                e.g: what do you see? 
                append in statement [?event involves ?concept]
                                
                e.g: what(<object|thing>) is <this|the small cube>?
                append in statement [* owl:sameAs ?concept]
                
                e.g: what <feature|color|size> is <the small cube|this>? #Feature or subClassOf Feature
                append in statement [* hasFeature ?concept]
                
            Case # query on the subject
                e.g: what is 'in' <the blue cube|this>?
                append in statement [] # query completed from statementBuilder
                 
                e.g: what(<object|thing>) is blue?
                append in statement [* hasFeature ?concept]
                
            Case # query on the a direct object but answer replacing subject
                e.g: what(object) is a cube?             
                append in statement [* {rdf:type} ?concept]
                
            
        'Who-question':
            
            Case # query on the subject
                e.g: who sees the man?
                append in statement [* performedBy ?concept] 
            
            Case # query on a direct object with state verb
                e.g: who is the man?
                append in statement [* rdfs:label ?concept] 
                
            Case # query on a direct object with action verb
                e.g: who does the man see?
                append in statement [* actsOnObject ?concept]
            
            Case # query on an indirect object
                e.g: who does the man give a cube
                append in statement [* receivedBy ?concept]         
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
        self.dic_place[None]['be'] = 'isAt'
                        
        #Dictionary for sentence.aim = 'thing' 
        self.dic_thing={None:self.dic_on_direct_obj.copy()}
                
        #Dictionary for sentence.aim = 'manner' 
        self.dic_manner={}
        
        #Dictionary for sentence.aim = 'people'
        self.dic_people={'QUERY_ON_DIRECT_OBJ':self.dic_on_direct_obj.copy(),                                                                                              
                    'QUERY_ON_INDIRECT_OBJ':self.dic_on_indirect_obj.copy()}
        
        #Dictionary for all question aims
        #
        adjectives_list = [ResourcePool().adjectives[adj] for adj in ResourcePool().adjectives]

        adj_s = []
        for adj in adjectives_list:
            if not adj in adj_s:
                adj_s.append(adj)

        adjectives_list = adj_s
        
        #What-question in Features
        self.dic_aim = dict([(feature.lower(), {None:{"be":"has"+feature.capitalize()}}) for feature in adjectives_list])
        #What-question
        self.dic_aim['thing'] = self.dic_thing
        #Who-question
        self.dic_aim['people'] = self.dic_people
        #Where-question
        self.dic_aim['place'] = self.dic_place
        #How-Question
        self.dic_aim['manner'] = self.dic_manner




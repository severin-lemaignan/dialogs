# coding=utf-8
""" This module encodes several emotional state of the robot like confusion,
joy, etc. as statements. These can be added to the knowledge base to express
the state of the robot during the dialogs."""

import logging
logger = logging.getLogger("dialogs." + __name__)

from dialogs.resources_manager import ResourcePool
from dialogs.helpers.helpers import generate_id, colored_print

def _send_state(state):

    models = [ResourcePool().default_model]
    policy = {"method":"add", "models":models}

    state_id = generate_id(False)
    statements = [state_id + " rdf:type " + state, 
                  "myself experiences " + state_id]
    try:
        logger.info(colored_print("Setting my mood to " + state, "magenta"))
        #logger.warning(colored_print("Not setting my mood due to Pellet bugs!", "magenta"))
        ResourcePool().ontology_server.revise(statements, policy)

    except AttributeError: #the ontology server is not started of doesn't know the method
        pass

def confused():
    _send_state("ConfusedState")

def satisfied():
    _send_state("SatisfiedState")

def sorry():
    _send_state("SorryState")

def happy():
    _send_state("HappyState")

def angry():
    _send_state("AngryState")

def sad():
    _send_state("SadState")



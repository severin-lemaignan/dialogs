#!/usr/bin/python
# -*- coding: utf-8 -*-

class SpeakerIdentifier(object):
    """This class is responsible for determining the speaker of the last 
    utterance.
    
    In the current version, it statically returns "HUMAN".
    """

    def get_current_speaker_id(self):
        return "HUMAN"

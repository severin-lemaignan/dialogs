#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import unittest
from resolution import Resolver
from statements_builder import StatementBuilder
from statements_builder import NominalGroupStatementBuilder
from statements_builder import VerbalGroupStatementBuilder
from sentence import *
from resources_manager import ResourcePool
from pyoro import OroServerError
from dialog_exceptions import DialogError
from dialog_exceptions import GrammaticalError

class AnaphoraMatcher:
    __init__(self):
        pass

#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import unittest

from dialog import Dialog

class TestDialog(unittest.TestCase):
	"""Tests the differents features of the Dialog module.
	This must be tested with oro-server using the testsuite.oro.owl ontology.
	"""
	
	def setUp(self):
		self.dialog = Dialog()

	def test_statement(self):

		stmt = "The cow eats an apple"
		expected_result = ['cow eats apple']
		
		res = self.dialog.handle_incoming_input(stmt)
		
		self.assertEqual(res, expected_result)

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG,
					format="%(message)s")
	unittest.main()

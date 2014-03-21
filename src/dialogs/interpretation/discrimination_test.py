#!/usr/bin/python
# -*- coding: utf-8 -*-


import unittest
import logging

logger = logging.getLogger('dialogs')

from dialogs.resources_manager import ResourcePool
from dialogs.dialog_core import Dialog
from discrimination import Discrimination
from dialogs.verbalization.verbalization import Verbalizer
from dialogs.dialog_exceptions import *

from dialogs.helpers.helpers import check_results, get_console_handler, get_file_handler


class TestDiscrimination(unittest.TestCase):
    """This function tests the main features of the class Discrimination"""

    def setUp(self):
        self.disc = Discrimination()
        self.verbalizer = Verbalizer()

        try:
            #ResourcePool().ontology_server.reset()

            ResourcePool().ontology_server.add(["raquel rdf:type Human",
                                                "Gamebox rdfs:subClassOf Box",
                                                "Gamebox rdfs:label \"game box\"",
                                                "BLUE_BOTTLE rdf:type Bottle",
                                                "BLUE_BOTTLE hasColor blue",
                                                "ORANGE_BOTTLE rdf:type Bottle",
                                                "ORANGE_BOTTLE hasColor orange",
                                                "ORANGE_BOTTLE isOn ACCESSKIT",
                                                "YELLOW_BOTTLE rdf:type Bottle",
                                                "YELLOW_BOTTLE hasColor yellow",
                                                'ACCESSKIT rdf:type Gamebox',
                                                'ACCESSKIT hasColor white',
                                                'ACCESSKIT hasSize big',
                                                'ACCESSKIT isOn table1',
                                                'ORANGEBOX rdf:type Gamebox',
                                                'ORANGEBOX hasColor orange',
                                                'ORANGEBOX hasSize big',
                                                'ORANGEBOX isOn ACCESSKIT',
                                                'SPACENAVBOX rdf:type Gamebox',
                                                'SPACENAVBOX hasColor white',
                                                'SPACENAVBOX hasSize big',
                                                'SPACENAVBOX isOn ACCESSKIT'
            ])

            ResourcePool().ontology_server.addForAgent("raquel",
                                                       ["BLUE_BOTTLE isVisible true",
                                                        "ORANGE_BOTTLE isVisible true"
                                                       ])

        except AttributeError: #the ontology server is not started of doesn't know the method
            raise (DialogError("The ontology server is not started!"))

    def test_01(self):
        logger.info("Test1: No ambiguity.")
        description = [['myself', '?obj', ['?obj rdf:type Bottle', '?obj hasColor blue']]]
        expected_result = "BLUE_BOTTLE"

        try:
            res = self.disc.clarify(description)
        except UnsufficientInputError:
            self.fail("Should need any more info")

        self.assertEquals(expected_result, res)

    def test_02(self):
        logger.info("\nTest2: Complete self.discriminant in robot model found.")
        description = [['myself', '?obj', ['?obj rdf:type Bottle']]]
        expected_result = "Which color is the bottle? Blue or orange or yellow."

        try:
            res = self.disc.clarify(description)
        except UnsufficientInputError as use:
            self.assertEquals(use.value['status'], 'SUCCESS')
            self.assertEquals(self.verbalizer.verbalize(use.value['question']), expected_result)
            return

        self.fail("Should trigger an unsufficient input exception!")

    def test_03(self):
        logger.info("\nTest3: No complete self.discriminant in robot model found.")
        description = [['myself', '?obj', ['?obj rdf:type Box']]]
        expected_result = ["Which color is the box? Orange or white.",
                           "Where is the Box? On the ACCESSKIT or on the table1?"]

        try:
            res = self.disc.clarify(description)
        except UnsufficientInputError as use:
            self.assertEquals(use.value['status'], 'SUCCESS')
            self.assertIn(self.verbalizer.verbalize(use.value['question']), expected_result)
            return

        self.fail("Should trigger an unsufficient input exception!")

    def test_04(self):
        logger.info("\nTest4: Including visibility constraints")
        description = [['myself', '?obj', ['?obj rdf:type Bottle']], ['raquel', '?obj', ['?obj isVisible true']]]
        expected_result = "Which color is the bottle? Blue or orange."

        try:
            res = self.disc.clarify(description)
        except UnsufficientInputError as use:
            self.assertEquals(use.value['status'], 'SUCCESS')
            self.assertEquals(self.verbalizer.verbalize(use.value['question']), expected_result)
            return

        self.fail("Should trigger an unsufficient input exception!")

    def test_05(self):
        logger.info("\nTest5: Testing location")
        description = [['myself', '?obj', ['?obj rdf:type Artifact', '?obj hasColor orange']]]
        expected_result = "Which type is the object? Game box or bottle."

        try:
            res = self.disc.clarify(description)
        except UnsufficientInputError as use:
            self.assertEquals(use.value['status'], 'SUCCESS')
            self.assertEquals(self.verbalizer.verbalize(use.value['question']), expected_result)
            return

        self.fail("Should trigger an unsufficient input exception!")


class TestDescriptionGeneration(TestDiscrimination):
    """This function tests the generation of unambiguous description of objects.
    """

    def test_descr_generation_01(self):
        logger.info("\nDescription Generation - Test1: Generate unambiguous description")
        objectID = 'BLUE_BOTTLE'
        expected_result = (True, ['?obj rdf:type Bottle', '?obj * blue'])
        res = self.disc.find_unambiguous_desc(objectID)

        logger.info("Result of desc generation: " + str(res))

        self.assertEquals(res[0], expected_result[0])
        self.assertTrue(check_results(res[1], expected_result[1], allow_question_mark=True))


    def test_descr_generation_02(self):
        logger.info("\nDescription Generation - Test2: Generate unambiguous description")
        objectID = 'ACCESSKIT'
        expected_result = (True, ['?obj rdf:type Gamebox', '?obj isOn table1'])
        res = self.disc.find_unambiguous_desc(objectID)

        logger.info("Result of desc generation: " + str(res))

        self.assertEquals(res[0], expected_result[0])
        self.assertTrue(check_results(res[1], expected_result[1], allow_question_mark=True))


    def test_descr_generation_03(self):
        logger.info("\nDescription Generation - Test3: Generate unambiguous description")
        objectID = 'SPACENAVBOX'
        expected_result = (True, ['?obj rdf:type Gamebox', '?obj * white', '?obj isOn ACCESSKIT'])
        res = self.disc.find_unambiguous_desc(objectID)

        logger.info("Result of desc generation: " + str(res))

        self.assertEquals(res[0], expected_result[0])
        self.assertTrue(check_results(res[1], expected_result[1], allow_question_mark=True))


class TestDiscriminateCompleteDialog(unittest.TestCase):
    """Tests the differents features of the Dialog module.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """

    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()

        self.oro = ResourcePool().ontology_server

        try:
            self.oro.reload()
            self.oro.add(['shelf1 rdf:type Shelf',
                          'table1 rdf:type Table',
                          'table2 rdf:type Table', 'table2 hasColor blue',
                          'Banana rdfs:subClassOf Plant',
                          'y_banana rdf:type Banana', 'y_banana hasColor yellow', 'y_banana isOn shelf1',
                          'green_banana rdf:type Banana', 'green_banana hasColor green', 'green_banana isOn table2',
                          'ACCESSKIT rdf:type Gamebox', 'ACCESSKIT hasColor white', 'ACCESSKIT hasSize big',
                          'ACCESSKIT isOn table1',
                          'ORANGEBOX rdf:type Gamebox', 'ORANGEBOX hasColor orange', 'ORANGEBOX hasSize big',
                          'ORANGEBOX isOn ACCESSKIT',
                          'MYBOX rdf:type Gamebox', 'MYBOX hasColor orange', 'MYBOX hasSize small',
                          'MYBOX isOn ACCESSKIT',
                          'SPACENAVBOX rdf:type Gamebox', 'SPACENAVBOX hasColor white', 'SPACENAVBOX hasSize big',
                          'SPACENAVBOX isOn ACCESSKIT',
                          'y_bottle rdf:type Bottle', 'y_bottle isLocated RIGHT',
                          'r_bottle rdf:type Bottle', 'r_bottle isLocated FRONT',
                          'b_bottle rdf:type Bottle', 'b_bottle isLocated BACK'
            ])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass

    def test_discriminate1(self):
        """ Color discriminant should be found"""

        logger.info("\n##################### test_discriminate1 ########################\n")
        ####
        stmt = "the banana is good"
        answer = "the green one"
        ####
        res = self.dialog.test('myself', stmt, answer)
        logger.info(res)
        expected_result = ['green_banana hasFeature good']
        self.assertTrue(check_results(res[0], expected_result))

        """ Color discriminant should be found"""

        logger.info("\n##################### test_discriminate2 ########################\n")
        ####
        stmt = "the banana is good"
        answer = "the yellow one"
        ####
        res = self.dialog.test('myself', stmt, answer)
        logger.info(res)
        expected_result = ['y_banana hasFeature good']
        self.assertTrue(check_results(res[0], expected_result))

    def test_discriminate3(self):
        """ Color discriminant should be found"""

        logger.info("\n##################### test_discriminate3 ########################\n")
        ####
        stmt = "give me the banana"
        answer = "the green one"
        ####
        expected_result = ['myself desires *',
                           '* rdf:type Give',
                           '* performedBy myself',
                           '* actsOnObject green_banana',
                           '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt, answer)
        logger.info(res)
        self.assertTrue(check_results(res[0], expected_result))


    def test_discriminate4(self):
        """No ambiguity."""

        logger.info("\n##################### test_discriminate4 ########################\n")
        ####
        stmt = "get the gamebox which is on the table"
        answer = None
        ####
        expected_result = ['myself desires *',
                           '* rdf:type Get',
                           '* performedBy myself',
                           '* actsOnObject ACCESSKIT']
        ###
        res = self.dialog.test('myself', stmt)
        logger.info(res)
        self.assertTrue(check_results(res[0], expected_result))

    def test_discriminate5(self):
        """ Size discriminant should be found """

        logger.info("\n##################### test_discriminate5 ########################\n")
        ####
        stmt = "get the orange gamebox"
        answer = "the big one"
        ####
        expected_result = ['myself desires *',
                           '* rdf:type Get',
                           '* performedBy myself',
                           '* actsOnObject ORANGEBOX']
        ###
        res = self.dialog.test('myself', stmt, answer)
        logger.info(res)
        self.assertTrue(check_results(res[0], expected_result))

    def test_discriminate6(self):
        """No complete discriminant found. More info required"""

        logger.info("\n##################### test_discriminate6 ########################\n")
        ####
        stmt = "get the big gamebox"
        answer = "the orange one"
        ####
        expected_result = ['myself desires *',
                           '* rdf:type Get',
                           '* performedBy myself',
                           '* actsOnObject ORANGEBOX']
        ###
        res = self.dialog.test('myself', stmt, answer)
        logger.info(res)
        self.assertTrue(check_results(res[0], expected_result))


    def test_discriminate7(self):
        """ Location discriminant should be found """

        logger.info("\n##################### test_discriminate7 ########################\n")
        ####
        stmt = "get the white gamebox"
        answer = "the one which is on the table1"
        ####
        expected_result = ['myself desires *',
                           '* rdf:type Get',
                           '* performedBy myself',
                           '* actsOnObject ACCESSKIT']
        ###
        res = self.dialog.test('myself', stmt, answer)
        logger.info(res)
        self.assertTrue(check_results(res[0], expected_result))

    def test_discriminate8(self):
        """ Location wrt robot discriminant should be found """

        logger.info("\n##################### test_discriminate8 ########################\n")
        ####
        stmt = "get the bottle"
        answer = "the one which is in front of you"
        ####
        expected_result = ['myself desires *',
                           '* rdf:type Get',
                           '* performedBy myself',
                           '* actsOnObject r_bottle']
        ###
        res = self.dialog.test('myself', stmt, answer)
        logger.info(res)
        self.assertTrue(check_results(res[0], expected_result))

    def test_discriminate9(self):
        logger.info("\n##################### Class grounding ########################\n")
        ####
        stmt = "a fruit is a plant"
        answer = "a kind of thing"
        ####
        expected_result = ['Plant rdfs:subClassOf Thing', 'Fruit rdfs:subClassOf Plant']
        ###
        res = self.dialog.test('myself', stmt, answer)
        logger.info(res)
        self.assertTrue(check_results(res[0], expected_result))

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDiscrimination)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDescriptionGeneration))
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDiscriminateCompleteDialog))

    return suite


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    logger.addHandler(get_console_handler())
    #logger.addHandler(get_file_handler("statements.log"))

    # executing verbalization tests
    unittest.TextTestRunner(verbosity=2).run(test_suite())

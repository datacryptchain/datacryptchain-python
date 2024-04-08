import os
import unittest
from pyfakefs import fake_filesystem_unittest as fakeunittest
from datacryptchain import datacryptchain as dcc
import fixtures

class TestLedgerValid(fakeunittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        
    def test_ledger_is_valid(self):
        LEDGER_FILENAME = "poodles_valid.dcl"
        valid_ledger = fixtures.VALID_LEDGER
        with open(LEDGER_FILENAME, "w") as text_file:
            text_file.write(valid_ledger)
        errors = dcc.validate_ledger(LEDGER_FILENAME)
        self.assertEqual(errors, 0)


class TestLedgerInalid(fakeunittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        
    def test_ledger_is_invalid(self):
        LEDGER_FILENAME = "poodles_invalid.dcl"
        invalid_ledger = fixtures.INVALID_LEDGER
        with open(LEDGER_FILENAME, "w") as text_file:
            text_file.write(invalid_ledger)
        errors = dcc.validate_ledger(LEDGER_FILENAME)
        self.assertEqual(errors, 1)
 

        
        


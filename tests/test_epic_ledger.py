import os
import unittest
from pyfakefs import fake_filesystem_unittest as fakeunittest
from datacryptchain import datacryptchain as dcc
from fixtures import test_ledgers

class TestLedgerValid(fakeunittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        
    def test_ledger_is_valid(self):
        LEDGER_FILENAME = "poodles_valid.dcl"
        valid_ledger = test_ledgers.VALID_LEDGER
        with open(LEDGER_FILENAME, "w") as text_file:
            text_file.write(valid_ledger)
        errors = dcc.validate_ledger(LEDGER_FILENAME)
        self.assertEqual(errors, 0)


class TestLedgerInvalid(fakeunittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        
    def test_ledger_is_invalid(self):
        LEDGER_FILENAME = "poodles_invalid.dcl"
        invalid_ledger = test_ledgers.INVALID_LEDGER
        with open(LEDGER_FILENAME, "w") as text_file:
            text_file.write(invalid_ledger)
        errors = dcc.validate_ledger(LEDGER_FILENAME)
        self.assertEqual(errors, 1)


class TestLedgerExtractable(fakeunittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        
    def test_ledger_is_extractable(self):
        LEDGER_FILENAME = "poodles_csv_test.dcl"
        CSV_FILENAME = "poodles_csv_test.csv"
        valid_ledger = test_ledgers.VALID_LEDGER
        with open(LEDGER_FILENAME, "w") as text_file:
            text_file.write(valid_ledger)
        errors = dcc.extract_csv(LEDGER_FILENAME, CSV_FILENAME)
        self.assertEqual(errors, 0)
        self.assertTrue(os.path.exists(CSV_FILENAME))
        
        


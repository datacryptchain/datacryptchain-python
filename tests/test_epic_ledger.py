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
        SKF = None
        valid_ledger = test_ledgers.VALID_LEDGER
        with open(LEDGER_FILENAME, "w") as text_file:
            text_file.write(valid_ledger)
        errors = dcc.extract_csv(SKF, LEDGER_FILENAME, CSV_FILENAME)
        self.assertEqual(errors, 0)
        self.assertTrue(os.path.exists(CSV_FILENAME))
        
        
class TestEncryptedCSVExtractable(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_encrypted_csv_is_extractable(self):
        DOWNLOAD_CSV = "triage_as_downloaded.csv"
        LEDGER_FILENAME = "triages.dcl"
        SKF = "secret_triages.dcs"
        CSV_FILENAME = "triages.csv"
    
        # The original downloaded csv should not have identifiers
        with open(DOWNLOAD_CSV, "r") as download_file:
            download_csv = download_file.read()

        self.assertTrue("9i-oz4E5IHU" in download_csv)
        self.assertFalse("7541760303" in download_csv)
        self.assertFalse("Jensen" in download_csv)        
        
        # Ensure the ledger does not contain any identifiers
        with open(LEDGER_FILENAME, "r") as ledger_file:
            ledger = ledger_file.read()

        self.assertTrue("9i-oz4E5IHU" in ledger)
        self.assertFalse("7541760303" in ledger)
        self.assertFalse("Jensen" in ledger)

        # Extract the CSV from the ledger
        errors = dcc.extract_csv(SKF, LEDGER_FILENAME, CSV_FILENAME)
        self.assertFalse(errors)

        # Now check the csv to ensure that the decrypted identifiers now show
        with open(CSV_FILENAME, "r") as csv_file:
            csv = csv_file.read()

        self.assertTrue("9i-oz4E5IHU" in csv)
        self.assertTrue("7541760303" in csv)
        self.assertTrue("Jensen" in csv)

        # Clean up
        os.remove("triages.csv")

                  
        

    

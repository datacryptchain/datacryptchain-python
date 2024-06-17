import os
import unittest
import Cryptodome
from pyfakefs import fake_filesystem_unittest as fakeunittest
from datacryptchain import datacryptchain as dcc
from fixtures import test_keys


class TestChainDecryption(unittest.TestCase):    
    
    def setUp(self):
        pass
        
    def test_chain_decryptable_with_key(self):
        PROJECT = "forest_cats"
        CHAIN_FILENAME = "forest_cats.dcc"
        SK_FILENAME = "fc_secret.dcs"
        fixture_path = os.path.join(os.path.dirname(__file__), "fixtures")
        os.chdir(fixture_path)
        
        # Test that file can be unpacked
        dcc.unpack_chain(PROJECT, SK_FILENAME) # TODO - Fix This Test
        self.assertTrue(os.path.exists("forest_cats.dcl"))
        self.assertTrue(os.path.exists("forest_cats.csv"))

        # Ensure that the unpacked file is valid
        errors = dcc.validate_ledger("forest_cats.dcl")
        self.assertEqual(errors, 0)

        # Ensure that the cats name appears in the csv
        with open("forest_cats.csv", "r") as csv_file:
                  csv = csv_file.read()
        self.assertTrue("skogkatt" in csv)
            
        #Clean up
        os.remove("forest_cats.csv")
        os.remove("forest_cats.dcl")    
            

        
      



        
        


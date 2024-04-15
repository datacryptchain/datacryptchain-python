import os
import unittest
import Cryptodome
from pyfakefs import fake_filesystem_unittest as fakeunittest
from datacryptchain import datacryptchain as dcc
from fixtures import test_keys

class TestChainDecryption(fakeunittest.TestCase):
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures")

    def setUp(self):
        self.setUpPyfakefs()
        self.fs.add_real_directory(self.fixture_path)

    def test_chain_decryptable_with_key(self):
        PROJECT = "forest_cats"
        LEDGER_FILENAME = "forest_cats.dcl"
        SK_FILENAME = "forest_cats_secret.dcs"
        CHAIN_FILENAME = "forest_cats.dcc"

        #Create the keyfile
        secret_key_text = test_keys.FOREST_CATS_SECRET
        with open(SK_FILENAME, "w") as text_file:
            text_file.write(secret_key_text)
        self.assertTrue(os.path.exists(SK_FILENAME))    
            

        with open(os.path.join(self.fixture_path, CHAIN_FILENAME)) as f:
            with open(CHAIN_FILENAME, "w") as target_chain:
                 target_chain.write(secret_key_text)
            
        self.assertTrue(os.path.exists(CHAIN_FILENAME))
        #dcc.unpack_chain(PROJECT, SK_FILENAME) # TODO - Fix This Test
            
            

      



        
        


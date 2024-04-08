import os
import unittest
from pyfakefs import fake_filesystem_unittest as fakeunittest
from datacryptchain import datacryptchain as dcc
import fixtures

class TestLedgerValid(fakeunittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        
    def test_ledger_is_valid(self):
        valid_ledger = fixtures.VALID_LEDGER
        #errors = dcc.make_keys()
        #self.assertEqual(errors, 0)
        #self.assertTrue(os.path.exists("public.dcp"))
        #self.assertTrue(os.path.exists("secret.dcs"))
        
        


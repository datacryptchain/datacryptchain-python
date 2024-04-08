import os
import unittest
from pyfakefs import fake_filesystem_unittest as fakeunittest

from datacryptchain import datacryptchain as dcc

class TestKeyCreation(fakeunittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        
    def test_user_can_initialize_project(self):
        errors = dcc.make_keys()
        self.assertEqual(errors, 0)
        self.assertTrue(os.path.exists("public.dcp"))
        self.assertTrue(os.path.exists("secret.dcs"))
        
        


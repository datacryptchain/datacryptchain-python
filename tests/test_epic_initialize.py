import os
import unittest
from pyfakefs import fake_filesystem_unittest as fakeunittest

from datacryptchain import datacryptchain as dcc

class TestProjectInitialization(fakeunittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        
    def test_user_can_initialize_project(self):
        errors = dcc.initialize_project("poodles")
        self.assertEqual(errors, 0)
        self.assertTrue(os.path.exists("poodles.dcl"))
        self.assertTrue(os.path.exists("poodles.csv"))
        self.assertFalse(os.path.exists("poodles.dcc"))
        


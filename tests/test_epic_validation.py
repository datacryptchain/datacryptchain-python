import csv
import os
import pandas as pd
import random
import re
import subprocess
import unittest
from pyfakefs import fake_filesystem_unittest as fakeunittest
import xml.etree.ElementTree as et
from datacryptchain import datacryptchain as dcc
from fixtures import test_ledgers, test_csvs

from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA as CRSA


#Tests the ability of the validator to detect corruption
class TestLedgerValidAfterCorruption(unittest.TestCase):    
    def setUp(self):
        pass
        
    def test_ledger_is_valid_after_corruption(self):
        ITERATIONS = 10000
        MAX_CSV_VERSIONS = 100
        PROPORTION_CORRUPTED = 0.05
        MAX_LINES_PER_UPDATE = 50
        VERBOSE = True
        csv_filename = "dachshunds.csv"
        max_csv_length = 0
        max_csv_versions = 0
        max_corruptions = 0
        number_errors = 0
        number_corrupted = 0
        EXPORT_REPORT = True

        df = pd.DataFrame(columns=['csv_entries', 'csv_versions', 'introduced_errors', 'detected_errors', 'status'])

        for i in range(ITERATIONS):
            to_corrupt = random.choice([True, False])
            introduced_errors = 0
            expected_min_errors = 0
            csv_versions = 1
            ledger_filename = "dachshunds.dcl"    

            # Clean up any old .dcc files
            try:
                os.remove("dachshunds.dcc")
            except OSError as e:
                pass
                
            # Create some test keys
            errors = dcc.make_keys()
            self.assertEqual(errors, 0)
            self.assertTrue(os.path.exists("public.dcp"))
            self.assertTrue(os.path.exists("secret.dcs"))

            #He initializes a ledger
            errors = dcc.initialize_project("dachshunds")
            self.assertEqual(errors, 0)
            self.assertTrue(os.path.exists("dachshunds.dcl"))
            self.assertTrue(os.path.exists("dachshunds.csv"))
            self.assertFalse(os.path.exists("dachshunds.dcc"))

            #He rewrites the csv with data
            dachshunds = test_csvs.DACHSHUNDS
            with open(csv_filename, "w") as csv_file:
                  csv_file.write(dachshunds)

            # He updates the ledger with the csv
            errors = dcc.update_ledger("dachshunds.dcl", "dachshunds.csv")
            csv_versions += 1
            self.assertEqual(errors, 0)

            # Check that the ledger if valid
            errors = dcc.validate_ledger("dachshunds.dcl")
            self.assertEqual(errors, 0)

            # He updates the ledger several times
            number_updates = random.randrange(MAX_CSV_VERSIONS)
            for nu in range(number_updates):
                # Create and append several random dachshunds (up to MAX_LINES_PER_UPDATE at a time)
                for n in range(random.randrange(MAX_LINES_PER_UPDATE)):
                    row_id = random.randrange(9999) 
                    name = random.choice(['Romeo', 'Layla', 'Rocky', 'Blue', 'Sally', 'Lulu', 'Cricket'])
                    size = random.choice(['standard', 'miniature'])
                    color = random.choice(['cream', 'red', 'black and tan', 'chocolate and cream', 'chocolate and tan']) 
                    height = random.randrange(120, 300)/10
                    weight = random.randrange(40, 140)/10
                    fields = [row_id, name, size, color, height, weight]

                    with open(csv_filename, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(fields)
              
                # He updates the ledger with the csv
                errors = dcc.update_ledger("dachshunds.dcl", "dachshunds.csv")
                csv_versions += 1
                self.assertEqual(errors, 0)

                # Check that the ledger if valid
                errors = dcc.validate_ledger("dachshunds.dcl")
                self.assertEqual(errors, 0)

            # Find final length of the csv file            
            with open("dachshunds.csv", 'r') as fp:
                csv_lines = len(fp.readlines())

            # He packs the ledger and csv into a dcc file
            errors = dcc.pack_ledger("dachshunds", pkf="public.dcp")
            self.assertTrue(os.path.exists("dachshunds.dcc"))

            # Remove the csv and dcl
            os.remove("dachshunds.csv")
            os.remove("dachshunds.dcl")
            self.assertFalse(os.path.exists("dachshunds.csv"))
            self.assertFalse(os.path.exists("dachshunds.dcl"))  

            # unpack the datacryptchain
            dcc.unpack_chain("dachshunds", skf="secret.dcs")
            errors = dcc.validate_ledger("dachshunds.dcl")
            self.assertEqual(errors, 0)
            self.assertTrue(os.path.exists("dachshunds.csv"))
            self.assertTrue(os.path.exists("dachshunds.dcl"))
            
            # change one character in the ledger
            previous_tree = et.parse("dachshunds.dcl")
            root = previous_tree.getroot()
            string_xml = et.tostring(root)
            blocks = root.findall("block")
            previous_hash = "None"
            errors = 0
            for block in blocks:
                block_hash = block.find("hash").text
                csv_content = block.find("csv").text
                random_10 = random.randrange(11)
                if random_10 < (PROPORTION_CORRUPTED * 10):
                    if to_corrupt:
                        digit_indexes = [i for i in range(0, len(csv_content)) if csv_content[i].isdigit()]
                        if digit_indexes:
                            sdi = random.choice(digit_indexes)
                            new_digit = str(random.randrange(10))
                            new_csv_text = csv_content[:sdi] + new_digit + csv_content[sdi + 1:]
                            if new_csv_text != csv_content:
                                introduced_errors = introduced_errors + 1
                                block.find("csv").text = new_csv_text 
                                new_csv_content = block.find("csv").text

            tree = et.ElementTree(root)
           
            with open (ledger_filename, "wb") as file :
                tree.write(file)

            # Check validation again
            corruption_errors = dcc.validate_ledger(ledger_filename, verbose=False)

            if introduced_errors > 0:
                number_corrupted +=1
                if corruption_errors > 0:
                    assertion_msg = f"PASS: {introduced_errors} introduced errors; {corruption_errors} validation errors; {csv_versions} csv versions; {csv_lines} csv entries"
                    error_status = "Pass"
                else:
                    assertion_msg = f"FAIL: {introduced_errors} introduced errors; {corruption_errors} validation errors; {csv_versions} csv versions; {csv_lines} csv entries"
                    error_status = "Fail"
                    number_errors += 1
                self.assertGreater(corruption_errors, 0)
                
            else:
                if corruption_errors > 0:
                    assertion_msg = f"FAIL: {introduced_errors} introduced errors; {corruption_errors} validation errors; {csv_versions} csv versions; {csv_lines} csv entries"
                    error_status = "Fail"
                    number_errors += 1
                else:
                    assertion_msg = f"PASS: {introduced_errors} introduced errors; {corruption_errors} validation errors; {csv_versions} csv versions; {csv_lines} csv entries"
                    error_status = "Pass"
                self.assertEqual(corruption_errors, 0)

            if VERBOSE:
                print (f"{assertion_msg}")
                
            #Update Summary Statistics
            max_csv_length = max([max_csv_length, csv_lines])
            max_csv_versions = max([max_csv_versions, csv_versions])
            max_corruptions = max([max_corruptions, corruption_errors])
            df.loc[len(df)] = [csv_lines, csv_versions, introduced_errors, corruption_errors, error_status]
        
            #clean up temporary files
            os.remove("dachshunds.csv")
            os.remove("dachshunds.dcl")
            os.remove("dachshunds.dcc")
            os.remove("public.dcp")
            os.remove("secret.dcs")
                      
        #Print a summary
        if VERBOSE:
            print(f"Number of Iterations: {ITERATIONS}")
            print(f"Number Corrupted: {number_corrupted}")
            print(f"Max CSV Length: {max_csv_length}")
            print(f"Max CSV Versions: {max_csv_versions}")
            print(f"Max Corruptions: {max_corruptions}")
            print(f"Number Validation Detection Errors: {number_errors}")
            print(df)

        # Export report
        if EXPORT_REPORT:
            df.to_csv('validation_report.csv')

            
      


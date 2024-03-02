DataCryptChain


Installation

1. Create a new virtual environment
2. Download the repository: http://git.stat59.com/stat59/datacryptchain.git 
3. pip install -r requirements.txt


Using DataCryptChain

Create New DataCryptChain Keys
 DataCryptChain keys are needed to encrypt and decrypt the chain      
 >> python datacryptchain.py makekeys
 This will create the secret key (secret.dcs) and the public key (public.dcp) in the current directory


Initialize a new project:
 >> python datacryptchain.py init poodles
 This creates a new datacryptchain ledger (poodles.dcl) as well as a working file poodles.csv
 You may edit the .csv file with any editor
 The ledger (.dcl) should never be edited


Update the Ledger
 >> python datacryptchain.py update poodles
 This will update the ledger with the current .csv

Validate the Ledger
 >> python datacryptchain.py validate poodles
 This will validate the DataCryptChain and return the number of errors

Pack the Ledger
 >> python datacryptchain.py pack poodles [--publickeyfile public.dcp]
 This will pack the ledger into an encrypted file for the public key.
 The ledger always contains the .csv file (do not transmit the .csv separately)

Unpack the Ledger
 >> python datacryptchain.py unpack poodles [--secretkeyfile secret.dcs]
 This will extract the ledger to the local directory (poodles.dcl)

Extract the csv
 >> python datacryptchain.py extract poodles
 Extracts the .csv file from the ledger
 
 
 





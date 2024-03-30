DataCryptChain


Installation from binary
1. Download the binary from https://www.datacryptchain.com/downloads/
2. Move the binary to /usr/local/bin or wherever you keep your executables



Installation from Source

1. Create a new virtual environment
2. Download the repository: http://git.stat59.com/stat59/datacryptchain.git 
3. pip install -r requirements.txt
4. Switch to the directory including datacryptchain.py
5. Build executable with pyinstaller datacryptchain.py --onefile
6. The executable will be built in the ~/dist directory
7. Move the executable to /usr/local/bin/



Using DataCryptChain

Create New DataCryptChain Keys
 DataCryptChain keys are needed to encrypt and decrypt the chain      
 >> datacryptchain makekeys
 This will create the secret key (secret.dcs) and the public key (public.dcp) in the current directory


Initialize a new project:
 >> datacryptchain init poodles
 This creates a new datacryptchain ledger (poodles.dcl) as well as a working file poodles.csv
 You may edit the .csv file with any editor
 The ledger (.dcl) should never be edited


Update the Ledger
 >> datacryptchain update poodles
 This will update the ledger with the current .csv

Validate the Ledger
 >> datacryptchain validate poodles
 This will validate the DataCryptChain and return the number of errors

Pack the Ledger
 >> datacryptchain pack poodles [--publickeyfile public.dcp] 
 This will pack the ledger into an encrypted file for the public key.
 The ledger always contains the .csv file (do not transmit the .csv separately)

Unpack the Ledger
 >> datacryptchain unpack poodles [--secretkeyfile secret.dcs]
 This will extract the ledger to the local directory (poodles.dcl)

Extract the csv
 >> datacryptchain extract poodles
 Extracts the .csv file from the ledger
 
 
 





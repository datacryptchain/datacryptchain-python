DataCryptChain

INSTALLATION

Note that DataCryptChain is a command line utility, and will need to be run from a terminal window.
For windows this is usually the Command Prompt.
On Linux or MacOS any terminal will work

Installation from Binary
Binaries are available for Linux, Mac OS, or Windows.
    Download the binary from https://www.datacryptchain.org/about/download
    Unpack the .zip file into a temporary directory

Installation from Binary - MacOS
  After downloading and extracting the .zip file, open the terminal in extracted directory.
  Execute the following commands from the temporary directory to install:
  >> chmod a+x ./datacryptchain
  >> xattr -d com.apple.quarantine ./datacryptchain
  >> sudo mv ./datacryptchain /usr/local/bin/
  You can now run datacryptchain from your Mac terminal application.

Installation from Binary - Windows
  After downloading and extracting the .zip file, copy the file datacryptchain into the directory c:\Windows
  Open Windows Search and type Command Prompt to open a terminal window, datacryptchain can be run from this terminal.

Installation from Binary - Linux
  After downloading and extracting the .zip file, open the terminal in the extracted directory.
  Execute the following in terminal from the temporary directory to install:
  >> sudo cp ./datacryptchain /usr/local/bin/
You can now run datacryptchain from your shell or terminal window.

Installation from Source
    Create a new virtual environment
    Clone the git repository: https://github.com/datacryptchain/datacryptchain-python.git
    pip install -r requirements.txt
    Switch to the directory including datacryptchain.py
    Build executable with pyinstaller datacryptchain.py --onefile
    The executable will be built in the ~/dist directory
    Move the executable to /usr/local/bin/


USING DATACRYPTCHAIN
  After installing the executable as above, open a Terminal (MacOS), Command Prompt (Windows), or Shell(Linux).
  Navigate to your work directory.
  All commands are executed from this terminal.

Create New DataCryptChain Keys
  DataCryptChain keys are needed to encrypt and decrypt the chain.
  >>datacryptchain makekeys
  This will create the secret key secret.dcs and the public key public.dcp in the current directory.
  Remember you should NEVER transmit your secret key.

Initialize a new project
  We can initialize a project by name.
  This will create a new project called poodles with a data file called poodles.csv and a blockchain ledger called poodles.dcl.
  >> datacryptchain init poodles
  This creates a new DataCryptChain ledger poodles.dcl as well as a working file poodles.csv.
  You may edit the .csv file with any editor such as Excel or LibreOffice.
  The ledger .dcl should never be edited, as editing the ledger will corrupt the ledger and invalidate it.

Update the Ledger
  Updating the ledger will add the contents of the current .csv to the ledger. This will also automatically update the blockchain.
  >> datacryptchain update poodles
  This will update the ledger with the current .csv for the project.

Validate the Ledger
  Validating ledgers ensures that the blockchain is complete without any errors.
  Errors in the blockchain indicate corruption (either intentional or unintentional) of the data.
  >> datacryptchain validate poodles
  This will validate the DataCryptChain and return the number of errors.
  Ledgers with any number of errors are invalid and should not be used.

Pack the Ledger
  This will pack the ledger into an encrypted file for the public key of the recipient.
  Only packed DataCryptChain, labelled as .dcc should be transmitted or shared.
  You will need the public DataCryptChain key for the recipient saved as a .dcp file.
  Keys can be requested from the recipient and be safely transmitted by email.
  Alternatively, check the public key directory on www.datacryptchain.org to see if the recipient has a registered key.
  >> datacryptchain pack poodles --publickeyfile /path/to/recepient_public_key.dcp
  The ledger always contains the .csv file (do not transmit the .csv separately).

Unpack the Ledger
  If you receive a transmitted DataCryptChain (labelled as .dcc) it will need to be unpacked before use.
  Note that you will only be able to unpack a DataCryptChain encrypted with your public key.
  If your secret key is located in the current directory as secret.dcs you do no need to specify the key location.
  >> datacryptchain unpack poodles
  However, If your secret key has a different name or location, you will need to specify its location.
  >> datacryptchain unpack poodles --secretkeyfile /path/to/your_secret_key.dcs
  This will extract the ledger to the local directory as .dcl and extract the most recent .csv.

Extract the csv
  You can at any time manually extract the most recent .csv from the ledger
  >> datacryptchain extract poodles 


TESTING
 >>  python -m unittest discover -s tests -v #run from ~/datacryptchain/ 





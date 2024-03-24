import argparse
import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA as CRSA
from Crypto.Random import get_random_bytes
from datetime import datetime, timezone

import xml.etree.ElementTree as et
import hashlib
import rsa
import csv

def decrypt_text(secretkeyfilename, hashed_text):
    decode_hashed_text = hashed_text
    decode_hashed_text_bytes = base64.b64decode(decode_hashed_text)
    with open(secretkeyfilename, 'rb') as p:
        private_key = rsa.PrivateKey.load_pkcs1(p.read())
    decode_text = rsa.decrypt(decode_hashed_text_bytes, private_key)
    decode_text = decode_text.decode()
    return decode_text        

def encrypt_text(publickeyfilename, text):
    text_bytes = bytes(text, "ascii")
    pcf = publickeyfilename
    with open(pcf, 'rb') as p:
        public_key = rsa.PublicKey.load_pkcs1(p.read())
    hashed_text_bytes = rsa.encrypt(text_bytes, public_key)
    hashed_text = base64.b64encode(hashed_text_bytes)
    hashed_text = hashed_text.decode()
    return hashed_text

def validate_ledger(ledger_filename):
    previous_tree = et.parse(ledger_filename)
    root = previous_tree.getroot()
    blocks = root.findall("block")
    previous_hash = "None"
    errors = 0
    for block in blocks:
        block_hash = block.find("hash").text
        csv_content = block.find("csv").text
        comment = block.find("comment").text
        datetime = block.find("datetime").text
        hashable_string = f"{previous_hash} | {csv_content} | {comment} | {datetime}"
        new_hash = hashlib.sha256(hashable_string.encode()).hexdigest()
        print(f"block hash: {block_hash} | calculated hash: {new_hash}")
        if block_hash != new_hash:
            errors = errors + 1
        previous_hash = block_hash #set this as previous hash for the next round
    return errors

INIT = "init"
MAKEKEY = "makekeys"
ENCRYPT_TEXT = "encrypt"
DECRYPT_TEXT = "decrypt"
DECRYPT_CSV = "decrypt_csv"
UPDATE = "update"
EXTRACT = "extract"
VALIDATE = "validate"
PACK = "pack"
UNPACK = "unpack"

parser = argparse.ArgumentParser(description='DataCryptChain')

parser.add_argument("command", type=str, help="the command")
parser.add_argument("target", type=str, help="the target", nargs="?")

parser.add_argument('--text', '-t',
                    dest='text',
                    action='store',
                    default=None,
                    help='text')

parser.add_argument('--secretkeyfile', '-skf',
                    dest='secretkeyfilename',
                    action='store',
                    default="secret.dcs",
                    help='Private Key File Name')

parser.add_argument('--publickeyfile', '-pbkf',
                    dest='publickeyfilename',
                    action='store',
                    default="public.dcp",
                    help='Public Key File Name')

parser.add_argument('--infile', '-i',
                    dest='infilename',
                    action='store',
                    default=None,
                    help='Input File Name')

parser.add_argument('--outfile', '-o',
                    dest='outfilename',
                    action='store',
                    default="outfile.csv",
                    help='Output File Name')


args = parser.parse_args()
command = args.command
target = args.target


if command == PACK:
    # TODO ensure that csv is up to date for ledger
    # TODO ensure that ledger is valid
    ledger_filename = target +".dcl"
    dcc_filename = target + ".dcc"
    pkf = args.publickeyfilename
    with open(ledger_filename, 'r') as file:
        ledger_text = file.read()

    recipient_key = CRSA.import_key(open(pkf).read())
    session_key = get_random_bytes(32)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(ledger_text.encode())

    with open(dcc_filename, "wb") as f:
        f.write(enc_session_key)
        f.write(cipher_aes.nonce)
        f.write(tag)
        f.write(ciphertext)


if command == UNPACK:
    ledger_filename = target +".dcl"
    dcc_filename = target + ".dcc"
    skf = args.secretkeyfilename
    private_key = CRSA.import_key(open(skf).read())

    with open(dcc_filename, "rb") as f:
        enc_session_key = f.read(private_key.size_in_bytes())
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    with open(ledger_filename, "wb") as f:
        f.write(data)

    # TODO: validate the ledger
    # TODO: unpack the csv


if command == VALIDATE:
    ledger_filename = target +".dcl"
    errors = validate_ledger(ledger_filename)

    print(f"The ledger has been validated with {errors} errors")


if command == EXTRACT: #extract the csv
    ledger_filename = target + ".dcl"
    csv_filename = target + ".csv"
    previous_tree = et.parse(ledger_filename)
    root = previous_tree.getroot()
    previous_csv = root.findall(".//csv")[-1].text

    with open(csv_filename, 'w', newline='') as csvoutfile:
        filewriter = csv.writer(csvoutfile, delimiter=",", quotechar='"')
        for row in previous_csv.splitlines():

            row_values=[]

            for value in row.split(','):
                try:
                    decode_text = decrypt_text(prf, value)
                    value = decode_text
                except:
                    pass
                row_values.append(value)
                filewriter.writerow(row_values)


if command == UPDATE: #update the ledger
    filename = target + ".dcl"
    ledger_filename = target + ".dcl"
    csv_filename = target + ".csv"
    previous_tree = et.parse(ledger_filename)
    root = previous_tree.getroot()

    previous_hash = root.findall(".//hash")[-1].text

    with open(csv_filename, 'r') as file:
        csv_content = file.read()

    comment = "DataCryptChain Updated"
    datetime = datetime.now(timezone.utc).ctime() + " UTC"
    hashable_string = f"{previous_hash} | {csv_content} | {comment} | {datetime}"
    new_hash = hashlib.sha256(hashable_string.encode()).hexdigest()

    m0 = et.Element("block")
    root.append(m0)
    m1 = et.SubElement(m0, "csv")
    m1.text = csv_content
    m2 = et.SubElement(m0, "comment")
    m2.text = comment
    m3 = et.SubElement(m0, "datetime")
    m3.text = datetime
    m4 = et.SubElement(m0, "hash")
    m4.text = new_hash    

    tree = et.ElementTree(root)

    with open (filename, "wb") as files :
        tree.write(files)


if command == INIT:
    filename = target + ".dcl"
    csv_filename = target +".csv"
    previous_hash = "None"
    csv_content = "Create Your New CSV Content Here"
    comment = "DataCryptChain Initialized"
    datetime = datetime.now(timezone.utc).ctime() + " UTC"
    hashable_string = f"{previous_hash} | {csv_content} | {comment} | {datetime}"
    new_hash = hashlib.sha256(hashable_string.encode()).hexdigest()
    warning = "<!-- DataCryptChain Ledger DO NOT EDIT THIS FILE -->"

    root = et.Element("DataCryptChain")
    m0 = et.Element("block")
    root.append(m0)
    m1 = et.SubElement(m0, "csv")
    m1.text = csv_content
    m2 = et.SubElement(m0, "comment")
    m2.text = comment
    m3 = et.SubElement(m0, "datetime")
    m3.text = datetime
    m4 = et.SubElement(m0, "hash")
    m4.text = new_hash

    tree = et.ElementTree(root)

    with open (filename, "wb") as f :
        tree.write(f)
    with open(csv_filename, "w") as csv_file:
        csv_file.write(csv_content)


if command == MAKEKEY:
    print("Public key and secret keys will be written to the current directory")
    (publicKey, privateKey) = rsa.newkeys(1024)
    with open('public.dcp', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
        with open('secret.dcs', 'wb') as p:
            p.write(privateKey.save_pkcs1('PEM'))


if command == ENCRYPT_TEXT:
    text = args.text
    pcf = args.publickeyfilename
    encrypted_text = encrypt_text(pcf, text)
    print(encrypted_text)


if command == DECRYPT_TEXT:
    skf = args.secretkeyfilename
    hashed_text = args.text    
    decode_text = decrypt_text(skf, hashed_text)    
    print(decode_text)


if command == DECRYPT_CSV:
    outfilename = args.outfilename
    skf = args.secretkeyfilename
    with open(args.infilename, newline='') as csvinfile:
        filereader = csv.reader(csvinfile, delimiter=",", quotechar='"')
        with open(outfilename, "w", newline='') as csvoutfile:
            filewriter = csv.writer(csvoutfile, delimiter=",", quotechar='"')
            for row in filereader:
                row_values=[]
                for value in row:
                    try:
                        decode_text = decrypt_text(skf, value)
                        value = decode_text
                    except:
                        pass
                    row_values.append(value)
                    filewriter.writerow(row_values)

         


    

    
    

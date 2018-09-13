#!/usr/bin/python
#-*- coding: utf-8 -*-

# Modules that you need for this to run
import os, random, sys, subprocess
from time import sleep
import Crypto
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

# Allows python to clear the printed screen
subprocess.call(["printf", "'\033c'"])

# color codes in python

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'
CLEAR = '\033c'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'

CBLACKBG  = '\33[40m'
CREDBG    = '\33[41m'
CGREENBG  = '\33[42m'
CYELLOWBG = '\33[43m'
CBLUEBG   = '\33[44m'
CVIOLETBG = '\33[45m'
CBEIGEBG  = '\33[46m'
CWHITEBG  = '\33[47m'

CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

CGREYBG    = '\33[100m'
CREDBG2    = '\33[101m'
CGREENBG2  = '\33[102m'
CYELLOWBG2 = '\33[103m'
CBLUEBG2   = '\33[104m'
CVIOLETBG2 = '\33[105m'
CBEIGEBG2  = '\33[106m'
CWHITEBG2  = '\33[107m'

# Function that prints the loading bar
def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

# this loops and updates the loading bar
def progress():
    # make a list
    items = list(range(0, 57))
    i = 0
    l = len(items)

    # Initial call to print 0% progress
    print_progress(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
    for item in items:
        # Do stuff...
        sleep(0.1)
        # Update Progress Bar
        i += 1
        print_progress(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)


# this is the encryption function
def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = "Encrypted_"+filename
	fileSize = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0, 0xFF))

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	# this writes to the file on the system
	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(fileSize)
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' '* (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))

# this is the decryption file function
def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename[11:]
	with open(filename, 'rb') as infile:
		filesize = long(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		#this writes to the file on the system
		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)

# this functioon gets a hash key password
def getKey(password):
	hasher = SHA256.new(password)
	return hasher.digest()

def Main():
	CLEAR
	print(CRED2)
	print('''
    ____                  _   _       
  / ____|                | | (_)      
 | |     _ __ _   _ _ __ | |_ _  ___  
 | |    | '__| | | | '_ \| __| |/ _ \ 
 | |____| |  | |_| | |_) | |_| | (_) |
  \_____|_|   \__, | .__/ \__|_|\___/ 
               __/ | |                
              |___/|_|                ''')
	print ('''
##########################################################################
#* Welcome to Cryptio! A python encryptor AES Encryption and Decryption *#
##########################<><><><><><><><><>##############################
####################### Creator: ShyGuy899 ###############################
####################### Version: 1.1.0.0 #################################
####################### Date Modified: 5/3/18 @ 3:pm ##################
##########################################################################''') 
	print(CRED2)
	print('''
1. Encrypt File?
2. Decrypt File?''')
	choice = int(input("Choice >>> "))

	if choice == 1:
		filename = raw_input("File to encrypt: ")
		password = raw_input("Password: ")
		encrypt(getKey(password), filename)
		print(CGREEN)
		progress()
		print("Done.")
	elif choice == 2:
		filename = raw_input("File to decrypt: ")
		password = raw_input("Password: ")
		decrypt(getKey(password), filename)
		print(CGREEN)
		progress()
		print("Done.")
	else:
		print("No option selected, closing.....")

if __name__ == '__main__':
	Main()

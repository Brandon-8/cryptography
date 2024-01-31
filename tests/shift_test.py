# A Variety of Unit Test functions for shift.py
import sys
import os

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)

import ciphers.shift as shift
import keyspace

Passed = 0
Total = 0

def print_result(funct_name, result):
    global Total, Passed
    Total += 1
    if result:
        message = 'PASSED' 
        Passed += 1
    else: 
        message ='FAILED'
    print(f'{funct_name}: {message}!')

def caesar(debug=False):
    plaintext = 'inconceivable'
    ciphertext = shift.shift_encrypt(plaintext)
    decrypt = shift.shift_decrypt(ciphertext)
    if debug:
        print(f'\ncaesar():\n\tPlain Text: {plaintext}\n\tCipher Text: {ciphertext}\n\tDecrypted Message: {decrypt}\n')
    
    res = True if decrypt == plaintext.lower() else False

    print_result('caesar', res)

def simple_punct(debug=False):
    key = 8
    plain = "This is the original message!"
    encrypt = shift.shift_encrypt(plain, key=key, space=keyspace.Punctuation)
    crack = shift.shift_crack(encrypt, space=keyspace.Punctuation)
    if debug:
        print(f'\nsimple_punct():\n\tPlain Text: {plain}\n\tCipher Text: {encrypt}\n\tDecrypted Message: {crack}\n')

    res = True if crack[0]['Plaintext'] == plain.lower() and crack[0]['Shift Value'] == key else False

    print_result('simple_punct', res)

def proper_nouns(debug=False):
    key = 19
    plain = "Jack and Jill Went Up the Hill"
    encrypt = shift.shift_encrypt(plain, key=key, space=keyspace.Punctuation)
    crack = shift.shift_crack(encrypt, space=keyspace.Punctuation, valid_percent=0.3, one_result=True)
    if debug:
        print(f'\nproper_nouns():\n\tPlain Text: {plain}\n\tCipher Text: {encrypt}\n\tDecrypted Message: {crack}\n')
   
    res = True if crack[0]['Plaintext'] == plain.lower() and crack[0]['Shift Value'] == key else False

    print_result('proper_nouns', res)

if __name__ == '__main__':
    caesar()
    simple_punct()
    proper_nouns()
    print(f'\n{Passed} / {Total} Tests Passed')
    
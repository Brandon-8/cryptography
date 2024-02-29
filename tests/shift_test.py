# A Variety of Unit Test functions for shift.py
import sys
import os
import pytest

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)

import ciphers.cipher as cipher
import alphabet

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

def test_caesar(debug=False):
    shift = cipher.Shift_Cipher(alphabet.LOWER, 3)
    plaintext = 'inconceivable'
    ciphertext = shift.encrypt(plaintext)
    decrypt = shift.decrypt(ciphertext)
    if debug:
        print(f'\ncaesar():\n\tPlain Text: {plaintext}\n\tCipher Text: {ciphertext}\n\tDecrypted Message: {decrypt}\n')
    
    res = True if decrypt == plaintext.lower() else False
    assert shift.decrypt(shift.encrypt(plaintext)) == plaintext
    print_result('caesar', res)

def test_simple_punct(debug=False):
    key = 8
    shift = cipher.Shift_Cipher(alphabet.PUNCT, key)
    plain = "this is the original message!"
    encrypt = shift.encrypt(plain)
    crack = shift.crack(encrypt)
    if debug:
        print(f'\nsimple_punct():\n\tPlain Text: {plain}\n\tCipher Text: {encrypt}\n\tDecrypted Message: {crack}\n')

    res = True if crack[0]['Plaintext'] == plain.lower() and crack[0]['Shift Value'] == key else False
    assert crack[0]['Plaintext'] == plain and crack[0]['Shift Value'] == key
    print_result('simple_punct', res)

def proper_nouns(debug=False):
    key = 19
    plain = "Jack and Jill Went Up the Hill"
    encrypt = cipher.shift_encrypt(plain, key=key, space=alphabet.Punctuation)
    crack = cipher.shift_crack(encrypt, space=alphabet.Punctuation, valid_percent=0.3, one_result=True)
    if debug:
        print(f'\nproper_nouns():\n\tPlain Text: {plain}\n\tCipher Text: {encrypt}\n\tDecrypted Message: {crack}\n')
   
    res = True if crack[0]['Plaintext'] == plain.lower() and crack[0]['Shift Value'] == key else False

    print_result('proper_nouns', res)

#if __name__ == '__main__':
#    caesar()
    #simple_punct()
    #proper_nouns()
    #print(f'\n{Passed} / {Total} Tests Passed')
    
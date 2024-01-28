# basic shift cipher function to encrypt, decrpyt given a shift value, and decrypt when the shift value is unknown
# Note: uppercase is not perserved
from keyspace import Standard
from util import check_word

def shift_encrypt(plaintext, key=3, space=Standard):
    """
    Take a plaintext and a shift value and shift the plaintext to produce ciphertext
    Inputs:
        plaintext (str): the message to be encrypted
        key (int): the shift value. Default 3 (for Caesar Cipher)
        space (list): the Keyspace being used. Default is standard (26 letters)
    Outputs:
        ciphertext (str): encrypted message
    """
    # convert all chars to lowercase
    plaintext = plaintext.lower()

    ciphertext = ''
    length = len(space)
    for letter in plaintext:
        # check that the plaintext is valid. i.e. all values are in the space
        try:
            idx = space.index(letter)
        except ValueError:
            print(f"Error: invalid character, {letter}, in plaintext")
            return None

        ciphertext += space[(idx + key) % length]
    return ciphertext

def shift_decrypt(ciphertext, key=3, space=Standard):
    """
    Take a ciphertext and a shift value and shift the ciphertext to produce plaintext
    Inputs:
        ciphertext (str): the encrypted message
        key (int): the shift value. Default 3 (for Caesar Cipher)
        space (list): the Keyspace being used. Default is standard (26 letters)
    Outputs:
        plaintext (str): decrypted message
    """
    # convert all chars to lowercase
    ciphertext = ciphertext.lower()
    
    plaintext = ''
    length = len(space)
    for letter in ciphertext:
        # check that the plaintext is valid. i.e. all values are in the space
        try:
            idx = space.index(letter)
        except ValueError:
            print(f"Error: invalid character, {letter}, in plaintext")
            return None

        plaintext += space[(idx - key) % length]
    return plaintext

def shift_crack(ciphertext, space=Standard):
    """
    Given a ciphertext, attempt to crack the cipher and return the plaintext
    when the shift value is unknown

    Note: The plaintext must be a known English word

    Inputs:
        ciphertext (str): the text to be decrypted
    
    Output:
        decrypt (list): list of possible decrpyted texts
                        Each entry is of the form: {'Plaintext': x, 'Shift Value': y}
    """
    possible_decrpyt = [] # may be possible to get more than one potential plaintext
    length = len(space)
    # Brute Force by checking every possible shift value
    for ii in range(length):
        poss = shift_decrypt(ciphertext, key=ii, space=space)
        #print(poss)
        if poss == None:
            return None
        
        # check if the decrypted text is english
        if check_word(poss):
            possible_decrpyt.append({'Plaintext': poss, 'Shift Value': ii})
    
    return possible_decrpyt
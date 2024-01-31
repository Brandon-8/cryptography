# basic shift cipher function to encrypt, decrpyt given a shift value, and decrypt when the shift value is unknown
# Note: uppercase is not perserved
from keyspace import Standard
from util import check_text, calc_char_frequency

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

def shift_crack_brute_force(ciphertext, space, valid_percent, one_result=False):
    possible_decrpyt = [] # may be possible to get more than one potential plaintext
    length = len(space)
    # Brute Force by checking every possible shift value
    for ii in range(length):
        poss = shift_decrypt(ciphertext, key=ii, space=space)

        if poss == None:
            return None
        
        # check if the decrypted text is english
        valid = check_text(poss)
        res = {'Plaintext': poss, 'Shift Value': ii, 'Valid': valid}
        if one_result and valid >= valid_percent:
            return res
        possible_decrpyt.append(res)  
    
    return possible_decrpyt

def shift_crack_frequency(ciphertext, space, valid_percent):
    # Note: This will only work for long messages. Message must contain the letter 'e'
    def _check_word(letter):
        shift = space.index(letter) - space.index('e')
        poss = shift_decrypt(ciphertext, key=shift, space=space)
            
        # check if the decrypted text is english
        valid = check_text(poss, valid_percent=valid_percent)
        if valid >= valid_percent:
            return {'Plaintext': poss, 'Shift Value': shift, 'Valid': valid}
        return None
    
    freq = calc_char_frequency(ciphertext)
    max_freq = 0
    possible_decrpyt = []
    for i, key in enumerate(freq.keys()):
        if i == 0: # most frequent letter
            max_freq = freq[key]
            res = _check_word(key)
            if res != None:
                possible_decrpyt.append(res)

        elif freq[key] == max_freq: # letters tied with same highest frequency
            res = _check_word(key)
            if res != None:
                possible_decrpyt.append(res)

        elif len(possible_decrpyt) == 0: # highest frequent letter yield no results, keep trying until match
            res = _check_word(key)
            if res != None:
                possible_decrpyt.append(res)
        else:
            break
    if len(possible_decrpyt) == 0:
        print('ERROR: Could Not crack decrpytion using Frequency Analysis\nTry Brute Force Method instead')
        return None
    return possible_decrpyt


def shift_crack(ciphertext, method='brute_force', space=Standard, valid_percent=0.80, one_result=False):
    """
    Given a ciphertext, attempt to crack the cipher and return the plaintext
    when the shift value is unknown

    Note: The plaintext must be a known English word

    Inputs:
        ciphertext (str): the text to be decrypted
        method (str): 'brute_force': test all possible shift values
                      'frequency': use frquency analysis
    
    Output:
        decrypt (list): list of possible decrpyted texts
                        Each entry is of the form: {'Plaintext': x, 'Shift Value': y}
    """
    if method.lower() == 'brute_force':
        all_options = shift_crack_brute_force(ciphertext, space, valid_percent=valid_percent, one_result=one_result)
        if type(all_options) == dict:
            poss = [all_options]
        else:
            sorted_list = sorted(all_options, key=lambda x: x['Valid'], reverse=True)
            poss = []
            for d in sorted_list:
                if d['Valid'] >= valid_percent:
                    poss.append(d)
                else:
                    break

    elif method.lower() == 'frequency':
        poss = shift_crack_frequency(ciphertext, space, valid_percent=valid_percent)
    else:
        print(f'Unknown Method {method}\nAvailable opitions are:\n\t"brute_force"\n\t"frequency"')
        return None
    
    return poss



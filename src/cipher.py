# basic shift cipher function to encrypt, decrpyt given a shift value, and decrypt when the shift value is unknown
# Note: uppercase is not perserved
import numpy as np
from alphabet import UPPER
from src.util import check_text, calc_char_frequency, ENGLISH_FREQUENCIES
import src.util as util
import random

DEFAULT_ALPHABET = UPPER
###########################
# Basic Cipher Parent Class
###########################
class Cipher():
    def __init__(self, alphabet=DEFAULT_ALPHABET, key=None):
        self.alphabet = alphabet
        self.key = key

    def key_to_int_list(self, key):
        self.key = [self.alphabet.index(i) for i in key]
    
    def string_to_int_list(self, text):
        int_list = [self.alphabet.index(i) for i in text]
        return int_list
    
    def key_to_string(self):
        return ''.join([self.alphabet[i] for i in self.key])
    
    def int_list_to_string(self, int_list):
        return ''.join([self.alphabet[i] for i in int_list])  
      
    def verify_text(self, text):
        """
        Verify the given text is valid. i.e. all letters are in the alphabet
        """
        for letter in text:
            if letter not in self.alphabet:
                print(f"Error: invalid character, \'{letter}\', in \'{text}\'")
                return False
        return True
    
    def verify_key(self):
        raise NotImplementedError
    
    def generate_random_key(self):
        raise NotImplementedError
    
    # getters and setters
    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def set_key(self, key):
        self.key = key
    
    def get_alphabet(self):
        return self.alphabet
    
    def get_key(self):
        return self.key


######################
# Shift Cipher
######################
class Shift_Cipher(Cipher):
    def __init__(self, alphabet=DEFAULT_ALPHABET, shift_value=3):
        super().__init__(alphabet, shift_value)
        if not self.verify_key(shift_value):
            print('INVALID KEY Specified. Generating Random Key')
            self.generate_random_key()

    def generate_random_key(self):
        length = len(self.alphabet)
        self.key = random.randint(0, length)

    def verify_key(self, newKey):
        if not isinstance(newKey, int):
            return False
        newKey = abs(newKey)
        if newKey < len(self.alphabet):
            return True
        return False

    def set_key(self, shift_value):
        if self.verify_key(shift_value):
            super().set_key(shift_value)
        else:
            print('ERROR: Invalid Key')

    def set_shift_value(self, shift_value):
        self.set_key(shift_value)

    def get_shift_value(self, shift_value):
        super().get_key(shift_value)

    def encrypt(self, plaintext):
        """
        Take a plaintext and a shift value and shift the plaintext to produce ciphertext
        Inputs:
            plaintext (str): the message to be encrypted
            key (int): the shift value. Default 3 (for Caesar Cipher)
            space (list): the Keyspace being used. Default is standard (26 letters)
        Outputs:
            ciphertext (str): encrypted message
        """
        if self.verify_text(plaintext):
            length = len(self.alphabet)
            ciphertext = ''.join([self.alphabet[(self.alphabet.index(letter) + self.key) % length] for letter in plaintext])
            return ciphertext

    def decrypt(self, ciphertext):
        """
        Take a ciphertext and a shift value and shift the ciphertext to produce plaintext
        Inputs:
            ciphertext (str): the encrypted message
            key (int): the shift value. Default 3 (for Caesar Cipher)
            space (list): the Keyspace being used. Default is standard (26 letters)
        Outputs:
            plaintext (str): decrypted message
        """
        self.key = -self.key
        plaintext = self.encrypt(ciphertext)
        self.key = -self.key
        return plaintext

    def shift_crack_brute_force(self, ciphertext, valid_percent, one_result=False):
        possible_decrpyt = [] # may be possible to get more than one potential plaintext
        length = len(self.alphabet)
        # Brute Force by checking every possible shift value
        for ii in range(length):
            self.set_key(ii)
            poss = self.decrypt(ciphertext)

            if poss == None:
                return None
            
            # check if the decrypted text is english
            valid = check_text(poss)
            res = {'Plaintext': poss, 'Shift Value': ii, 'Valid': valid}
            if one_result and valid >= valid_percent:
                return res
            possible_decrpyt.append(res)  
        
        self.set_key(None)
        return possible_decrpyt

    def shift_crack_frequency(self, ciphertext, valid_percent):
        # Note: This will only work for long messages. Message must contain the letter 'e'
        def _check_word(letter):
            shift = self.alphabet.index(letter) - self.alphabet.index('e')
            poss = self.shift_decrypt(ciphertext, key=shift)
                
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

    def crack(self, ciphertext, method='brute_force', valid_percent=0.80, one_result=False):
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
            all_options = self.shift_crack_brute_force(ciphertext, valid_percent=valid_percent, one_result=one_result)
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
            poss = self.shift_crack_frequency(ciphertext, valid_percent=valid_percent)
        else:
            print(f'Unknown Method {method}\nAvailable opitions are:\n\t"brute_force"\n\t"frequency"')
            return None
        
        return poss


######################
# Vigenere Cipher
######################
class Vigenere_Cipher(Cipher):
    def __init__(self, alphabet=DEFAULT_ALPHABET, key=None):
        self.random_key_length = 256
        super().__init__(alphabet, key)
        if key and self.verify_key(key):
            self.key_to_int_list(key)

        else:
            print('No Key Specified. Generating Random Key')
            self.generate_random_key()
    
    def generate_random_key(self):
        length = len(self.alphabet)
        self.key = [random.randint(0, length) for _ in range(self.random_key_length)]

    def verify_key(self, newKey):
        if not newKey:
            return False

        if not self.verify_text(newKey):
            return False
        
        return True

    def set_key(self, newKey):
        if self.verify_key(newKey):
            self.key_to_int_list(newKey)  
          
    def encrypt(self, plaintext):
        if self.verify_text(plaintext):
            length = len(self.alphabet)
            length_text = len(plaintext)
            print(len(self.key), length, length_text)
            ciphertext = ''.join([self.alphabet[(self.alphabet.index(plaintext[i]) + self.key[i % len(self.key)]) % length] for i in range(length_text)])
            return ciphertext
        return None

    def decrypt(self, ciphertext):
        self.key = np.array(self.key) * -1
        plaintext = self.encrypt(ciphertext)
        self.key = self.key * -1
        return plaintext
    

######################
# Substitution Cipher
######################
class Substituion_Cipher(Cipher):
    def __init__(self, alphabet=DEFAULT_ALPHABET, key=None):
        super().__init__(alphabet, key)
        if key and self.verify_key(key):
            self.key_to_int(key)

        else:
            print('No Key Specified. Generating Random Key')
            self.generate_random_key()
            
    def generate_random_key(self):
        length = len(self.alphabet)
        self.key = random.sample(range(length), length)

    def verify_key(self, newKey):
        if not newKey:
            return False
        if len(newKey) != len(self.alphabet):
            print(f'ERROR: Invalid Key: Key has len {len(newKey)}, alphabet has len {len(self.alphabet)}')
            return False
        
        if not self.verify_text(newKey):
            return False
        
        for letter in self.alphabet:
            if letter not in newKey:
                print(f'ERROR: Invalid Key: \'{letter}\' in alphabet but not Key')
                return False
        return True

    def set_key(self, newkey):
        if self.verify_key(newkey):
            self.key_to_int_list(newkey)  
        
    def encrypt(self, plaintext):
        if self.verify_text(plaintext):
            if not self.key:
                print('ERROR: No key specified for Substitution Cipher')
                return None
            return ''.join([self.alphabet[self.key[self.alphabet.index(letter)]] for letter in plaintext])
        return None
    
    def decrypt(self, ciphertext):
        print(ciphertext)
        if self.verify_text(ciphertext):
            if not self.key:
                print('ERROR: No key specified for Substitution Cipher')
                return None
            return ''.join([self.alphabet[self.key.index(self.alphabet.index(letter))] for letter in ciphertext])
        return None
    
    # Not Implemented
    def crack(self, ciphertext, valid_percent):
        # Note: This will only work for long messages. Message must contain the letter 'e'
        def _check_word(letter):
            shift = self.alphabet.index(letter) - self.alphabet.index('e')
            poss = self.shift_decrypt(ciphertext, key=shift)
                
            # check if the decrypted text is english
            valid = check_text(poss, valid_percent=valid_percent)
            if valid >= valid_percent:
                return {'Plaintext': poss, 'Shift Value': shift, 'Valid': valid}
            return None
        
        freq = calc_char_frequency(ciphertext)
        table = dict(sorted(ENGLISH_FREQUENCIES.items(), key=lambda x: x[1], reverse=True))
        print(freq)
        print('-------------\n', table)
        english_freq = "etaoinshrdlcumwfgypbvkjxqz"
        mapping = {}
        for cipher_letter in freq :
            # Take the most frequent ciphertext letters and map them to the most frequent English letters
            mapping[cipher_letter] = english_freq [len(mapping)]
        
        plaintext = ''.join(mapping.get(letter, letter) for letter in ciphertext)
        return plaintext
        """
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
            print('ERROR: Could Not crack decrpytion using Frequency Analysis')
            return None
        return possible_decrpyt
        """

######################
# Affine Cipher
######################
class Affine_Cipher(Cipher):
    def __init__(self, alphabet=DEFAULT_ALPHABET, key=None):
        super().__init__(alphabet, key)
        if key and self.verify_key():
            #self.key_to_int_list(key)
            pass
        else:
            print('No Key Specified. Generating Random Key')
            self.generate_random_key()
    
    def verify_key(self):
        try:
            a,b = self.key
            return util.is_coprime(a, len(self.alphabet))
        except:
            raise ValueError('Invalid Key')
    
    def generate_random_key(self):
        poss_a = []
        n = len(self.alphabet)
        for ii in range(1, n-1): 
            # if 1 is included and chosen for a, get a shift cipher
            if util.is_coprime(ii, n):
                poss_a.append(ii)
        
        a = random.choice(poss_a)
        b = random.randint(0, 25)
        self.key = (a,b)
        
    def encrypt(self, plaintext):
        a,b = self.key
        n = len(self.alphabet)
        if self.verify_text(plaintext):
            int_list = self.string_to_int_list(plaintext)
            encrypt = [((a*ii) + b) % n for ii in int_list]
            return self.int_list_to_string(encrypt)
        return None
    
    def decrypt(self, ciphertext):
        a,b = self.key
        n = len(self.alphabet)
        x = util.modular_inverse(a, n)
        temp = self.key
        self.key = (x, (-b*x) % n)
        decrypt = self.encrypt(ciphertext)
        self.key = temp
        return decrypt
    
##########################
# General Affine Cipher
##########################
# Not Implemented
class General_Affine_Cipher(Cipher):
    def __init__(self, alphabet=DEFAULT_ALPHABET, key=None, dimension=None):
        raise NotImplementedError
        super().__init__(alphabet, key)
        if key and self.verify_key():
            #self.key_to_int_list(key)
            pass
        else:
            print('No Key Specified. Generating Random Key')
            self.generate_random_key()
    
    def verify_key(self):
        try:
            a,b = self.key
            return util.is_coprime(a, len(self.alphabet))
        except:
            raise ValueError('Invalid Key')
    
    def generate_random_key(self):
        poss_a = []
        n = len(self.alphabet)
        for ii in range(1, n-1): 
            # if 1 is included and chosen for a, get a shift cipher
            if util.is_coprime(ii, n):
                poss_a.append(ii)
        
        a = random.choice(poss_a)
        b = random.randint(0, 25)
        self.key = (a,b)
        
    def encrypt(self, plaintext):
        a,b = self.key
        n = len(self.alphabet)
        if self.verify_text(plaintext):
            int_list = self.string_to_int_list(plaintext)
            encrypt = [((a*ii) + b) % n for ii in int_list]
            return self.int_list_to_string(encrypt)
        return None
    
    def decrypt(self, ciphertext):
        a,b = self.key
        n = len(self.alphabet)
        x = util.modular_inverse(a, n)
        temp = self.key
        self.key = (x, (-b*x) % n)
        decrypt = self.encrypt(ciphertext)
        self.key = temp
        return decrypt



###################################
# Linear Feedback Shift Registers
###################################
    



##########
# RSA
##########
    


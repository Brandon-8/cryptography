# Helper util functions
import enchant
import string
import numpy as np

Dict = enchant.Dict("en_US")

Punctuation_List = ['.', '?', '!', ',', ';', ':']

ENGLISH_FREQUENCIES = {
    'a': 0.0817, 'b': 0.0150, 'c': 0.0278, 'd': 0.0425,
    'e': 0.1270, 'f': 0.0223, 'g': 0.0202, 'h': 0.0609,
    'i': 0.0697, 'j': 0.0015, 'k': 0.0077, 'l': 0.0403,
    'm': 0.0241, 'n': 0.0675, 'o': 0.0751, 'p': 0.0193,
    'q': 0.0010, 'r': 0.0599, 's': 0.0633, 't': 0.0906,
    'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015,
    'y': 0.0197, 'z': 0.0007
}

def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)

def is_divisor(num, divisor):
    return num % divisor == 0

def congruent_modulo(a,b,n):
    # compute if a and b are congruent to each other modulo n
    return is_divisor((a-b), n)

def extended_gcd(a,b):
    if b == 0:
        return 1, 0
    x,y = extended_gcd(b, a % b)
    return y, x - (a // b) * y

def bezout_coefficients(a,b):
    return extended_gcd(a,b)

def modular_inverse(a,m):
    x, y = bezout_coefficients(a, m)
    if a*x + m*y != 1:
        raise ValueError(f"Modular Inverse does not exists for {a} mod {m}")
    else:
        return x % m
    
def is_coprime(a,b):
    return True if gcd(a,b) == 1 else False

def avail_languages():
    """
    See which languages are currently available
    """
    avail = enchant.list_languages()
    print(f"Available languages: {avail}")
    return avail

def current_language():
    """
    See what language is being used
    """
    curr = Dict.tag
    print(f"Current language is: {curr}")
    return curr

def set_language(lang):
    """
    Set the language to be used to check for words
    Default is "en_US"

    Input:
        lang (str): language to be used
    """
    global Dict
    if enchant.dict_exists(lang):
        Dict = enchant.Dict(lang)
        print(f"Language set to: {lang}")
    else:
        print(f"Invalid Language: {lang}")
        exit(-1)

def remove_punctuation(input):
    """
    Remove the punctuation from a given string

    Inputs:
        input (str): input string with punctuation

    Outputs:
        result (str): the input str without any punctuation
    """
    # Create a translation table
    translator = str.maketrans('', '', string.punctuation)
    
    # Use translate method to remove punctuation
    result = input.translate(translator)
    
    return result

def remove_trailing_punctuation(input):
    if input == '':
        return ''
    if input[-1] in Punctuation_List:
        return input[:-1]
    return input

def check_text(s, valid_percent=0.50):
    """
    Calculate the percentage of words in a text are English. Check percentage vs binary 
    (all words are English vs at least one word is not English) to account for Proper Nouns 
    not found in dict


    Inputs:
        s (str): a given string to test for english words
        valid_percent (float): between 0-1, percentage of words that must be in the eng dict
                               for the string to be valid (Account for Proper Nouns not in eng dict)
    
    Outputs:
        True: if s only has english words, False otherwise
    """
    # remove all punctuation from the str and split so
    # each word in s is its own entry in s_list
    #s_clean = remove_punctuation(s)
    s_list = s.split(' ')
    #cutoff = len(s_list) * valid_percent
    valid_count = 0
    # check validity of each word in s
    for word in s_list:
        word = remove_trailing_punctuation(word)

        # Invalid if leading/trailing white space
        if word == '':
            return False
        

        valid = Dict.check(word)
        if valid:
            valid_count += 1

    return valid_count/len(s_list)

def calc_char_frequency(s):
    freq = {}
    # Counting the frequency of each character in the string
    for c in s:
        if c in freq: 
            freq[c] += 1 
        else: 
            freq[c] = 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
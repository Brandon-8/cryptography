# Helper util functions
import enchant
import string
import numpy as np

Dict = enchant.Dict("en_US")

Punctuation_List = ['.', '?', '!', ',', ';', ':']
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
# Helper util functions
import enchant
import string

Dict = enchant.Dict("en_US")

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

def check_word(s, valid_percent=0.50):
    """
    Check that a string contains only english words

    Inputs:
        s (str): a given string to test for english words
        valid_percent (float): between 0-1, percentage of words that must be in the eng dict
                               for the string to be valid (Account for Proper Nouns not in eng dict)
    
    Outputs:
        True: if s only has english words, False otherwise
    """
    # remove all punctuation from the str and split so
    # each word in s is its own entry in s_list
    s_clean = remove_punctuation(s)
    s_list = s_clean.split(' ')
    cutoff = int(len(s_list) * valid_percent)
    valid_count = 0
    # check validity of each word in s
    for word in s_list:
        # Invalid if leading/trailing white space
        if word == '':
            return False
        
        valid = Dict.check(word)
        if valid:
            valid_count += 1
            
    if valid_count >= cutoff:
        return True
    return False

def calc_char_frequency(s):
    freq = {}
    # Counting the frequency of each character in the string
    for c in s:
        if c in freq: 
            freq[c] += 1 
        else: 
            freq[c] = 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
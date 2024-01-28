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

def check_word(s):
    """
    Check that a string contains only english words

    Inputs:
        s (str): a given string to test for english words
    
    Outputs:
        True: if s only has english words, False otherwise
    """
    # remove all punctuation from the str and split so
    # each word in s is its own entry in s_list
    s_clean = remove_punctuation(s)
    s_list = s_clean.split(' ')

    # check validity of each word in s
    for word in s_list:
        # Invalid if leading/trailing white space
        if word == '':
            return False
        
        valid = Dict.check(word)
        if not valid:
            return False
    return True
# A Variety of Unit Test functions for util.py
import sys
import os

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)

import util

if __name__ == '__main__':
    print('Hello')
    print(util.current_language())
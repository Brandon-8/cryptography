from keyspace import Space, Punctuation
from ciphers.shift import shift_encrypt, shift_decrypt, shift_crack
import numpy as np

if __name__ == '__main__':
    # test caesar cipher
    plaintext = 'inconceivable'
    ciphertext = shift_encrypt(plaintext)
    decrypt = shift_decrypt(ciphertext)
    print(f'Plain Text: {plaintext}\nCipher Text: {ciphertext}\nDecrypted Message: {decrypt}\n')

    # crack a shift cipher of a complex message (punctuation and spaces)
    # with an unknown key value
    plain = "This is the original message!"
    encrypt = shift_encrypt(plain, key=8, space=Punctuation)
    crack = shift_crack(encrypt, space=Punctuation)
    print(f'Plain Text: {plain}\nCipher Text: {encrypt}\nDecrypted Message: {crack}\n')

    # crack a shift cipher of a complex message (punctuation and spaces) using frequency analysis
    # with an unknown key value
    #plain_freq = "This is a really long message! Hopefully the frequency analysis will work, Brandon"
    #plain_freq = "Brandon walks Josey"
    plain_freq = 'Je ne sais pas!'
    encrypt_freq = shift_encrypt(plain_freq, key=8, space=Punctuation)
    crack_freq = shift_crack(encrypt_freq, method='frequency', space=Punctuation, valid_percent=0.3)
    print(f'Plain Text: {plain_freq}\nCipher Text: {encrypt_freq}\nDecrypted Message: {crack_freq}\n')

    import util
    util.avail_languages()
    util.current_language()
    util.set_language("en_GB")
    util.current_language()
    util.set_language("fr_FR")
    util.current_language()
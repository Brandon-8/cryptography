from keyspace import Space, Punctuation
from shift import shift_encrypt, shift_decrypt, shift_crack

if __name__ == '__main__':
    # test caesar cipher
    plaintext = 'inconceivable'
    ciphertext = shift_encrypt(plaintext)
    decrypt = shift_decrypt(ciphertext)
    print(f'Plain Text: {plaintext}\nCipher Text: {ciphertext}\nDecrypted Message: {decrypt}')

    # crack a shift cipher of a complex message (punctuation and spaces)
    # with an unknown key value
    plain = "This is the original message!"
    encrypt = shift_encrypt(plain, key=8, space=Punctuation)
    crack = shift_crack(encrypt, space=Punctuation)
    print(f'Plain Text: {plain}\nCipher Text: {encrypt}\nDecrypted Message: {crack}')
from alphabet import LOWER, SPACE, PUNCT
from src.cipher import Shift_Cipher, Substituion_Cipher, Vigenere_Cipher, Affine_Cipher
import numpy as np

if __name__ == '__main__':
    shift = Shift_Cipher(LOWER, 3)
    # test caesar cipher
    plaintext = 'inconceivable'
    ciphertext = shift.encrypt(plaintext)
    decrypt = shift.decrypt(ciphertext)
    print(f'Plain Text: {plaintext}\nCipher Text: {ciphertext}\nDecrypted Message: {decrypt}\n')

    sub = Substituion_Cipher(LOWER)
    key = 'kviruxpqbysjtmwcehladozgfn'
    sub.set_key(key)
    # test substitution cipher
    plaintext = 'secretmessage'
    ciphertext = sub.encrypt(plaintext)
    decrypt = sub.decrypt(ciphertext)
    print(f'Plain Text: {plaintext}\nCipher Text: {ciphertext}\nDecrypted Message: {decrypt}\n')

    print('######## Frequency Analysis ########')
    sub1 = Substituion_Cipher(alphabet=SPACE)
    print(sub1.key)
    plaintext = 'this is a really important message that will hopefully be decrypted using frequency analysis'.upper()
    ciphertext = sub1.encrypt(plaintext)
    decrypt = sub1.decrypt(ciphertext)
    crack = sub1.crack(ciphertext, valid_percent=0.8)
    print(f'Plain Text: {plaintext}\nCipher Text: {ciphertext}\nDecrypted Message: {decrypt}\n')
    print(f'Crack: {crack}')


    shift1 = Shift_Cipher(shift_value=28)
    print(shift1.key)
    shift1.set_key(-26)
    print(shift1.key)
    shift1.set_key(7)
    print(shift1.key)

    print('######################')
    vig = Vigenere_Cipher(alphabet=SPACE)
    #print(vig.key, len(vig.key))
    plaintext = 'this is the plaintext'.upper()
    ciphertext = vig.encrypt(plaintext)
    decrypt = vig.decrypt(ciphertext)
    print(f'Plain Text: {plaintext}\nCipher Text: {ciphertext}\nDecrypted Message: {decrypt}\n')
   

    print('######################')
    vig1 = Vigenere_Cipher(key='BAD')
    #print(vig1.key, len(vig1.key))
    plaintext = 'greetings'.upper()
    ciphertext = vig1.encrypt(plaintext)
    decrypt = vig1.decrypt(ciphertext)
    print(f'Plain Text: {plaintext}\nCipher Text: {ciphertext}\nDecrypted Message: {decrypt}\n')
   
    print('######################')
    aff = Affine_Cipher(LOWER, key=(3,5))
    plaintext = 'plaintext'
    ciphertext = aff.encrypt(plaintext)
    decrypt = aff.decrypt(ciphertext)
    print(f'Plain Text: {plaintext}\nCipher Text: {ciphertext}\nDecrypted Message: {decrypt}\n')
   
    print('######################')
    aff1 = Affine_Cipher(LOWER)
    print(aff1.key)
    #from util import congruent_modulo, bezout_coefficients
    #print(congruent_modulo(-5,7,4), congruent_modulo(1,-1,2), congruent_modulo(1,-1,3))
    #print(bezout_coefficients(7, 5))
    #from util import gcd    
    #print(gcd(12, 16), gcd(16, 12), gcd(12, 4), gcd(4, 0))
    #print(gcd(60, 15), gcd(0,4), gcd(0,0))
    # crack a shift cipher of a complex message (punctuation and spaces)
    # with an unknown key value
    #plain = "This is the original message!"
    #encrypt = shift_encrypt(plain, key=8, space=Punctuation)
    #crack = shift_crack(encrypt, space=PUNCTUATION)
    #print(f'Plain Text: {plain}\nCipher Text: {encrypt}\nDecrypted Message: {crack}\n')

    # crack a shift cipher of a complex message (punctuation and spaces) using frequency analysis
    # with an unknown key value
    #plain_freq = "This is a really long message! Hopefully the frequency analysis will work, Brandon"
    #plain_freq = "Brandon walks Josey"
    #plain_freq = 'Je ne sais pas!'
    #encrypt_freq = shift_encrypt(plain_freq, key=8, space=Punctuation)
    #crack_freq = shift_crack(encrypt_freq, method='frequency', space=Punctuation, valid_percent=0.3)
    #print(f'Plain Text: {plain_freq}\nCipher Text: {encrypt_freq}\nDecrypted Message: {crack_freq}\n')

"""

    def encrypt(a, b, plain):
        import numpy as np
        temp = np.matmul(a, plain)
        temp = temp + b
        temp = temp % 26
        #print(temp)
        return temp
    
    def decrypt(a, b, ciphertext):
        import numpy as np
        
        inv = np.array([[a[1][1], -a[0][1]], [-a[1][0], a[0][0]]])
        denom = (a[0][0] * a[1][1]) - (a[1][0] * a[0][1])
        inv = inv * denom
        inv = inv % 26
        #print(inv)

        #ciphertext = ciphertext - b
        temp = np.matmul(inv, ciphertext)
        temp = temp % 26
        temp1 = np.matmul(-1*inv, b) % 26
        temp = (temp - temp1) % 26
        print(temp)
        return temp

    a = [[8, 25], [19, 0]]
    b = [0, 6]

    #plain = [11, 4]
    #plain1 = [12, 14]
    #plain2 = [13, 18]
    #ciphertext = encrypt(a,b, plain)
    #print(ciphertext) 
    #ciphertext1 = encrypt(a,b, plain1)
    #print(ciphertext1) 
    #ciphertext2 = encrypt(a,b, plain2)
    #print(ciphertext2)   
    #d = decrypt(a,b, ciphertext)
    #d1 = decrypt(a,b, ciphertext1)
    #d2 = decrypt(a,b, ciphertext2)

    plain = [14, 17]
    plain1 = [0, 13]
    plain2 = [6, 4]
    ciphertext = encrypt(a,b, plain)
    print(ciphertext) 
    ciphertext1 = encrypt(a,b, plain1)
    print(ciphertext1) 
    ciphertext2 = encrypt(a,b, plain2)
    print(ciphertext2)   
    d = decrypt(a,b, np.array([17, 12]))
    d1 = decrypt(a,b, np.array([13, 6]))
    d2 = decrypt(a,b, np.array([18, 16]))

    #a = [[4, 21], [7, 8]]
    #b = [21, 12]
    #plain = [4, 22]
    #ciphertext = encrypt(a,b, plain)
    #print(ciphertext)
    d = decrypt(a,b, np.array([18, 16]))
    d1 = decrypt(a,b, np.array([18, 19]))
    d2 = decrypt(a,b, np.array([12, 22]))

    #d = decrypt(a,b, np.array([12, 21]))
    #d1 = decrypt(a,b, np.array([17, 6]))
    #d2 = decrypt(a,b, np.array([19, 14]))
    #import util
    #util.avail_languages()
    #util.current_language()S
    #util.set_language("en_GB")
    #util.current_language()
    #util.set_language("fr_FR")
    #util.current_language()

    for a in range(26):
        for b in range(26):
            for x in range(26):
                eq1 = 14*a + 17*b + x
                eq2 = 13*b + x
                eq3 = 6*a + 4*b + x
                if eq1 % 26 == 17 and eq2 % 26 == 13 and eq3 % 26 == 18:
                    print(a,b,x)
                    break
    print('-----')
    for c in range(26):
        for d in range(26):
            for y in range(26):
                eq1 = 14*c + 17*d + y
                eq2 = 13*d + y
                eq3 = 6*c + 4*d + y
                if eq1 % 26 == 12 and eq2 % 26 == 6 and eq3 % 26 == 16:
                    print(c,d,y)
                    break

    s = 'abcdefgh'
    print(s.index('c'))
"""
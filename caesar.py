import sys
import operator
from itertools import cycle
from collections import deque

def solver():
    # Get frequency of each letter in cipher text
    frequency = [CIPHER.count(chr(x))/float(len(CIPHER)) for x in range(ord('a'), ord('z')+1)]
    # Create object that allows you to rotate items in a list (simulates increasing by one)
    rotate_frequency = deque(LETTER_FREQS)

    # Calculate correlations for each i
    shift_corr = [0] * 26
    for i in range(0, 26):
        shift_corr[i] = sum(x*y for x, y in zip(rotate_frequency, frequency))
        rotate_frequency.rotate(-1)

    # Sort by highest probability    
    most_likely_keys = [i[0] for i in sorted(enumerate(shift_corr), key=lambda x:x[1], reverse=True)]
    print "Keys ordered by most likely: " + ','.join(map(str, most_likely_keys))

    print "####################"


    # Take the guess for a key, try to decrypt
    while True:
        shift = int(raw_input("Enter key: "))
        shifted_letters = []
        for letter in CIPHER:
            shifted_letters.append(ALPHABET[(ALPHABET.index(letter) + shift) % 26])
        result = ''.join(shifted_letters)
        print result
        check_right = raw_input("Is this correct? ")
        if check_right.startswith("y"):
            print "Well done!"
            return 0

# Letters a-z
ALPHABET = ''.join(map(chr, range(ord('a'), ord('z')+1)))
# Frequencies taken from class (unknown original source)
LETTER_FREQS = [0.080,0.015,0.030,0.040,0.130,0.020,0.015,0.060,0.065,0.005,0.005,0.035,0.030,0.070,0.080,0.020,0.002,0.065,0.060,0.090,0.030,0.010,0.015,0.005,0.020,0.002]
# Ciphertext
f = open(sys.argv[1], 'r')
CIPHER = f.read().replace(' ', '').replace('\n', '').lower()
f.close()

solver()

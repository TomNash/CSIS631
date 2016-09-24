import sys
import operator
from itertools import cycle

def solver():
    caesar_sum = dict()
    for i in range(0, len(ALPHABET)):
        chi_sq = 0.0
        cipher_shift = ''.join(map(chr, [(ord(x)+i) % 97 % 26 + 97 for x in CIPHER]))
        for j in range(0, len(ALPHABET)):
            letter = ALPHABET[j]
            chi_sq += (cipher_shift.count(letter) - len(CIPHER)*LETTER_FREQS[j])**2 / (len(CIPHER)*LETTER_FREQS[j])
        caesar_sum[i] = chi_sq
    sorted_chi_sq = sorted(caesar_sum.items(), key=operator.itemgetter(1))
    possible_chars = [solution[0] for solution in sorted_chi_sq]
    letters = [ALPHABET[x] for x in possible_chars]
    print "Keys ordered by most likely: " + ", ".join(letters)
        
    print "####################"

    while True:
        key = raw_input("Enter key: ")
        pairs = zip(CIPHER, cycle(key))
        result = ''
        for pair in pairs:
            total = reduce(lambda x, y: ALPHABET.index(x) + ALPHABET.index(y), pair)
            result += ALPHABET[total % 26]
        print result
        check_right = raw_input("Is this correct? ")
        if check_right.startswith("y"):
            print "Well done!"
            return 0


ALPHABET = map(chr, range(ord('a'), ord('z')+1))
LETTER_FREQS = [x / 100.0 for x in [8.167, 1.492, 2.782, 4.253, 12.702, 2.228,
                2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507,
                1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150,
                1.974, 0.074]]

f = open(sys.argv[1], 'r')
CIPHER = f.read().replace(' ', '').replace('\n', '').lower()
f.close()

solver()

import sys
import numpy
import operator
import collections
from itertools import islice
from itertools import cycle

def window(seq, n=2):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result    
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def solver():
    print "####################"
    sequences_list = []
    chi_sq_sums = dict()
    period_lengths = range(1, 15)

    for period in period_lengths:
        sequences = [""] * period
        for i in range(0, len(CIPHER), period):
            for j in range(0, period):
                if i+j < len(CIPHER):
                    sequences[j] += CIPHER[i+j]
        average_ic = 0.0
        for sequence in sequences:
            n = len(sequence)
            freqs = collections.Counter(sequence)
            freqsum = 0.0
            for letter in ALPHABET:
                freqsum += freqs[letter] * (freqs[letter]-1)
            average_ic += freqsum / (n*(n-1))
        sequences_list.append(sequences)
        chi_sq_sums[period] = average_ic/len(sequences)
    sorted_chi_sq_sums = sorted(chi_sq_sums.items(), key=operator.itemgetter(1), reverse=True)

    for i in range(0, 14):
        print "Key of length " + str(sorted_chi_sq_sums[i][0]) + ": " + str(sorted_chi_sq_sums[i][1]) + (" <--- most likely" if i == 0 else "")

    print "####################"
    use_period = int(raw_input("Use period length: "))
    sequences = sequences_list[use_period-1]

    pos = 0
    for sequence in sequences:
        caesar_sum = dict()
        for i in range(0, len(ALPHABET)):
            chi_sq = 0.0
            sequence_shift = ''.join(map(chr, [(ord(x)+i) % 97 % 26 + 97 for x in sequence]))
            shift_key = abs(i-26) if abs(i-26) != 26 else 0
            for j in range(0, len(ALPHABET)):
                letter = ALPHABET[j]
                chi_sq += (sequence_shift.count(letter) - len(sequence)*LETTER_FREQS[j])**2 / (len(sequence)*LETTER_FREQS[j])
            caesar_sum[shift_key] = chi_sq
        sorted_chi_sq = sorted(caesar_sum.items(), key=operator.itemgetter(1))
        pos += 1
        possible_chars = [solution[0] for solution in sorted_chi_sq[0:3]]
        letters = [ALPHABET[x] for x in possible_chars]
        print "Key letter " + str(pos) + " top 3 guesses: " + ", ".join(letters)
        
    print "####################"

    while True:
        key = raw_input("Enter key: ")
        pairs = zip(CIPHER, cycle(key))
        result = ''
        for pair in pairs:
            total = reduce(lambda x, y: ALPHABET.index(x) - ALPHABET.index(y), pair)
            result += ALPHABET[total % 26]
        print result
        check_right = raw_input("Is this correct? ")
        if check_right.startswith("y"):
            print "Well done!"
            return 0
        else:
            check_new_period = raw_input("Try new period? ")
            if check_new_period.startswith("y"):
                solver()	
            else:
                print "Try again.",

ALPHABET = map(chr, range(ord('a'), ord('z')+1))
LETTER_FREQS = [x / 100.0 for x in [8.167, 1.492, 2.782, 4.253, 12.702, 2.228,
                2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507,
                1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150,
                1.974, 0.074]]

f = open(sys.argv[1], 'r')
CIPHER = f.read().replace(' ', '').replace('\n', '').lower()
f.close()

print "Replicated n-length substrings and distances between them:"
for i in range(2, 15):						
    chunks = [''.join(ele) for ele in list(window(CIPHER, n=i))]
    for substring in [item for item, count in collections.Counter(chunks).items() if count > 1]:
        indices = [i for i, x in enumerate(chunks) if x == substring]
        for j in range(0, len(indices)-1):
            print str(substring) + ": " +  str(indices[j+1]-indices[j])

solver()

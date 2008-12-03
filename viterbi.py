import re

def normalize(word):
    "Put word in standard form to avoid trivial mismatches."
    return re.sub(r'[^a-z]+', '', word.lower())

def read_dictionary(file):
    "Return a map from words to their costs."
    costs = {}
    for line in file:
        coststr, word = line.split()
        word = normalize(word)
        # TODO: compute combined cost, not min
        costs[word] = min(float(coststr), costs.get(word, 1000.0))
    return costs

dictionary = read_dictionary(open('freqlist2.txt'))
max_word_length = max(len(w) for w in dictionary)

def try_to_split(wordsruntogether):
    sequence, score = viterbi_segment(wordsruntogether.lower())
    return [sequence]

def viterbi_segment(text):
    "Find the best segmentation of the string of characters."
    # Adapted from Russell & Norvig, AIMA.
    # best[i] = best cost for text[0:i]
    # words[i] = best word ending at position i
    n = len(text)
    words = [''] + list(text)
    best = [0.0] + [1.e3] * n
    ## Fill in the vectors best, words via dynamic programming
    for i in range(n + 1):
        for j in range(max(0, i - max_word_length), i):
            w = text[j:i]
            cost = compute_wordcost(w)
            if cost + best[i - len(w)] <= best[i]:
                best[i] = cost + best[i - len(w)]
                words[i] = w
    ## Now recover the sequence of best words
    sequence = []; i = n
    while 0 < i:
        sequence.append(words[i])
        i -= len(words[i])
    sequence.reverse()
    ## Return best word-sequence and its cost
    return sequence, best[-1]

def compute_wordcost(word):
    try:
        return dictionary[word]
    except KeyError:
        if word.isdigit():
            return 10
        elif any(letter.isdigit() for letter in word):
            return 1e6
        else:
            # TODO: use n-gram frequencies
            return 10 + 2.4 * len(word)

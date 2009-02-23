import re

def try_to_split(wordsruntogether):
    """Return a list of words that could have been smushed to make
    wordsruntogether."""
    words, cost = viterbi_segment(wordsruntogether.lower())
    return words

def viterbi_segment(text):
    "Return the lowest-cost segmentation of the text, and its cost."
    # Adapted from Russell & Norvig, AIMA.
    # The best segmentation of text[:i] will have cost costs[i] and
    # last word text[lasts[i]:i]. Fill them in by dynamic programming:
    costs, lasts = [0.0], [0]
    for i in range(1, len(text) + 1):
        cost_k, k = min((costs[j] + word_cost(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        costs.append(cost_k)
        lasts.append(k)
    # Trace back the words of the best segmentation:
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words, costs[-1]


# The unigram cost model.
# Cost for known words is proportional to -log(word_frequency).
# For others, we try to stay roughly consistent.

def word_cost(word):
    if word in dictionary:
        return dictionary[word]
    if word.isalpha() or all(letter.isalpha() or 128 <= ord(letter)
                             for letter in word):
        # TODO: use n-gram frequencies
#       return 10 + letter_cost * len(word)
        # XXX these numbers are still kind of fucked:
        #  e.g. mm f -> mmf, jan -> j an
        #       heb -> he b
        #       sonyh1 -> so nyh 1
        return per_word_cost + letter_cost * len(word)
    if any(letter.isalpha() for letter in word):
        return 1e6
    if word.isdigit():
        return 10
    if any(letter.isdigit() for letter in word):
        return 1e6
    return 10


## The dictionary

def read_dictionary(file):
    "Return a map from words to their costs."
    costs = {}
    for line in file:
        coststr, word = line.split()
        word = normalize(word)
        # TODO: compute combined cost, not min
        costs[word] = min(float(coststr), costs.get(word, 1000.0))
    return costs

def normalize(word):
    "Put word in standard form to avoid trivial mismatches."
    return re.sub(r'[^a-z]+', '', word.lower())

dictionary = read_dictionary(open('freqlist.txt'))
max_word_length = max(map(len, dictionary))


# A letter-cost just a bit under the cost of the most common 1-letter
# word, to keep word-jumbles from getting split wherever they happen
# to have an 'a', etc.
#letter_cost = dictionary['a'] - 0.06093
letter_cost = dictionary['a'] - 0.01

per_word_cost = max(dictionary.values())
#print per_word_cost, letter_cost

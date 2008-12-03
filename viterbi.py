import re

def try_to_split(wordsruntogether):
    """Return a list of just one segmentation.
    A segmentation satisfies ''.join(segmentation) == wordsruntogether."""
    sequence, cost = viterbi_segment(wordsruntogether.lower())
    return [sequence]

def viterbi_segment(text):
    "Return the best segmentation of the text, and its cost."
    # Adapted from Russell & Norvig, AIMA.
    # costs[i] = best cost for text[0:i]
    # words[i] = best word ending at position i
    costs, words = [0.0], ['']
    # Fill in costs and words via dynamic programming.
    for i in range(1, len(text) + 1):
        cost, word = min((costs[j] + compute_wordcost(text[j:i]), text[j:i])
                         for j in range(max(0, i - max_word_length), i))
        costs.append(cost)
        words.append(word)
    # Trace back the lowest-cost sequence of words.
    sequence = []
    i = len(text)
    while 0 < i:
        sequence.append(words[i])
        i -= len(words[i])
    sequence.reverse()
    return sequence, costs[-1]


# The unigram cost model.
# Cost for known words is proportional to -log(word_frequency).
# For others, we try to stay roughly consistent.

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
max_word_length = max(len(w) for w in dictionary)


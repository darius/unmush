"""
Find the most probable split of wordsruntogether into words.
"""

import heapq

def normalize(word):
    "Put word in standard form to avoid trivial mismatches."
    return word.lower()         # TODO: strip punctuation

def read_dictionary(file):
    "Return a map from words to their costs."
    costs = {}
    for line in file:
        coststr, word = line.split()
        word = normalize(word)
        # TODO: compute combined cost, not min
        costs[word] = min(float(coststr), costs.get(word, 1000.0))
    return costs

dictionary = read_dictionary(open('freqlist.txt'))

call_count = 0

def try_to_split(wordsruntogether, limit=5):
    global call_count, table, cache
    call_count += 1
    if call_count % 10000 == 0:
        table = {}
        cache = {}
    # TODO: when normalize() strips punctuation, don't necessarily do
    #   that here; try splitting on it first
    s = normalize(wordsruntogether)
    if not s:
        return [[wordsruntogether]]
    splits = really_try_to_split(s, limit)
    if splits: return [words for score, words in splits]
    return [[wordsruntogether]]

# table[string] is to hold a list of the best splits of string
table = {}

def really_try_to_split(s, limit):
    try:
        return table[s]
    except KeyError:
        c = compute_really_try_to_split(s, limit)
        table[s] = c
        return c

def compute_really_try_to_split(s, limit):
    """Return a list of some ways to split s into separate
    words, in order of decreasing probability. Judge probability using the
    dictionary."""
    n = len(s)
    if n == 1:
        return [(wordcost(s), (s,))]
    candidates = []
    for i in range(max(1, (n - limit) // 2),
                   min(n, (n + limit) // 2)):
        candidates.extend(combine(really_try_to_split(s[:i], limit),
                                  really_try_to_split(s[i:], limit)))
    return winnow(candidates)

def combine(splitsL, splitsR):
    return winnow(combine_cross(splitsL, splitsR))

def combine_cross(splitsL, splitsR):
    # TODO: add a small penalty for each space introduced -- I guess?
    for costL, wordsL in splitsL:
        for costR, wordsR in splitsR:
            if wordsL and wordsR:
                w = wordsL[-1] + wordsR[0]
                yield ((costL - wordcost(wordsL[-1])
                        + wordcost(w)
                        - wordcost(wordsR[0]) + costR),
                       wordsL[:-1] + (w,) + wordsR[1:])
                if not w.isdigit():
                    yield costL + costR, wordsL + wordsR
            else:
                yield costL + costR, wordsL + wordsR

def winnow(splits):
    return heapq.nsmallest(4, set(splits))

cache = {}

def wordcost(word):
    try:
        return cache[word]
    except KeyError:
        c = compute_wordcost(word)
        cache[word] = c
        return c

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


if __name__ == '__main__':
    import sys
    for line in sys.stdin: #open('all_tags'):
        tag = line.rstrip('\n')
        splits = try_to_split(tag)
        print tag, ' '.join(splits[0])

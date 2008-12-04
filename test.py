import viterbi as splitter

import sys
import time

stem = 'evaluate/dev'

def readlines(file):
    return open(file).read().split('\n')

source = readlines(stem + '.sample')
wanted = readlines(stem + '.ref')

resultsfile = open('%s.%s.out' % (stem, splitter.__name__), 'w')
start = time.time()
results = []
for tag in source:
    splits = splitter.try_to_split(tag)
    result = ' '.join(splits[0])
    resultsfile.write(result + '\n')
    results.append(result)
end = time.time()
resultsfile.close()

evalfile = open('%s.%s.eval' % (stem, splitter.__name__), 'w')
n_errors = 0
for result, good in zip(results, wanted):
    if result != good:
        n_errors += 1
        evalfile.write(good + '\n')
        evalfile.write(result + '\n')
        evalfile.write('\n')

evalfile.write('# errors: %d\n' % n_errors)
evalfile.write('Speed: %g tags/sec\n' % (len(wanted) / (end - start)))
evalfile.close()

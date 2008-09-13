"""
Create a random sample of N of the tags from stdin.
Chosen tags to stdout, unchosen ones to stderr.
"""

import random
import sys

N = 400

tags = [line.rstrip('\n') for line in sys.stdin]

chosen = random.sample(tags, N)

for choice in sorted(chosen):
    print choice

for omitted in sorted(set(tags) - set(chosen)):
    sys.stderr.write(omitted + '\n')

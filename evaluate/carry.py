"""
Carry over the full.ref reference data to a subsample of full.sample.
"""

import sys

tags = [line.rstrip('\n') for line in open('full.sample')]
refs = [line.rstrip('\n') for line in open('full.ref')]
reftable = dict(zip(tags, refs))

for line in sys.stdin:
    tag = line.rstrip('\n')
    print reftable[tag]

#!/usr/bin/env python

import numpy as np
import itertools

R = [
    (0, 1),
    (1, 2),
    (2, 3),
]

S = [
    (0, 1),
    (1, 2),
    (2, 3),
]

def hash_join(R, S):
    h = {}
    for a, b in R:
        h.setdefault(b, []).append(a)

    j = []
    for b, c in S:
        if not h.has_key(b):
            continue
        for r in h[b]:
            j.append( (r, b, c) )

    return j

def mr(R, S):
    m = []
    for a, b in R:
        m.append( (b, ('R', a)) )
    for b, c in S:
        m.append( (b, ('S', c)) )

    m = sorted(m, key=lambda x:x[0])

    r = []
    for key, vals in itertools.groupby(m, key=lambda x:x[0]):
        vals = [x[1] for x in vals]
        print key, vals
        rs = [x for x in vals if x[0] == 'R']
        ss = [x for x in vals if x[0] == 'S']
        for ri in rs:
            for si in ss:
                r.append( (ri[1], key, si[1]) )
    return r

print hash_join(R, S)
print mr(R, S)
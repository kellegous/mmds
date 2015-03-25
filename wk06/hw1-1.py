#!/usr/bin/env python

import numpy as np
import itertools

M = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
])

v = np.array([1, 2, 3, 4])

def mr(M, v):
    t = []
    mr, mc = M.shape
    for i in range(mc):
        for j in range(mr):
            t.append((i, M[i, j] * v[j]))

    t = sorted(t, key=lambda x:x[0])
    for x in t:
        print (x[0]+1, x[1])

    r = np.zeros((mr, 1))
    for key, vals in itertools.groupby(t, key=lambda x:x[0]):
        vals = [x[1] for x in vals]
        r[key] = sum(vals)
        print '%s, %s' % (key, sum(vals))
    return r.transpose()

print np.dot(M, v.transpose())
print mr(M, v)
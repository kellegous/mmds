#!/usr/bin/env python

import numpy as np
import itertools

M = np.array([
    [1, 2, 3],
    [4, 5, 6],
])

N = np.array([
    [20, 30, 30, 40, 50],
    [60, 70, 80, 90, 21],
    [31, 41, 51, 61, 71],
])

# x = 2
# y = 3
# z = 5

# x + z = 7, got 7 YES
# x + z = 7, got 3 NO 
# z = 5, got 30 NO
# x+z = 7, got 30 NO

def mr(M, N):
    m1 = []
    mr, mc = M.shape
    nr, nc = N.shape

    # map 1
    for i in range(mr):
        for j in range(mc):
            m1.append( (j, ('M', i, M[i,j])) )

    for j in range(nr):
        for k in range(nc):
            m1.append( (j, ('N', k, N[j,k])) )

    m1 = sorted(m1, key=lambda x:x[0])

    # reduce 1
    r1 = []
    for key, vals in itertools.groupby(m1, key=lambda x:x[0]):
        vals = [x[1] for x in vals]
        print len(vals)
        ms = [x for x in vals if x[0] == 'M']
        ns = [x for x in vals if x[0] == 'N']
        for m in ms:
            for n in ns:
                r1.append( ((m[1], n[1]), m[2]*n[2]) )

    m2 = r1[:]
    print len(m2)
    m2 = sorted(m2, key=lambda x:x[0])

    r = np.zeros((mr, nc))
    for key, vals in itertools.groupby(m2, key=lambda x:x[0]):
        vals = [x[1] for x in vals]
        print len(vals)
        r[key[0], key[1]] = sum(vals)
    return r


print np.dot(M, N)
print mr(M,N)
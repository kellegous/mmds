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

def mr(M, N):
    t = []
    mr, mc = M.shape
    nr, nc = N.shape

    for i in range(mr):
        for j in range(mc):
            l = [ ((i, k), ('M', j, M[i,j])) for k in range(nc) ]
            print len(l)
            t.extend(l)
            # for k in range(nc):
            #   t.append( ((i, k), ('M', j, M[i,j])) )

    for j in range(nr):
        for k in range(nc):
            l = [ ((i, k), ('N', j, N[j, k])) for i in range(mr) ]
            print len(l)
            t.extend(l)
            # for i in range(mr):
            #   t.append( ((i, k), ('N', j, N[j, k])) )

    t = sorted(t, key=lambda x:x[0])
    print len(t)

    r = np.zeros((mr, nc))  
    #reduce
    for key, vals in itertools.groupby(t, key=lambda x:x[0]):
        vals = [x[1] for x in vals]
        print 'reducer %s has %d tuples' % (key, len(vals))
        a = sorted([x for x in vals if x[0] == 'M'], key=lambda x:x[1])
        b = sorted([x for x in vals if x[0] == 'N'], key=lambda x:x[1])

        v = zip([x[2] for x in a], [x[2] for x in b])
        if len(v) == 0:
            continue

        i, j = key
        r[i, j] = sum([k*v for k,v in v])
    return r

print np.dot(M, N)
print mr(M, N)
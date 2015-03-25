#!/usr/bin/env python

import os
import sys
import math
import numpy as np

P = [
    ((5, 4), 1),
    ((8, 3), 1),
    ((3, 3), -1),
    ((7, 2), -1),
]

def dist_to_line(pl0, pl1, p):
    dx, dy = pl1[0] - pl0[0], pl1[1] - pl0[1]
    a = abs((pl1[1] - pl0[1]) * p[0] - (pl1[0] - pl0[0]) * p[1] + pl1[0]*pl0[1] - pl0[0]*pl1[1])
    return a / math.sqrt(dx*dx + dy*dy)

def closest_to(L, pts):
    dist = [dist_to_line(L[0][0], L[1][0], x[0]) for x in pts]
    ix = np.argmin(dist)
    return pts[ix], dist[ix]

def solve(A, B):
    # find the point in B closest to the line through both points in A
    p, d = closest_to(A, B)

    M = np.hstack((
        np.array([list(x[0]) for x in A] + [list(p[0])]),
        np.ones((3, 1))))
    b = np.array([x[1] for x in A] + [p[1]])
    x = np.linalg.solve(M, b)
    return x, d

# just try to solve this with a parallel line to both classes
S = [
    solve([a for a in P if a[1] == 1], [a for a in P if a [1] == -1]),
    solve([a for a in P if a[1] == -1], [a for a in P if a [1] == 1]),
]

# which one would give us the largest margin?
ix = np.argmax([x[1] for x in S])
x = S[ix][0]
print 'm0 = %0.2f' % x[0]
print 'm1 = %0.2f' % x[1]
print ' b = %0.2f' % x[2]

#!/usr/bin/env python

import math
import numpy as np

rps = [
    (0, 0, 'x'),
    (10, 10, 'y')
]

pts = [
    (1, 6, 'a'),
    (3, 7, 'b'),
    (4, 3, 'c'),
    (7, 7, 'd'),
    (8, 2, 'e'),
    (9, 5, 'f')
]

nms = ['a', 'b', 'c', 'd', 'e', 'f']

def l2(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    return math.sqrt(dx*dx + dy*dy)

def find_max(reps, pts):
    return np.argmax([ min([l2(p, x) for x in reps]) for p in pts])

for i in range(0, 5):
    ix = find_max(rps, pts)
    rps.append(pts.pop(ix))

for i, p in enumerate(rps[2:]):
    print '%d: %s' % (i, p[2])

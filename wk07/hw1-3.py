#!/usr/bin/env python

import numpy as np
import os
import sys

L = np.array([
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [0, 0, 1, 0],
]).transpose()

def normalize(v):
    return v / np.max(v)

h = np.array([[1.0, 1.0, 1.0, 1.0]]).transpose()

for i in range(2):
    a = normalize(np.dot(L.transpose(), h))
    print a
    h = normalize(np.dot(L, a))
    print h

# print '%0.6f | %0.6f' % (a[1], 3.0 / 5.0)
# print '%0.6f | %0.6f' % (h[2], 1.0)
# print '%0.6f | %0.6f' % (a[1], 1.0 / 8.0)
# print '%0.6f | %0.6f' % (h[0], 1.0 / 5.0)

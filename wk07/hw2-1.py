#!/usr/bin/env python

import numpy as np

A = np.array([
    [ 0.0, 0.5, 0.5, 0.0 ],
    [ 1.0, 0.0, 0.0, 0.0 ],
    [ 0.0, 0.0, 0.0, 1.0 ],
    [ 0.0, 0.0, 1.0, 0.0 ],
]).transpose()

w = 1.0/3.0

B = np.array([
    [2*w, 2*w, 2*w, 2*w],
    [w, w, w, w],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

beta = 0.7

r = np.ones((A.shape[0], 1)) / A.shape[0]

for i in range(100):
    r = beta * np.dot(A, r) + (1 - beta)*np.dot(B, r)
    print r

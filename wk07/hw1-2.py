#!/usr/bin/env python

import numpy as np
import os
import sys

strs = {
    's1' : 'abcef',
    's2' : 'acdeg',
    's3' : 'bcdefg',
    's4' : 'adfg',
    's5' : 'bcdfgh',
    's6' : 'bceg',
    's7' : 'cdfg',
    's8' : 'abcd',
}

def index(vals, J):
    idx = {}
    for val in vals:
        n = int(np.floor(J * len(val) + 1))
        for i in range(n):
            idx.setdefault(val[i:i+1], []).append(val)
    return idx

def search(idx, J, str):
    r = []
    n = int(np.floor(J * len(str) + 1))
    for i in range(n):
        r.extend(idx[str[i:i+1]])
    return r

idx = index(strs.values(), 0.2)
for v in ['s1', 's3', 's6']:
    val = strs[v]
    res = [x for x in search(idx, 0.2, val) if x != val]
    print '%s: %d (%d)' % (v, len(res), len(set(res)))
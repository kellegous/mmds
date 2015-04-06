#!/usr/bin/env python

import Levenshtein
import numpy as np
import os
import sys

def lcs(a, b):
  lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
  # row 0 and column 0 are initialized to 0 already
  for i, x in enumerate(a):
    for j, y in enumerate(b):
      if x == y:
        lengths[i+1][j+1] = lengths[i][j] + 1
      else:
        lengths[i+1][j+1] = \
            max(lengths[i+1][j], lengths[i][j+1])
# read the substring out from the matrix
  result = ""
  x, y = len(a), len(b)
  while x != 0 and y != 0:
    if lengths[x][y] == lengths[x-1][y]:
      x -= 1
    elif lengths[x][y] == lengths[x][y-1]:
      y -= 1
    else:
      assert a[x-1] == b[y-1]
      result = a[x-1] + result
      x -= 1
      y -= 1
  return result

words = ['he', 'she', 'his', 'hers']
n = len(words)

pairs = set()
for a in words:
  for b in words:
    if a != b:
      pairs.add(tuple(sorted([a, b])))

def dist(a, b):
  x = len(lcs(a, b))
  return (len(a) - x) + (len(b) - x)

for a, b in pairs:
  print '%s, %s => %d' % (a, b, dist(a, b))
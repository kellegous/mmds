#!/usr/bin/env python

import numpy as np
import random
import os
import sys
import pprint

random.seed(420)

class LHash(object):
  def __init__(self, fn):
    self._fn = fn

  def hash(self, x):
    return self._fn(x)

class MHash(object):
  def __init__(self, n):
    self._a = random.randint(1, 0xffff)
    self._b = random.randint(0, 0xffff)
    self._c = n

  def hash(self, x):
    return (self._a * x + self._b) % self._c

class Hash(object):
  """ simple tabulation hash """
  def __init__(self):
    self._tab = np.random.randint(0x0, 0xf, (8, 16))

  def hash(self, x):
    h = 0
    for i in range(0, 8):
      h ^= self._tab[i][(x>>(i*4)) & 0xf]
    return h

def jaccard_sim(a, b):
  return float(len(a.intersection(b))) / float(len(a.union(b)))

def minhash(M, hashes):
  nr, nc = M.shape
  nh = len(hashes)

  H = np.ones((nh, nc)) * 1e23
  for r in range(0, nr):
    hv = [h.hash(r+1) for h in hashes]
    for c in range(0, nc):
      if M[r, c]:
        for i in range(0, nh):
          if hv[i] < H[i, c]:
            H[i, c] = hv[i]
  return H

def hw_hash(x):
  # R4, R6, R1, R3, R5, R2
  v = [3, 5, 0, 2, 4, 1]
  return v[x-1]

M = np.array([
  [0, 1, 1, 0],
  [1, 0, 1, 1],
  [0, 1, 0, 1],
  [0, 0, 1, 0],
  [1, 0, 1, 0],
  [0, 1, 0, 0]
])

print M

print minhash(M, [LHash(lambda x:hw_hash(x))])
# nsyms = 10
# ndocs = 5

# docs = [set([random.randint(0, nsyms - 1) for j in range(0, nsyms)]) for i in range(0, ndocs)]

# M = np.zeros((nsyms, ndocs), dtype='bool')
# for i in range(0, ndocs):
#   for j in docs[i]:
#     M[j, i] = True

# Sa = np.zeros((ndocs, ndocs))
# for i in range(0, ndocs):
#   for j in range(0, ndocs):
#     Sa[i,j] = jaccard_sim(docs[i], docs[j])

# # hashes = [Hash() for i in range(0, 6)]
# hashes = [MHash(10) for i in range(0, 6)]
# H = minhash(M, hashes)
# Sb = np.zeros((ndocs, ndocs))
# for i in range(0, ndocs):
#   for j in range(0, ndocs):
#     # S[i,j] = jaccard_sim(set(H[:, i]), set(H[:, j]))
#     Sb[i, j] = np.sum(H[:, i] == H[:, j]) / float(H.shape[0])

# print Sa - Sb
# hashes = [
#   LHash(lambda x:x%5),
#   LHash(lambda x:(2*x + 1) % 5)
# ]

# M = np.array([
#   [1, 0],
#   [0, 1],
#   [1, 1],
#   [1, 0],
#   [0, 1]
# ], dtype='bool')

# print minhash(M, hashes)
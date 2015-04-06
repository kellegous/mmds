#!/usr/bin/env python

import os
import sys

def f(S):
  M = 1000000
  return ((31.0/32.0)*S*S - 3*M*S) / 3*M


# S = 500,000,000; P = 10,000,000,000
# S = 500,000,000; P = 5,000,000,000
# S = 200,000,000; P = 1,600,000,000
# S = 100,000,000; P = 540,000,000

S = [
  500000000/4,
  500000000/4,
  200000000/4,
  100000000/4
]

P = [
  10000000000,
  5000000000,
  1600000000,
  540000000
]

def pct(e, a):
  return 100 * (abs(e - a) / float(a))

for p, s in zip(P, S):
  M = 1e6
  Ta = 3.0*M*(1 + (p/s))
  Tb = (31.0/32.0) * s
  print '(%d, %d)' % (p, s*4)
  print '%d %d %s' % (Ta, Tb, pct(Ta, Tb))
  # print '%d %d' % ()
  # pp = f(s)
  # print '%d %d %d %s' % (s, p, pp, pct(p, pp))


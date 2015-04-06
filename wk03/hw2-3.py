#!/usr/bin/env python

import pprint
import json
import os
import sys

def surprise(seq):
  his = {}
  for n in seq:
    his[n] = his.get(n, 0) + 1
  pprint.pprint(his)
  return sum([v*v for k,v in his.items()])

ams = [
  [5, 33, 67],
  [31, 48, 50],
  [9, 50, 68],
  [22, 42, 62],
]

def median(v):
  return sorted(v)[len(v)>>1]

def estimate(r, s):
  v = [sum([v == s[x-1] and p>=(x-1) for p, v in enumerate(s)]) for x in r]
  return [len(s) * (2*m - 1) for m in v]

def main():
  s = [(i % 10) + 1 for i in range(0, 75)]

  print surprise(s)

  for a in ams:
    print '%s => %d' % (json.dumps(a), median(estimate(a, s)))

  return 0

if __name__ == '__main__':
  sys.exit(main())
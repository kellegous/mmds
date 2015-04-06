#!/usr/bin/env python

import numpy as np

def l1(a, b):
  return np.sum(np.abs(b - a))

def l2(a, b):
  d = b - a
  return np.sqrt(np.sum(d*d))

tgs = [
  (0, 0),
  (100, 40),
]

tgs = [np.array(x) for x in tgs]

pts = [
  (51,18),
  (53,18),
  (53,10),
  (52,13),
]

pts = [np.array(x) for x in pts]

for pt in pts:
  d1 = [l1(pt, tg) for tg in tgs]
  d2 = [l2(pt, tg) for tg in tgs]
  print '%s => %d %d %s %s' % (pt, np.argmin(d1), np.argmin(d2), d1, d2)
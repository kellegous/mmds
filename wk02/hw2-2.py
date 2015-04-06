#!/usr/bin/env python

items = range(1, 101)

def basket(j):
  return set([i for i in items if j%i ==0])

basks = [(j, basket(j)) for j in range(1, 101)]

cands = [
  [2, 3, 5, 45],
  [8, 10, 20],
  [8, 12, 96],
  [1, 2, 4]
]

def check(cand, basks):
  l, r = set(c[:-1]), set([c[-1]])
  count = 0
  for j, b in basks:
    if b.intersection(l) == l:
      count += 1
      if b.intersection(r) != r:
        return False
  return count > 0

for c in cands:
  if check(c, basks):
    print c
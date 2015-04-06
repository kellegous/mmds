#!/usr/bin/env python

import json
import sys
import os

streams = [
  [1, 3, 6, 8],
  [4, 6, 9, 10],
  [3, 4, 8, 10],
  [1, 6, 7, 10],
]

def h(x):
  return (3*x + 7) % 11

def c(x):
  m = [0xf, 0x7, 0x3, 0x1]
  for i in range(0, 4):
    if m[i] & x == 0:
      return 4-i
  return 0

def main():
  for stream in streams:
    r = max([c(h(x)) for x in stream])
    print '%s = %d' % (json.dumps(stream), r*r)

if __name__ == '__main__':
  sys.exit(main())
#!/usr/bin/env python

import numpy as np
import random
import os
import optparse
import sys

def randsym():
  return chr(random.randint(ord('A'), ord('Z')))

def gen_basket(n=10):
  rn = random.randint(0, n)
  return set([randsym() for x in range(0, n)])

def main():
  parser = optparse.OptionParser()
  parser.add_option('-n', '--n', dest='n', default=10000, type='int', help='')
  parser.add_option('-l', '--len', dest='l', default=10, type='int', help='')
  opt, args = parser.parse_args()
  for i in range(opt.n):
    print ''.join(sorted(list(gen_basket(opt.l))))

if __name__ == '__main__':
  sys.exit(main())
#!/usr/bin/env python

A = 'ABRACADABRA'
B = 'BRICABRAC'

def shingles_of(s):
  return set([s[i:i+2] for i in range(0, len(s) - 1)])

def jac_sim(a, b):
  return float(len(a.intersection(b))) / float(len(a.union(b)))

SA = shingles_of(A)
SB = shingles_of(B)

print 'How many 2-shingles does ABRACADABRA have?'
print len(SA)

print 'How many 2-shingles does BRICABRAC have?'
print len(SB)

print 'How many 2-shingles do they have in common?'
print len(SB.intersection(SA))

print 'What is the Jaccard similarity between the two documents"?'
print jac_sim(SA, SB)
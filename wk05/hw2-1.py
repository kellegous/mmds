#!/usr/bin/env python

from lib import *

pts = [
	(28, 145, 'y'),
	(65, 140, 'y'),
	(50, 130, 'y'),
	(25, 125, 'g'),
	(38, 115, 'y'),
	(55, 118, 'y'),
	(44, 105, 'g'),
	(29, 97, 'g'),
	(50, 90, 'y'),
	(63, 88, 'y'),
	(43, 83, 'y'),
	(35, 63, 'g'),
	(55, 63, 'g'),
	(42, 57, 'g'),
	(50, 60, 'y'),
	(23, 40, 'g'),
	(64, 37, 'g'),
	(50, 30, 'y'),
	(33, 22, 'g'),
	(55, 20, 'g')
]


cts = [p for p in pts if p[2] == 'g']

print 'Assigning'
a0 = assign(cts, pts)
for a in a0:
	print a

print 'Averaging'
cts = [average(x) for x in a0]
for c in cts:
	print c

print 'Assigning'
a1 = assign(cts, pts)
for a in a1:
	print a



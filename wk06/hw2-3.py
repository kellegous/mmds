#!/usr/bin/env python

A = 0
S = 1

pos = [
	(28,145),
	(38,115),
	(43,83),
	(50,130),
	(50,90),
	(50,60),
	(50,30),
	(55,118),
	(63,88),
	(65,140),
]

neg = [
	(23,40),
	(25,125),
	(29,97),
	(33,22),
	(35,63),
	(42,57),
	(44, 105),
	(55,63),
	(55,20),
	(64,37),
]

def classify(p):
	if p[A] < 45:
		return p[S] >= 110
	else:
		return p[S] >= 75

e = [p for p, v in zip(pos, [classify(x) for x in pos]) if not v] + \
	[p for p, v in zip(neg, [classify(x) for x in neg]) if v]
print e
# print [classify(x) for x in pos]
# print [classify(x) for x in neg]
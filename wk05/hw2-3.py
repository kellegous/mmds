#!/usr/bin/env python

def maxbudget(bidders):
	s = sorted(bidders, key=lambda x:-x[2])
	return [x for x in s if x[2] == s[0][2]]

def sim(qs, bidders, tie=0):
	R = 0
	for q in qs:
		sel = [b for b in bidders if b[1].find(q) >= 0 and b[2] > 0]
		if len(sel) == 0:
			continue
		sel = maxbudget(sel)
		if len(sel) > 1:
			s = sel[tie]
		else:
			s = sel[0]
		R += 1
		s[2] -= 1
	return R


#for sol in ['xyyx', 'xyyz', 'xyzx', 'zxyy']:
for sol in ['xxxy', 'xzyz', 'xyyx', 'xyzx']:
	r = min(
		[sim(sol, [ ['A', 'xy', 2], ['B', 'xz', 2] ], t) for t in [0, 1]]
	)
	print '%s => %d' % (sol, r)

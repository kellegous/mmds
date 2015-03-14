
import math

def dist(a, b):
	dx, dy = b[0] - a[0], b[1] - a[1]
	return math.sqrt(dx*dx + dy*dy)

def closest_to(pts, pt):
	np = pts[0]
	nd = 1e10
	for p in pts:
		d = dist(pt, p)
		if d < nd:
			nd = d
			np = p
	return np

def assign(cts, pts):
	h = {}
	for c in cts:
		h[c] = []
	for p in pts:
		h[closest_to(cts, p)].append(p)
	return h.values()

def average(pts):
	n = float(len(pts))
	sx = sum([p[0] for p in pts])
	sy = sum([p[1] for p in pts])
	return (sx / n, sy / n)
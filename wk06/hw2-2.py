#!/usr/bin/env python

import numpy as np

pos = [
	(5, 10),
	(7, 10),
	(1, 8),
	(3, 8),
	(7, 8),
	(1, 6),
	(3, 6),
	(3, 4),
]

neg = [
	(5, 8),
	(5, 6),
	(7, 6),
	(1, 4),
	(5, 4),
	(7, 4),
	(1, 2),
	(3, 2),
]

C = [(x, 1) for x in pos] + [(x, -1) for x in neg]

m, b = np.array([-1, 1]), -2

d = np.dot(np.array([list(x[0]) for x in C]), m) + b
for i, m in enumerate(np.sign(d) == np.array([x[1] for x in C])):
	print "%s %d %0.2f" % (C[i][0], C[i][1], d[i])

#!/usr/bin/env python

import numpy as np

# A $.10    .015    .010    .005    $1
# B $.09    .016    .012    .006    $2
# C $.08    .017    .014    .007    $3
# D $.07    .018    .015    .008    $4
# E $.06    .019    .016    .010    $5

class Bid(object):
    def __init__(self, name, bid, budget, ctrs):
        self.name = name
        self.bid = bid
        self.budget = budget
        self.ctrs = ctrs

    def __str__(self):
        ctrs = "[%s]" % ', '.join([str(x) for x in self.ctrs])
        return "(%s, %0.2f, %d, %s)" % (self.name, self.bid, self.budget, ctrs)

bids = [
    Bid('A', 0.10, 1, [.015, .010, .005]),
    Bid('B', 0.09, 2, [.016, .012, .006]),
    Bid('C', 0.08, 3, [.017, .014, .007]),
    Bid('D', 0.07, 4, [.018, .015, .008]),
    Bid('E', 0.06, 5, [.019, .016, .010])
]

for x in range(101):
    print x
#!/usr/bin/env python

from lib import *

pts = [
    (5, 10),
    (20, 5)
]

def reps(a, b):
    return [a, b]
    w, h = b[0] - a[0], b[1] - a[1]
    return [
        a,
        (a[0] + w, a[1]),
        b,
        (a[0], a[1] + h)
    ]

sols = [
# Yellow: UL=(3,3) and LR=(10,1); Blue: UL=(13,10) and LR=(16,4)
    [
        reps((3, 3), (10, 1)),
        reps((13, 10), (16, 4))
    ],
# Yellow: UL=(3,3) and LR=(10,1); Blue: UL=(15,14) and LR=(20,10)
    [
        reps((3, 3), (10, 1)),
        reps((15, 14), (20, 10))
    ],
# Yellow: UL=(6,15) and LR=(13,7); Blue: UL=(16,19) and LR=(25,12)
    [
        reps((6, 15), (13, 7)),
        reps((16, 19), (25, 12))
    ],
# Yellow: UL=(7,12) and LR=(12,8); Blue: UL=(16,19) and LR=(25,12)
    [
        reps((7, 12), (12, 8)),
        reps((16, 19), (25, 12))
    ]
]

# sols = [
#   [
#       reps((7, 12), (12, 8)),
#       reps((16, 19), (25, 12))
#   ],
#   [
#       reps((6, 15), (13, 7)),
#       reps((16, 16), (18, 5))
#   ],
#   [
#       reps((3, 3), (10, 1)),
#       reps((15, 14), (20, 10))
#   ],
#   [
#       reps((7, 8), (12, 5)),
#       reps((13, 10), (16, 4))
#   ]
# ]

for s in sols:
    y, b = s
    print '%s' % ([closest_to(pts, x) for x in y])
    print '%s' % ([closest_to(pts, x) for x in b])
    print
# for s in sols:
#   smp = pts + s[0] + s[1]
#   cts = pts
#   for i in range(1):
#       cls = assign(cts, smp)
#       cts = [average(c) for c in cls]
#       smp = cls[0] + cls[1]

#   print set([pts[0]] + s[0])
#   print set(cls[0])

#   print set([pts[1]] + s[1])
#   print set(cls[1])
#   ok = set([pts[0]] + s[0]) == set(cls[0]) and set([pts[1]] + s[1]) == set(cls[1])
#   print ok
#   # for c in cls:
#   #   print c
#   # print ok
#   print
# cts = [(cent_for(*x[:2]), cent_for(*x[2:])) for x in rcts]
# for c in cts:
#   print c
#   for p in pts:
#       print '%s closest_to %s' % (p, closest_to(c, p))
#   print
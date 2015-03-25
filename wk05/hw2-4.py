#!/usr/bin/env python

S = [ 'AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH', 'AH', 'ADG', 'ADF' ]

def setup(S):
    S = [set([c for c in x]) for x in S]
    U = set()
    for s in S:
        U.update(s)
    return (S, U)


def dumb(S, U):
    s = []
    u = set()
    for e in S:
        u.update(e)
        s.append(e)
        if u == U:
            return s

def simple(S, U):
    s = []
    u = set()
    for e in S:
        if len(e - u) > 0:
            u.update(e)
            s.append(e)
            if u == U:
                return s

def largefirst(S, U):
    return simple(sorted(S, key=lambda x: -len(x)), U)

S, U = setup(S)
print len(dumb(S, U)) / 4.0
print len(simple(S, U)) / 4.0
print len(largefirst(S, U)) / 4.0
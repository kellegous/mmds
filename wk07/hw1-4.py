#!/usr/bin/env python

def f(k, x):
    return 4*(21 + k + 3*(x + (1 - x)*k))
print [f(k, x) for k, x in [(2, 0.5), (2, 0.75), (3, 0.75), (3, 0.5)]] 

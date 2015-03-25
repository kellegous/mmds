#!/usr/bin/env python

import numpy as np
import os
import sys

a = 0.6
b = 0.4

w = np.power(a, 3)
x = np.power(b, 3)

y = 1 - np.power(1 - a, 2)
z = 1 - np.power(1 - b, 2)


print 'w = %0.6f' % w
print 'x = %0.6f' % x
print 'y = %0.6f' % y
print 'z = %0.6f' % z
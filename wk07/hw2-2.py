#!/usr/bin/env python

import numpy as np
import math

beta = 0.85
a = 1.0/ (1 - np.power(beta, 3))
b = beta / (1.0 + beta + np.power(beta, 2))
c = beta / (1.0 + beta + np.power(beta, 2))
print 'a = %0.6f, b = %0.6f, c = %0.6f' % (a, b, c)
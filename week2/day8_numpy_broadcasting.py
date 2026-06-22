#26
print(sum(range(5),-1))
from numpy import *
print(sum(range(5),-1))

import numpy as np
#27
Z=np.array([1,2,3])
print(Z**Z)
print(2 << Z >> 2)
print(Z < -Z)
print(1j*Z)
print(Z/1/1)
# print(Z<Z>Z)

#28
# print(np.array(0) / np.array(0))
# print(np.array(0) // np.array(0))
# print(np.array([np.nan]).astype(int).astype(float))

#29 — How to round away from zero
Z = np.array([-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5])
print("29-Round away from zero:",np.copysign(np.ceil(np.abs(Z)), Z))   #np.ceil always rounds up (toward +∞), so we take absolute value first, ceil it, then restore the original sign with np.copysign

#30
Z1 = np.random.randint(0,10,10)
Z2 = np.random.randint(0,10,10)
print("Z1:",Z1)
print("Z2:",Z2)
print("30-Intersection of Z1 and Z2:",np.intersect1d(Z1,Z2))   

#31 — Ignoring all numpy warnings
defaults = np.seterr(all="ignore")   # suppress warnings
print("31-Ignoring numpy warnings:",np.ones(1) / 0) 
np.seterr(**defaults)          
print("31-Restoring numpy warnings:",np.ones(1) / 0)  

#32
# print(np.sqrt(-1) == np.emath.sqrt(-1)) # np.sqrt(-1) returns nan (real domain only). np.emath.sqrt(-1) returns 1j (complex domain)

#33
yesterday = np.datetime64('today') - np.timedelta64(1,'D')
today     = np.datetime64('today')
tomorrow  = np.datetime64('today') + np.timedelta64(1,'D')
print("Yesterday:", yesterday)
print("Today:    ", today)
print("Tomorrow: ", tomorrow)

#34
Z=np.arange('2025-07','2025-08',dtype='datetime64[D]')
print("34:",Z)

#35 — How to compute ((A+B)*(-A/2)) in place (without copy)?
A=np.ones(3)*2
B=np.ones(3)*3
tmp=A.copy()
np.add(A,B,out=A)
np.divide(tmp,2,out=tmp)
np.negative(tmp,out=tmp)
np.multiply(A,tmp,out=A)
print("35-In-place computation:",A)
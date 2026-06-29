## Day 10 — Eigenvalue Revision (from Day 9)

Eigenvalues are scalar values that describe how much an eigenvector 
is stretched or shrunk when a matrix transformation is applied to it.

When a matrix acts on an eigenvector, the direction of that vector 
stays completely unchanged — it does not rotate or tilt at all. 
Only its magnitude changes, and the eigenvalue is exactly that 
scaling factor.

If the eigenvalue is > 1, the vector stretches.
If the eigenvalue is between 0 and 1, the vector shrinks.
If the eigenvalue is negative, the vector flips direction AND scales.
If the eigenvalue is 0, the vector collapses to zero.

In ML, eigenvalues matter because PCA uses them to measure how much 
variance each principal component captures. The largest eigenvalue = 
the direction of maximum variance in the data. That is why PC1 
explained 98.9% variance in our Day 9 experiment — its eigenvalue 
was by far the largest.
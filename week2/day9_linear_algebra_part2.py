import numpy as np
# ── Part 1: Dot Product + Cosine Similarity ──────────────────────────────────

def dot_product(a,b):
    return sum(a[i]*b[i] for i in range(len(a)))

def magnitude(a):
    return sum(x**2 for x in a)**0.5

def cosine_similarity(a,b):
    """ 1.0  = identical direction
        0.0  = perpendicular (unrelated)
        -1.0 = opposite directions
    """
    dot=dot_product(a,b)
    mag=magnitude(a)*magnitude(b)
    if mag==0:
        return 0.0
    return dot/mag

a=np.array([1,2,3],dtype=float)
b=np.array([4,5,6],dtype=float)
c=np.array([100,200,300],dtype=float)

print("=== Dot Product ===")
print(f"Manual dot product(a,b):    {dot_product(a,b)}")
print(f"Numpy dot product(a,b):     {np.dot(a,b)}")

print("=== Cosine Similarity ===")
print(f"cos_sim(a,b): {cosine_similarity(a,b):.4f}")
print(f"cos_sim(a,c): {cosine_similarity(a,c):.4f}")

np_cosine=np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
print(f"Numpy cos_sim(a,b): {np_cosine:.4f}")

#perpendicular vectors
perp1=np.array([1,0],dtype=float)
perp2=np.array([0,1],dtype=float)
print(f"\nPerpendicular vectors cos_sim: {cosine_similarity(perp1,perp2):.4f}")


# ── Part 2: L1 and L2 Norms ──────────────────────────────────────────────────

def l1_norm(a):
    """
    L1 norm — sum of absolute values.
    Also called Manhattan distance.
    Think: how far would you walk on a grid to get from origin to point a?
    Used in: Lasso regression, sparse ML models.
    """
    return sum(abs(x) for x in a)

def l2_norm(a):
     """
    L2 norm — square root of sum of squares.
    Also called Euclidean distance.
    Think: straight-line distance from origin to point a.
    Used in: Ridge regression, cosine similarity denominator, gradient clipping.
    """
     return sum(x**2 for x in a)**0.5

v=np.array([3,-4,0],dtype=float)
print("\n=== Norms ===")
print(f"Vector v:       {v}")
print(f"Manual L1 norm: {l1_norm(v)}")
print(f"Numpy L1 norm:  {np.linalg.norm(v,ord=1)}")
print(f"Manual L2 norm: {l2_norm(v)}")
print(f"Numpy L2 norm:  {np.linalg.norm(v,ord=2)}")

print(f"\nL2 for [3,-4,0] should be 5.0: {l2_norm(v)==5.0}")

print("\n=== Why Norms Matter ===")
# Normalizing a vector to unit length (L2 norm = 1)
# This is what embedding models do before storing vectors
v_normalized=v/np.linalg.norm(v)
print(f"Normalized v: {v_normalized.round(4)}")
print(f"L2 of normalized v: {np.linalg.norm(v_normalized):.4f}")

w=np.array([100,1,1],dtype=float)
print(f"\nVector with outlier:{w}")
print(f"L1 norm: {l1_norm(w)}")
print(f"L2 norm: {l2_norm(w):.4f}")

# ── Part 3: PCA Sketch using np.linalg.eig ───────────────────────────────────

# Step 1: Create some 2D data with a clear pattern
# Points roughly along a diagonal — high correlation between x and y
np.random.seed(42)
x=np.random.randn(100)
y=x*2 + np.random.randn(100)*0.5

# Stack into a 100x2 matrix (100 samples, 2 features)
data=np.column_stack([x,y])
print("=== PCA Sketch ===")
print(f"Data shape:     {data.shape}")

# Step 2: Center the data (subtract mean of each feature)
# PCA requires zero-mean data — otherwise eigenvectors point toward the mean
data_centered=data- data.mean(axis=0)
print(f"Mean before centering: {data.mean(axis=0).round(4)}")
print(f"Mean after centering: {data_centered.mean(axis=0).round(4)}")

# Step 3: Compute the covariance matrix
# Shape: (2, 2) — describes how x and y vary together
cov_matrix=np.cov(data_centered.T)
print(f"Covariance matrix:\n{cov_matrix.round(4)}")
# Off-diagonal values will be large and positive — x and y are correlated

# Step 4: Finding eigenvectors and eigenvalues
eigenvalues, eigenvectors=np.linalg.eig(cov_matrix)
print(f"\nEigenvalues:      {eigenvalues.round(4)}")
print(f"Eigenvectors:\n{eigenvectors.round(4)}")

# Step 5: Sort by eigenvalue — largest eigenvalue = most important direction
sorted_idx=np.argsort(eigenvalues)[::-1]
eigenvalues_sorted=eigenvalues[sorted_idx]
eigenvectors_sorted=eigenvectors[:,sorted_idx]
print(f"\nSorted eigenvalues:     {eigenvalues_sorted.round(4)}")
print(f"Top eigenvector (PC1): {eigenvectors_sorted[:,0].round(4)}")

# Step 6: Project data onto top principal component
# This is dimensionality reduction — 2D data → 1D
pc1=eigenvectors_sorted[:,0]
data_projected=data_centered @ pc1
print(f"\nProjected data shape: {data_projected.shape}")
print(f"First 5 projected values: {data_projected[:5].round(4)}")

# Step 7: Explained variance — how much info does PC1 capture?
explained_variance=eigenvalues_sorted/eigenvalues_sorted.sum()
print(f"\nVariance explained by PC1: {explained_variance[0]*100:.1f}%")
print(f"Variance explained by PC2: {explained_variance[1]*100:.1f}%")
# PC1 should explain ~95%+ because x and y are strongly correlated
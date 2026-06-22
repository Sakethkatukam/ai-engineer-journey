import numpy as np

# ── BLOCK 1: VECTOR OPERATIONS ──────────────────────────────

v1 = np.array([2, 3])
v2 = np.array([1, -1])

v_add = v1 + v2
print("Vector addition:", v_add) 

v_scaled = 3 * v1
print("Scalar multiply:", v_scaled)    

dot = np.dot(v1, v2)
print("Dot product:", dot)                # 2*1 + 3*(-1) = -1

# Vector magnitude (length)
mag_v1 = np.linalg.norm(v1)
print("Magnitude of v1:", mag_v1)         # sqrt(4+9) = 3.606

# Unit vector (direction only, magnitude = 1)
unit_v1 = v1 / np.linalg.norm(v1)
print("Unit vector:", unit_v1)
print("Its magnitude:", np.linalg.norm(unit_v1))  

# ── BLOCK 2: MATRIX MULTIPLICATION ──────────────────────────

# A matrix = a transformation. Columns = where basis vectors land.
A=np.array([[2,0],
            [0,3]])
B=np.array([[0,-1],
            [1,0]])
AB= A @ B
print("A @ B:\n",AB)

BA = B @ A
print("B @ A:\n",BA)

print("Are A@B and B@A equal?", np.array_equal(AB, BA))

v=np.array([1,1])
transformed=A@v
print("A applied to [1,1]:",transformed)

#to verify where do the basis vectors land under A?
i_hat = np.array([1, 0])
j_hat = np.array([0, 1])
print("î lands at:", A @ i_hat) #A's first column
print("ĵ lands at:", A @ j_hat) #A's second column

# ── BLOCK 3: TRANSFORMATION MATRICES ────────────────────────

# 1. Scaling
scale=np.array([[2,0],[0,0.5]])

# 2. Rotation by angle theta
theta=np.radians(90)
rotation=np.array([[np.cos(theta),-np.sin(theta)],
                   [np.sin(theta),  np.cos(theta)]])
# 3. Shear (slants the space)
shear = np.array([[1, 1],[0, 1]])
test_vec = np.array([1, 0])

print("Original vector:", test_vec)
print("After scaling:", scale @ test_vec)
print("After rotation:", np.round(rotation @ test_vec, decimals=5))
print("After shear:", shear @ test_vec)

combined = scale @ rotation
result = combined @ test_vec
print("\nRotate then scale, applied to [1,0]:", np.round(result, decimals=5))

# ── BLOCK 4: DETERMINANT ────────────────────────────────────

# Determinant = how much a transformation scales area (2D) or volume (3D)

A = np.array([[2, 0],
              [0, 3]])
det_A = np.linalg.det(A)
print("\nDeterminant of A:", det_A)   # 2*3 = 6 -> area scaled by 6x

# A transformation that squashes space to a line (det = 0)
singular = np.array([[2, 4],
                      [1, 2]])   # second row is a multiple of the first
det_singular = np.linalg.det(singular)
print("Determinant of singular matrix:", det_singular)

# A transformation that flips space (negative determinant)
flip = np.array([[0, 1],
                  [1, 0]])
det_flip = np.linalg.det(flip)
print("Determinant of flip matrix:", det_flip)

# Is the singular matrix invertible?
try:
    inv = np.linalg.inv(singular)
    print("Inverse:\n", inv)
except np.linalg.LinAlgError as e:
    print("Cannot invert:", e)
import numpy as np

# ── 1. Creating Arrays ──────────────────────────────────────────

# From a Python list
a = np.array([1, 2, 3, 4, 5])
print(a)            # [1 2 3 4 5]
print(a.dtype)      # int64  — NumPy auto-detects type
print(a.shape)      # (5,)   — 5 elements, 1 dimension

# 2D array (matrix) — list of lists
b = np.array([[1, 2, 3],
              [4, 5, 6]])
print(b.shape) 
print(b.ndim)     

# Built-in array creators
print(np.zeros((3, 4)))       # 3x4 matrix of 0.0
print(np.ones((2, 3)))        # 2x3 matrix of 1.0
print(np.eye(3))              # 3x3 identity matrix
print(np.arange(0, 10, 2))   # [0 2 4 6 8] — like range()
print(np.linspace(0, 1, 5))  # [0. 0.25 0.5 0.75 1.] — 5 evenly spaced
print(np.random.randn(3, 3)) 

a = np.array([1, 2, 3])    
b = np.array([[1], [2], [3]])  
c = np.array([[1, 2, 3]])   

print(a.shape) 
print(b.shape) 
print(c.shape) 

# ── 2. Indexing and Slicing ──────────────────────────────────────

m = np.array([[10, 20, 30],
              [40, 50, 60],
              [70, 80, 90]])

# Single element — [row, col]
print(m[0, 0]) 
print(m[1, 2])  
print(m[-1, -1]) # 90 

# Slicing — [row_start:row_end, col_start:col_end]
print(m[0, :])    # [10 20 30]  — entire first row
print(m[:, 1])    # [20 50 80]  — entire second column
print(m[0:2, 1:]) # [[20 30]    — rows 0-1, cols 1-2
                  #  [50 60]]

# Boolean indexing — grab elements matching a condition
print(m[m > 50]) 

# ── 3. Operations ────────────────────────────────────────────────

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# Element-wise — no loops needed
print(a + b)   
print(a * b)    
print(a ** 2)   
print(a / 2)   

# Aggregate operations
print(a.sum())   
print(a.mean())  
print(a.max())   
print(a.std())    # standard deviation

# Axis argument — critical for ML
m = np.array([[1, 2, 3],
              [4, 5, 6]])

print(m.sum())         # 21  — sum of everything
print(m.sum(axis=0))   # [5 7 9]  — sum down rows (per column)
print(m.sum(axis=1))   # [6 15]   — sum across cols (per row)

# ── 4. Broadcasting ──────────────────────────────────────────────

# Scalar broadcast — works on every element
a = np.array([1, 2, 3])
print(a + 10)    # [11 12 13]  — 10 broadcast across all elements

# 2D + 1D broadcast
m = np.array([[1, 2, 3],
              [4, 5, 6]]) 
row = np.array([10, 20, 30]) 

print(m + row)  # row was broadcast across BOTH rows of m

# Column vector broadcast
col = np.array([[100],
                [200]])    
print(m + col)  # col was broadcast across all 3 columns

# ── 5. ML Functions from Scratch ─────────────────────────────────

# ── 5a. Dot Product ──────────────────────────────────────────────
# Sum of element-wise products of two vectors
# Used to measure similarity and in every matrix operation

def dot_product(a:np.ndarray, b:np.ndarray)->float:
    return np.sum(a * b)

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
result = dot_product(a, b)
print(f"Dot product: {result}")          # 1*4 + 2*5 + 3*6 = 32
print(f"NumPy verify: {np.dot(a, b)}")   

# ── 5b. Matrix Multiply ──────────────────────────────────────────
# Each output cell = dot product of a row from A with a column from B
# This is how data flows through neural network layers

def matrix_multiply(A:np.ndarray, B:np.ndarray)->np.ndarray:
    # A is (m, n), B is (n, p), output is (m, p)
    assert A.shape[1] == B.shape[0], \
        f"Shape mismatch: {A.shape} vs {B.shape}"
    
    rows_A = A.shape[0]
    cols_B = B.shape[1]
    result = np.zeros((rows_A, cols_B))
    
    for i in range(rows_A):
        for j in range(cols_B):
            result[i, j] = dot_product(A[i, :], B[:, j])
    
    return result

A = np.array([[1, 2],
              [3, 4]])   # shape (2, 2)
B = np.array([[5, 6],
              [7, 8]])   # shape (2, 2)

result = matrix_multiply(A, B)
print(f"\nMatrix multiply:\n{result}")
print(f"NumPy verify:\n{A @ B}")   # @ is the matmul operator and also np.matmul(A,B)

# ── 5c. Sigmoid ──────────────────────────────────────────────────
# Squashes any value into range (0, 1)
# Used as activation function. Output = "probability-like" value.
# Formula: 1 / (1 + e^(-x))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

x = np.array([-3, -1, 0, 1, 3])
print(f"\nSigmoid: {sigmoid(x)}")
# Large negative → near 0
# 0 → exactly 0.5
# Large positive → near 1

# Works on scalars too
print(f"sigmoid(0) = {sigmoid(0)}")    # 0.5
print(f"sigmoid(100) = {sigmoid(100)}") # ~1.0
print(f"sigmoid(-100) = {sigmoid(-100)}") # ~0.0

# ── 5d. Softmax ──────────────────────────────────────────────────
# Converts a vector of scores into probabilities that sum to 1
# Used in the final layer of classification networks
# Formula: e^x_i / sum(e^x)

def softmax(x):
    # Subtract max for numerical stability — prevents floating-point overflow when computing exponentials of large numbers.
    # This is a trick every production implementation uses
    exp_x = np.exp(x - np.max(x))   #This keeps the resulting exponential values within a manageable range (between 0 and 1)
    return exp_x / exp_x.sum()

scores = np.array([2.0, 1.0, 0.1])
probs = softmax(scores)
print(f"\nSoftmax input:  {scores}")
print(f"Softmax output: {probs}")
print(f"Sum of output:  {probs.sum()}")  # must be exactly 1.0

# ── 5e. MSE Loss ─────────────────────────────────────────────────
# Mean Squared Error — measures how wrong your model's predictions are
# Lower = better. Goal of training = minimize this.
# Formula: mean((predictions - targets)^2)

def mse_loss(predictions, targets):
    return np.mean((predictions - targets) ** 2)

# Perfect predictions → loss = 0
predictions = np.array([3.0, 2.5, 4.0, 5.0])
targets      = np.array([3.0, 2.5, 4.0, 5.0])
print(f"\nPerfect MSE: {mse_loss(predictions, targets)}")  # 0.0

# Bad predictions → high loss
bad_predictions = np.array([0.0, 0.0, 0.0, 0.0])
print(f"Bad MSE: {mse_loss(bad_predictions, targets)}")

# Slightly off → small loss
ok_predictions = np.array([2.8, 2.3, 4.2, 4.9])
print(f"OK MSE: {mse_loss(ok_predictions, targets)}")

# Practice Exercises Before You Push

# Create a (4, 4) matrix of random integers between 1–100. Extract all values greater than 50 using boolean indexing.
# Without using a loop, normalize this array to have values between 0 and 1:
# arr = np.array([10, 25, 3, 88, 42, 67])

arr=np.random.randint(1,101, size=(4,4))
res=arr[arr>50]
normalized=(res-res.min())/(res.max()-res.min())
print("Original matrix:",arr)
print("Values > 50:",res)
print("Normalised:",normalized)

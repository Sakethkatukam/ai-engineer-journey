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

## Day 10 — Statistics + Probability (StatQuest)

### Key Concepts
- **Bayes Theorem**: P(B|A) = [P(A|B) · P(B)] / P(A)
  - P(B) = prior, P(A|B) = likelihood, P(A) = evidence, P(B|A) = posterior
  - Used to flip "P(evidence | class)" into "P(class | evidence)"

- **Probability vs Likelihood**: 
  Probability varies the data, holding parameters fixed. 
  Likelihood varies the parameters, holding the data fixed.

- **Log-Likelihood**: used instead of raw likelihood because multiplying 
  many small probabilities (<1) causes numerical underflow. Taking log 
  converts products into sums, which are numerically stable. Log is 
  monotonic, so the parameter that maximizes likelihood also maximizes 
  log-likelihood — nothing is lost.

- **Naive Bayes trick**: when comparing posteriors across classes, P(A) 
  (the evidence) is constant across all classes being compared, so it 
  can be dropped: posterior ∝ likelihood × prior.

- **Eigenvalues (Day 9 revision)**: scale eigenvectors without changing 
  their direction. Largest eigenvalue = direction of max variance in PCA.

### Code Patterns Worth Remembering
- Gaussian PDF from scratch:
  `(1/(σ√2π)) * exp(-(x-μ)²/(2σ²))`
- Sample variance uses ddof=1 (Bessel's correction, n-1) not ddof=0 
  (population, n) — always ddof=1 for ML work on samples.
- Verify custom implementations against NumPy built-ins immediately 
  (np.mean, np.var, np.std with ddof=1) before trusting your own code.
- Gaussian Naive Bayes: compute posterior ∝ likelihood × prior per 
  class, normalize by their sum if you want actual probabilities, 
  predict argmax.

### Open Questions / Unclear
- None — all 3 comprehension check questions corrected and re-verified.
  Q1 formula was wrong initially (fixed), Q2 needed sharper distinction 
  (fixed), Q3 needed real "why" beyond plotting style (fixed).
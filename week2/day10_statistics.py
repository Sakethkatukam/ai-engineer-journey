import numpy as np
import matplotlib.pyplot as plt

def gaussian_pdf(x, mu, sigma):
    """
    Compute the Gaussian probability density at point(s) x.
    mu: mean, sigma: standard deviation
    """
    coeff=1/(sigma*np.sqrt(2*np.pi))
    exponent=- ((x-mu)**2)/(2*sigma**2)
    return coeff*np.exp(exponent)

x_vals=np.linspace(-5,5,100)
y_vals=gaussian_pdf(x_vals,mu=0,sigma=1)

plt.plot(x_vals, y_vals)
plt.title("Standard Normal Distribution (mean=0, std=1)")
plt.xlabel("x")
plt.ylabel("density")
plt.savefig("day10_gaussian.png")
plt.show()

def sample_mean(data):
    return np.sum(data)/len(data)

def sample_variance(data, ddof=1):
    """
    ddof=1 gives the SAMPLE variance (Bessel's correction, divide by n-1)
    ddof=0 gives the POPULATION variance (divide by n)
    We default to ddof=1 since in ML we almost always work with samples, not full populations.
    """
    mean=sample_mean(data)
    squared_diffs=(data-mean)**2
    return np.sum(squared_diffs)/(len(data)-ddof)

def sample_std(data,ddof=1):
    return np.sqrt(sample_variance(data,ddof))

data=np.array([2,4,4,4,5,5,7,9])
my_mean=sample_mean(data)
my_var=sample_variance(data)
my_std=sample_std(data)
print(f"My mean: {my_mean}, Numpy mean: {np.mean(data)}")
print(f"My variance: {my_var}, Numpy variance (ddof=1): {np.var(data,ddof=1)}")
print(f"My std: {my_std}, Numpy std (ddof=1): {np.std(data,ddof=1)}")

# Toy dataset: weights of apples vs oranges
apple_weights = np.array([150, 160, 170, 155, 165, 145, 158])
orange_weights = np.array([130, 135, 140, 128, 138, 142, 133])

# Step A: Learn the Gaussian parameters for each class (this is "training")
apple_mean = sample_mean(apple_weights)
apple_std = sample_std(apple_weights)

orange_mean = sample_mean(orange_weights)
orange_std = sample_std(orange_weights)

print(f"\nApple:  mean={apple_mean:.2f}, std={apple_std:.2f}")
print(f"Orange: mean={orange_mean:.2f}, std={orange_std:.2f}")

# Step B: Priors — P(class) before seeing any data
n_apples = len(apple_weights)
n_oranges = len(orange_weights)
n_total = n_apples + n_oranges

prior_apple = n_apples / n_total
prior_orange = n_oranges / n_total

print(f"\nPrior P(apple) = {prior_apple:.3f}")
print(f"Prior P(orange) = {prior_orange:.3f}\n")

def bayes_classify(weight, mean_a, std_a, prior_a, mean_o, std_o, prior_o):
    """
    Classify a fruit given its weight using Bayes Theorem.
    Posterior ∝ Likelihood × Prior  (we skip dividing by P(A) — the evidence —
    because it's the same constant for both classes, so it doesn't affect 
    which one is bigger. This is standard practice in Naive Bayes.)
    """
    likelihood_apple = gaussian_pdf(weight, mean_a, std_a)
    likelihood_orange = gaussian_pdf(weight, mean_o, std_o)

    posterior_apple = likelihood_apple * prior_a
    posterior_orange = likelihood_orange * prior_o

    # Normalize so they actually sum to 1 (optional but informative)
    total = posterior_apple + posterior_orange
    posterior_apple_normalized = posterior_apple / total
    posterior_orange_normalized = posterior_orange / total

    prediction = "apple" if posterior_apple > posterior_orange else "orange"

    return prediction, posterior_apple_normalized, posterior_orange_normalized


test_weights = [150, 135, 145, 160]
for w in test_weights:
    pred, p_apple, p_orange = bayes_classify(w, apple_mean, apple_std, prior_apple,
                                             orange_mean, orange_std, prior_orange)
    print(f"Weight {w}g → Predicted: {pred} (P(apple)={p_apple:.3f}, P(orange)={p_orange:.3f})")
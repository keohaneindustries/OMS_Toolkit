# %% imports
from myimports import *
from lib.data.generate_random.uniform import UniformDenseRandom as udr
from lib.models.linear_regression import estimate_coeffs, rel_diff
from lib.results.plotting import plot_1d_regression_fit

# %%
prompt = """\
The empirical scaling of linear least squares appears to be pretty good, being roughly linear in  mm  or at worst 
quadratic in  nn . But there is still a downside in time and storage: each time there is a change in the data, 
you appear to need to form the data matrix all over again and recompute the solution from scratch, possibly touching 
the entire data set again!

This begs the question, is there a way to incrementally update the model coefficients whenever a new data point, 
or perhaps a small batch of new data points, arrives? Such a procedure would be considered incremental or online, 
rather than batched or offline.
"""
# %%
lms_algo_desc = """\
Summary of the LMS algorithm.

- Choose any initial guess,  θ (0)θ~(0) , such as  θ (0)←0θ~(0)←0 .
- For each observation  (yk,x̂ Tk)(yk,x^kT) , do the update:
    θ (k+1)←θ k+Δkθ~(k+1)←θ~k+Δk 
    where  Δk=ϕ⋅x̂ k(yk−x̂ Tkθ (k))Δk=ϕ⋅x^k(yk−x^kTθ~(k)) 

"""
# %%
m = 100000
n = 1
X, y, theta_true = udr.generate_sample_problem(m, n, sigma=0.1)

print("Condition number of the data matrix:", np.linalg.cond(X))

theta = estimate_coeffs(X, y)
e_rel = rel_diff(theta, theta_true)

print("Relative error:", e_rel)

# %%
LAMBDA_MAX = max(np.linalg.eigvals(X.T.dot(X)))
print(LAMBDA_MAX)
# %%
PHI = 1.99 / LAMBDA_MAX  # Fudge factor
rel_diffs = np.zeros((m + 1, 1))

theta_k = np.zeros((n + 1)).reshape((n + 1, 1))
for k in range(m):
    rel_diffs[k] = rel_diff(theta_k, theta_true)

    # Implement the online LMS algorithm.
    # Take (y[k], X[k, :]) to be the k-th observation.
    ###
    ### YOUR CODE HERE
    ###
    xk = X[k, :].reshape((1, (len(X[k, :]))))
    yk = y[k].reshape((1, (len(y[k]))))
    #     print("xk:\t", xk, "\t", xk.shape)
    #     print("yk:\t", yk, "\t",  yk.shape)

    suba = np.dot(xk, theta_k)
    #     print("suba:\t", suba, "\t",  suba.shape)
    subb = (yk - suba)
    #     print("subb:\t", subb, "\t",  subb.shape)
    fx = np.matmul(xk.T, subb)
    #     print("fx:\t", fx, "\t",  fx.shape)
    delta_k = fx * PHI
    #     print("deltak:\t", delta_k, "\t",  delta_k.shape)
    #     print("thetak:\t", theta_k, "\t",  theta_k.shape)
    theta_k += delta_k

theta_lms = theta_k
rel_diffs[m] = rel_diff(theta_lms, theta_true)

# %% test
print (theta_true.T)
print (theta.T)
print (theta_lms.T)

print("\n('Passed' -- this cell appears to run without error, but we aren't checking the solution.)")
# %%
plt.plot(range(len(rel_diffs)), rel_diffs)

# %% sanity-check regression fit plot
STEP = int(X.shape[0] / 500)
if n == 1:
    plot_1d_regression_fit(X, y, STEP, theta, theta_true, theta_lms)
else:
    print("Plot is multidimensional; I live in Flatland, so I don't do that.")
# %%
# Setup problem and compute the batch solution
m = 100000
n = 1
X, y, theta_true = udr.generate_sample_problem(m, n, sigma=0.1)
theta_batch = estimate_coeffs(X, y)

# Your turn, below: Implement a hybrid batch-LMS solution
# assuming you observe the first few data points all at
# once, and then see the remaining points one at a time.

###
### YOUR CODE HERE
###

# %% imports
from myimports import *

prompt = r"""1. Form $C \equiv X^T X$. This object is sometimes called the [Gram matrix](
https://en.wikipedia.org/wiki/Gramian_matrix) or Gramian of $X$.
2. Form $b \equiv X^T y$.
3. Solve $C \theta^* = b$ for $\theta^*$."""


# %% solve neq
def solve_neq(X, y):
    C = _form_gram_matrix(X)
    b = _form_beta(X, y)
    theta_est = _solve_theta(C, b)
    return theta_est


def _form_gram_matrix(X):
    return np.matmul(X.T, X)


def _form_beta(X, y):
    return np.matmul(X.T, y)


def _solve_theta(C, b):
    return sp.linalg.solve(C, b)

# %% calc_residual_norm

def calc_residual_norm_squared(X, y, theta):
    return sp.linalg.norm(_resid_vector(X, y, theta))

def _resid_vector(X, y, theta):
    return np.matmul(X, theta) - y

#%%

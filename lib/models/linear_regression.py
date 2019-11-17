#%% imports
from myimports import *


#%% linreg function
def linreg(X, Y):
    X = sm.add_constant(X)
    model = regression.linear_model.OLS(Y, X).fit()
    X = X[:, 1]
    return model

#%% oms-derived univariate linear model
def univariate_linreg(x, y) -> tuple:
    """Returns (alpha, beta) s.t. y ~ alpha*x + beta."""
    m = len(x); assert len(y) == m
    u = np.ones(m)
    alpha = _calc_a(x, y, m, u)
    beta = _calc_b(x, y, m, u, alpha)
    return (alpha, beta)

def _calc_a(*args):
    return _calc_numerator_a(*args) / _calc_denominator_a(*args)

def _calc_numerator_a(x, y, m: int, u: np.ndarray):
    return np.vdot(x, y) - (1 / m) * (np.vdot(u, x)) * (np.vdot(u, y))

def _calc_denominator_a(x, y, m: int, u: np.ndarray):
    return np.vdot(x, x) - (1 / m) * ((np.vdot(u, x)) ** 2)

def _calc_b(x, y, m: int, u: np.ndarray, a):
    return (1 / m) * np.vdot(u, (y - x * a))

#%%

def estimate_coeffs(X, y):
    """
    Solves X*theta = y by a linear least squares method.
    """
    result = np.linalg.lstsq(X, y, rcond=None)
    theta = result[0]
    return theta

#%%
def rel_diff(x, y, ord=2):
    """
    Computes ||x-y|| / ||y||. Uses 2-norm by default;
    override by setting 'ord'.
    """
    return np.linalg.norm (x - y, ord=ord) / np.linalg.norm (y, ord=ord)

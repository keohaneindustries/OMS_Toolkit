# %% imports
from myimports import *
from lib.results.data_display import *


# %% generate a generic problem

class UniformDenseRandom:

    @staticmethod
    def r_matrix_uniform(m, n, low, high):
        return np.random.uniform(low=low, high=high, size=(m, n))

    @staticmethod
    def r_matrix_eps(m, n, eps):
        return UniformDenseRandom.r_matrix_uniform(m, n, 0, eps)


    @staticmethod
    def gen_empty_problem(m: int, n: int):
        """ simulates data. returns a triple (X, y, theta) defined as follows:
        X: an m x (n+1) data matrix
        y: a response vector
        theta: the "true" model parameters

        each entry of X (i, j) == i ** j
        https://en.wikipedia.org/wiki/Vandermonde_matrix
        theta[0] is the intercept
        """
        from numpy import arange, tile, cumprod, insert, ones
        # 1 + x + x^2 + ... + x^n, x = 0:m
        X = np.empty((m, n + 1))
        x_col = arange(m).reshape((m, 1))  # 0, 1, 2, ..., m-1
        X[:, 0] = 1.0
        X[:, 1:] = tile(x_col, reps=(1, n))
        X[:, 1:] = cumprod(X[:, 1:], axis=1)
        theta = ones((n + 1, 1))
        y = np.sum(X, axis=1).reshape((m, 1))
        return X, y, theta

    @staticmethod
    def generate_sample_problem(m: int, n: int, sigma=1.0 / (2 ** 0.5)):
        theta = UniformDenseRandom.generate_model(n)
        X, y = UniformDenseRandom.generate_data(m, theta, sigma)
        return X, y, theta

    @staticmethod
    def generate_model(n):
        """Returns a set of (random) n+1 linear model coefficients."""
        return np.random.rand(n + 1, 1)

    @staticmethod
    def generate_data(m, theta, sigma=1.0 / (2 ** 0.5)):
        """
        Generates 'm' noisy observations for a linear model whose
        predictor (non-intercept) coefficients are given in 'theta'.
        Decrease 'sigma' to decrease the amount of noise.
        """
        assert (type(theta) is np.ndarray) and (theta.ndim == 2) and (theta.shape[1] == 1)
        n = len(theta)
        X = np.random.rand(m, n)
        X[:, 0] = 1.0
        y = X.dot(theta) + sigma * np.random.randn(m, 1)
        return (X, y)


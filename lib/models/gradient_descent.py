# %% imports
from myimports import *


# %% 2-d random descent

def _f_gradient_1(x0, x1):
    return x0 ** 2 + x1 ** 2

def _f_gradient_2(x0, x1):
    return (2 * x0, 2 * x1)

def two_d_gradient(x0, x1) -> tuple:
    from numpy import vectorize, meshgrid
    f_vec = vectorize(_f_gradient_1)
    grad_f_vec = vectorize(_f_gradient_2)

    X0, X1 = meshgrid(x0, x1)
    Z = f_vec(X0, X1)

    dX0, dX1 = grad_f_vec(X0, X1)

    return X0, X1, dX0, dX1, Z


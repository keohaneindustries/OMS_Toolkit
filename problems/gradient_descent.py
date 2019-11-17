# %% imports
from myimports import *
from lib.models.gradient_descent import two_d_gradient
from lib.results.plotting import three_d_bi_plot, two_d_descent


# %% random 2-d gradient descent

def r_two_d_gradient(x=None, y=None):
    if (x is None) or (y is None):
        x = np.linspace(-2, 2, 11)
        y = np.linspace(-2, 2, 11)

    X, Y, dX, dY, Z = two_d_gradient(x, y)

    three_d_bi_plot(X, Y, Z)
    two_d_descent(X, Y, dX, dY, Z)
    return


# %%

r_two_d_gradient()

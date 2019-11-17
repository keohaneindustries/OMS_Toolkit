# %% imports
from lib.results.data_display import *
from lib.data.generate_random.uniform import UniformDenseRandom as udr


# %% random perturbations

def perturb_system(X: np.ndarray, y: np.ndarray, eps: float):
    """
    1. Let $\Delta X$ be the first perturbation. It should have the same dimensions as $X$, and its entries should
    lie in the interval $[-\epsilon, \epsilon]$. The value of $\epsilon$ is given by `eps`.
    2. The second is $\Delta y$, a small perturbation to the response variable, $y$. Its entries should also lie in
    the same interval, $[-\epsilon, \epsilon]$,

    :param X:
    :param y:
    :param eps:
    :return:
    """
    dX = udr.r_matrix_uniform(*X.shape, -eps, eps)
    dy = udr.r_matrix_uniform(*y.shape, -eps, eps)

    X_perturbed = X + dX
    y_perturbed = y + dy
    return X_perturbed, y_perturbed



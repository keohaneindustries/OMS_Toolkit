# %% imports
from myimports import *


#%% random calcs
def calc_lims(v, buffer=0.1):
    vmin = v.min()
    vmax = v.max()
    dv = (vmax - vmin) * buffer
    return vmin - dv, vmax + dv

def calc_lims_of_many(V: list, buffer=0.1):
    tmin, tmax = None, None
    for v in V:
        vmin, vmax = calc_lims(v, buffer)
        if (tmin is None) or (vmin < tmin):
            tmin = vmin
        if (tmax is None) or (vmax > tmax):
            tmax = vmax
    return tmin, tmax

def calc_xylim_of_series(T: list, ax: int=0, ay: int=1):
    X = []
    Y = []
    for t in T:
        X.append(np.array([t[ax, :], t[ax, :]]))
        Y.append(np.array([t[ay, :], t[ay, :]]))

    xmin, xmax = calc_lims_of_many(X)
    ymin, ymax = calc_lims_of_many(Y)
    xylim = [xmin, xmax, ymin, ymax]
    return xylim

# %% plot linear regression
def plot_linreg(X, Y, model: regression.linear_model.RegressionResults):
    a = model.params[0]
    b = model.params[1]
    X2 = np.linspace(X.min(), X.max(), 100)
    Y_hat = X2 * b + a

    plt.scatter(X, Y, alpha=0.3)  # Plot the raw data
    plt.plot(X2, Y_hat, 'r', alpha=0.9)  # Add the regression line, colored in red
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    plt.show()

    pprint(model.summary())
    return


# %% plot a best-fit line for a univariate linear regression
def plot_univariate_linreg(x, y, fit: bool = True, alpha=None, beta=None):
    from numpy import linspace, floor, ceil

    if fit:
        from lib.models.linear_regression import univariate_linreg
        alpha, beta = univariate_linreg(x, y)
    else:
        assert alpha is not None; assert beta is not None

    # Two points make a line:
    x_fit = linspace(floor(x.min()), ceil(x.max()), 2)
    y_fit = alpha * x_fit + beta

    plt.scatter(x, y, marker='o')
    plt.plot(x_fit, y_fit, 'r--')
    plt.title('Best-fit linear model')
    plt.show()
    return


#%% plot a 3-D surface

def three_d_bi_plot(X, Y, Z):
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(figsize=(10, 5))

    ax3d = fig.add_subplot(121, projection='3d')
    ax3d.plot_wireframe(X, Y, Z)
    plt.xlabel('x')
    plt.ylabel('y')

    ax2d = fig.add_subplot(122)
    cp = ax2d.contour(X, Y, Z)
    plt.xlabel('x')
    plt.ylabel('xy')
    plt.show()
    return

#%% plot a 2-D gradient descent

def two_d_descent(X, Y, dX, dY, Z):
    cp = plt.contour(X, Y, Z)
    plt.quiver(X, Y, dX, dY, scale=40, headwidth=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('square')
    plt.show()
    return

#%% scatter_thetas

def scatter_thetas(Thetas, theta_true=None, ax=0, ay=-1, xylim=None, title=None):
    """ Makes a 2-D scatter plot of given theta values.

    If the thetas have more than two dimensions, only the first and last are displayed by default.
    (Override by setting ax and ay.)

    """
    assert type(Thetas) is np.ndarray and Thetas.shape[0] >= 2
    plt.scatter(Thetas[ax, :], Thetas[ay, :])
    plt.xlabel('{}-coordinate'.format(ax if ax >= 0 else Thetas.shape[0] + ax))
    plt.ylabel('{}-coordinate'.format(ay if ay >= 0 else Thetas.shape[0] + ay))
    if xylim is not None:
        plt.axis(xylim)
    else:
        plt.axis('equal')
    if theta_true is not None:
        assert type(theta_true) is np.ndarray and theta_true.shape[0] >= 2 and theta_true.shape[1] == 1
        plt.scatter(theta_true[ax], theta_true[ay], marker='*', color='red', s=15 ** 2)
    if title is not None:
        plt.title(title)
    plt.show()
    plt.axis('square')
    return

#%% compare scatter thetas
def compare_scatter_thetas(T0, title0, T1, title1, ax=0, ay=1, **kwargs):
    xylim = calc_xylim_of_series([T0, T1], ax, ay)
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    scatter_thetas(T0, title=title0, ax=ax, ay=ay, xylim=xylim, **kwargs)
    plt.subplot(1, 2, 2)
    scatter_thetas(T1, title=title1, ax=ax, ay=ay, xylim=xylim, **kwargs)
    plt.show()
    return

#%% sanity check regression fit
def plot_1d_regression_fit(X, y, step, theta=None, theta_true=None, theta_lms=None):
    assert y.shape[1] == 1 # single-dimensional
    assert (theta is not None) or (theta_true is not None) or (theta_lms is not None)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(X[::step, 1], y[::step], 'b+')  # blue - data
    if theta_true is not None:
        ax1.plot(X[::step, 1], X.dot(theta_true)[::step], 'r*')  # red - true
    if theta is not None:
        ax1.plot(X[::step, 1], X.dot(theta)[::step], 'go')  # green - batch
    if theta_lms is not None:
        ax1.plot(X[::step, 1], X.dot(theta_lms)[::step], 'mo')  # magenta - pure LMS
    plt.show()
    return

#%%



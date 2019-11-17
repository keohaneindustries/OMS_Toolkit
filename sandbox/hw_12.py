
#%% imports
from myimports import *
from lib.data.load.cse6040download import download_dataset, localize_file

#%% region part0

#%% data import
dataset = {'lsd.dat': '4c119057baf86cff8da03d825d7ce141'}
download_dataset(dataset)
print("\n(All data appears to be ready.)")

#%% trun data
df = pd.read_fwf(localize_file('lsd.dat'),
              colspecs=[(0, 4), (7, 13)],
              names=['lsd_concentration', 'exam_score'])
pprint(df)

plt.scatter(df['lsd_concentration'], df['exam_score'])
plt.xlabel ('LSD Tissue Concentration')
plt.title ('Shocking news: Math scores degrade with increasing LSD!')
plt.plot()

#%% load data to sandbox
# Compute the coefficients for the LSD data:
x, y = df['lsd_concentration'], df['exam_score']

#%%
def _calc_numerator_a(x, y, m: int, u: np.ndarray):
    return np.vdot(x, y) - (1 / m) * (np.vdot(u, x)) * (np.vdot(u, y))

def _calc_denominator_a(x, y, m: int, u: np.ndarray):
    return np.vdot(x, x) - (1 / m) * ((np.vdot(u, x)) ** 2)

def _calc_a(*args):
    return _calc_numerator_a(*args) / _calc_denominator_a(*args)

def _calc_b(x, y, m: int, u: np.ndarray, a):
    return (1 / m) * np.vdot(u, (y - x * a))


#%% definition of linreg_fit
def linreg_fit(x, y):
    """Returns (alpha, beta) s.t. y ~ alpha*x + beta."""
    from numpy import ones
    m = len(x); assert len(y) == m
    u = ones(m)
    ###
    ### YOUR CODE HERE
    ###
    alpha = _calc_a(x, y, m, u)
    beta = _calc_b(x, y, m, u, alpha)

    return (alpha, beta)


#%% test cell
# Compute the coefficients for the LSD data:
x, y = df['lsd_concentration'], df['exam_score']

alpha, beta = linreg_fit(x, y)

print("alpha:", alpha)
print("beta:", beta)


#%% region part1

#%%

def f(x0, x1):
    return x0 ** 2 + x1 ** 2


from numpy import sin, cos, vectorize, isclose
from numpy.random import randn

f_vec = vectorize(f)
theta = randn(1000)
assert all(isclose(f_vec(sin(theta), cos(theta)), 1.0))

print("\n(Passed!)")

from numpy import linspace, meshgrid
x0 = linspace(-2, 2, 11)
x1 = linspace(-2, 2, 11)
X0, X1 = meshgrid(x0, x1)

#%%
def grad_f(x0, x1):
    ###
    ### YOUR CODE HERE
    ###
    return (2 * x0, 2 * x1)

#%%
# Test cell: `grad_f_test`

grad_f_vec = vectorize(grad_f)
z = randn(5)
gx, gy = grad_f_vec(z, -z)
assert all(isclose(gx * 0.5, z)) and all(isclose(gy * (-0.5), z)), "Your function might have a bug..."

print("\n(Passed!)")



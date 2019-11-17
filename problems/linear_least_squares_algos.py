# %% imports
from lib.data.transformations.tibbles import show_2vecs_tibble, make_data_tibble
from lib.data.transformations.system import perturb_system
from lib.results.data_display import *
from lib.results.plotting import scatter_thetas, compare_scatter_thetas
from lib.models.lls_algo import *
from lib.data.generate_random.uniform import UniformDenseRandom as udr

# Stash this function for later:
SAVE_LSTSQ = np.linalg.lstsq  # You may ignore this line, which some test cells will use

# %%

print("Sample generated problem:")
m, n = 10, 2
X, y, theta_true = udr.gen_empty_problem(m, n)

s = r'X = {}, \quad y = {} \quad \implies \quad \theta^* = {}'.format(nparray_to_bmatrix(X),
                                                                      nparray_to_bmatrix(y),
                                                                      nparray_to_bmatrix(theta_true))
print(s)
# display(Math(s))

# %% Algorithm #1: direct solution of the normal equations
print(X.T.dot(X))
print(X.T.dot(y))

theta_neq = solve_neq(X, y)
print("theta_neq:\n", theta_neq)

print("Your implementation's solution versus the true solution:")
show_2vecs_tibble(theta_neq, theta_true, xname='theta_neq', yname='theta_true', error=True)

# %%

r_norm_neq = calc_residual_norm_squared(X, y, theta_neq)
print("\nThe squared residual norm:", r_norm_neq)

# %% practice generating a random error matrix

Z = udr.r_matrix_eps(5, 3, 1e-2)
assert Z.shape == (5, 3)
assert ((Z >= 0) & (Z <= 1e-2)).all()
print("\n(Passed.)")

# %% artificially introduce error into the system

EPSILON = 0.1
X_perturbed, y_perturbed = perturb_system(X, y, EPSILON)

Delta_X = X_perturbed - X
Delta_y = y_perturbed - y
s = r'\Delta X = {}, \quad \Delta y = {}'.format(nparray_to_bmatrix(Delta_X[:5, :]),
                                                 nparray_to_bmatrix(Delta_y[:5]))
# display(Math(s))
print(s)


# %% run a sensitivity experiment
def run_perturbation_trials(solver, X, y, eps=0.01, trials=100):
    Thetas = np.zeros((X.shape[1], trials))  # Store all computed thetas
    for t in range(trials):
        X_p, y_p = perturb_system(X, y, eps)
        Thetas[:, t:t + 1] = solver(X_p, y_p)
    return Thetas


Thetas_neq = run_perturbation_trials(solve_neq, X, y)

print("Unperturbed solution:")
print(theta_neq)

print("First few perturbed solutions (columns):")
print(Thetas_neq[:, :5])

# %% plot it

scatter_thetas(Thetas_neq, theta_true=theta_true, ax=0, ay=2)

# %% stress test algo 1
cond_X = np.linalg.cond(X)
cond_XTX = np.linalg.cond(X.T.dot(X))

assert 1. <= cond_X <= 3e3
assert 1. <= cond_XTX <= 6e6

show_cond_fancy(cond_X, 'X')
show_cond_fancy(cond_XTX, 'X^T X')
show_cond_fancy(cond_X ** 2, 'X', opt='^2')

# %% Generate a "hard" problem
m_hard, n_hard = 100, 6
X_hard, y_hard, theta_hard_true = udr.gen_empty_problem(m_hard, n_hard)

df_hard = make_data_tibble(X_hard, y_hard)
print("First few rows of data:\n", df_hard.head())
print("True parameter estimates:\n{}".format(theta_hard_true))

cond_X_hard = np.linalg.cond(X_hard)
cond_XTX_hard = np.linalg.cond(X_hard.T.dot(X_hard))

name_X_hard = 'X_h'
show_cond_fancy(cond_X_hard, name_X_hard)
show_cond_fancy(cond_XTX_hard, '{}^T {}'.format(name_X_hard, name_X_hard))

# %%
Thetas_hard_neq = run_perturbation_trials(solve_neq, X_hard, y_hard)
scatter_thetas(Thetas_hard_neq, theta_true=theta_hard_true, ax=0, ay=2)

print("Residual norm for one of the trials:")
theta_hard_neq_example = np.random.randint(Thetas_hard_neq.shape[1])
# calc_residual_norm(X_hard, y_hard, theta_hard_neq_example)

# %% algorithm 2: QR decomp
prompt = """\
1. Compute  X=QRX=QR .
2. Form the modified right-hand side,  z=QTyz=QTy .
3. Use back-substitution to solve  Rθ∗=zRθ∗=z ."""

print(X[:5], "\n ...\n")

###
### YOUR CODE HERE
###
Q, R = np.linalg.qr(X)

# Print the dimensions of your result
print("Q:", Q.shape, "\n")
print("R:", R.shape, "==")
print(R)

# %% Test cell: `qr_test`

assert type(Q) is np.ndarray, "`Q` is not a Numpy array but should be."
assert type(R) is np.ndarray, "`R` is not a Numpy array but should be."
assert Q.shape == (m, n + 1), "`Q` has the wrong shape: it's {} rather than {}.".format(Q.shape, (m, n + 1))
assert R.shape == (n + 1, n + 1), "`R` has the wrong shape: it's {} rather than {}.".format(R.shape, (m, n + 1))
for i in range(R.shape[0]):
    for j in range(i):
        assert np.isclose(R[i][j], 0.0), "R[{}][{}] == {} instead of 0!".format(i, j, R[i][j])

QTQ = Q.T.dot(Q)
assert np.isclose(QTQ, np.eye(Q.shape[1])).all(), "Q^T Q is not nearly the identity matrix, as it should be."

assert np.isclose(X, Q.dot(R)).all(), "QR is not sufficiently close in values to X!"

print("\n(Passed!)")

# %% show the "condition number" (complexity) of R
cond_R = np.linalg.cond(R)

show_cond_fancy(cond_X, 'X')
show_cond_fancy(cond_XTX, 'X^T X')
show_cond_fancy(cond_R, 'R')


# %% my implementation of QR

def solve_qr(X, y):
    ###
    ### YOUR CODE HERE
    ###
    Q, R = np.linalg.qr(X)
    z = np.matmul(Q.T, y)
    return sp.linalg.solve_triangular(R, z)


theta_qr = solve_qr(X, y)

print("Comparing your QR solution to the true solution:")
print(show_2vecs_tibble(theta_qr, theta_true, xname='theta_qr', yname='theta_true', error=True))

print("Residual norm:", calc_residual_norm_squared(X, y, theta_qr))

# %% Test cell: `solve_qr_test`
import re

try:
    del np.linalg.lstsq
    solve_qr(X, y)
except NameError as n:
    if re.findall('lstsq', n.args[0]):
        print("*** Double-check that you did not try to use `lstsq()`. ***")
    raise n
except AttributeError as a:
    if re.findall('lstsq', a.args[0]):
        print("*** Double-check that you did not try to use `lstsq()`. ***")
    raise a
finally:
    np.linalg.lstsq = SAVE_LSTSQ

assert np.isclose(theta_qr, theta_true).all(), "Your QR-based solution should be closer to the true solution."

print("\n(Passed!)")

# %% plot algo 1 vs algo 2
Thetas_hard_qr = run_perturbation_trials(solve_qr, X_hard, y_hard)

# Plot side-by-side against normal equations method
# You should observe that the QR-based method does, indeed, produce estimates much closer to the true value despite
# the problem's high condition number.


compare_scatter_thetas(Thetas_hard_neq, 'Normal equations',
                       Thetas_hard_qr, 'QR',
                       ax=0, ay=-1, theta_true=theta_hard_true)

print("Sample estimate for one of the trials:")
theta_hard_neq_example = Thetas_hard_neq[:, np.random.randint(Thetas_hard_neq.shape[1])]
theta_hard_qr_example = Thetas_hard_qr[:, np.random.randint(Thetas_hard_qr.shape[1])]
msg = "- {}-based method: theta^T =\n\t{}"
print(msg.format("Gramian", theta_hard_neq_example.T))
print(msg.format("QR", theta_hard_qr_example.T))

# %% evaluate performance side-by-side
print("=== Performance of the normal equations-based algorithm ===")
# % timeit solve_neq(X_hard, y_hard)

print("\n=== Performance of the QR-based algorithm ===")
# % timeit solve_qr(X_hard, y_hard)

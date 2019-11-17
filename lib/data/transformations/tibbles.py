# %% imports
from myimports import *  # from IPython.display import display, Math


# %%
def show_2vecs_tibble(x, y, xname='x', yname='y', error=False):
    """Display two column vectors side-by-side in a tibble."""
    assert type(x) is np.ndarray and x.ndim >= 2 and x.shape[1] == 1
    assert type(y) is np.ndarray and y.ndim >= 2 and y.shape[1] == 1
    assert x.shape == y.shape
    x_df = pd.DataFrame(x, columns=[xname])
    y_df = pd.DataFrame(y, columns=[yname])
    df = pd.concat([x_df, y_df], axis=1)
    if error:
        df['error'] = x - y
    # display(df)
    return df


# Display (X, y) problem as a tibble
def make_data_tibble(X, y=None):
    df = pd.DataFrame(X, columns=['x_{}'.format(i) for i in range(X.shape[1])])
    if y is not None:
        y_df = pd.DataFrame(y, columns=['y'])
        df = pd.concat([y_df, df], axis=1)
    return df


def canonicalize_tibble(X: pd.DataFrame):
    """Returns a tibble in _canonical order_."""
    # Enforce Property 1:
    var_names = sorted(X.columns)
    Y = X[var_names].copy()

    # Enforce Property 2:
    Y.sort_values(by=var_names, inplace=True)

    # Enforce Property 3:
    Y.set_index([list(range(0, len(Y)))], inplace=True)

    return Y


def tibbles_are_equivalent(A: pd.DataFrame, B: pd.DataFrame):
    """Given two tidy tables ('tibbles'), returns True iff they are
    equivalent.
    """
    A_canonical = canonicalize_tibble(A)
    B_canonical = canonicalize_tibble(B)
    cmp = A_canonical.eq(B_canonical)
    return cmp.all().all()

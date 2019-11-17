# %% imports
from myimports import *  # from IPython.display import display, Math


# %%

def sci_to_latex(x, fmt='{:.2e}'):
    s_raw = fmt.format(x)
    s, e = s_raw.split('e')
    return s + r'\times 10^{{{}}}'.format(int(e))


def show_cond_fancy(x, name, opt=''):
    """Display a condition number in 'fancy' format (using LaTeX)."""
    x_s = sci_to_latex(x)
    s = r'\kappa({}){} \approx {}'.format(name, opt, x_s)
    # display(Math(s)))
    return s


# From: https://stackoverflow.com/questions/17129290/numpy-2d-and-1d-array-to-latex-bmatrix
def nparray_to_bmatrix(a):
    """Returns a LaTeX bmatrix"""
    assert len(a.shape) <= 2, 'bmatrix can at most display two dimensions'
    lines = str(a).replace('[', '').replace(']', '').splitlines()
    rv = [r'\begin{bmatrix}']
    rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
    rv += [r'\end{bmatrix}']
    return '\n'.join(rv)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm
import matplotlib.colors as mcolors
from matplotlib.ticker import MaxNLocator


# %% plot function
def _autoplot(obs: pd.DataFrame, title: str, xvar: str, yvar: str):
    # plot the heatmap
    cmap = plt.get_cmap('PuRd')
    # cmap = plt.get_cmap('PiYG')
    gammas = [2.0, 1.5, 1.0, 0.8, 0.5, 0.3]
    gamma = gammas[1]
    # gamma = 1.2
    dx, dy = 0.025, 0.025
    yg, xg = np.mgrid[slice(0, 2 + dy, dy),
                      slice(0, 1 + dx, dx)]

    ## chart our own filters
    x1 = [1]
    y11 = [1]
    y12 = [2]
    plt.plot(x1, y11, color='blue', label='width_min_1')
    plt.plot(x1, y12, color='blue', label='width_max_1')

    plt.hist2d(obs.loc[:, xvar], obs.loc[:, yvar], bins=[xg[0], yg[:, 0]], norm=mcolors.PowerNorm(gamma), cmap=cmap)
    plt.axis([0, 1, 0, 2])
    # plt.legend(loc='best')
    plt.xlabel('cpDelta')
    plt.ylabel('Live / Typical IV Width (NBBO)')

    plt.title("{title}".format(title=title))
    plt.tight_layout()
    plt.show()
    return

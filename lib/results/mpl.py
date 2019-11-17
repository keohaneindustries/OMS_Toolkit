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


# %% imports
import numpy as np
import pandas as pd
import datetime as dt

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import plotly.graph_objs as go


# %% mpl utils
# years = mdates.YearLocator()  # every year
# months = mdates.MonthLocator()  # every month
# months_fmt = mdates.DateFormatter('%y')
# months_fmt = mdates.DateFormatter('%Y-%m')
# wdays = mdates.WeekdayLocator()
locator = mdates.AutoDateLocator(minticks=11, maxticks=14)
formatter = mdates.ConciseDateFormatter(locator)


# %% transform it into return space
def to_returns(df: pd.DataFrame, timing_col: str, y_cols: list) -> pd.DataFrame:
    min_datapoint = df.sort_values(timing_col)[y_cols].fillna(method='bfill', axis=1).iloc[0, :]
    returns = df[[timing_col, *y_cols]].copy()
    returns.loc[:, y_cols] = returns[y_cols] / min_datapoint * 100.
    return returns


# %% load it

df = load_and_clean()
returns = to_returns(df, timing_col=TradeDateTime, y_cols=AllStocks)


# %% mpl

def chart_as_panels(df: pd.DataFrame, x_col: str, y_cols: list):
    nrows, ncols = 3, 2
    title_template = "{item}"

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True)
    X = df[x_col]
    y_col_ix = 0
    for i in range(nrows):
        for j in range(ncols):
            y_col = y_cols[y_col_ix]
            axs[i, j].plot(X, df[y_col])
            axs[i, j].set_title(title_template.format(item=y_col))
            y_col_ix += 1

    datemin = np.datetime64(df[TradeDateTime].values[0], 'M')
    datemax = np.datetime64(df[TradeDateTime].values[-1], 'M') + np.timedelta64(1, 'M')
    pxmin = 0.
    pxmax = 150.

    for ax in axs.flat:
        # ax.set(xlabel=x_col, ylabel='pct return')
        ax.set(ylabel='pct return')
        # ax.xaxis.set_minor_locator(wdays)
        # ax.xaxis.set_minor_formatter(months_fmt)
        ax.set_xlim(datemin, datemax)
        ax.set_ylim(pxmin, pxmax)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.grid(True)

    for ax in axs.flat:
        ax.label_outer()

    # axs.grid(True)
    fig.autofmt_xdate()
    plt.show()
    return


chart_as_panels(returns, x_col=TradeDateTime, y_cols=AllStocks)

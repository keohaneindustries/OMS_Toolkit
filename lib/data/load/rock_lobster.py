"""
## Example data: Rock lobsters!

As a concrete example of a classification task, consider the results of [the following experiment](
http://www.stat.ufl.edu/~winner/data/lobster_survive.txt).

Some marine biologists started with a bunch of lobsters of varying sizes (size being a proxy for the stage of a
lobster's development). They then tethered and exposed these lobsters to a variety of predators. Finally, the outcome
that they measured is whether the lobsters survived or not.

The data is a set of points, one point per lobster, where there is a single predictor (the lobster's size) and the
response is whether the lobsters survived (label "1") or died (label "0").

> For the original paper, see [this link](https://www.sciencedirect.com/science/article/pii/S0022098115000039). For
what we can only guess is what marine biologists do in their labs, see [this image](http://i.imgur.com/dQDKgys.jpg) (
or this [possibly not-safe-for-work alternative](
http://web.archive.org/web/20120628012654/http://www.traemcneely.com/wp-content/uploads/2012/04/wpid-Lobster-Fights
-e1335308484734.jpeg)).
"""

# %% imports
from myimports import *
from lib.data.load.cse6040download import download_all, LOCAL_BASE


# %%
class RockLobsterData:
    # datasets = {'lobster_survive.dat.txt': '12fc1c22ed9b4d7bf04bf7e0fec996b7',
    #             'logreg_points_train.csv': '25bbca6105bae047ac4d62ee8b76c841',
    #             'log_likelihood_soln.npz': '5a9e17d56937855727afa6db1cd83306',
    #             'grad_log_likelihood_soln.npz': 'a67c00bfa95929e12d423105d8412026',
    #             'hess_log_likelihood_soln.npz': 'b46443fbf0577423b084122503125887'}
    datasets = {'lobster_survive.dat.txt': None,
                'logreg_points_train.csv': None,
                'log_likelihood_soln.npz': None,
                'grad_log_likelihood_soln.npz': None,
                'hess_log_likelihood_soln.npz': None}
    local_suffix = 'rock-lobster/'
    url_suffix = 'rock-lobster/'

    @staticmethod
    def load_these_lobsters(temp=False, plot=False):

        download_all(RockLobsterData.datasets, local_suffix=RockLobsterData.local_suffix,
                     url_suffix=RockLobsterData.url_suffix)

        local_dir = "{}{}".format(LOCAL_BASE, RockLobsterData.local_suffix)
        df_lobsters = pd.read_table('{}lobster_survive.dat.txt'.format(local_dir),
                                    sep=r'\s+', names=['CarapaceLen', 'Survived'])
        print(df_lobsters.head())
        print("...")
        print(df_lobsters.tail())

        if plot:
            RockLobsterData.plot_these_lobsters(df_lobsters)

        if temp:
            RockLobsterData.remove_data()
        return df_lobsters

    @staticmethod
    def plot_these_lobsters(df_lobsters: pd.DataFrame):
        ax = sns.violinplot(x="Survived", y="CarapaceLen",
                            data=df_lobsters, inner="quart")
        ax.set(xlabel="Survived? (0=no, 1=yes)",
               ylabel="",
               title="Body length (carpace, in mm) vs. survival")
        return

    @staticmethod
    def remove_data():
        local_base = "{}{}".format(LOCAL_BASE, RockLobsterData.url_suffix)
        for filename, _ in RockLobsterData.datasets:
            local_file = "{}{}".format(local_base, filename)
            if os.path.exists(local_file):
                os.remove(local_file)
        if os.path.exists(local_base):
            os.removedirs(local_base)
        return

# %%


# %%

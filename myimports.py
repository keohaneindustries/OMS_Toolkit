#%% imports
import numpy as np
import pandas as pd
import sys
import os
import re
from collections import OrderedDict, namedtuple
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import time
from timeit import timeit
import itertools
import functools
import datetime as dt
import random
import scipy as sp
import scipy.linalg
import seaborn as sns
from statsmodels import regression
import statsmodels.stats as stats
import statsmodels.api as sm
import argparse
import sklearn as skl
from pprint import pprint
import lib.data.load.cse6040download as cse
#%%
import pandas as pd
from pandas.tseries.offsets import CDay
from pandas.tseries.holiday import AbstractHolidayCalendar, nearest_workday, Holiday
from pandas.tseries.holiday import USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay, USLaborDay
from pandas.tseries.holiday import USThanksgivingDay
# NYD, IND, XMAS

AbstractHolidayCalendar.holidays

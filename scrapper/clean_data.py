# %%
import glob
import tabula
import urllib
import urllib.request
from bs4 import BeautifulSoup
import os
import json
import csv
import pandas as pd
import numpy as np
from dateutil.parser import ParserError
import re


# %%
fileDir = os.path.dirname(os.path.realpath('__file__'))
files_dir = os.path.join(fileDir, "downloads")
csv_all_in_one = pd.read_csv(os.path.join(files_dir, 'merged.csv'))
# csv_all_in_one.head()


# %%
# add unique column
csv_all_in_one["identifier"] = range(1, len(csv_all_in_one)+1)
csv_all_in_one.set_index('identifier', inplace=True)

# slice file urls into file names
csv_all_in_one["filename"] = csv_all_in_one["file"].apply(
    lambda x: x.split('\\')[9])
csv_all_in_one.drop(columns="file", inplace=True)
csv_all_in_one = csv_all_in_one.replace(',', '', regex=True)
#csv_all_in_one = csv_all_in_one.replace(np.nan, 0)
#csv_all_in_one.drop(columns=["file",  "Unnamed: 0"], inplace=True)


# csv_all_in_one.head()

# %%
csv_all_in_one.columns = csv_all_in_one.columns.str.replace("|\\r|\\n", "-")
# print(csv_all_in_one.columns)


# %%
pattern_amt_o = re.compile(r"^\w")
pattern_debt_cat = re.compile(r'(Total | Debt | FGN)')

# amt_o = csv_all_in_one["Amount Outstanding in-USD"].str.contains(pattern_amt_o)
# amt_o.head(n=20)

# %%
# na set to false because columns contain multiple value types. String, nan, numeric, say. Thus nan is handled as false vlues not meeting the truthy conditions.
debt_cat_true = [(csv_all_in_one["Debt Category"].str.contains("Debt|FGN|Total", regex=True, na=False)),
                 csv_all_in_one["Amount Outstanding in-USD"].str.contains(
                     pattern_amt_o, na=False),
                 csv_all_in_one["Unnamed: 0.1"].str.contains(
                     "[D]ebt|[T]otal|FGN", regex=True, na=False)
                 ]

debt_cat_then = [csv_all_in_one["Debt Category"],
                 csv_all_in_one["Amount Outstanding in-USD"],
                 csv_all_in_one["Unnamed: 0.1"]
                 ]


csv_all_in_one["debt_cat"] = np.select(debt_cat_true,
                                       debt_cat_then,
                                       default=np.nan)
# %%
pattern_amt_usd = re.compile(r"Total|Debt")
amt_in_USD_inM_true = [np.logical_and((csv_all_in_one["Amount Outstanding in-USD"].str.contains(pattern_amt_o, regex=True, na=False)),
                                      csv_all_in_one["Amount Outstanding in-NGN"].isnull()),
                       csv_all_in_one["Amount Outstanding in-USD"].str.contains(
                           pattern_amt_o, regex=True, na=False),
                       csv_all_in_one["Debt Category"].str.contains(
                           pattern_amt_usd, regex=True, na=False)
                       ]


amt_in_USD_inM_then = [csv_all_in_one["Amount Outstanding-in NGN"],
                       csv_all_in_one["Amount Outstanding in-NGN"],
                       csv_all_in_one["Amount Outstanding in-USD"]
                       ]


csv_all_in_one["amt_in_USD_inM"] = np.select(amt_in_USD_inM_true,
                                             amt_in_USD_inM_then,
                                             default=np.nan)

# %%

csv_all_in_one["amt_in_USD_inM"] = np.where((csv_all_in_one["Debt Category"].str.contains(pattern_amt_usd, regex=True, na=False)) &
                                            (csv_all_in_one["Amount Outstanding in-NGN"].isnull()) &
                                            (csv_all_in_one["Amount Outstanding-in NGN"].isnull()),
                                            csv_all_in_one["Unnamed: 1"],
                                            csv_all_in_one["amt_in_USD_inM"])


# %%
# useful commands
# csv_all_in_one.loc[3]
# csv_all_in_one.to_csv(os.path.join(files_dir, 'merged_wip_.csv'))
# csv_all_in_one[csv_all_in_one["Debt Category"] == "Grand-Total (A+B)"]
# csv_all_in_one["Debt Category"].unique()

# %%
# if true
amt_in_NGN_inM_true = [csv_all_in_one["Debt Category"] == "Grand-Total (A+B)",
                       np.logical_and(csv_all_in_one["Debt Category"] == "Grand-Total (A+B)",
                                      csv_all_in_one["Amount Outstanding in-NGN"].isnull()),
                       (csv_all_in_one["Debt Category"] == "Grand-Total (A+B)") & (csv_all_in_one["Amount Outstanding in-NGN"].isnull()) & (csv_all_in_one["Amount Outstanding-in NGN"].isnull())]

# the take
amt_in_NGN_inM_then = [csv_all_in_one["Amount Outstanding in-NGN"],
                       csv_all_in_one["Amount Outstanding-in NGN"],
                       csv_all_in_one["Amount Outstanding in NGN"]]
# psor values
csv_all_in_one["amt_in_NGN_inM"] = np.select(amt_in_NGN_inM_true,
                                             amt_in_NGN_inM_then,
                                             default=np.nan)

csv_all_in_one.head(n=30)

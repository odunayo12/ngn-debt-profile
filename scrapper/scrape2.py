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
# %% page fetcher function


def make_soup(url):
    the_page = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(the_page, 'html.parser')
    return soup_data


# %% fetch the page
soup = make_soup(
    'https://www.dmo.gov.ng/debt-profile/total-public-debt?filter%5Bsearch%5D=&limit=100')

i = 1

# %% gets current file directory
fileDir = os.path.dirname(os.path.realpath('__file__'))

# %% crawler loop
# locates all spans with class 'whitespace_preserver' in the table tag
for record in soup.table.findAll('span', {'class', 'whitespace_preserver'}):
    # print(record.text)
    # locates all anchor, 'a' tags
    for data in record.findAll('a'):
        #print('https://www.dmo.gov.ng' + data.get('href'))
        # print(data.text)
        #pdf = data.get('title')
        # adds the suffix and prefix addresses
        pdf = 'https://www.dmo.gov.ng' + data.get('href') + "/file"
        # print(pdf)
        # should any tag not have data-id the following catches the error and and affix a custom name to the pdf
        try:
            # sets pdf name to its data-id value
            pdf_title = data.get('data-id') + '.pdf'
            #pdf_title = data.text
        except TypeError:
            # if pdf_title == "":
            pdf_title = str(i)
            i = i+1 + ".pdf"
        else:
            filename = pdf_title
            # sets the download destination to
            filepath = os.path.join(fileDir, "downloads", filename)
        # opens, reads and close each file
        pdf_file = open(filepath, "wb")
        pdf_file.write(urllib.request.urlopen(pdf).read())
        pdf_file.close()

# join paths
files_dir = os.path.join(fileDir, "downloads")
import_files_dir = os.path.join(files_dir, '*.pdf')
import_files = [
    folder_content for folder_content in glob.glob(import_files_dir)]
# extract the whole pdf in the directory and convert to csv
for pdf_filepath in import_files:
    csv_filepath = pdf_filepath.replace('.pdf', '.csv')
    tabula.convert_into(pdf_filepath, csv_filepath,
                        lattice=True,  output_format="csv", pages="all")


# %%
all_csv_files = glob.glob(os.path.join(files_dir, '*.csv'))
# all_files
df_from_file = [item for item in all_csv_files]
#csv_merge = pandas.concat([pandas.read_csv(f) for f in df_from_file], ignore_index=True)

# %%
li = []

for each_file in all_csv_files:
    csv_merge = pd.read_csv(
        each_file, sep=',', encoding='unicode_escape', error_bad_lines=False)
    csv_merge['file'] = each_file.split('/')[-1]
    li.append(csv_merge)

all_merged = pd.concat(li)
all_merged.to_csv(os.path.join(files_dir, 'merged.csv'))
# all_merged.tail(n=10)

# https://realpython.com/python-data-cleaning-numpy-pandas/


# %%
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

# csv_all_in_one.loc[3]
# csv_all_in_one.head()

# %%
csv_all_in_one.columns = csv_all_in_one.columns.str.replace("|\\r|\\n", "-")
# print(csv_all_in_one.columns)
# %%
pattern_amt_o = re.compile(r"^\w")


amt_o = csv_all_in_one["Amount Outstanding in-USD"].str.contains(pattern_amt_o)
amt_o.head(n=20)

# %%

csv_all_in_one["debt_cat"] = np.where(csv_all_in_one["Debt Category"]
                                      == "Grand-Total (A+B)", csv_all_in_one["Debt Category"],
                                      np.where(csv_all_in_one["Amount Outstanding in-USD"].str.contains(pattern_amt_o), csv_all_in_one["Amount Outstanding in-USD"], ""))

csv_all_in_one.head(n=10)
# %%

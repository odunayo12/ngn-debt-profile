# %%
import glob
import tabula
import urllib
import urllib.request
from bs4 import BeautifulSoup
import os
import json
import csv
import pandas
from dateutil.parser import ParserError
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
files_dir = os.path.join(fileDir, "downloads")
# files_dir
# %%
all_csv_files = glob.glob(os.path.join(files_dir, '*.csv'))
# all_files
df_from_file = [item for item in all_csv_files]
#csv_merge = pandas.concat([pandas.read_csv(f) for f in df_from_file], ignore_index=True)

# %%
li = []

for each_file in all_csv_files:
    csv_merge = pandas.read_csv(
        each_file, sep=',', encoding='unicode_escape', error_bad_lines=False)
    csv_merge['file'] = each_file.split('/')[-1]
    li.append(csv_merge)

all_merged = pandas.concat(li)
all_merged.to_csv(os.path.join(files_dir, 'merged.csv'))
# all_merged.tail(n=10)

# https://realpython.com/python-data-cleaning-numpy-pandas/


# %%
# csv_merge = pandas.read_csv(df_from_file, sep=',',
#                             encoding='unicode_escape', error_bad_lines=False)
# csv_merge
# files_dir = os.path.join(fileDir, "downloads")
# files_dir
# files_dir2 = "C:/Users/rotim/OneDrive - bwedu/Web Developmnet/ngn-debt-profile/scrapper/downloads"
# # %%
# tabula.convert_into_by_batch(files_dir, output_format='csv', pages=all)


# # %%
# # %%
# import_files_dir = os.path.join(files_dir, '*.pdf')

# # %%
# import_files = [
#     folder_content for folder_content in glob.glob(import_files_dir)]
# # %%
# for pdf_filepath in import_files:
#     csv_filepath = pdf_filepath.replace('.pdf', '.csv')
#     tabula.convert_into(pdf_filepath, csv_filepath,
#                         lattice=True,  output_format="csv", pages="all")
# # %%

# %%

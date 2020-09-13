# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#import bs4
from multiprocessing.pool import ThreadPool
from time import time
import requests
import os
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup


# %%
my_url = 'https://www.dmo.gov.ng/debt-profile/total-public-debt?filter%5Bsearch%5D=&limit=100'


# %%
ureq(my_url)


# %%
uClient = ureq(my_url)  # opens the address


# %%
page_html = uClient.read()  # stores the page's html cotent in a variable


# %%
uClient.close()  # closes the address


# %%
page_soup = soup(page_html, 'html.parser')  # html parser


# %%
page_soup.body.table.span


# %%
# grabs each span with class whitespace_preserver
media_files = page_soup.table.findAll(
    'span', {'class', 'whitespace_preserver'})


# %%
len(media_files)  # length of divs
# media_files


# %%
media_files[0]

# %% Prints the data-id attribute of each 'a' tag
for item in media_files:
    for tag_a in item.findAll('a'):
        print(tag_a.get('data-id'))
# %%
media_download = media_files[1]


# %%
media_downloads = media_files[1].a["href"]


# %%
# continue at https://youtu.be/XQgXKtPSzUI?t=1003
media_download.a['href']
media_download.a['data-id']


# %%
media_downloads


# %%
file_addresses = []


# %%
for item in media_files:
    try:
        download_address = 'https://www.dmo.gov.ng' + item.a['href'] + '/file'
        #download_address_id = item.a['data-id']
    except TypeError:
        print("")
    else:
        #print('(' + "'" + download_address_id  + "'," + " '" + download_address + "')" )
        file_addresses.append(download_address)


# %%
print(file_addresses)

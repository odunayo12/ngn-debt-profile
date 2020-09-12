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
page_soup.body.span


# %%
# grabs each div with class koowa_media__item
media_files = page_soup.findAll('span', {'class', 'whitespace_preserver'})


# %%
len(media_files)  # length of divs
# media_files


# %%
media_files[1]


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
        # note that item is now the new name and has to replace media_files
        download_address = 'https://www.dmo.gov.ng' + item.a['href']
        download_address_id = item.a['data-id']
    except TypeError:
        print("")
    else:
        #print('(' + "'" + download_address_id  + "'," + " '" + download_address + "')" )
        to_append = '(' + "'" + download_address_id + \
            "'," + " '" + download_address + "')"
        file_addresses.append(to_append)


# %%
print(file_addresses)


# %%


# %%
# https://stackoverflow.com/questions/918154/relative-paths-in-python
fileDir = os.path.dirname(os.path.realpath('__file__'))
print(fileDir)


# %%
# https://likegeeks.com/downloading-files-using-python/
def url_response(url):
    fileName, url = url
    r = requests.get(url, stream=True)
    with open(fileName, 'wb') as f:
        for ch in r:
            f.write(ch)


# %%


# %%
for x in file_addresses:
    url_response(x)


# %%
my_list = [1, 2, 3]
# new_list = [x, ", Event"+1 for x in my_list]
# new_list

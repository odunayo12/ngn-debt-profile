# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#import bs4
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup


# %%
my_url = 'https://www.dmo.gov.ng/debt-profile/total-public-debts?limit=20&limitstart=0'


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
media = page_soup.findAll('div', {'class', 'koowa_media__item'})


# %%
len(media)  # length of divs


# %%
media[0]

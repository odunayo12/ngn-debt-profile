# %%
import urllib
import urllib.request
from bs4 import BeautifulSoup
import os

# %%


def make_soup(url):
    the_page = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(the_page, 'html.parser')
    return soup_data


# %%
soup = make_soup(
    'https://www.dmo.gov.ng/debt-profile/total-public-debt?filter%5Bsearch%5D=&limit=100')

i = 1
# %%
fileDir = os.path.dirname(os.path.realpath('__file__'))

# %%

# %%
for record in soup.findAll('span', {'class', 'whitespace_preserver'}):
    # print(record.text)
    for data in record.findAll('a'):
        #print('https://www.dmo.gov.ng' + data.get('href'))
        # print(data.text)
        #pdf = data.get('title')
        pdf = 'https://www.dmo.gov.ng' + data.get('href')
        # print(pdf)

        pdf_title = data.get('title')
        if pdf_title == "":
            filename = str(i)
            i = i+1 + ".pdf"
        else:
            filename = pdf_title
            filepath = os.path.join(fileDir, "downloads", filename)

        pdf_file = open(filename, "wb")
        pdf_file.write(urllib.request.urlopen(pdf).read())
        pdf_file.close()


# %%
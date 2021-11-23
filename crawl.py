# Requests + BeautifulSoup
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Define a site, header request object, and create a request.
site = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site, headers=hdr)

# The following try statement catches and prints any HTTP error that BeautifulSoup encounters when opening the website at the URL.
try:
    page = urlopen(req)
except HTTPError as err:
    print(err.code)
    # if err.code == 403:
    #     print(err.code)
    # else:

# Create an object to parse the HTML format
soup = BeautifulSoup(page, 'html.parser')

# Retrieve all popular news links (Fig. 1)
paragraphs = []
links = []
#for i in soup.find('div', {'class':'outer-wrap'}).find_all('a'):
for j in soup.find_all('div', {'class':'mw-parser-output'}):
    for i in j.find_all('p'):
        #print (i.text)
        paragraphs.append(i.text)

        # find each of the <a> elements to identify links.
        for k in i.find_all('a'):
            #print (k['href'])
            links.append(k['href'])

# Print a summary of findings.
print('Number of Paragraphs: ' + str(len(paragraphs)))
print('Number of Links: ' + str(len(links)))



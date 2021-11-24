# Jacob Isber
# File:
# Desc:
# Requests + BeautifulSoup
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError



class WebCrawler():
    def __init__(self, root, verbose):
        self.root = root
        self.verbose = verbose

    def get_documents(self):
        pass

    def set_documents(self, d):
        pass

    def get_links(self):
        pass

    def collect(self, s, d):
        pass

    def crawl(self):

        def findAllDiv(clas):
            # for i in soup.find('div', {'class':'outer-wrap'}).find_all('a'):
            for j in soup.find_all('div', {'class': clas}):
                for i in j.find_all('p'):
                    # print (i.text)
                    if i.text != '':
                        paragraphs.add(i.text)

                    # find each of the <a> elements to identify links.
                    for k in i.find_all('a'):
                        # print (k['href'])
                        links.append(k['href'])

        def findAllTable(clas):
            # for i in soup.find('div', {'class':'outer-wrap'}).find_all('a'):
            for j in soup.find_all('table', {'class': clas}):
                    # print (i.text)
                    tables.add(j.text)

        # Define a site, header request object, and create a request.
        site = self.root
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)
        # The following try statement catches and prints any HTTP error that BeautifulSoup encounters when opening
        # the website at the URL.
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
        paragraphs = set()
        tables = set()
        links = []

        findAllDiv("entry-content")
        findAllDiv("person_content")
        findAllTable("table_default")

        print(paragraphs)
        print(tables)
        # Print a summary of findings.
        print('Number of Paragraphs: ' + str(len(paragraphs)))
        print('Number of Links: ' + str(len(links)))

    def clean(self):
        pass

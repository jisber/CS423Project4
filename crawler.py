# Jacob Isber
# File:
# Desc:
# Requests + BeautifulSoup
import string

import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import re


class WebCrawler():
    def __init__(self, root, verbose):
        self.root = root
        self.verbose = verbose
        self.links = None
        self.paragraphs = None
        self.tables = None

    def get_documents(self):
        print("Returning documents")
        document_list = self.clean(self.paragraphs)
        return document_list

    def set_documents(self, d):
        pass

    def get_links(self):
        print("Returning Links")
        print(self.links)
        return self.links

    def set_links(self, l):
        self.links = l

    def collect(self, s, d):
        # Define a site, header request object, and create a request.
        site = s
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
        paragraphs = []

        links = []

        for k in soup.find_all('a', href=True):

            expected_string = (k['href'])
            if "http" in expected_string:
                if k['href'].find("utk.edu") != -1:
                    links.append(k['href'])
            elif "https" in expected_string:
                if k['href'].find("utk.edu") != -1:
                    links.append(k['href'])

        links = list(set(links))
        print(links)

        new_links = []
        if d >= 1:
            for i in links:
                site = i
                hdr = {'User-Agent': 'Mozilla/5.0'}
                req = Request(site, headers=hdr)

                try:
                    page = urlopen(req)
                except HTTPError as err:
                    print(err.code)

                soup = BeautifulSoup(page, 'html.parser')
                for k in soup.find_all('a', href=True):
                    expected_string = (k['href'])
                    if "http" in expected_string:
                        if k['href'].find("utk.edu") != -1:
                            new_links.append(k['href'])
                    elif "https" in expected_string:
                        if k['href'].find("utk.edu") != -1:
                            new_links.append(k['href'])

        new_links = new_links + links
        new_links = list(set(new_links))

        self.set_links(new_links)

        # Print a summary of findings.
        print('Number of Paragraphs: ' + str(len(paragraphs)))
        print('Number of Links: ' + str(len(links)))

        print('Number of New Links: ' + str(len(new_links)))


    # def crawl(self):
    #
    #     def findAllDiv(clas):
    #         # for i in soup.find('div', {'class':'outer-wrap'}).find_all('a'):
    #         for j in soup.find_all('div', {'class': clas}):
    #             for i in j.find_all('p'):
    #                 # print (i.text)
    #                 if i.text != '':
    #                     paragraphs.add(i.text)
    #
    #                 # find each of the <a> elements to identify links.
    #                 for k in i.find_all('a'):
    #                     # print (k['href'])
    #                     links.append(k['href'])
    #
    #     def findAllTable(clas):
    #         # for i in soup.find('div', {'class':'outer-wrap'}).find_all('a'):
    #         for j in soup.find_all('table', {'class': clas}):
    #                 # print (i.text)
    #                 tables.add(j.text)
    #
    #     # Define a site, header request object, and create a request.
    #     site = self.root
    #     hdr = {'User-Agent': 'Mozilla/5.0'}
    #     req = Request(site, headers=hdr)
    #     # The following try statement catches and prints any HTTP error that BeautifulSoup encounters when opening
    #     # the website at the URL.
    #     try:
    #         page = urlopen(req)
    #     except HTTPError as err:
    #         print(err.code)
    #         # if err.code == 403:
    #         #     print(err.code)
    #         # else:
    #
    #     # Create an object to parse the HTML format
    #     soup = BeautifulSoup(page, 'html.parser')
    #
    #     # Retrieve all popular news links (Fig. 1)
    #     paragraphs = set()
    #     tables = set()
    #     links = []
    #
    #     findAllDiv("entry-content")
    #     findAllDiv("person_content")
    #     findAllTable("table_default")
    #
    #     self.links = links
    #     self.paragraphs = paragraphs
    #     self.tables = tables
    #
    #     print(links)
    #     print(paragraphs)
    #     print(tables)
    #     # Print a summary of findings.
    #     print('Number of Paragraphs: ' + str(len(paragraphs)))
    #     print('Number of Links: ' + str(len(links)))
    #
    #     return paragraphs, links, tables

    def clean(self, text_list):

        decode_list = []

        for i in text_list:

            # Removes all uni - code
            strencode = i.encode("ascii", "ignore")
            strdecode = strencode.decode()

            # Removes all twitter handels
            strdecode = re.sub('@[^\s]+','',strdecode)

            # Removes all punctuation
            strdecode = re.sub(' +', ' ',strdecode)

            # Removes double space
            strdecode = strdecode.translate(str.maketrans('', '', string.punctuation))

            # Converts to lower case
            strdecode = strdecode.lower()

            # Appends to new list
            decode_list.append(strdecode)

        return decode_list

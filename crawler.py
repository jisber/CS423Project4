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
        #self.paragraphs = None
        self.tables = None
        self.documents = None
        self.link_doc_dict = {}
    def get_documents(self):
        #print("CLEANING TEXT - STARTED")
        #print(self.documents)
        #print("CLEANING TEXT - DONE")
        return self.documents

    def set_documents(self, d):
        self.documents = d

    def get_links(self):
        print("Returning Links")
        #print(self.links)
        return self.links

    def set_links(self, l):
        self.links = l

    def collect(self, s, d):

        if self.verbose == 't':
            print("COLLECTING LINKS - STARTED")

        # Define a site, header request object, and create a request.
        site = s
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers=hdr)

        # The following try statement catches and prints any HTTP error that BeautifulSoup encounters when opening
        # :the website at the URL.
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

        counter = 1
        for k in soup.find_all('a', href=True):
            if self.verbose == 't':
                print("COLLECTED: LINK(" + str(counter) + ")")

            expected_string = (k['href'])
            if "http" in expected_string:
                if k['href'].find("utk.edu") != -1:
                    links.append(k['href'])
                    counter += 1
            elif "https" in expected_string:
                if k['href'].find("utk.edu") != -1:
                    links.append(k['href'])
                    counter += 1

        links = list(set(links))

        new_links = []
        if d >= 1:
            for i in links:
                if self.verbose == 't':
                    print("COLLECTED: LINK(" + str(counter) + ")")
                    counter += 1
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

        if self.verbose == 't':
            print("COLLECTING LINKS - DONE")
        # # Print a summary of findings.
        # print('Number of Paragraphs: ' + str(len(paragraphs)))
        # print('Number of Links: ' + str(len(links)))
        #
        # print('Number of New Links: ' + str(len(new_links)))


    def crawl(self):

        if self.verbose == 't':
            print("CRAWLING LINKS - STARTED")

        # Retrieve all popular news links (Fig. 1)
        paragraphs = []
        tables = []
        links = []

        counter = 0

        link_counter = -1
        for i in self.links:
            print("ON LINK", link_counter)
            temp = []
            if self.verbose == 't':
                print("CRAWLING: LINK(" + str(counter) + ")")
                counter += 1

            site = i
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(site, headers=hdr)

            try:
                page = urlopen(req)
            except:
                link_counter += 1
                continue
            # except HTTPError as err:
            #     print(err.code)
                # if err.code == 403:
                #     print(err.code)
                # else:

            # Create an object to parse the HTML format
            soup = BeautifulSoup(page, 'html.parser')

            for j in soup.find_all('div', {'class': "entry-content"}):
                for i in j.find_all('p'):
                    if i.text != '':
                        temp = i.text
                        temp = str(link_counter) + temp + str(link_counter)
                        paragraphs.append(temp)

            for j in soup.find_all('div', {'class': "person_content"}):
                for i in j.find_all('p'):
                    if i.text != '':
                        temp = i.text
                        temp = temp + str(link_counter)
                        paragraphs.append(temp)

            for j in soup.find_all('table', {'class': "table_default"}):
                if j.text != '':
                    temp = j.text
                    temp = temp + str(link_counter)
                    paragraphs.append(temp)

            link_counter += 1

        self.set_documents(paragraphs)

        #print("DICT", self.link_doc_dict)

        if self.verbose == 't':
            print("CRAWLING LINKS - DONE")

    def clean(self, text_list):

        print("CLEANING TEXT - STARTED")
        decode_list = []

        print(len(text_list))

        for i in text_list:
            # Removes all uni - code
            strencode = i.encode("ascii", "ignore")
            strdecode = strencode.decode()

            # Removes all twitter handels
            strdecode = re.sub('@[^\s]+','',strdecode)

            # Removes all punctuation
            strdecode = re.sub(' +', ' ',strdecode)

            strdecode = strdecode.strip()

            # Removes double space
            strdecode = strdecode.translate(str.maketrans('', '', string.punctuation))

            # Converts to lower case
            strdecode = strdecode.lower()

            # Appends to new list
            decode_list.append(strdecode)

        print("CLEANING TEXT - DONE")
        return decode_list

import string

import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import re


class WebCrawler():

    def __init__(self, root, verbose):
        """
        Default constructor for WebCrawler
        :param root: link
        :param verbose: t or f variable that is used to print debugging information
        """
        self.root = root
        self.verbose = verbose
        self.links = None
        self.tables = None
        self.documents = None
        self.link_doc_dict = {}

    def get_documents(self):
        """
        Gets the documents
        :return: list of documents
        """
        return self.documents

    def set_documents(self, d):
        """
        Sets the documents
        :param d: list of documents
        :return: None
        """
        self.documents = d

    def get_links(self):
        """
        Gets the links
        :return: All links
        """
        return self.links

    def set_links(self, l):
        """
        Takes in a list and sets the links
        :param l: list of links
        :return: None
        """
        self.links = l

    def collect(self, s, d):
        """
        Grabs all the links possible from the provided link
        :param s: Start Link
        :param d: Depth
        :return: None
        """
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
        # First interation that goes through and grabs all the original links on depth 0
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
        depth_counter = 0

        # If the depth is greater than 0 go through the original links and grab all the links in a recurring way
        if d >= 1:
            while depth_counter <= d:
                print("YOU ARE AT DEPTH ", depth_counter)
                for i in links:
                    print("ON LINK", i)
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

                depth_counter += 1
                new_links = new_links + links
                new_links = list(set(new_links))
        else:
            new_links = new_links + links
            new_links = list(set(new_links))

        # Set the links
        self.set_links(new_links)

        print(len(self.links))
        print(self.links)
        if self.verbose == 't':
            print("COLLECTING LINKS - DONE")

    def crawl(self):
        """
        Crawls all through links and collects all thr paragrpahs
        :return: None
        """
        if self.verbose == 't':
            print("CRAWLING LINKS - STARTED")

        # Retrieve all popular news links (Fig. 1)
        paragraphs = []

        counter = 0

        link_counter = -1

        # Starts the for loop to go and grab every link
        for i in self.links:
            link_counter += 1
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
                continue

            # Create an object to parse the HTML format
            soup = BeautifulSoup(page, 'html.parser')

            # Grabs all entry-content, person_content, table_default from the text
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
                        temp = str(link_counter) + temp + str(link_counter)
                        paragraphs.append(temp)

            for j in soup.find_all('table', {'class': "table_default"}):
                if j.text != '':
                    temp = j.text
                    temp = str(link_counter) + temp + str(link_counter)
                    paragraphs.append(temp)

        self.set_documents(paragraphs)

        if self.verbose == 't':
            print("CRAWLING LINKS - DONE")

    def clean(self, text_list):
        """
        My clean function that clenses the text
        :param text_list: List of paragraphs
        :return: a list of clean paragraphs
        """
        print("CLEANING TEXT - STARTED")
        decode_list = []

        print(len(text_list))

        for i in text_list:
            # Removes all uni - code
            strencode = i.encode("ascii", "ignore")
            strdecode = strencode.decode()

            # Removes all twitter handels
            strdecode = re.sub('@[^\s]+', '', strdecode)

            # Removes all punctuation
            strdecode = re.sub(' +', ' ', strdecode)

            strdecode = strdecode.strip()

            # Removes double space
            strdecode = strdecode.translate(str.maketrans('', '', string.punctuation))

            # Converts to lower case
            strdecode = strdecode.lower()

            # Appends to new list
            decode_list.append(strdecode)

        print("CLEANING TEXT - DONE")
        return decode_list

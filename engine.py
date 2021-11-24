# Jacob Isber
# File:
# Desc:

import crawler
import interface


class SearchEngine():

    def __init__(self, root, mode, query, verbose):
        self.root = root
        self.mode = mode
        self.query = query
        self.verbose = verbose

        # self.engine = SearchEngine(self.root, self.mode, self.query, self.verbose)

        self.crawl = crawler.WebCrawler(self.root, self.verbose)
        self.interface = interface.SearchInterface(self.mode, SearchEngine, self.query)

    def start(self):
        print("Running start")

    def delete(self):
        print("Running delete")

    def train(self):
        print("Running train")

    def exit(self):
        print("Exiting")

# Jacob Isber
# File:
# Desc:
import os

import crawler
import interface
from sklearn.feature_extraction.text import TfidfVectorizer
import re, string
import pandas as pd
import numpy as np
from os import path
import pickle
import warnings


class SearchEngine():

    def __init__(self, root, mode, query, verbose):
        self.root = root
        self.mode = mode
        self.query = query
        self.verbose = verbose

        # self.engine = SearchEngine(self.root, self.mode, self.query, self.verbose):exi
        self.crawl = crawler.WebCrawler(self.root, self.verbose)
        self.interface = interface.SearchInterface(self.mode, self, self.query)
        self.clean_docs = []
        self.links = []

    def start(self):
        print("Running start")
        self.listen()

    def delete(self):
        print("Running delete")
        docFile = 'docs.pickle'
        linksFile = 'links.pickle'
        if os.path.isfile(docFile):
            os.remove(docFile)
        if os.path.isfile(linksFile):
            os.remove(linksFile)

    def train(self):

        trigger = 0
        if path.exists("docs.pickle"):
            if path.exists("links.pickle"):
                with open("docs.pickle", 'rb') as f:
                    self.clean_docs = pickle.load(f)

                with open("links.pickle", 'rb') as f:
                    self.links = pickle.load(f)

                print(self.links)
                trigger = 1

        if trigger == 0:
            print("Running train")
            self.crawl.collect(self.root, 0)
            self.crawl.crawl()
            doc = self.crawl.get_documents()
            links = self.crawl.get_links()
            clean_doc = self.crawl.clean(doc)
            self.clean_docs = clean_doc

            with open("docs.pickle", 'wb') as f:
                pickle.dump(self.clean_docs, f)

            with open("links.pickle", 'wb') as f:
                pickle.dump(links, f)

        self.compute_td_idf()

    def exit(self):
        print("Exiting")
        exit()

    def handle_query(self, var):
        print("Handeling query")
        self.query = var
        self.compute_td_idf()

    def listen(self):
        print("Listening")
        self.interface.listen()

    def compute_td_idf(self):
        print("Computing td idf")

        # Step 2: Vectorize the documents
        # Use the Scikit-learn built-in vectorizer.

        # Instantiate the Tfidfvectorizer
        tfidf_vectorizer = TfidfVectorizer()

        # Send our docs into the Vectorizer
        tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(self.clean_docs)

        # Transpose the result into a more traditional TF-IDF matrix, and convert it to an array.
        X = tfidf_vectorizer_vectors.T.toarray()

        # Convert the matrix into a dataframe using feature names as the dataframe index.
        df = pd.DataFrame(X, index=tfidf_vectorizer.get_feature_names())

        # [ RETRIEVAL STAGE ]

        query = self.query
        print(self.query)

        # Vectorize the query.
        q = [query]
        q_vec = tfidf_vectorizer.transform(q).toarray().reshape(df.shape[0], )

        # Calculate cosine similarity.
        sim = {}
        for i in range(len(df.columns) - 1):
            sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)

        # Sort the values
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)


        # Print the articles and their similarity values
        print(self.clean_docs)

        num = 0
        if len(self.links) < 100:
            num = 2
        elif len(self.links) < 1000:
            num = 3
        elif len(self.links) < 10000:
            num = 4

        for k, v in sim_sorted:
            if v > 0:
                index = self.clean_docs[k]
                index = index[:num]
                index = re.sub("[^0-9]", "",index)
                print(str(self.links[int(index) + 1]) + " [DOCUMENT " + str(k) + "] - (" + str("{:.2f}".format(v)) + ')')


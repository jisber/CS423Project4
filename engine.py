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

    def __init__(self, root, mode, query, verbose, depth):
        """
        Default constructor for SearchEngine
        :param root: Link
        :param mode: interactive (i) or command-line (c)
        :param query: Query Key
        :param verbose: t or f variable that is used to print debugging information
        :param depth: Depth to collect links at
        """
        self.root = root
        self.mode = mode
        self.query = query
        self.verbose = verbose
        self.depth = depth

        # self.engine = SearchEngine(self.root, self.mode, self.query, self.verbose):exi
        self.crawl = crawler.WebCrawler(self.root, self.verbose)
        self.interface = interface.SearchInterface(self.mode, self, self.query)
        self.clean_docs = []
        self.temp_docs = []
        self.links = []
        self.num = 2

    def start(self):
        """
        Calls self.listen and starts the entire search engine
        :return: None
        """
        self.listen()

    def delete(self):
        """
        Deletes pickle files
        :return: None
        """
        doc = 'docs.pickle'
        links = 'links.pickle'
        if os.path.isfile(doc):
            os.remove(doc)
        if os.path.isfile(links):
            os.remove(links)

    def train(self):
        """
        When ran, will either collect and crawl the links or load the information from pickle files
        :return: None
        """
        trigger = 0

        # If the pickle files exist load it
        if path.exists("docs.pickle"):
            if path.exists("links.pickle"):
                with open("docs.pickle", 'rb') as f:
                    self.clean_docs = pickle.load(f)

                with open("links.pickle", 'rb') as f:
                    self.links = pickle.load(f)

                trigger = 1

        if trigger == 0:
            # Else Run collect, crawl, and clean
            print("Running train")
            self.crawl.collect(self.root, self.depth)
            self.crawl.crawl()
            doc = self.crawl.get_documents()
            self.links = self.crawl.get_links()
            clean_doc = self.crawl.clean(doc)
            self.clean_docs = clean_doc

            with open("docs.pickle", 'wb') as f:
                pickle.dump(self.clean_docs, f)

            with open("links.pickle", 'wb') as f:
                pickle.dump(self.links, f)

            self.compute_td_idf()

    def exit(self):
        """
        Exits the program
        :return: None
        """
        exit()

    def handle_query(self, var):
        """
        Handles the query recieved from listen
        :param var: the query from var
        :return: None
        """

        # Calls train if the training set has not been ran before
        if len(self.clean_docs) <= 0:
            self.train()

        self.query = var

        # Computes td_idf
        df, tdif = self.compute_td_idf()
        # [ RETRIEVAL STAGE ]

        query = self.query
        #print(self.query)

        # Computes cosine similarities
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', 'invalid value encountered in double_scalars')
            # Vectorize the query.
            q = [query]
            q_vec = tdif.transform(q).toarray().reshape(df.shape[0], )
            # Calculate cosine similarity.
            sim = {}
            for i in range(len(df.columns) - 1):
                sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)

            # Sort the values
            sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

        # Print the articles and their similarity values
        # print(self.clean_docs)

        if len(self.links) < 100:
            self.num = 2
        elif len(self.links) < 1000:
            self.num = 3
        elif len(self.links) < 10000:
            self.num = 4

        # The rest of this is just how I print out the search answers

        used_links = []
        count = 1
        break_count = -1
        for k, v in sim_sorted:
            if v > 0:
                break_count = 1
                index = self.clean_docs[k]
                index = index[:self.num]
                index = re.sub("[^0-9]", "", index)
                if self.links[int(index)] not in used_links:
                    expected_string = self.links[int(index)][:5]
                    if expected_string == "https":
                        tmp_link = str(self.links[int(index)])
                        tmp_link = list(tmp_link)
                        tmp_link[4] = ''
                        tmp_link = "".join(tmp_link)
                        if tmp_link not in used_links:
                            print("[" + str(k) + "] " + str(self.links[int(index)]) + " - (" + str(
                                "{:.2f}".format(v)) + ')')
                            used_links.append(tmp_link)
                            count += 1
                            if count > 5:
                                break
                    else:
                        print("[" + str(k) + "] " + str(self.links[int(index)]) + " - (" + str(
                            "{:.2f}".format(v)) + ')')
                        used_links.append(self.links[int(index)])
                        count += 1
                        if count > 5:
                            break

        if break_count == -1:
            print("Your search did not match any documents")

    def listen(self):
        # Calls the listen interface
        self.interface.listen()

    def compute_td_idf(self):
        """
        Vectorized the documents that uses scikit-learn
        :return: dataframe and a tfidf_vectorized
        """

        # Step 2: Vectorize the documents
        # Use the Scikit-learn built-in vectorizer.
        # Instantiate the Tfidfvectorizer
        tfidf_vectorizer = TfidfVectorizer()

        # Send our docs into the Vectorizer
        tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(self.clean_docs)

        # Transpose the result into a more traditional TF-IDF matrix, and convert it to an array.
        X = tfidf_vectorizer_vectors.T.toarray()
        # Convert the matrix into a dataframe using feature names as the dataframe index.
        df = pd.DataFrame(X, index=tfidf_vectorizer.get_feature_names_out())

        return df, tfidf_vectorizer

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

    def __init__(self, root, mode, query, verbose, depth):
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
        self.listen()

    def delete(self):
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

                trigger = 1

        if trigger == 0:
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
        exit()

    def handle_query(self, var):
        if len(self.clean_docs) <= 0:
            self.train()

        self.query = var
        df, tdif = self.compute_td_idf()
        # [ RETRIEVAL STAGE ]

        query = self.query
        print(self.query)
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

        # num = 0
        if len(self.links) < 100:
            self.num = 2
        elif len(self.links) < 1000:
            self.num = 3
        elif len(self.links) < 10000:
            self.num = 4


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
                    print( "[" + str(count) + "] " + str(self.links[int(index)]) + " - (" + str("{:.2f}".format(v)) + ')')
                    used_links.append(self.links[int(index)])
                    count += 1
                    if count > 5:
                        break

        if break_count == -1:
            print("Your search did not match any documents")

    def listen(self):
        self.interface.listen()

    def compute_td_idf(self):
        # print(self.clean_docs[:12])
        #
        # def parse_string(i):
        #     tmp_l = i.split()
        #     tmp_str = tmp_l[0]
        #     index = re.sub("[^0-9]", "", tmp_str)
        #     return index
        #
        # con = 0
        # curr_para = None
        # tmp_para = []
        # for count, i in enumerate(self.clean_docs):
        #     curr_str = i
        #     next_str = self.clean_docs[count + 1]
        #     curr_str_para = parse_string(curr_str)
        #     next_str_para = parse_string(self.clean_docs[count + 1])
        #     if curr_str_para == next_str_para:
        #         curr_para = curr_str + next_str
        #     else:
        #         tmp_para.append(curr_para)
        #     con += 1
        #     if con == 12:
        #         print(tmp_para)
        #         exit()
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

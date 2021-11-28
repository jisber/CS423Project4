# Jacob Isber
# File:
# Desc:

import crawler
import interface
from sklearn.feature_extraction.text import TfidfVectorizer
import re, string
import pandas as pd
import numpy as np

class SearchEngine():

    def __init__(self, root, mode, query, verbose):
        self.root = root
        self.mode = mode
        self.query = query
        self.verbose = verbose

        # self.engine = SearchEngine(self.root, self.mode, self.query, self.verbose):exi
        self.crawl = crawler.WebCrawler(self.root, self.verbose)
        self.interface = interface.SearchInterface(self.mode, self, self.query)
        self.clean_docs = None

    def start(self):
        print("Running start")
        self.listen()

    def delete(self):
        print("Running delete")

    def train(self):
        print("Running train")
        self.crawl.collect(self.root, 0)
        self.crawl.crawl()
        doc = self.crawl.get_documents()
        links = self.crawl.get_links()
        clean_doc = self.crawl.clean(doc)
        self.clean_docs = clean_doc

        print("Writing to Docs")
        f = open("docs.pickle", 'a')
        for i in clean_doc:
            for j in i:
                print(j)
                if j != "\n":
                    f.write(j+"\n")
        f.close()

        print("Writing to Links")
        f = open("links.pickle", "a")
        for i in links:
            f.write(i + "\n")
        f.close()

        self.compute_td_idf()

    def exit(self):
        print("Exiting")
        exit()

    def handel_query(self, var):
        print("Handeling query")
        print(var)

    def listen(self):
        print("Listening")
        self.interface.listen()

    def compute_td_idf(self):
        print("Computing td idf")

        print(self.clean_docs[0])
        # Step 2: Vectorize the documents
        # Use the Scikit-learn built-in vectorizer.

        # Instantiate the Tfidfvectorizer
        tfidf_vectorizer = TfidfVectorizer()

        # Send our docs into the Vectorizer
        tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(self.clean_docs[0])

        # Transpose the result into a more traditional TF-IDF matrix, and convert it to an array.
        X = tfidf_vectorizer_vectors.T.toarray()

        # Convert the matrix into a dataframe using feature names as the dataframe index.
        df = pd.DataFrame(X, index=tfidf_vectorizer.get_feature_names())

        # [ RETRIEVAL STAGE ]

        query = 'and'

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
        for k, v in sim_sorted:
            if v != 0.0:
                print("[DOCUMENT " + str(k) + "] - (" + str("{:.2f}".format(v)) + ')')

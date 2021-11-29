from sklearn.feature_extraction.text import TfidfVectorizer 
import re, string
import pandas as pd
import numpy as np
 
# each of the folowing statements comes from one of the UTK EECS webpages.
docs=[
    "Min H. Kao, born in Chu-Shan, Taiwan, is Executive Chairman of Garmin Ltd., which designs and manufactures navigation and communication equipment. Kao co-founded Garmin in 1989 with the vision of enriching people’s lives by bringing Global Positioning System (GPS) technology to the consumer market.", 

    "Curious to learn more about where you would be living? Learn more about our vibrant and thriving community just minutes from hundreds of miles of natural greenways, the Great Smoky Mountain National Park, and a bustling downtown with new restaurants and shops popping up every year.",

    "The Min H. Kao Electrical Engineering and Computer Science Building is located on the corner of Cumberland Avenue and Estabrook Road. The 150,000-square-feet building holds offices, classrooms, laboratories, conference rooms, a 147-seat auditorium, and a sixth-floor terrace with stunning views of downtown Knoxville. It is also home to the Center for Ultra-wide-area Resilient Electric Energy Transmission Networks (CURENT), an NSF Engineering Research Center.", 

    "By 1896, the program was gaining steam with 85 students pursuing electrical engineering degrees. The influx of students and the addition of new equipment expanded the university’s electrical laboratory to its limits in Science Hall. The addition of Estabrook Hall to campus in 1899 made room for a new power plant in addition to experimental labs.", 

    "Sophomores through seniors are assigned a professional advisor and faculty mentor in EECS. Students will need to meet with their professional advisor once a year to plan their schedule and get cleared for course registration. Faculty mentors provide guidance and advice on career and employment opportunities, graduate school, and EECS elective courses."
]

# [ RANKING STAGE ]

# Step 1: Data Cleaning
# Perform data cleaning on the dataset to text information that complicates relevance.

documents_clean = []
for d in docs:
    # Lowercase all letters in the text.
    d_temp = d.lower()
    # Remove punctuations in the text.
    d_temp = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', d_temp)

    documents_clean.append(d_temp)

# Step 2: Vectorize the documents
# Use the Scikit-learn built-in vectorizer.

# Instantiate the Tfidfvectorizer
tfidf_vectorizer=TfidfVectorizer() 

# Send our docs into the Vectorizer
tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(docs)

# Transpose the result into a more traditional TF-IDF matrix, and convert it to an array.
X = tfidf_vectorizer_vectors.T.toarray()

# Convert the matrix into a dataframe using feature names as the dataframe index.
df = pd.DataFrame(X, index=tfidf_vectorizer.get_feature_names())


# [ RETRIEVAL STAGE ]

query = 'and'

# Vectorize the query.
q = [query]
q_vec = tfidf_vectorizer.transform(q).toarray().reshape(df.shape[0],)

# Calculate cosine similarity.
sim = {}
for i in range(len(df.columns)-1):
    sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)

# Sort the values 
sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

# Print the articles and their similarity values
for k, v in sim_sorted:
    if v != 0.0:
        print("[DOCUMENT "+str(k)+"] - (" + str("{:.2f}".format(v)) + ')')

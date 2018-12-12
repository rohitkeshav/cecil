from nltk import word_tokenize
from nltk.corpus import stopwords
from scipy.spatial import distance

import numpy as np
import pandas as pd

import string


# tokenize a doc
def tokenizer(doc, j_tokens=False):

    stop_words = stopwords.words('english')
    mt = str.maketrans('', '', string.punctuation)

    words = [token.strip() for token in word_tokenize(doc.translate(mt).lower()) if
             token.strip() not in stop_words and token.strip() not in string.punctuation]

    if j_tokens:
        return words

    token_count = {token: words.count(token) for token in set(words)}

    return token_count


# TF_IDF on the list of docs
# there definitely a better of doing this
def tf_idf(docs, check_with=None):

    if check_with is not None:
        docs.insert(0, check_with)

    docs_tokens = {idx: tokenizer(doc) for idx, doc in enumerate(docs)}

    # Get document-term matrix
    dtm = pd.DataFrame.from_dict(docs_tokens, orient="index")
    dtm = dtm.fillna(0)

    # Get normalized term frequency (tf) matrix
    tf = dtm.values
    doc_len = tf.sum(axis=1)
    tf = np.divide(tf.T, doc_len).T

    # Get document frequency df
    df = np.where(tf > 0, 1, 0)

    # Get smoothed tf_idf
    smoothed_idf = np.log(np.divide(len(docs) + 1, np.sum(df, axis=0) + 1)) + 1
    smoothed_tf_idf = tf * smoothed_idf

    # calculate cosine distance of every pair of documents
    # convert the distance object into a square matrix form
    # similarity is 1-distance
    similarity = 1 - distance.squareform(distance.pdist(smoothed_tf_idf, 'cosine'))

    # find top 5 docs similar to first one
    similar_docs = np.argsort(similarity)[:, ::-1][0, 1:4]
    print('similar docs', similar_docs)

    retval = list()
    # Print the top 5 similar reviews
    for idx, doc in enumerate(docs):
        if idx in similar_docs:
            # print(docs[idx])
            retval.append(idx)

    return retval

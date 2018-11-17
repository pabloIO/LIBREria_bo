import sys
import os.path
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import json
from config.config import env
import csv


class TfIdfAnalyzer(object):
    def __init__(self, language):
        self.STOP_WORDS = self.import_stop_words(language)

    def import_stop_words(self, language):
        if language == 'sp':
            jsonfile = os.path.join(env['UPLOADS_DIR'], 'local_data/stop_words_es.json')
        elif language == 'en':
            jsonfile = os.path.join(env['UPLOADS_DIR'], 'local_data/stop_words_en.json')
        else:
            jsonfile = os.path.join(env['UPLOADS_DIR'], 'local_data/stop_words_es.json')
        with open(jsonfile, 'r') as file:
            jsondict = json.load(file)
        return jsondict['stop_words']

    def tf_idf(self, word_data, language,  max_df=0.1):
        ## Get stop words list from JSON FILE
        ## max_df default = 0.1
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=max_df,
                                    stop_words=self.STOP_WORDS)
        x = vectorizer.fit_transform(word_data)
        features = vectorizer.get_feature_names()
        dense_matrix = x.toarray()
        return dense_matrix, features

    def count_vectorizer(self, data, max_df=0.1):
        ## Get stop words list from JSON FILE
        
        vectorizer = CountVectorizer(stop_words=self.STOP_WORDS, max_df=max_df)
        x = vectorizer.fit_transform(data)
        features = vectorizer.get_feature_names()
        dense_matrix = x.toarray()
    #     print(len(features))
    #     print(dense_matrix.shape)
    #     print(features)
    #     print(pd)
        return dense_matrix, features

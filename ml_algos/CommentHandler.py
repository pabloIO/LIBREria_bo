from PyPDF2 import PdfFileReader, PdfFileWriter
import sys
import os.path
import pandas as pd
import numpy as np
from config.config import env
from .tf_idf import TfIdfAnalyzer

class CommentHandler(TfIdfAnalyzer):
    def __init__(self, language, comments):
        super().__init__(language)
        self.comments = comments

    def read_text_data(self):
        # return pd.DataFrame({'texto':self.comments})
        df = pd.DataFrame([], columns=['texto'])
        for comment in self.comments:
            df2 = pd.DataFrame([comment['text']], columns=['texto'])
            df = df.append(df2)
        return df

    def get_word_cloud(self, max_df):
        try:
            data = self.read_text_data()['texto']
            total_df = {}
            matrix, features = self.tf_idf(data, max_df)
            data_frame = pd.DataFrame(matrix, columns=features)
            for f in features:
                count = np.sum(data_frame[f])
                total_df[f] = count
            dict_sort = sorted(total_df.items(), key=lambda kv: kv[1])
            ## get 100 frequent items
            filtered = dict_sort[::-1][:100]
            return filtered
        except Exception as e:
            print(e)
            return []
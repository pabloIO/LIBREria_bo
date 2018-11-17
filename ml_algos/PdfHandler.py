from PyPDF2 import PdfFileReader, PdfFileWriter
import sys
import os.path
import pandas as pd
import numpy as np
from config.config import env
from .tf_idf import TfIdfAnalyzer

class PdfHandler(TfIdfAnalyzer):
    def __init__(self, language, pdf):
        super.__init__(self, language)
        self.pdf_file =  pdf

    def read_pdf_text_data(self):
        '''
        Test loading and parsing of a file. Extract text of the file and compare to expected
        textual output. Expected outcome: file loads, text matches expected.
        '''
        df = pd.DataFrame([], columns=['texto'])
        with open(self.pdf_file, 'rb') as inputfile:
            # Load PDF file from file
            ipdf = PdfFileReader(inputfile) 
            for i in range(ipdf.getNumPages()):
                ipdf_p1 = ipdf.getPage(i)
                ipdf_p1_text = ipdf_p1.extractText() \
                            .replace('\n', '') \
                            .encode('utf-8') \
                            .decode('utf-8') \
                            .split()
                df2 = pd.DataFrame(ipdf_p1_text, columns=['texto'])
                df = df.append(df2)
        return df
    
    def get_word_cloud(self, max_df):
        data = self.read_pdf_text_data()['texto']
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
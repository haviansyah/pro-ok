import gensim
import json
import re
import pprint
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords,wordnet
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from itertools import product
import numpy as np
import scipy.stats
from nltk import FreqDist

nltk.data.path.append('../../nltk_data/')
class Preprocessing():
    stop_words = stopwords.words('indonesian')
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()


    def initial_clean(self,text):
        """
        Function to clean text of websites, email addresess and any punctuation
        We also lower case the text
        """
        text = re.sub("((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)", " ", text)
        text = re.sub("[^a-zA-Z ]", "", text)
        text = text.lower() # lower case the text
        text = nltk.word_tokenize(text)
        return text
    

    def remove_stop_words(self,text):
        """
        Function that removes all stopwords from text
        """
        return [word for word in text if word not in self.stop_words]


    def stem_words(self,text):
        """
        Function to stem words, so plural and singular are treated the same
        """
        try:
            text = [self.stemmer.stem(word) for word in text]
            text = [word for word in text if len(word) > 1]
        except IndexError:  # the word "oed" broke this, so needed try except
            pass
        return text


    def preprocess(self,data):
        """
        This function applies all the functions above into one
        """
        # if data == "":
        #     data = self.text      
        return self.stem_words(self.remove_stop_words(self.initial_clean(data)))
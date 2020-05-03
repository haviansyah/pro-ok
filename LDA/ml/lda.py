from gensim import models, corpora, similarities
from gensim.models import LdaModel, TfidfModel, LdaMulticore
import pandas as pd
import numpy as np

SOME_FIXED_SEED = 42
np.random.seed(SOME_FIXED_SEED)

class LDA():
    def __init__(self,df = pd.DataFrame()):
        self.df = df
    
    def train(self,num_topics=700,chunksize=300,alpha = 1e-2, eta = 0.5e-2):
        """
        This function trains the lda model
        We setup parameters like number of topics, the chunksize to use in Hoffman method
        We also do 2 passes of the data since this is a small dataset, so we want the distributions to stabilize
        """
        dictionary = corpora.Dictionary(self.df)
        corpus = [dictionary.doc2bow(doc) for doc in self.df]
        # low alpha means each document is only represented by a small number of topics, and vice versa
        # low eta means each topic is only represented by a small number of words, and vice versa
        lda = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=2,random_state=2)
        return dictionary,corpus,lda

    def train_tfidf(self,num_topics=12):
        dictionary = corpora.Dictionary(self.df)
        corpus = [dictionary.doc2bow(doc) for doc in self.df]
        tfidf = TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        lda_model = LdaMulticore(corpus_tfidf, num_topics=num_topics, id2word=dictionary, passes=2,workers=2)        
        return dictionary, corpus_tfidf, lda_model,tfidf

    def pretrained(self,lda,dicti):
        dictionary = corpora.Dictionary.load(dicti)
        model = LdaMulticore.load(lda)
        return dictionary, model
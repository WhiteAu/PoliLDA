import sys
import csv
import nltk
import numpy
from gensim import corpora, models, similarities



class DataList():
    """
    self.data_list: the list representation of data. drop this if memory is issue
    self.dictionary: the id2word dict used by LDA model
    self.LDA_corpus: the LDA-styled matrix used
    """        
    def __init__(self, path=None, file=None):
        self.data_list = []
        if path is None:
            rec_path = 'resources/data/'
        else: 
            rec_path = path

        if file is None:
            self.fn = 'small_example.csv'
        else:
            self.fn = file
            
        data = csv.reader(open((rec_path+fn), 'rb'), delimiter=',', quotechar='"')
            
        for line in data:
            self.data_list.append(line)
            #for col in xrange(len(line)):
                
               # if col not in data_key:
               #     pass
        self.data_list = self.data_list[1:] #first line is just long-hand explanation. we don't need it!

        #self.data_list = numpy.matrix(self.data_list)

        self.dictionary = corpora.Dictionary(self.data_list)
        self.LDA_corpus = [self.dictionary.doc2bow(text) for text in self.data_list]

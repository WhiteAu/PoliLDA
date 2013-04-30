import sys
import csv
import nltk
import numpy
from gensim import corpora, models, similarities



class DataList():
        
    def __init__(self, path=None, file=None):
        self.data_list = []
        self.data_key = []
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
        self.data_list = self.data_list[1:]
        self.data_list = numpy.matrix(self.data_list)


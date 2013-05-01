import sys
import pickle
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
        data_header = self.make_header()
        self.data_list = self.data_list[1:,:32] #first line is just long-hand explanation. we don't need it! Last column is filler. Don't need it!

        #self.data_list = numpy.matrix(self.data_list)

        self.dictionary = corpora.Dictionary(self.data_list)
        self.LDA_corpus = [self.dictionary.doc2bow(text) for text in self.data_list]


    def clean_data(self, head, save=False):
        """
        adds header information in head to each column entry in data_list
        save: if True will save self.data_list to <filename>.cln
        """
        clean = []
        for i in len(xrange(self.data_list)):
            for j in len(xrange(self.datalist[i])):
                self.data_list[i][j] = head[i] + self.data_list[i][j]
        if save:
            try:
                fp = open((rec_path+fn+'.cln'), 'w')
                pickle.dump(self.data_list, fp)
                close(fp)

    def arrange_by_uid(self):
        key = {}
        users = set(self.data_list[0]) #make set of unique users
                    

    def make_header(self):
        """
        grunty header creation gleaned from example data
        """
        head = []
        head[0] = 'UID:'
        head[1] = 'React:'#In example data, this and Time header are switched, but data is not.
        head[2] = 'Time:'
        head[3] = 'How:'
        head[4] = 'Econ:'
        head[5] = 'HC:'
        head[6] = 'FP:'
        head[7] = 'Abort:'
        head[8] = 'Econ2:'
        head[9] = 'HC2:'
        head[10] = 'FP2'
        head[11] = 'Abort2:'
        head[12] = 'PoliAware:'
        head[13] = 'FavSrc:'
        head[14] = 'Gender:'
        head[15] = 'Age:'
        head[16] = 'Income:'
        head[17] = 'Race:'
        head[18] = 'Religion'
        head[19] = 'Christian:+'
        head[20] = 'State:'
        head[21] = 'TVChnl:'
        head[22] = 'Pref(Econ):'
        head[22] = 'Pref(FP)'
        head[23] = 'Pref(Cand):'
        head[24] = 'Vote:'
        head[25] = 'VoteConf:'
        head[26] = 'VoteLikely:'
        head[27] = 'PoliViews:'
        head[28] = 'Ready?'
        head[29] = 'Prio(Immigration):'
        head[30] = 'Competence(Immigration)'
        head[31] = 'PartyAffiliation:'#should pare the corresponding cell of this down
        head[32] = 'FillerQ:'#Can probably delete this whole column safely

        return head

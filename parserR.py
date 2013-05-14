import sys
import pickle
import csv
import nltk
import numpy
import pytz
import datetime
from gensim import corpora, models, similarities



class DataList():
    """
    self.data_list: the list representation of data. drop this if memory is issue
    self.dictionary: the id2word dict used by LDA model
    self.LDA_corpus: the LDA-styled matrix used
    """        
    def __init__(self, path=None, file=None):
        self.data_list = []

	#Read in the topic information from the STATEMENTS file
	statements = []
	path_st = 'resources/corpora/'
	file_st = 'STATEMENTS-oct3_coded_transcript_sync.csv'
	data_st = csv.reader(open((path_st+file_st), 'rb'), delimiter=',', quotechar='"')
	for line in data_st:
	    statements.append(line)

	statements = statements[1:]
	for items in statements:
	    items[0]=items[0].translate(None, ':')
	    items[1]=items[1].translate(None, ':')

        #Read in the reaction data
	if path is None:
            rec_path = 'resources/data/'
        else: 
            rec_path = path

        if file is None:
            self.fn = 'small_example.csv'
        else:
            self.fn = file
           
        data = csv.reader(open((rec_path+self.fn), 'rb'), delimiter=',', quotechar='"')
            
        #For each reaction item, add the topic data if a correlation can be made
	#Correlation is based on sync start/end time and speaker
	total_dropped = 0
	total = 0
	for line in data:
	    timestamp = line[2]
	    timestamp = timestamp[12:]
	    timestamp = timestamp[:-4]
	    timestamp = timestamp.translate(None, ':')
	    speaker = line[1]
	    if speaker[:1] == 'O':
		speaker = '2'
	    elif speaker[:1] == 'R':
	  	speaker = '1'
	    else:
		speaker = '0'

	    check=0
	    for st in statements:
		if timestamp >= st[0] and timestamp <= st[1] and speaker is st[2]:
		    line.append(st[3])
		    line.append(st[4])
		    line.append(st[5])
		    line.append(st[6])
		    check=1
		    total+=1
	    if check == 0:
		line.append('')
		line.append('')
		line.append('')
		line.append('')
		total_dropped+=1
	
            self.data_list.append(line)
	print 'Total reactions with statment correlation: '
	print total
	print 'Total with no statement correlation: '
	print total_dropped


        data_header = self.make_header()
        self.data_list = self.data_list[1: ] #first line is just long-hand explanation. we don't need it! Last column is filler. Don't need it!

        #self.data_list = numpy.matrix(self.data_list)

        self.dictionary = corpora.Dictionary(self.data_list)
        self.LDA_corpus = [self.dictionary.doc2bow(text) for text in self.data_list]


    def clean_data(self, head, save=False):
        """
        adds header information in head to each column entry in data_list
        save: if True will save self.data_list to <filename>.cln
        """
        clean = self.data_list
        #print len(clean)

        for i in xrange(len(clean)): #foreach row
            #print len(clean[0])
            for j in xrange(len(clean[i])): #foreach column
                #print head[j]
                clean[i][j] = head[j] + clean[i][j]
        if save:
            try:
                fp = open((rec_path+fn+'.cln'), 'w')
                pickle.dump(clean, fp)
                close(fp)
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
        
        return clean

    def arrange_by_column(self, data, col=0):
        '''
        arrangement = [] #the list to be returned
        row = [] #the aggregated list that holds all values after sorting
        uid = data[0][col] #marker
        print 'col id is: %s' %uid
        for i in xrange(len(data)):
            if data[i][col] == uid:
                print 'len row before: %d' %len(row)
                row = row + data[i] #grow the row
                print 'len row after: %d' %len(row)
                #row.append(data[i]) #grow the row
            else:
                uid = data[i][col] #update marker
                print 'col id is: %s' %uid
                print 'len arrangement before: %d' %len(arrangement)
                arrangement.append(row) #store the row and reset it
                print 'len arrangement after: %d' %len(arrangement)
                row = []
        '''
        arrangement = []
        ids = {}
        uid = data[0][col]
        print 'data length is: %d' %len(data)
        for i in xrange(len(data)):
            val = data[i][col]
            if val not in ids:
                ids[val] = []
            ids[val] += data[i]
            
        for key in ids:
            arrangement.append(ids[key])
	#print arrangement
        
	return arrangement

    def drop_columns(self, clean, drop=None):
        """
        Drops columns from a list
        """
        if drop is None:
            return clean
        
        else:
            c = numpy.delete(np.array(clean), drop)

        return c.tolist()

    def make_header(self):
        """
        grunty header creation gleaned from example data
        """
        head = [None]*38
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
        head[18] = 'Religion:'
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
        head[33] = 'foo:'
	head[34] = 'STMT_QTopic:'
	head[35] = 'STMT_Topic:'
	head[36] = 'STMT_Frame:'
	head[37] = 'STMT_Tone:'
        return head
    
    def make_clean(self, col=0, drop=None):
        '''
        fast macro to do things
        '''
        head = self.make_header()
        data = self.data_list
        clean = self.clean_data(head)
        #print clean
        clean = self.drop_columns(clean, drop=[4, 5])
        clean = self.arrange_by_column(clean, col=col)
        #print len(clean)
        sum = 0
        #for k in xrange(len(clean)):
            #print len(clean[k])
            #sum += len(clean[k])
        #print sum
        #print type(clean)
        
        dic = corpora.Dictionary(clean)        
        nuclean = [dic.doc2bow(text) for text in clean]
        return nuclean, dic

import sys
import pickle
import csv
import nltk
import numpy
import re
from gensim import corpora, models, similarities



class DataList():
    """
    self.data_list: the list representation of data. drop this if memory is issue
    self.dictionary: the id2word dict used by LDA model
    self.LDA_corpus: the LDA-styled matrix used
    """        
    def __init__(self, path=None, file=None, drop=None):
        self.data_list = []
        self.dropped = drop
	#Read in the topic information from the STATEMENTS file
	statements = []
	path_st = 'resources/corpora/'
	file_st = 'STATEMENTS2-oct3_coded_transcript_sync.csv'
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
                total_dropped+=1
	
            if check == 1:
                line = self.parse_line(line, kill=drop)
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

    def parse_line(self, line, kill=None):
        react = re.compile('([A-Z][a-z]*:)([A-Z][a-z]*)') #regex to pull out cand name that user agrees/disagrees with
        
        #tone = re.compile('')


        r = react.match(line[1])
        if r is None:
            print line[1]
	elif r.group(2) is 'Agree':
            line[1] = r.group(1)+'Pos'
	else:
            line[1] = r.group(1)+'Neg'  
        
        n = 0
        if kill is not None:
            for c in kill:
	    #print c
	    #print c-n
                del line[c-n] 
                n += 1
        
        return line
        
        

    def clean_data(self, head, save=False):
        """
        adds header information in head to each column entry in data_list
        save: if True will save self.data_list to <filename>.cln
        """
        clean = self.data_list
	print len(head)
        print len(clean)
	print len(clean[0])

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

    def arrange_by_column(self, data, col=0, col2=None):
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
        uid2 = data[0][col2]  if col2 else None
        print 'data length is: %d' %len(data)
        for i in xrange(len(data)):
            val = data[i][col]
            if col2:
                val2 = data[i][col2]
	    else:
		val2 = None
            
            key = val+val2 if val2 else val
            if key not in ids:
                
                ids[key] = []
            ids[key] += data[i]
            
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
            c = numpy.delete(numpy.array(clean), drop)

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
        head[23] = 'Pref(FP)'
        head[24] = 'Pref(Cand):'
        head[25] = 'Vote:'
        head[26] = 'VoteConf:'
        head[27] = 'VoteLikely:'
        head[28] = 'PoliViews:'
        head[29] = 'Ready?'
        head[30] = 'Prio(Immigration):'
        head[31] = 'Competence(Immigration)'
        head[32] = 'PartyAffiliation:'#should pare the corresponding cell of this down
        head[33] = 'FillerQ:'#Can probably delete this whole column safely
        #head[34] = 'foo:'
	head[34] = 'STMT_QTopic:'
	head[35] = 'STMT_Topic:'
	head[36] = 'STMT_Frame:'
	head[37] = 'STMT_Tone:'
        return head
    
    def make_clean(self, col=0):
        '''
        fast macro to do things
        '''
        #set at init time
        if self.dropped is None:
            head = self.make_header()
        else:
            head = self.make_header_mod()
        
        data = self.data_list
        clean = self.clean_data(head)
        #print clean
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


    def make_header_mod(self):
        """
        grunty header creation gleaned from example data
        """
        head = [None]*29
        head[0] = 'UID:'
        head[1] = 'React:'#In example data, this and Time header are switched, but data is not.
        head[2] = 'Time:'
        #head[3] = 'How:'
        head[3] = 'Econ:'
        head[4] = 'HC:'
        head[5] = 'FP:'
        head[6] = 'Abort:'
        head[7] = 'Econ2:'
        head[8] = 'HC2:'
        head[9] = 'FP2'
        head[10] = 'Abort2:'
        #head[12] = 'PoliAware:'
        #head[13] = 'FavSrc:'
        head[11] = 'Gender:'
        head[12] = 'Age:'
        head[13] = 'Income:'
        head[14] = 'Race:'
        head[15] = 'Religion:'
        head[16] = 'Christian:+'
        head[17] = 'State:'
        #head[21] = 'TVChnl:'
        #head[22] = 'Pref(Econ):'
        #head[23] = 'Pref(FP)'
        #head[24] = 'Pref(Cand):'
        head[18] = 'Vote:'
        head[19] = 'VoteConf:'
        head[20] = 'VoteLikely:'
        head[21] = 'PoliViews:'
        #head[29] = 'Ready?'
        head[22] = 'Prio(Immigration):'
        head[23] = 'Competence(Immigration)'
        head[24] = 'PartyAffiliation:'#should pare the corresponding cell of this down
        #head[32] = 'FillerQ:'#Can probably delete this whole column safely
        #head[33] = 'foo:'
	head[25] = 'STMT_QTopic:'
	head[26] = 'STMT_Topic:'
	head[27] = 'STMT_Frame:'
	head[28] = 'STMT_Tone:'
        return head
